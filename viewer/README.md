# Spaciel viewer builds

## Selected road network — V33 (15 November 2026)

**Roadcraft V33 is the default for all new viewer integrations.** The canonical manifest is [data/roads/manifest.json](../data/roads/manifest.json); its source-independent runtime graph is [roadcraft_v33_usable.json](../data/roads/roadcraft_v33_usable.json). Load it with [loadSpacielRoads()](src/road-network.js): `roads[].points`, `roads[].widthPx`, `roads[].roadClass`, `roads[].edgeSamples`, plus the graph-aware `router.snap()` and `router.route()`. The connected graph contains **1,390 nodes, 1,962 paths and 11 user-approved joins**. Routes remain in atlas pixels, not real-world travel times.

Use [road-kerb-lod.mjs](src/road-kerb-lod.mjs) when experimenting with close-zoom pavement/kerb styling; the appearance uses the same centreline and road width, and adds **no extra navigable graph geometry**. The V23 graph is retained as an archive; V32 was rejected. Edge samples marked modelled are not surveyed kerbs. The private V19/WebGL viewer has **not** been rebuilt automatically.

## Latest private integrated city infill — Realisation 14 (11 November 2026)

**One citywide skyline-first infill pass** retained **all 7,367 existing Realisation 13 buildings**, including its restored large original SketchUp structures, and added or recovered **1,454** small native-source building instances. The private review city now has **8,821 building objects** and **8,810** registered direct-face original-source mesh instances across **60** architecture tiles. The previous large buildings were not resized, moved or removed, and **202** smaller building identities from the held reserve were reinstated. **824** earlier reserved smaller placements are still retained separately, not forcibly packed into blocks where they cannot fit.

The infill uses the accepted road-separated buildable areas, preserves Hot Zone voids, screens against working coastline and roads and differentiates denser districts from suburban, port, military and resort blocks. **27 contextual waterfront-edge, road-end-vicinity and peripheral-source placement examples** are highlighted in the new viewer. **556 tagged locations**, location/street/district search, the offline V17 road fallback and the experimental V21 road retrieval remain in place.

All new native projected mesh hulls passed local geometric checks against earlier buildings, one another and the working painted-road/water exclusions. Desktop/mobile standalone fallback checks passed; **actual GPU WebGL2 drawing and served modular browser tests remain unverified**. The app is a full combined mockup, not yet the restored final V19 UI or certified final map.

The standalone viewer, complete private modular ZIP, full polygon data, provenance and comparison imagery are in private ChatGPT Library `/Spaciel/working-data/`. [Read the Realisation 14 technical review](../reports/native_skp_realisation_14_full_infill_2026_11_11.md).

## Previous architecture milestones

- [Realisation 13 — skyline-first large original placements](../reports/native_skp_realisation_13_skyline_first_2026_11_11.md)
- [Realisation 12 — first reversible major building repack](../reports/native_skp_realisation_12_staged_restoration_2026_11_11.md)
- [Realisation 11 — complete screened source catalogue](../reports/native_skp_realisation_11_complete_source_catalogue_2026_11_11.md)
- [Realisation 08 — native source tiling](../reports/native_skp_realisation_08_tiled_private_viewer_2026_11_11.md)

## Public code / private source-data separation

The public `viewer/src/` contains only source-independent architecture loaders, view selection and placement-preview helpers. **Do not commit the original SketchUp models, GLB/mesh catalogue, full-source HTML, private spatial data, registered native silhouettes or source tile files to this public repository** until redistribution rights are established.
