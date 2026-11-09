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

- The original top-level SketchUp instance positions and transforms have now been extracted directly from the user-supplied source. The recovered V2 road-derived transform maps those positions to the Atlas, but particular V10 target-site identities are still **unverified**. Do not reuse the old density-based source registration.
- Road audit detects where a road centreline crosses a footprint (or two footprint polygons overlap). It does **not** verify safe road-edge offsets, elevation/bridge separation, shoreline, slope, or visual plausibility.
- Some V10 polygons may intentionally overlap or need modest correction. The flags are advisory, never an automatic geometry rewrite.
- All measurements in native source catalogue are metres; target footprints and road linework use atlas pixels. Before matching sizes across sources, use a validated geometric registration; do not equate pixel values with metres.
- This is a public repository. Do not upload the original commercial/licensed `.skp` or binary model libraries until their redistribution rights are settled. This repository deliberately contains only analysis-derived catalogues, geometry target placements and decision records.
## Collision-audit results

The preserved target layer has 11,508 footprint polygons. A first geometric check against 2,422 cleaned road chains found zero direct road-centreline crossings, but 40 footprints are within three atlas pixels of their nearest centreline. The dataset also contains 3,182 polygon-overlap pairs involving 2,432 sites. These are manual-review flags; no footprints were removed or moved. See `data/checks/` for the detailed records.

The next stage is manual visual assessment of original in-place candidates, followed by careful limited rotations/translations and use of smaller original buildings for genuine gaps.

## Original SKP placement recovery — 9 November 2026

- The named (1) and (2) SKP sources in the user's Library are SHA256-identical: `17317588df75a4bea8a87ad86d0438ff112c693f6c54e4ca9da4fa4c53842ee0`.
- Parsed **16,499 original top-level instances** and their 13-value placement transforms; 4,902 instances reference 4,427 of the 4,462 screened usable building envelopes.
- Replayed nine saved V2 road-registration controls on the current cleaned Atlas-pixel V17 roads: maximum nearest-road-line distance **2.604 Atlas px**, against **119.229 px** for the former V1 visual fit. These are saved controls, not an independent survey.
- Non-destructive source placement QA: **739** original source hulls intersect a road centreline; **242** are less than five Atlas pixels away; **271** overlap an approved target by at least half the source hull and clear that road check. Of those, **224** avoid significant overlap with another original source hull. One best candidate per target gives a **137-site first visual shortlist**.
- Source hulls are **convex-hull approximations** and may conceal concavities. Their overlap with a target is not proof of an original building's historical identity or final suitability.

**New working files:** `data/registration/` contains the source-derived transform and nine controls; `data/placement/native_original_instance_review.csv` contains the 4,902 source-position review records; `data/placement/in_place_high_overlap_visual_shortlist.csv` contains 137 top-priority visual-review candidates; `reports/` documents provenance and limitations; and `scripts/` contains reproducible extraction and diagnostic tools.

The original SKP binaries and exact source-derived polygon hulls are **not** committed to this public repository. The latter are retained in the user's private Spaciel Library archive.


## Architectural visual triage — 9 November 2026, pass 2

The 137 original-position shortlist remains **unapproved**: 12 have source/target footprint IoU >= 0.45, 23 are partially aligned, 61 are small original buildings inside larger proposed sites and 41 cross a proposed footprint. Geometry screening found a single watertight source shell for each, but 77 have fewer than 36 triangles and may be simple massing rather than finished architecture.

A separate non-destructive translation audit found 84 candidate original models that can be shifted at most 12 Atlas pixels toward nearby proposed sites **without scaling or rotation**; five meet tighter inspection criteria. Nothing has been applied to the layout or the live viewer.

See [the pass-2 report](reports/architecture_review_phase2.md), [source geometry triage](data/review/in_place_137_architectural_structure_triage.csv), [small-move register](data/review/small_move_candidates_no_scaling.csv), and [five first inspections](data/review/small_move_first_five.csv). The private interactive viewer with original SKP-derived geometry is retained in the user's Spaciel Library and **not** published here.
