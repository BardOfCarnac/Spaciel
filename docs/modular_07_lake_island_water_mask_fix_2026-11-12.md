# Spaciel Modular 07 — inland lake island removed from water classification

**12 November 2026 — device-review build, source preserved.**

The user confirmed that restoring the October 12 V7 full-regional Delaunay triangulation in Modular 06 was visibly better, but identified stepped/pixelated water edges and an unwanted island in the inland lake.

## Identified cause and targeted correction

The legacy V19 water renderer uses a **1112 × 1392 R8UI shoreline class texture at 20 m spacing**, sampled by integer `texelFetch` with `GL_NEAREST` filtering. This independently creates pixel-stepped wet/dry boundaries on the October irregular triangular mesh. The 48,262 approved source faces are not the origin of those particular hard shoreline steps, although geometry resolution and original atlas pixels can affect other visible details.

The lake is shoreline **class 3**. Two isolated **class-0 land** components in the lake were visually identified and audited:
- Component 7: 546 grid cells.
- Component 8: 28 grid cells.
- Combined inclusive mask bounds: (x=852..905, y=748..815) in the existing V19 20m grid.

Both components are now class 3, with **574 and only 574 shoreline cells changed**. The matching baked RGBA coastal-distance PNG was regenerated using the exact prior Euclidean-distance encoding (`round(distance_transform_edt(wet))` in the green channel), so original shallow-water contours do not outline the removed island. The RGBA field changed only within lake water, not the rest of the ocean. The terrain vertices within these isolated components already had the local water elevation (-4 m), so **no terrain vertex, face, height or low-corner colour was changed**.

The original October V7 mesh remains exactly **24,303 vertices / 48,262 faces**, source SHA256 `fbac86f9f9d2e4cbde8c5e235e27f17fb737df34ddc4111bfc9bccd797c2550a`. Realisation 14 native buildings, V23 road candidate, water shader, pins, bubble v07, icon-colour focus, and search behaviour are preserved.

## Validation and limitations

23/23 Node regression tests passed, 26 source JavaScript files passed syntax checks, archive integrity passed. A source-data before/after mask preview is preserved privately. **WebGL2 appearance on the user's device is not yet visually certified**, and the main shorelines still use the nearest-neighbour mask; no global anti-alias or water layer redesign was done in this version.

Private runnable files and before/after are saved in `/Spaciel/working-data/`:
- `Spaciel_Modular_07_Portable.html`
- `Spaciel_Modular_07_Private.zip`
- `Spaciel_Modular_07_Lake_Repair_Comparison.png`

The entire Modular 06 source remains the fallback, untouched. Full viewer/map/model assets stay private pending rights review.
