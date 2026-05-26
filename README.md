# Maine Income Inequality

An interactive map of every Maine town shaded by how unevenly income is shared (the Census Gini index). Click a town to see how its income gap has changed since 2014 alongside the Maine state average.

Live: <https://dsmacleod.github.io/maine-inequality/>
Embed: <https://dsmacleod.github.io/maine-inequality/embed.html>

## Inputs

- `data/inequality.json` — town-level Gini scores for 536 Maine places, 2014–2024 (5-year rolling ACS averages, table B19083), plus the Maine state series. Sourced from the predecessor `maine-inequality-interactive` repo.
- `data/maine-cousubs.geo.json` — Maine county subdivision boundaries, derived from the Census Bureau's 2023 cartographic boundary shapefile (`cb_2023_23_cousub_500k`) and simplified with Douglas–Peucker (ε ≈ 0.001°, ~111 m).

## Outputs

- `embed.html` — single-file widget. Choropleth + click-to-drill trend panel. No build, no dependencies.
- `index.html` — preview page that wraps the embed in an iframe and shows the embed snippet.

## Reframing "Gini"

The widget calls it "income inequality score" everywhere reader-facing. The technical term and 0–1 scale are tucked into a "How the score works" expandable footnote.

## Updating data

Data is currently a one-time pull from the source repo. To refresh when ACS publishes a new 5-year vintage, regenerate `inequality.json` from the upstream pipeline (`mainestateeconomist207/Distribution-of-Personal-Income-in-Maine`) and re-run the cleanup in this repo's history (sentinel scrubbing, name normalization, GEOID construction).
