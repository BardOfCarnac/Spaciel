# Spaciel — native SketchUp building placement workbench

This repository contains a **working baseline**, not a completed city viewer or a published website.

## Design principle

Use the approved V10 footprint layout as approximate **where buildings should sit**, not as moulds that stretch models. Keep original building geometry, proportions, and (once registered) approximate SKP positions wherever feasible. Rotate/translate buildings modestly to align to roads and plots, preserve important architectural silhouettes, and fill gaps with smaller suitable native SKP buildings. Do not replace distinctive original geometry with simple extruded proxies unless necessary. Preserve roads, coastline and terrain.

## Files

- `data/footprints/v10_approved_building_slots.geojson`: all 11,508 V10 target polygons in atlas pixels. True polygon boundaries, not simplified bounding boxes.
- `data/footprints/v10_approved_building_slots.csv`: searchable site centroids, dimensions and initial collision flags.
- `data/roads/v17_cleaned_road_centerlines.geojson`: cleaned routing-derived V17 road linework in the same atlas frame. This is *not* a measured kerb/road-width polygon.
- `data/catalogue/skp_native_buildings_sorted_by_size.csv`: all 4,470 screened native source shapes, sorted by ground size, with width/depth/height, original SKP source IDs/GUIDs, appearance complexity and quality flags. 4,462 passed closed-building-envelope screening. These are source-face building masses, not guaranteed detailed architectural masterpieces.
- `data/decisions/approved_1520_native_mesh_reuse_proposals.csv`: prior un-stretched source-model substitutions, retained strictly as **proposal candidates**, not as approved historical positions.
- `data/checks/*`: review flags for line/plot crossings and plot/plot overlaps.

## How to use

1. Import footprints and road centrelines into an editor using the shared **atlas-pixel** coordinate frame.
2. Pick source models by native physical dimensions and architecture, preserving source geometry and dimensions; prefer their original placement and orientation once a trustworthy SKP-to-atlas registration is established.
3. Check candidate model projected hulls against the V17 road centreline graph, nearby model hulls, coastline and slope. Allow small, deliberate shifts/rotations; choose smaller originals to fill gaps.
4. Flag exceptions for visual review; do not automatically erase or move approved footprints.

## Important limitations

- Native models' *actual original SKP locations* have **not yet been matched reliably** to the V10 atlas. The previous provisional density transform created false-positive overlaps even when shifted. Thus this repository does not falsely claim source model positions are registered.
- Road audit detects where a road centreline crosses a footprint (or two footprint polygons overlap). It does **not** verify safe road-edge offsets, elevation/bridge separation, shoreline, slope, or visual plausibility.
- Some V10 polygons may intentionally overlap or need modest correction. The flags are advisory, never an automatic geometry rewrite.
- All measurements in native source catalogue are metres; target footprints and road linework use atlas pixels. Before matching sizes across sources, use a validated geometric registration; do not equate pixel values with metres.
- This is a public repository. Do not upload the original commercial/licensed `.skp` or binary model libraries until their redistribution rights are settled. This repository deliberately contains only analysis-derived catalogues, geometry target placements and decision records.