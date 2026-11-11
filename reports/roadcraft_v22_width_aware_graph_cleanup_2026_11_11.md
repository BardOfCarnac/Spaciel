# Roadcraft V22 — width-aware topology cleanup (experimental)

Date: 11 November 2026. **Not an approved replacement of existing routing graph or V21 experimental roads.**

## Principle
The official 2045 map depicts roads as **thick drawn strokes**. Tiny diamond cycles, closely paired junctions, dangling stubs and degree-two wiggles that fit entirely inside one painted road should be interpreted as tracing artefacts, not distinct streets or junctions. The road stroke is the unit of visual evidence.

## Actual routing-data experiment
This pass operates on a copy of `night_city_2045_cleaned_connected_graph.json` — the **routing graph**, not the display-only V17 line chains. The source has 4,545 nodes, 5,267 unique undirected edges and 723 independent cycles. Major-road classes are inferred from V17's visual layer. The graph is in the common 5175×7966 atlas coordinate frame.

For each selected interpretation width, the algorithm:
1. Contracts already-connected cycles whose full extent lies inside the local or major road width.
2. Unifies a pair of *already-connected* junction nodes separated by less than a fraction of the width.
3. Prunes an immediate dangling hair shorter than the road radius, but retains longer cul-de-sacs.
4. Simplifies degree-two road geometry within a small fraction of the road width, protecting branch junctions and named-road candidate continuity.
5. Exports a genuine routable **node / path** candidate plus a display GeoJSON. Visual stroke overlaps **do not** create new routing connections.

Available tested local stroke interpretation widths: 6, 10, 14, 18, 22, 26 working atlas px. Yellow-road corridor width is provisionally 1.55x the local street width.

## Midpoint trial — 18px local / 27.9px major
- 80 tiny diamond cycles collapsed.
- 8 pairs of sub-width connected junctions unified.
- 46 terminal micro-spurs pruned.
- Independent cycle rank: 723 → **630** (93 redundant cycles removed).
- 2,112 simplified routing chains exported.
- **One connected component retained**.

Every width preset passes an independent validity check on routing path endpoints, finite coordinates, graph cycle rank and source-network connectivity.

## Why this is not yet final
The width is an interpretive stroke threshold, not a surveyed road width. The atlas and V17 major/local classification need comparison with original printed road strokes; densely drawn parallel streets, genuine roundabouts, bridges and junctions must be checked before promotion. The source routing graph connects even some elevated crossings, which this pass does not correct. V21 is an independently maintained experimental cartographic layer: **this pass has not silently overwritten or substituted V21 data**.

## Private artifacts
Saved to the private Spaciel ChatGPT Library under `/Spaciel/working-data/`:
- `Spaciel_Roadcraft_V22_Stroke_Width_Viewer.html` — full interactive before/after, width slider, city atlas context, correction focus and JSON export.
- `Spaciel_Roadcraft_V22_Private_Review_Package.zip` — six candidate graph JSONs, GeoJSON, source-independent scripts, QA and screenshot.
- `roadcraft_v22_width_18.json` and `roadcraft_v22_default_width18_display.geojson` — default export.
- `Spaciel_Roadcraft_V22_Before_After.png` — visual review sample.

### Next
Review the 14–18px presets in representative dense grids and major-road junctions. Once the user approves a visual treatment, reconcile the logic against the latest V21 road geometry, preserve named road continuity, and run route tests before integrating it as the main Spaciel routing layer.

Only aggregate methods and QA are recorded here; the full atlas and combined private viewer are not committed to public GitHub.
