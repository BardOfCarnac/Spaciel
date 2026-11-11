# Spaciel Realisation 13 — skyline-first infill baseline (private)

Date: 11 November 2026 · **Exploratory non-destructive review**, not approved final city geometry.

## Change of placement priority
Original large SketchUp buildings are placed first, at their original source scale and orientation. Their approximate historical SKP anchors are starting points rather than rigid final destinations. The rough older road-separated building areas and previously used buildable footprint are allowed, with limits on major displacement, a developed-neighbourhood density check to exclude isolated offshore candidates, atlas shoreline/water screening, and road exclusions. Small provisional buildings overlapping a large original are temporarily sent to an **infill reserve**, to be repacked around the larger architecture in a later pass.

## Staged results
- **399** additional recovered-but-unplaced large source definitions given new staged placements in the Night City viewer, using recovered original direct-face model geometry.
- Now **13 of the largest 20** screened original-source definitions by ground area are represented in the staged layout; previously this was zero.
- **71** of the newly staged original-source buildings are at least 100 metres high.
- **1,027** overlapping smaller provisional placements held for future repack, their identities and earlier geometry **preserved separately** (not discarded from earlier baselines).
- The new staged city contains **7,367** building objects, of which **7,356** have registered original-source direct-face 3D mesh placements across **60** spatial architecture tiles.
- These 399 source models contribute **23,512** original direct-face triangles. Minimum mesh-to-planned source-footprint overlap is approximately **99.93%**.
- The older Round 12 staged **two** major restorations, previously moved five smaller buildings, protected Hot Zone landmark and 11 shoreline holds remain represented where relevant.
- Location index and its **556** tagged places, geographic search, terrain and existing roads remain unchanged.

## Road and coastline conditions
The placement pass used V17 road-centreline separation (4.9 atlas pixels) and a conservative painted-atlas road-colour exclusion (screened at under 4.5% of polygon area to tolerate printed labels), together with approximate shoreline/water and recognised urban-area checks.

These are **not** authenticated kerb boundaries or fully corrected coast and V21 geometry. Site frontage and specific buildings near roads and shoreline still need manual visual review. This is intentionally a forgiving *massing and skyline* trial rather than a site-by-site engineering clearance.

## QA
- All new source geometry placed with original dimensions and no stretching. The source models retain their original local geometry; atlas translations are applied to historical source transforms.
- Desktop and mobile self-contained HTML browser interaction tests pass with zero JavaScript errors, including building focus, gold-outline toggle, 556 tagged places and unified geographic search.
- Modular files and runtime tile manifest constructed. **HTTP-based modular browser navigation was blocked by the test environment**, so it is not certified as a deployed site.
- **Real-hardware WebGL2 render quality and performance remain unverified**. Canvas fallback draws massing rather than original native faces.

## Private deliverables
Saved to private ChatGPT Library `/Spaciel/working-data/`:
- `Spaciel_Realisation_13_Skyline_First_Viewer.html`
- `Spaciel_Realisation_13_Private_Modular_and_Infill_Reserve.zip`
- `Spaciel_Realisation_13_City_Before_After.png`
- `Spaciel_R13_Placements_PRIVATE.geojson`
- `Spaciel_R13_Restoration_Decisions_PRIVATE.json`
- `Spaciel_R13_Integration_QA.json` and README

**Rights:** Public GitHub receives only aggregate technical notes; do not publish licensed SKP-derived source meshes, private spatial payloads or viewer HTML.

## Next
Visually inspect the skyline in WebGL2, then refill the 1,027 reserved provisional placements where practical and give the remaining blocks character. Avoid further destructive repacking until the user reviews the larger building placement style.
