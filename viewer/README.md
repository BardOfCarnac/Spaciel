# Spaciel viewer builds

## Latest private architectural review — Realisation 09 (11 November 2026)

The existing city has **7,993 provisional placements**, **7,981** with registered direct-face SKP geometry in **60** tiles; **11** shoreline cases and one protected Hot Zone mass remain held. V17 roads, online experimental V21 and **556 tagged locations** remain unchanged.

**Important architecture correction:** the largest original source buildings were largely missing from the placement layout, even after recovering the 7,981 meshes. Realisation 09 recovered **100 previously unused large original source models** and creates a separate private landmark placement-review mode. **None is automatically installed.** Original SKP site suggestions require manual registration to the actual atlas.

The portable HTML, modular private project, 100 source-derived GLBs, preview gallery and site audit are in ChatGPT Library `/Spaciel/working-data/`. See [the Realisation 09 report](../reports/native_skp_realisation_09_large_originals_2026_11_11.md).

**Testing:** portable desktop/mobile Canvas fallback checks passed, including model selection, rotation, draft placement and export control wiring; modular HTTP testing was blocked by the test browser. Actual WebGL2 on-device appearance is not yet verified.

## Earlier milestones
- [Realisation 08 — tiled architecture](../reports/native_skp_realisation_08_tiled_private_viewer_2026_11_11.md)
- [Realisation 07 — direct-face registration](../reports/native_skp_realisation_07_private_viewer_2026_11_11.md)
- [Original roads/buildings/tags integration](../reports/roads_buildings_tags_integrated_mockup_2026_11_11.md)

## Public source code, private geometry

Public files in this repository are intentionally source-independent:
- `src/native-architecture-tiles.js` — template and tile loader
- `src/architecture-view-tiles.js` — camera-aware tile selection
- `src/large-building-placement.js` — source-independent model-footprint preview helpers

Do **not** upload the source-derived SKP/GLB mesh library, private viewer HTML, placement geometry or source-built spatial tile data to this public repository until redistribution rights are verified.
