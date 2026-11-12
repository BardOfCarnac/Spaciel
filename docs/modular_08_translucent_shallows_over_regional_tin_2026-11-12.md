# Spaciel Modular 08 — translucent water above the original faceted seabed

**12 November 2026 — private GPU-review build, not a user-approved visual baseline.**

The user proposed extending the approved original triangulation visually beneath the shallows, with optical water layered above. Modular 07 painted optical water directly onto wet terrain fragments, leaving a hard 20m nearest-neighbour wet/dry boundary despite the real 48,262-face October 12 V7 regional adaptive Delaunay terrain. Modular 08 changes the compositing order and shoreline sampling, not that terrain source.

## Changes

- **Keep the existing approved October V7 regional TIN** intact: 24,303 source vertices and 48,262 original nonuniform faces, with the original lowest-corner face colours and fine 4% edges. The same faces continue below the sea. Their original -4m flat offshore elevations are **not invented bathymetry**, and no synthetic subdivisions or new terrain elevations are claimed.
- **Water is a separate surface.** The existing V3.4 optical water colour, glints, bands and sunlight material is drawn on two registered, world-space surface triangles at 0m elevation, above the original terrain. Alpha blending reveals underlying facets near the coast and becomes denser offshore. Terrain depth testing naturally occludes water where shore terrain is higher.
- **Smooth the water boundary independently of the TIN.** Convert the repaired Modular 07 R8UI 1112×1392 shore classes to an R8 signed-distance field, treating classes 1/2/3 as wet and unclassified marine cells as wet only when the V7 road/camera DEM is at most 0.5m. The compressed signed field is uploaded as normalized R8 with bilinear filtering, so smoothstep alpha softens rather than snapping to 20m pixel centres.
- **Retain the lake-island fix** (the 574 repaired land-mask pixels). The legacy local elevation-following water treatment is provisionally retained for inland river and reservoir cells above 0.5m height; a global 0m water plane would incorrectly flood or hide elevated lakes. Further lake-level registration is separate.
- **Preserve all other modules:** R14 native building meshes, V23 candidate road source, 661 pins, v07 bubbles, magnifier search, focused spectrum colours, camera and labels.

## Verification and limitations

28/28 automated tests pass, all JavaScript syntax checks pass, and the private ZIP passes integrity checks. A Chromium fallback browser opened the **real self-contained Modular 08 HTML** at mobile width and reported 661 pins, with no page errors. WebGL2 was unavailable, so GPU coastline appearance and translucent shading have **not** been visually certified.

This is a foundation for shoreline layering, not a claim of surveyed underwater relief. Some offshore V7 source elevations are broadly flat at -4m. Authentic detail would require verified bathymetry, or a separately approved procedural seabed.

The full private build is stored under `/Spaciel/working-data/Spaciel_Modular_08_Private.zip` and `Spaciel_Modular_08_Portable.html` in the user's Spaciel Library. The map/source-model assets are not uploaded publicly. Modular 07 remains available for rollback.
