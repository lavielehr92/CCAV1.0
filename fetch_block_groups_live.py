"""
Fetch Philadelphia Census Block Group boundaries and ACS demographics using a live API key.
Outputs:
  - philadelphia_block_groups.geojson (geometries)
  - demographics_block_groups.csv (metrics used by the app)

ENV:
  CENSUS_API_KEY in environment or in a .env file (same folder)
"""

import os
import json
import pandas as pd
import geopandas as gpd
import requests
from typing import Dict, List

# Optional dotenv support (load both project root and MyKeys/.env if present)
def _load_env():
    try:
        from dotenv import load_dotenv
        # Try default .env in CWD
        load_dotenv()
        # Try MyKeys/.env relative to this file and to CWD
        candidates = [
            os.path.join(os.getcwd(), "MyKeys", ".env"),
            os.path.join(os.path.dirname(__file__), "MyKeys", ".env"),
        ]
        for p in candidates:
            if os.path.exists(p):
                load_dotenv(dotenv_path=p, override=False)
    except Exception:
        pass

_load_env()

STATE_FIPS = "42"   # Pennsylvania
COUNTY_FIPS = "101" # Philadelphia County
ACS_YEAR = "2022"
ACS_DATASET = f"https://api.census.gov/data/{ACS_YEAR}/acs/acs5"

# Variables to fetch
K12_ENROLLMENT_VARS: Dict[str, str] = {
    # ACS B14007 - School Enrollment by Level of School for the Population 3 Years and Over
    "B14007_001E": "enrolled_total",
    "B14007_002E": "enrolled_k",
    "B14007_003E": "enrolled_1_4",
    "B14007_004E": "enrolled_5_8",
    "B14007_005E": "enrolled_9_12",
}

VAR_MAP: Dict[str, str] = {
    # Income & poverty
    "B19013_001E": "median_income",
    "B17001_001E": "pop_poverty_total",
    "B17001_002E": "pop_below_poverty",
    # Total population
    "B01003_001E": "total_pop",
    # Race (selected)
    "B03002_003E": "white_alone",
    "B03002_004E": "black_alone",
    # Households with children under 18
    "B11005_002E": "hh_with_u18",
}

VAR_MAP.update(K12_ENROLLMENT_VARS)


def _get_census_key() -> str | None:
    # Support several env var names
    for name in [
        "CENSUS_API_KEY",
        "CensusBureauAPI_KEY",
        "CENSUSBUREAUAPI_KEY",
        "CENSUS_KEY",
    ]:
        val = os.getenv(name)
        if val:
            return val
    return None


def fetch_acs_block_groups() -> pd.DataFrame:
    params = {
        "get": ",".join(VAR_MAP.keys()),
        "for": "block group:*",
        "in": f"state:{STATE_FIPS} county:{COUNTY_FIPS}",
    }
    api_key = _get_census_key()
    if api_key:
        params["key"] = api_key

    r = requests.get(ACS_DATASET, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    headers = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    # GEOID = state + county + tract + block_group
    df["GEOID"] = df["state"] + df["county"] + df["tract"] + df["block group"]

    # Convert numeric fields
    for code, name in VAR_MAP.items():
        df[name] = pd.to_numeric(df[code], errors="coerce")

    # Derived fields - total enrolled in kindergarten through grade 12
    enrollment_cols = [
        "enrolled_k",
        "enrolled_1_4",
        "enrolled_5_8",
        "enrolled_9_12",
    ]
    df["k12_pop"] = df[enrollment_cols].fillna(0).sum(axis=1)

    total_k12 = df["k12_pop"].sum()
    print(f"K-12 enrollment (B14007) across block groups: {total_k12:,.0f}")
    df["poverty_rate"] = (df["pop_below_poverty"] / df["pop_poverty_total"].replace(0, pd.NA)) * 100
    # Race percentages (if available)
    df["pct_black"] = (df["black_alone"] / df["total_pop"].replace(0, pd.NA)) * 100
    df["pct_white"] = (df["white_alone"] / df["total_pop"].replace(0, pd.NA)) * 100

    # Friendly schema for the app
    out = df[[
        "GEOID", "median_income", "k12_pop", "poverty_rate",
        "total_pop", "pct_black", "pct_white", "hh_with_u18"
    ]].copy()
    out.rename(columns={
        "GEOID": "block_group_id",
        "median_income": "income",
    }, inplace=True)

    return out


def fetch_block_group_shapes() -> gpd.GeoDataFrame:
    # 2022 TIGER/Line block groups for the state; filter to county
    url = f"https://www2.census.gov/geo/tiger/TIGER2022/BG/tl_2022_{STATE_FIPS}_bg.zip"
    gdf = gpd.read_file(url)
    gdf = gdf[gdf["COUNTYFP"] == COUNTY_FIPS].copy()
    gdf["GEOID"] = gdf["STATEFP"] + gdf["COUNTYFP"] + gdf["TRACTCE"] + gdf["BLKGRPCE"]
    gdf = gdf.to_crs(epsg=4326)
    return gdf


def main():
    print("Downloading block group shapes …")
    gdf = fetch_block_group_shapes()
    print(f"Shapes: {len(gdf)}")

    print("Fetching ACS data …")
    demo = fetch_acs_block_groups()
    print(f"ACS rows: {len(demo)}")

    # Merge and compute centroids
    gdf["GEOID"] = gdf["GEOID"].astype(str)
    demo["block_group_id"] = demo["block_group_id"].astype(str)

    merged = gdf.merge(demo, left_on="GEOID", right_on="block_group_id", how="left")

    # Compute projected centroids for accurate lat/lon
    merged_proj = merged.to_crs(3857)
    cent_proj = merged_proj.geometry.centroid
    cent_ll = gpd.GeoSeries(cent_proj, crs=3857).to_crs(4326)
    merged["lat"] = cent_ll.y
    merged["lon"] = cent_ll.x
    # Ensure only one geometry column exists when writing
    if "centroid" in merged.columns:
        del merged["centroid"]

    # Add placeholders to match the app's expected columns
    merged["%Christian"] = 25.0
    merged["%first_gen"] = 35.0

    print("Saving outputs …")
    merged.to_file("philadelphia_block_groups.geojson", driver="GeoJSON")

    demographics = merged[[
        "block_group_id", "income", "k12_pop", "poverty_rate", "lat", "lon",
        "%Christian", "%first_gen", "total_pop", "pct_black", "pct_white", "hh_with_u18",
        "TRACTCE", "enrolled_total"
    ]].copy()
    demographics.rename(columns={"enrolled_total": "k12_enrollment_total"}, inplace=True)

    neg_mask = demographics["k12_pop"] < 0
    if neg_mask.any():
        print(f"Warning: Found {neg_mask.sum()} block groups with negative K-12 values. Resetting to 0.")
        demographics.loc[neg_mask, "k12_pop"] = 0

    missing_mask = demographics["k12_pop"].isna()
    if missing_mask.any():
        print(f"Warning: Imputing 0 for {missing_mask.sum()} block groups missing K-12 enrollment.")
        demographics.loc[missing_mask, "k12_pop"] = 0
    demographics["k12_imputed"] = missing_mask
    print(
        f"Demographics output: {len(demographics)} block groups with {int(demographics['k12_pop'].sum()):,} K-12 students."
    )
    demographics.to_csv("demographics_block_groups.csv", index=False)

    print("Done. Files written:\n - philadelphia_block_groups.geojson\n - demographics_block_groups.csv")


if __name__ == "__main__":
    main()
