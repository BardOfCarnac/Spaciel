# Spaciel viewer builds

## Latest private mockup — Realisation 08 (11 November 2026)

**Source-derived SketchUp architecture, roads and location tags** are combined in a private viewer. **7,981 of 7,993 building placements** have registered *direct-face* SketchUp source geometry; 11 shoreline holds and one protected landmark remain provisional masses. The architecture is divided into **60** compressed spatial tiles and the modular renderer selects up to **16 nearby GPU tiles** at a time, using lighter massing at whole-city zoom. The viewer retains **556 tagged locations**, unified geographic search and offline V17 roads with an experimental online V21 attempt.

The complete **portable HTML** and **modular private ZIP** are held in ChatGPT Library under `/Spaciel/working-data/`. They are not hosted or published in this public repository.

**Testing:** Desktop and mobile fallback browser checks passed, and simulated WebGL tile-buffer construction passed including tile eviction after panning. **Actual hardware GPU/WebGL2 appearance and performance are not yet verified.** Original nested SketchUp components, materials, shoreline/road conflicts and full V19 UI restoration remain open.

[Read the Realisation 08 technical report](../reports/native_skp_realisation_08_tiled_private_viewer_2026_11_11.md). Earlier review milestones are documented in [Realisation 07](../reports/native_skp_realisation_07_private_viewer_2026_11_11.md) and the [initial integrated mockup](../reports/roads_buildings_tags_integrated_mockup_2026_11_11.md).

## Generic public source

- `src/native-architecture-tiles.js` — source-agnostic compressed tile loader.
- `src/architecture-view-tiles.js` — source-agnostic camera-aware tile selection and 16-tile LOD budget.

**Publication boundary:** Viewer HTML, geometry bundles, registered source meshes and original SKP remain private until redistribution rights are established. Do not upload the private ZIP, spatial data, original model library or full HTML to this public repository.
