# Spaciel — native-scale building assembly, draft 01

Date: 10 November 2026. **Review-only working result. No city layout has been changed or published.**

## Goal

Place original SketchUp architectural forms into the already-approved Night City V10 building areas, preserving source model dimensions and existing architectural character. Prefer keeping original SKP instances where they sit. Where that is not geometrically feasible, reuse the original model's unscaled geometry elsewhere within an appropriate plot, with translation and rotation only. Empty areas are acceptable when nothing fits safely.

## First placement results

- 11,508 approved V10 target footprint polygons considered across the map.
- 4,902 screened original SKP source instances available as native 2D projection envelopes.
- **8,618** provisional building placements selected, linked to their original SKP model/instance IDs.
- **228** retain the source-instance location; **8,390** are unscaled reuses moved to target sites.
- These cover **8,516 distinct target IDs** (not full site-area coverage). **2,992** target IDs have no direct assignment. Some overlap existing accepted buildings and some have no safe size/position match.
- **2,568 distinct native source definition IDs** used. Repeated source designs are permitted, but the algorithm modestly penalises excessive repetition.
- Native 3D source models were **not scaled**. Geometry screening is based on each model's 2D convex-hull projection, not a newly generated building mesh.
- Per-site `style` from the approved V10 working character layout influenced source-height selection. This is a heuristic, not a visual district-by-district approval.

## Geometry validation

An initial pixel-based spatial screen enforced a 2.6 Atlas-pixel buffer around cleaned V17 road centrelines and avoided occupancy conflicts. Independent Shapely geometry validation then found four small residual overlaps; four later infill proposals were removed. Final checks: **zero source-hull to road-buffer violations** and **zero overlaps greater than 1.3% of the smaller placed hull**.

### Important limitations

- This is a 2D **placement plan with original model IDs and transformation instructions**. The exact original SketchUp 3D face meshes have not yet been instantiated into the terrain viewer at these proposed locations.
- The 2.6-pixel road-centreline clearance is provisional and is **not** a verified road-surface width or building setback.
- Coastline, foundations, grade changes, individual landmark identity, and small site-level architectural composition all require follow-up inspection.
- Source polygons are **convex hulls**; they may exaggerate a concave building's real occupied area.
- The approved target polygons have 3,182 documented overlap pairs; this draft leaves the original V10 polygons unchanged.
- A source model's source-world position does not by itself certify its historical identity on the V10 footprint.

## Private review and repository rules

The user has a standalone, interactive HTML review page with zoom, pan, source/target filtering, placement metadata and manual review-decision export, alongside a detailed source-derived GeoJSON and CSV. They are kept **private** because the original model's extracted geometry and per-instance placements may be subject to rights restrictions. This public repository stores only the overview, counts and reproducible code.

## Suggested next pass

Inspect the assembly in a few representative character areas (dense urban, suburban, waterfront, military and Hot Zone). Prioritise the 2,992 target IDs still without a direct assignment; some will correctly remain empty or belong to larger grouped areas. Introduce verified road widths, coast and terrain checks before merging the source meshes into the full V19/3D renderer.