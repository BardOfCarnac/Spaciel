# Spaciel integration inventory — 2026-11-11 (v1)

Status: AUDITED / NON-DESTRUCTIVE. This is a registry of located source files and integration contracts, not a claim that the final viewer exists. Prepared from the repository default branches, experimental branches, and metadata for the private Spaciel Library. The standalone viewers and original source assets have **not** been copied into the public repository.

## Repository ownership and publication boundary

- **Application, working geometry and public code:** https://github.com/BardOfCarnac/Spaciel (main).
- **Earlier terrain and geographic registration:** https://github.com/BardOfCarnac/Cartogram (main).
- **Private licensed/source-derived viewers and meshes:** ChatGPT Library /Spaciel/working-data/.
- **Frozen approved interaction reference:** ChatGPT Library /Spaciel/approved-baselines/.
- Do not commit private complete HTML, original SketchUp (.skp), source-derived GLBs, source-face spatial tiles, licensed atlas art, or complete licensed-derived placements to this public repository without confirming redistribution rights.
- Treat a reference in this inventory as *located*, not necessarily visually approved, production ready or already integrated.

## Component register

| Component | Best located reference | Authority/status | Format and integration condition |
| --- | --- | --- | --- |
| Elevation registration, basic terrain | Cartogram: data/night-city-2045/terrain/registration.json; terrain/README.md; tools/build_night_city_heightfield.py; terrain-source.json; water-mask.geojson | Historical canonical terrain inputs, **not** the final integrated mesh | 780 x 1200 registered map-pixel basis; original DEM and full heightfield are not in public repo; bridge to final atlas explicitly |
| Current terrain triangulation, crater and bowl viewer | Approved design from previous map work; integrated private viewer may embed terrain/height data | Exact latest standalone terrain source and shader/mesh **not individually certified by this audit** | Recover/test latest mesh and height sampler; do not substitute coarse Cartogram contour layer for final terrain |
| Optical water | Private Spaciel_Water_Material_Implementation_Spec_v1.md (approved visual contract, 10 Nov); Coastal Water V2 look reference; experiment/ocean-v3-living-light-20261110: experiments/Spaciel_Ocean_V3_Living_Light.html | Visual direction approved; V3 experimental; V19 spectral integration/repaired branch remains experimental | Must share final land/water mask and world-space shoreline distance field, no synthetic coast; fix low-resolution shore, large dark patch, seam/line; keep glints separate from phase |
| Road network — stable fallback | Spaciel main: data/roads/v17_cleaned_road_centerlines.geojson and data/roads/v17_road_width_classes_by_chain.csv | Reliable offline baseline in private review viewers; not certified road-edge geometry | 2,422 chains; 5175 x 7966 working atlas frame; width estimates need review |
| Road network — latest experiment | Spaciel branch experiment/roadcraft-v21-cartographic-grammar: experiments/roadcraft_v21_cartographic_grammar_viewer.html and roadcraft_v21_straightening_proposals.json | **Experimental, not approved final**; see reports/roadcraft_v21_round3_combined_review.md | 792 x 1224 source frame; provisional registration into working atlas; 607 potential road/footprint ribbon conflicts, not a move list |
| Buildings / placements | Private Spaciel_Realisation_09_Landmark_Review.html and Spaciel_Realisation_09_Review_and_Modular.zip; public viewer/README.md and reports/native_skp_realisation_09_large_originals_2026_11_11.md | Latest private review workbench; no new large model placement automatically approved | 7,993 provisional placements; protected Hot Zone landmark and 11 shoreline holds preserved |
| Native source building draw path | Private Realisation 08 tiled viewer and assets; public viewer/src/native-architecture-tiles.js and architecture-view-tiles.js | Tiled source-face rendering prepared; real GPU/WebGL2 appearance still unverified | 7,981 registered direct-face instances, 3,079 templates across 60 spatial tiles; up to 16 GPU tiles at a time |
| Unplaced large architectural buildings | Private Realisation 09 100 source-derived GLBs, gallery and QA | Candidates only, not installed | Largest 20 source definitions missing from city placements; do not assign sites using unverified registration |
| Main locations, category tags | Spaciel main: data/locations/spaciel_locations_556_corrected_2026-11-10.json; docs/location_register_fix_and_book_reconciliation_2026-11-10.md; scripts/apply_location_patch_2026_11_10.js | 556/556 corrected records have unique IDs and display tags; not proof every V19 build carries patch | Preserve coordinates and row order, map by record_index plus name; carry category and display_tag together; 51 Playland attractions deferred |
| Pin viewer / icon roles / spectrum bar | Private /Spaciel/approved-baselines/Spaciel_Approved_Category_Morph_2026-11-11.html; docs/approved_category_visibility_morph_2026-11-11.md; icon prototypes in Cartogram/tools/ | Frozen approved 661-pin V19 reference (556 main + 105 separate Vend-R pins) | Preserve glyphs, 7 colour families, bubble placement and spectrum bar; distinguish separately plotted Vend-R pins from linked venue search |
| Visibility morph | Same approved V19 snapshot and docs/approved_category_visibility_morph_2026-11-11.md | **Approved / frozen** | Out: glyph -> ball -> nothing 610 ms; in starts at 85 ms, lasts 615 ms; 720 ms overall; unaffected pins stay in place; used on any icon disappearance |
| Unified search | Spaciel main: src/search/spaciel-search.js and .css; data/search/unified_geographic_v1.json; tests/test_unified_search.js; docs/unified_search_standard.md | Canonical reusable search module exists, not automatically mounted to every viewer | 24 districts + 11 neighbourhoods + 527 named streets + live pins and linked Vend-R venues; single search handler, shared camera selection adapter |
| District/neighbourhood ghost text | Private Spaciel_District_Ghost_Labels_Study_02.html; subsequent draft placement JSON supplied in map discussions | Prototype/study and 24-district draft; integrated production JSON not located on main | Register 1396 x 1536 study coordinates to world atlas; maintain zoom thresholds/ghost behaviour; do not confuse search geography with artwork placements |
| Viewer shell, camera, interaction | Private Realisation 09/08 modular ZIPs; Spaciel main viewer/src/ generic loaders; V19 approved HTML for visual UI | Private viewer works in Canvas fallback smoke tests; public repo is **not** a complete runnable final app | Preserve colour bar, bubbles, bottom interface, selection and approved camera behaviour; verify WebGL2 on actual hardware |

## Coordinate contract and registration risks

**Do not assume that identical-looking pixels are identical coordinates.**

- Cartogram terrain historical grid: **780 x 1200** (see its registration.json), tied to DEM/regeneration.
- Sourcebook/V21 road art frame: **792 x 1224**.
- V19 main POI register bitmap frame: **3300 x 5100**.
- V19 search district/neighbourhood source: **792 x 1224** in the combined review; search module also documents prototype **900 x 1390** framing for district/neighbourhood results. These are different adapters and must be checked against the actual data.
- Ghost Label Study 02: **1396 x 1536**.
- Native building and modern combined-viewer working atlas: **5175 x 7966**, x right, y down (data/registration/atlas_skp_roads_v2.json).
- SKP source plan: **6930 x 5562**, registered via V2 transform, but source-site identities remain unverified.
- Round Five private mockup scales V19 POIs 3300 x 5100 into 5175 x 7966 and uses V17 streets already in 5175 x 7966 (reports/roads_buildings_tags_integrated_mockup_2026_11_11.md).
- The 3604 x 3604 DEM and final terrain mesh must not be assumed interchangeable with Cartogram's older 780 x 1200 reference.

**Integration rule:** create one central coordinate adapter (named source frame -> single world frame), one shared land/water mask, and one elevation sampler. All layer positions, coastline SDF, building bases, roads, labels and camera destinations must resolve through these services. Do not independently scale or fudge each rendering module.

## Recommended modular boundaries (proposed, not already implemented)

1. **Geography / data:** atlas registration, transforms, terrain elevation, city masks, road graph, district outlines, location catalogue, search index.
2. **Renderer:** camera and scene, terrain mesh, water material, road strokes, tiled architectural instances, labels, POI markers.
3. **Interaction controller:** selection, filters, layer visibility, transitions, popup state, camera destinations and app deep-links.
4. **UI:** approved V19 spectrum bar, search panel, glyphs, bubble/window presentations and layer/debug controls.

Explicit interfaces to add:
- transformPoint(fromFrame, toFrame, [x,y]) and assert bounds.
- heightAt(worldXY) and isLand(worldXY) with one datum.
- roadLayer.load(version) with fallback status visibly exposed.
- buildingTiles.load(camera) with original placement IDs and review holds.
- locations.load(base, patch) with unique-ID and tag/category assertions.
- search.resolve(query) -> typed focus target; focus(target) delegates to controller.
- marker.transition(oldVisible, newVisible) preserving approved morph.
- labels.layout(camera, districtGeometry) separate from search index.
- ocean.sample(worldXY, sun, view) using authoritative coast and SDF.

## Prioritised integration checks

1. Save/keep frozen V19 and Realisation 09 private snapshots unmodified; record file checksums in private manifest where accessible.
2. Build central coordinate transform audit using stable known control points and shoreline anchors; verify both POIs and building/road controls across the city before changes.
3. Restore true terrain with consistent height sampling, then align approved coastline and water SDF; inspect the reported dark water patch, straight seam, coastline pixelation and Del Coronado inlet.
4. Bring in V17 stable roads, V21 separately switchable as experimental; inspect flagged conflicts visually (607 preliminary checks in 10 Nov review), no bulk building moves.
5. Load Realisation 08/09 architecture on actual WebGL2 hardware; test tiled buffer lifecycle, identity, original mesh geometry, held shoreline points and 100 unplaced large candidates.
6. Apply corrected 556-POI dataset to a **new** viewer snapshot with ID/tag tests; confirm 661-pin visual policy as appropriate, custom icon family and bubbles unchanged.
7. Mount unified search exactly once; exercise district, neighbourhood, street, place, venue and filter switching.
8. Import ghost label draft as editable data, register correctly, and check hierarchy, visibility, collisions and shoreline clipping.
9. Run desktop/mobile touch and GPU tests; render comparison shots at citywide, district, street and coastline zoom levels. Verify no change to approved morph timing and UI look.

## Known gaps / caution flags

- No complete public modular application or approved full water/terrain merger found on Spaciel/main.
- Private portable and modular architecture viewers are **found** in the Library, but their actual GPU output on user hardware is not established.
- The V21 road shape is experimental and includes registration/road-width assumptions.
- The 11 shoreline building holds, protected Hot Zone landmark, 100 unplaced large source models and possible road/building conflicts are not final placements.
- The 556 corrected location register is not automatically applied merely because its patch was committed; different viewer snapshots may carry different data.
- The approved ghost-label placements are a draft data source, not a committed canonical production layer.
- Water's approved V2 look has not been proven correctly joined to the production coastline at all scales.
- The user requested that actual terrain massing, coast and approved icon/category logic survive the integration; avoid prototype stand-ins when those authoritative assets can be recovered.

## Status handling

Use **APPROVED/FROZEN** only for explicitly accepted UI/visual behaviour; **DATA CORRECTED** for published datasets awaiting viewer migration; **EXPERIMENTAL** for Roadcraft V21 and water trials; **PROVISIONAL** for building placements/model candidates; **UNVERIFIED** for GPU output and unresolved coordinate alignment. Do not silently upgrade status in future integration passes.

## Source pointers

- [Spaciel main README](../README.md)
- [Spaciel private viewers registry](../viewer/README.md)
- [Combined viewer report](../reports/roads_buildings_tags_integrated_mockup_2026_11_11.md)
- [V21 road review](../reports/roadcraft_v21_round3_combined_review.md)
- [Realisation 08](../reports/native_skp_realisation_08_tiled_private_viewer_2026_11_11.md)
- [Realisation 09](../reports/native_skp_realisation_09_large_originals_2026_11_11.md)
- [Approved category morph](approved_category_visibility_morph_2026-11-11.md)
- [Unified search](unified_search_standard.md)
- [Location corrections](location_register_fix_and_book_reconciliation_2026-11-10.md)
- [Cartogram terrain registration](https://github.com/BardOfCarnac/Cartogram/tree/main/data/night-city-2045/terrain)
- [Ocean experimental branch](https://github.com/BardOfCarnac/Spaciel/tree/experiment/ocean-v3-living-light-20261110)
- [Roadcraft V21 experimental branch](https://github.com/BardOfCarnac/Spaciel/tree/experiment/roadcraft-v21-cartographic-grammar)
