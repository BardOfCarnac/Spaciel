# Spaciel — broader-block packing, Round Three / Draft 04

**Status:** Provisional 2D working layout, NOT an approved final map or a published source-model asset.

## Design decision

The historic V10 building footprints are not parcels to fill one by one. Round Two preserved 6,257 source-scale model footprints in a footprint-derived gold region, while the older October 560 road-separated urban blocks cover much more of Night City. This pass leaves the 6,257 previous placements untouched and fills additional *reviewable* area in the recovered older road-block geography.

## Output

- Previously placed: **6,257**, preserved.
- Newly placed, rigid transformations without stretching: **1,601**.
- Total provisional building outlines: **7,858**.
- Distinct original SketchUp model source definitions across the combined draft: **3,081**.
- Coverage of the union of current gold and recovered broad blocks at 3304×5100 working raster: **34.29%**. (Not comparable to Round Two gold-only percentage without noting the larger denominator.)
- Roof-outline coverage within the specifically approved-for-trial *extra* review area: **16.12%**. Remaining space includes intentional gaps and candidates not verified safe.

## Constraints / QA

- No original-source geometry was rescaled, enlarged or stretched; only translation and rotation.
- Road corridor exclusion is based on current V17 cleaned lines with stylized 9–15 m width estimates and a minimum extra margin, **not certified kerb boundaries**.
- A recovered Hot Zone preserve polygon is withheld from new placements; its existing sparse Round Two treatment is unchanged.
- Highly saturated atlas water/landscape colours are conservatively excluded from new placements. This is not a complete shoreline polygon or park masterplan.
- All new polygons passed coarse mask and occupancy tests, and a post-placement source-polygon audit against existing models, other new models and road-line proximity. Unresolved tolerances and areas need a visual check.
- Source model IDs, model polygon outlines and placements remain private because the SketchUp source's redistribution rights were not established. Only aggregate counts and this method are committed publicly.

## Important limitations

This is a citywide **infill trial**, not a fully repacked skyline. Some old V10 gold polygons lie outside the recovered 560 blocks. The combined preview keeps those previous buildings but does not imply all polygon combinations are certified land. Water, actual coastlines, grades, fine road widths, and neighbourhood-scale aesthetic review remain open. No 3D viewer was altered.