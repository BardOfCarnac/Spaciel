# Spaciel viewer builds

## Latest private skyline-first mockup — Realisation 13 (11 November 2026)

Per the updated placement approach, **large original SketchUp models take priority**. A reversible private city mockup now places **399 additional original large buildings** near their approximate historical source areas, without changing their original model shapes or scale. **1,027 smaller provisional placements** have been held in a fully recoverable infill reserve so smaller buildings can later be packed around the restored skyline. Previously **none** of the 20 largest screened source definitions was placed; **13** are now represented.

The resulting staged viewer contains **7,367 building objects**, including **7,356** source-derived direct-face mesh instances in **60** architectural tiles; **71** of the new buildings exceed 100 m in original source height. Our **556 tagged locations**, search, V17 offline road graph and experimental V21 layer remain unchanged. Road placement uses approximate atlas-painted exclusions and must receive a final visual review. [Read Realisation 13 aggregate report](../reports/native_skp_realisation_13_skyline_first_2026_11_11.md).

The self-contained HTML, modular private viewer ZIP, before/after image and detailed reversible infill reserve are available in the private ChatGPT Library at `/Spaciel/working-data/`. Desktop/mobile HTML fallback checks passed. GPU WebGL2 hardware visual testing and a served modular test remain outstanding.

## Previous milestones
- [Realisation 12 — staged two-building restoration](../reports/native_skp_realisation_12_staged_restoration_2026_11_11.md)
- [Realisation 11 — completed screened source catalogue](../reports/native_skp_realisation_11_complete_source_catalogue_2026_11_11.md)
- [Realisation 10 — approximate original anchors](../reports/native_skp_realisation_10_original_anchors_2026_11_11.md)
- [Realisation 09 — first original large source recovery](../reports/native_skp_realisation_09_large_originals_2026_11_11.md)
- [Realisation 08 — tiled architecture](../reports/native_skp_realisation_08_tiled_private_viewer_2026_11_11.md)

## Public code, private source geometry

The public `viewer/src/` holds source-independent loading, view and placement helpers only. The original SKP/GLBs, private source-derived HTML viewer, geometry tiles, footprint coordinates and original source registries are not committed to this public repository.
