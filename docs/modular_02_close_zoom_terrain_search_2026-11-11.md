# Spaciel Modular 02 — close native architecture, roads, terrain and search

**11 November 2026.** Implementation of the user's requested integration atop the *real, user-validated Modular 01 V19 viewer*, not a replacement prototype. Full viewer and commercial/derived source assets remain in private Spaciel working files.

## What changes

- **Architecture:** default source-face SketchUp-derived V19 set (7,981 placements) persists at all zoom levels. No automatic distance-based swap back to old V19 masses; the old representation can still be explicitly selected for diagnosis. Closest camera distance reduced to **55 m** and low-altitude camera target follows the detailed terrain. Missing/slow source-face tiles show loading rather than silently replacing buildings. No new per-building road/kerb-clearance certification was made, so existing architectural registration is retained as provisional.
- **Roadcraft:** existing **2,422 V17 chains** unchanged in position/topology, with visual default widths **18 m primary / 12 m local** instead of roughly 15/9 m. A width multiplier re-meshes surfaces only; it does not edit road centrelines or routing. Re-draping occurs when high-detail elevations decode.
- **Terrain:** actual approved **V19 FINAL 20 m edited terrain raster**, 1112×1392 source float samples in the V19 world registration, decoded and tiled for nearby WebGL2 rendering; coarse 50 m terrain provides distant/background fallback. This is **not a claim to integrate the raw 1 m USGS DEM**, or the latest October irregular adaptive triangle mesh. The fully adaptive high-resolution meshing pass remains to be done separately.
- **Search:** approved **left-anchored magnifier → rightward expanding bar**, with magnifier ending on far right, directly editable input, Enter/icon submission, suggestions, and Escape/click-outside closing. Unified V19 search dataset: **24 districts, 11 neighbourhoods, 527 named streets** plus live map locations and Vend-R venues. Works in main WebGL viewer and 2D fallback.

## QA and preservation

9/9 regression tests passed (including real decoded terrain data shape/sampler), all JavaScript syntax checks passed. Chromium without WebGL2 displayed the real map, 661 pin UI and working search without JavaScript errors; the icon was measured at x≈28 px when collapsed and x≈851 px when expanded in a 1150px viewport, then returned to x≈28 px on close. **GPU 3D geometry, terrain shader and native tile drawing still require actual WebGL2 hardware checks.** These are not yet certified on the user's system.

The user-approved Modular 01 files are unchanged and should remain the rollback baseline. The private ZIP contains the modular source; the portable HTML is an offline build from that source. Do not publish embedded commercial sourcebook/SketchUp-derived assets in this repository.

## Follow-up verification

Test native architecture and roads together at 55m camera distance, coastline & crater height continuity, water layering, first-person-like proximity, camera/pin click behaviour, category transitions, and mobile interactions. Any road/building conflict should be reported against the V17 centrelines without losing original SKP geometry.
