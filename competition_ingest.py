"""Fetch and geocode K-8 competitor schools using the Census Geocoder service.

This module keeps the dashboard's school competition layer synchronized with a
fresh pull from census.gov rather than the legacy static CSV.  The script
geocodes a curated list of Southwest Philadelphia K-8 competitors and outputs
``competition_schools.csv`` for downstream use in ``app_fixed.py``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import json
import sys

import pandas as pd
import requests

COMPETITION_SCHOOLS: tuple[dict[str, str], ...] = (
    {
        "school_name": "St. Barnabas Catholic School",
        "type": "Catholic",
        "grades": "K-8",
        "address": "6334 Buist Ave, Philadelphia, PA",
        "notable_info": "Independence Mission Schools network; broad financial aid",
        "capacity_hint": "medium",
    },
    {
        "school_name": "St. Thomas Aquinas Catholic School",
        "type": "Catholic",
        "grades": "PK-8",
        "address": "1631 S 18th St, Philadelphia, PA",
        "notable_info": "South Philadelphia Independence Mission School",
        "capacity_hint": "medium",
    },
    {
        "school_name": "St. Francis de Sales School",
        "type": "Catholic",
        "grades": "PK-8",
        "address": "921 S 47th St, Philadelphia, PA",
        "notable_info": "University City parish school with strong neighborhood ties",
        "capacity_hint": "medium",
    },
    {
        "school_name": "St. Peter's School",
        "type": "Private",
        "grades": "PK-8",
        "address": "319 Lombard St, Philadelphia, PA",
        "notable_info": "Independent private drawing families from University City",
        "capacity_hint": "medium",
    },
    {
        "school_name": "Greene Towne Montessori School",
        "type": "Private",
        "grades": "PK-3",
        "address": "2133 Arch St, Philadelphia, PA",
        "notable_info": "Progressive Montessori; overlaps on early grades",
        "capacity_hint": "small",
    },
    {
        "school_name": "Harrity Elementary – Mastery Schools",
        "type": "Charter",
        "grades": "K-8",
        "address": "5600 Christian St, Philadelphia, PA",
        "notable_info": "Mastery charter campus serving Southwest families",
        "capacity_hint": "large",
    },
    {
        "school_name": "Independence Charter School",
        "type": "Charter",
        "grades": "K-8",
        "address": "1600 Lombard St, Philadelphia, PA",
        "notable_info": "Citywide dual-language STEAM charter",
        "capacity_hint": "large",
    },
    {
        "school_name": "Christopher Columbus Charter School",
        "type": "Charter",
        "grades": "K-8",
        "address": "1242 S 13th St, Philadelphia, PA",
        "notable_info": "Two S. Philly campuses; attracts Center City families",
        "capacity_hint": "large",
    },
    {
        "school_name": "Russell Byers Charter School",
        "type": "Charter",
        "grades": "PK-8",
        "address": "1911 Arch St, Philadelphia, PA",
        "notable_info": "Expeditionary learning charter downtown",
        "capacity_hint": "large",
    },
    {
        "school_name": "The Philadelphia School",
        "type": "Private",
        "grades": "PK-8",
        "address": "2501 Lombard St, Philadelphia, PA",
        "notable_info": "Independent progressive school serving Center/University City",
        "capacity_hint": "medium",
    },
    {
        "school_name": "Holy Child Academy",
        "type": "Private",
        "grades": "PK-8",
        "address": "475 Shadeland Ave, Drexel Hill, PA",
        "notable_info": "Independent private west of city appealing to same families",
        "capacity_hint": "medium",
    },
    {
        "school_name": "Friends Select School",
        "type": "Private",
        "grades": "PK-12",
        "address": "17th St & Benjamin Franklin Pkwy, Philadelphia, PA",
        "notable_info": "Quaker school; lower grades overlap with CCA targets",
        "capacity_hint": "large",
    },
    {
        "school_name": "Philadelphia Free School",
        "type": "Private",
        "grades": "K-12",
        "address": "4950 Springfield Ave, Philadelphia, PA",
        "notable_info": "Democratic school model; attracts West Philly families",
        "capacity_hint": "small",
    },
    {
        "school_name": "The City School",
        "type": "Christian",
        "grades": "K-12",
        "address": "860 N 24th St, Philadelphia, PA",
        "notable_info": "Faith-based independent; competes for Christian families",
        "capacity_hint": "medium",
    },
)

CAPACITY_HINTS = {
    "small": 200,
    "medium": 350,
    "large": 600,
}

CACHED_OUTPUT = Path(__file__).resolve().parent / "competition_schools.csv"
GEOCODER_URL = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"


@dataclass(frozen=True)
class CompetitionConfig:
    output_path: Path = CACHED_OUTPUT
    benchmark: str = "Public_AR_Current"
    force_refresh: bool = False


def _geocode_address(address: str, *, benchmark: str) -> tuple[float | None, float | None]:
    params = {
        "address": address,
        "benchmark": benchmark,
        "format": "json",
    }
    response = requests.get(GEOCODER_URL, params=params, timeout=30)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:  # pragma: no cover - network failure path
        raise RuntimeError(f"Geocoder request failed for '{address}': {response.text[:200]}") from exc

    payload = response.json()
    try:
        matches = payload["result"]["addressMatches"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError(f"Unexpected geocoder payload for '{address}': {json.dumps(payload)[:200]}") from exc

    if not matches:
        return None, None

    location = matches[0]["coordinates"]
    return float(location["y"]), float(location["x"])


def _fetch_competition_dataframe(config: CompetitionConfig) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for school in COMPETITION_SCHOOLS:
        lat, lon = _geocode_address(school["address"], benchmark=config.benchmark)
        if lat is None or lon is None:
            continue
        capacity = CAPACITY_HINTS.get(school.get("capacity_hint", "medium"), 350)
        rows.append({
            **school,
            "lat": lat,
            "lon": lon,
            "capacity": capacity,
        })

    if not rows:
        raise RuntimeError("No competitor schools could be geocoded. Verify addresses or geocoder availability.")

    df = pd.DataFrame(rows)
    return df


def load_competition_schools(
    *,
    output_path: Path | str = CACHED_OUTPUT,
    benchmark: str = "Public_AR_Current",
    force_refresh: bool = False,
) -> pd.DataFrame:
    """Return competition schools, refreshing from census.gov when requested."""
    output_path = Path(output_path)

    if output_path.exists() and not force_refresh:
        try:
            return pd.read_csv(output_path)
        except Exception:
            pass

    df = _fetch_competition_dataframe(
        CompetitionConfig(output_path=output_path, benchmark=benchmark, force_refresh=force_refresh)
    )
    df.to_csv(output_path, index=False)
    return df


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Refresh competition_schools.csv via the Census Geocoder")
    parser.add_argument("--benchmark", default="Public_AR_Current", help="Census geocoder benchmark (default: %(default)s)")
    parser.add_argument(
        "--output",
        type=Path,
        default=CACHED_OUTPUT,
        help="Location to store the refreshed competition CSV",
    )
    parser.add_argument("--force", action="store_true", help="Force a fresh geocode even if the CSV exists")

    args = parser.parse_args(argv)

    try:
        df = load_competition_schools(output_path=args.output, benchmark=args.benchmark, force_refresh=args.force)
    except RuntimeError as exc:
        print(f"[competition_ingest] Error: {exc}", file=sys.stderr)
        return 1

    print(f"[competition_ingest] Geocoded {len(df)} competitor schools. Saved to {args.output}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
