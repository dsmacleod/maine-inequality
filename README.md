# Maine Income Inequality

An interactive map of every Maine town shaded by how unevenly income is shared (the Census Gini index). Click a town to see how its income gap has changed since 2014 alongside the Maine state average.

Live: <https://dsmacleod.github.io/maine-inequality/>
Embed: <https://dsmacleod.github.io/maine-inequality/embed.html>

Deep-link to a specific town: `embed.html?town=2301902795` (Bangor) — the `town` param is a Census GEOID (`state + county + cousub` FIPS).

## Inputs

- `data/inequality.json` — town-level data for 536 Maine places: Gini inequality scores 2014–2024 (5-year rolling ACS averages, table **B19083**), latest median household income (table **B19013**, 2020–2024 ACS5), plus the Maine state series for both. Inequality series sourced from the predecessor `maine-inequality-interactive` repo; income merged in by `fetch_income.py`.
- `data/maine-cousubs.geo.json` — Maine county subdivision boundaries, derived from the Census Bureau's 2023 cartographic boundary shapefile (`cb_2023_23_cousub_500k`) and simplified with Douglas–Peucker (ε ≈ 0.001°, ~111 m).

## Outputs

- `embed.html` — single-file widget. Choropleth + click-to-drill panel showing median household income (with % vs. state), inequality score, change since 2014, and rank among Maine towns. No build, no dependencies. Supports `?town=GEOID` deep links.
- `index.html` — preview page that wraps the embed in an iframe and shows the embed snippet.

## Reframing "Gini"

The widget calls it "income inequality score" everywhere reader-facing. The technical term and 0–1 scale are tucked into a "How the score works" expandable footnote.

## Updating data

Refresh after each ACS 5-year vintage release (typically every December):

1. Regenerate `inequality.json` Gini series from the upstream pipeline (`mainestateeconomist207/Distribution-of-Personal-Income-in-Maine`), then re-run this repo's cleanup (sentinel scrubbing, name normalization, GEOID construction).
2. Update the `VINTAGE` constant in `fetch_income.py` and re-run with a Census API key:
   ```sh
   CENSUS_API_KEY=… python3 fetch_income.py
   ```
   Get a free key at <https://api.census.gov/data/key_signup.html>.
