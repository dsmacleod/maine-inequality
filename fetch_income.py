"""Fetch Maine county-subdivision median household income (ACS B19013) and merge into data/inequality.json.

Reads CENSUS_API_KEY from environment. Run once after each ACS vintage release;
the embed itself stays key-free since it just reads the prepared JSON.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

VINTAGE = "2024"  # latest ACS 5-year
STATE_FIPS = "23"  # Maine
DATA_PATH = Path(__file__).parent / "data" / "inequality.json"


def fetch(url: str) -> list:
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def clean(v: str | None) -> int | None:
    if v is None:
        return None
    try:
        n = int(v)
    except (ValueError, TypeError):
        return None
    # ACS sentinel values for missing/suppressed
    return None if n < 0 else n


def main() -> int:
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        print("error: set CENSUS_API_KEY in env", file=sys.stderr)
        return 1

    base = f"https://api.census.gov/data/{VINTAGE}/acs/acs5"
    cousub_url = f"{base}?get=NAME,B19013_001E&for=county+subdivision:*&in=state:{STATE_FIPS}&key={key}"
    state_url = f"{base}?get=NAME,B19013_001E&for=state:{STATE_FIPS}&key={key}"

    cousub_rows = fetch(cousub_url)
    state_rows = fetch(state_url)

    # Header is row 0; data starts at row 1.
    # cousub columns: NAME, B19013_001E, state, county, county subdivision
    cousub_by_geoid: dict[str, int | None] = {}
    for row in cousub_rows[1:]:
        _name, mhi, state, county, sub = row
        geoid = f"{state}{county}{sub}"
        cousub_by_geoid[geoid] = clean(mhi)

    state_mhi = clean(state_rows[1][1])

    data = json.loads(DATA_PATH.read_text())
    matched = unmatched = 0
    for place in data["places"]:
        mhi = cousub_by_geoid.get(place["geoid"])
        place["mhi"] = mhi
        if mhi is None:
            unmatched += 1
        else:
            matched += 1
    data["maine"]["mhi"] = state_mhi
    data["mhi_vintage"] = f"ACS 5-year {VINTAGE} (B19013)"

    DATA_PATH.write_text(json.dumps(data, separators=(",", ":")))
    print(f"merged median household income: {matched} matched, {unmatched} no data, Maine={state_mhi}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
