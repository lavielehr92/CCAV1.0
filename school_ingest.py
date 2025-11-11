"""Retrieve K-12 school points from census.gov TIGER/Line POINTLM files.

This loader downloads the latest TIGER point landmarks for the configured
counties, filters for primary/secondary schools, and caches the results to
``census_schools.csv`` for downstream EDI computation.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import geopandas as gpd
import pandas as pd

TIGER_POINT_URL = "https://www2.census.gov/geo/tiger/TIGER{year}/POINTLM/tl_{year}_{state}{county}_pointlm.zip"
DEFAULT_YEAR = 2023
STATE_FIPS = "42"
DEFAULT_COUNTIES: tuple[str, ...] = ("029", "045", "091", "101")
CACHE_PATH = Path(__file__).resolve().parent / "census_schools.csv"


@dataclass(frozen=True)
class SchoolConfig:
    year: int = DEFAULT_YEAR
    state: str = STATE_FIPS
    counties: Sequence[str] = DEFAULT_COUNTIES
    output_path: Path = CACHE_PATH
    force_refresh: bool = False


_MTFFC_DESCRIPTIONS = {
    "K1231": "Elementary/Secondary School",
    "K1232": "Elementary/Secondary School",
    "K1233": "Elementary/Secondary School",
    "K1223": "Secondary School",
    "K1222": "Secondary School",
    "K1221": "Secondary School",
    "K1220": "Secondary School",
    "K1210": "Primary School",
}


def _fetch_county_points(config: SchoolConfig, county: str) -> gpd.GeoDataFrame:
    url = TIGER_POINT_URL.format(year=config.year, state=config.state, county=county)
    gdf = gpd.read_file(url)
    return gdf


def _filter_school_points(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    school_mask = gdf["MTFCC"].astype(str).str.startswith("K12")
    schools = gdf.loc[school_mask].copy()
    if schools.empty:
        return pd.DataFrame(columns=["school_name", "type", "lat", "lon", "mtfcc"])

    schools["lat"] = schools.geometry.y
    schools["lon"] = schools.geometry.x
    schools["school_name"] = schools["FULLNAME"].fillna("Unnamed School")
    schools["mtfcc"] = schools["MTFCC"].astype(str)
    schools["type"] = schools["mtfcc"].map(_MTFFC_DESCRIPTIONS).fillna("K-12 School")
    frame = schools[["school_name", "type", "lat", "lon", "mtfcc"]].drop_duplicates()
    return frame


def _normalise_and_merge(frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["lat", "lon"])
    df = df[~df["school_name"].str.contains("Cornerstone Christian Academy", case=False, na=False)]
    df["capacity"] = 400
    return df


def load_census_schools(
    *,
    year: int = DEFAULT_YEAR,
    state: str = STATE_FIPS,
    counties: Sequence[str] | None = None,
    output_path: Path | str = CACHE_PATH,
    force_refresh: bool = False,
) -> pd.DataFrame:
    counties = tuple(counties) if counties else DEFAULT_COUNTIES
    output_path = Path(output_path)

    if output_path.exists() and not force_refresh:
        try:
            df = pd.read_csv(output_path)
            if {"lat", "lon", "school_name"}.issubset(df.columns):
                return df
        except Exception:
            pass

    config = SchoolConfig(year=year, state=state, counties=counties, output_path=output_path, force_refresh=force_refresh)
    frames = []
    for county in counties:
        gdf = _fetch_county_points(config, county)
        frame = _filter_school_points(gdf)
        if not frame.empty:
            frames.append(frame)

    if not frames:
        raise RuntimeError("No Census school landmarks found; verify county codes or year.")

    merged = _normalise_and_merge(frames)
    merged.to_csv(output_path, index=False)
    return merged


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Refresh census_schools.csv from TIGER/Line POINTLM data")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR)
    parser.add_argument("--state", type=str, default=STATE_FIPS)
    parser.add_argument("--counties", nargs="*", default=list(DEFAULT_COUNTIES))
    parser.add_argument("--output", type=Path, default=CACHE_PATH)
    parser.add_argument("--force", action="store_true")

    args = parser.parse_args(argv)

    try:
        df = load_census_schools(
            year=args.year,
            state=args.state,
            counties=args.counties,
            output_path=args.output,
            force_refresh=args.force,
        )
    except RuntimeError as exc:
        print(f"[school_ingest] Error: {exc}")
        return 1

    print(f"[school_ingest] Retrieved {len(df):,} schools. Saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
