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

## Minimum SketchUp building standard — 10 November 2026

A plain enclosed source building is acceptable: walls/sides, a roof or top, and a convincing solid silhouette. **Low face or triangle counts alone are not grounds for rejection.** Open, missing-wall, or staple-like shapes still require inspection or repair. All 137 first-pass candidates meet the initial one-shell watertight geometry screen; visual completeness and siting are independently pending. See [building acceptance policy](docs/building_acceptance_policy.md) and [137-entry minimum-shell review](data/review/in_place_137_minimum_closed_shell_screen.csv). No positions or building geometry have been altered.

## Native-scale building assembly — draft 01 (10 November 2026)

A **non-destructive, whole-city 2D placement trial** has now assigned **8,618 original-source model instances** to the approved building areas: **228** retain their original source position and **8,390** are reused via translation/rotation without scaling. The proposals refer to **2,568 distinct original SketchUp source definitions** and **8,516 target site IDs**. The remaining 2,992 target IDs have no direct assignment; some are intentionally empty or overlap other approved slots. Independent geometry checks found no placed 2D hull within 2.6 atlas pixels of cleaned road centrelines and no significant hull-to-hull overlaps after cleaning four provisional conflicts.

This is **not** yet integrated as finished 3D geometry; source model solids, district look, foundations, coastlines and actual street widths still need review. See [the method and full limitations](reports/native_building_assembly_draft01.md) and [rebuild script](scripts/assemble_native_buildings_draft01.py). Detailed source-derived hulls, placement coordinates and offline interactive review website remain in the private Spaciel Library, not this public repository.

## Current building placement approach — Draft 02 (10 November 2026)

**IMPORTANT: The approved gold regions are shared buildable blocks, not one building per old V10 footprint.** Draft 01's 8,618 one-to-one footprint-derived assignments are **superseded** and must not be treated as the approved city arrangement. The 11,508 old outlines contributed to the gold regions; none is a mandatory destination.

Draft 02 freely packs unchanged native-source model footprints **anywhere inside the gold masks**, guided broadly by neighbourhood style. Current non-destructive 2D trial: **3,571** model shapes; **140** at their source positions and **3,431** moved/rotated without scaling. Exact geometry checks found no model-to-model overlaps above 0.5% of the smaller hull and no road centreline intersections. Source hulls cover **30.3%** of gold area; halos reserve **46.6%**. This is a conservative *first fill* with legitimate open space, not a finished 3D skyline.

- [Gold buildable blocks (editable GeoJSON)](data/blocks/gold_buildable_regions_v1.geojson)
- [Block-first placement report](reports/block_first_assembly_draft02.md)
- [Rebuild method](scripts/assemble_native_buildings_block_first_v2.py)

The original source-derived exact placement hulls and interactive visual review page are stored privately in Spaciel's working Library, not in this public repository. Source model rights remain to be checked before publication of original 3D geometry.


## Current building-layout baseline — Round Two / Draft 03 (10 November 2026)

**Important:** The gold areas are *shared buildable city blocks*, never one-to-one destinations for V10 historical footprints. Draft 02 was a first free-block placement but left excessive unused edges (3,571 placements, 30.3% gold roof-outline coverage). The older one-to-one Draft 01 remains superseded.

Round Two **repacked** the unapproved Draft 02 placements rather than retaining their arbitrary interior positions. It kept the 140 original-location source buildings, reused the source models at original proportions, preferentially established street frontages and then filled internal spaces. Draft 03 contains **6,257 provisional 2D native-source placements**, using **2,930 original source designs**, covering **57.06%** of the approved gold area with roof outlines. The Hot Zone remains intentionally sparse; corporate/urban blocks are denser. 

The final geometry audit found **zero** road-centreline intersections, **zero** hulls outside the gold mask at working raster resolution, **zero** overlapping pairs greater than 0.5% of the smaller hull, and **6,257 valid hulls**. Small subthreshold overlap remains; full road widths, coastline, slopes, source mesh and district outlines still need 3D/manual validation. **No final 3D city or live site has been updated.**

Review the [Round Two report](reports/block_fill_round2.md), [method](scripts/assemble_native_buildings_block_round2.py), [validation](reports/block_fill_round2_geometry_audit.json) and [district-style coverage](reports/block_fill_round2_style_coverage.json).

The interactive before/after website and detailed source-derived placement GeoJSON are in the user's **private Spaciel Library**, not this public GitHub repository, pending checks of the original SketchUp model's redistribution rights.


## Historical block-area recovery — review only (10 November 2026)

The Draft 03 gold placement area was derived from existing V10 building footprints, not from all available city land. Its undercoverage was confirmed by recovering the old October V6 morphology layer with **560 approximate character block polygons** (5.92M atlas px² union versus 3.29M atlas px² in the current gold layer). Old block polygons sometimes cross roads and are **not** a complete buildable-land mask. A preliminary exclusion of current stylised V17 roadway corridors identifies **2.25M additional atlas px²** worth reviewing, still subject to accurate coastline, parks, deliberate voids, terrain and road width checks.

The current 6,257-placement Draft 03 arrangement **remains untouched**. The extra areas are candidates only; they are not an instruction to densely build on all available land.

Files: [560 recovered character blocks](data/blocks/recovered_october_560_character_blocks.geojson), [possible expansion areas (not approved)](data/blocks/recovered_additional_territory_REVIEW_ONLY.geojson), [rebuild script](scripts/recover_earlier_block_coverage.py), and [full recovery report](reports/recovered_earlier_city_block_areas.md). The interactive comparison website and visual reference remain in the user's private Spaciel working Library, rather than deploying the site.


## Round Three / Draft 04 — expanded road-block infill (10 November 2026)

**Current provisional 2D placement baseline: 7,858 original-source building outlines**, including all **6,257 Round Two placements retained** and **1,601 additional original-scale source models** rigidly translated/rotated into recovered broad-block territory. The **140** native-source positions retained in Round Two are unchanged. Total distinct original SKP designs across the trial: **3,081**.

The newly recovered placement field comes from the older **560 road-separated planning blocks**, instead of treating old V10 building footprint polygons as fixed sites. This pass adds buildings only in the extra territory and protects the current gold/Round Two layout. We subtract current stylised V17 road corridors, a recovered Hot Zone preservation outline and brightly marked atlas water/landscape areas before trying new placements.

**Key qualification:** Only **16.12% of the additionally eligible trial area** is covered by new roof outlines. A remaining gap does not automatically mean a planning error: some areas are fragmented, landscaped or intentionally open. The overall union of gold plus recovered blocks has **34.29% outline coverage**, a different denominator from Round Two's **57.06% coverage of gold alone**. These figures are not contradictory.

The source placement outlines and the self-contained interactive viewer are saved privately in the Spaciel working Library, not published to this public repository. Source redistribution rights have not been verified. There are no changes to the 3D viewer or public website.

- [Round Three methodology and summary](reports/round3_broader_block_infill.md)
- [Round Three build script](scripts/assemble_native_buildings_broader_blocks_round3.py)
- [Recovered broad blocks, review only](data/blocks/recovered_road_exclusion_blocks_v2_REVIEW_ONLY.geojson)

Still to verify: actual shoreline, parks and designed open spaces, surveyed road edges, terrain foundations, and street-level aesthetics. Nothing here should be treated as a finished authoritative building layout.

## Hot Zone skyline landmark retained — 10 November 2026

The Round Three layout has a small **landmark preservation revision**: the largest mapped Hot Zone building footprint from the approved V10 plan (`original-4125`, about 8,357 atlas px²) is now explicitly retained. Eleven smaller provisional buildings competing with its outline and a 2.5-px margin were removed; no other city placements changed. The resulting **working 2D footprint count is 7,848**: 7,847 retained original-source placements plus the protected historical large-building footprint. This shape is 60.4 atlas pixels clear of the cleaned road-centreline graph.

This **does not yet restore the exact 3D SketchUp mesh** or prove its source identity, height or facade. That must be matched during 3D integration. This retains the important large-building silhouette and stops subsequent infill from consuming its site. Details: [preservation report](reports/hotzone_landmark_retention_round3.md), [protected footprint](data/landmarks/hotzone_largest_earlier_building_retained.geojson), and [replay script](scripts/retain_hotzone_landmark_round3.py). The revised full building placement file and single-file review website are stored privately in the Spaciel working Library; the public website has not been changed.
