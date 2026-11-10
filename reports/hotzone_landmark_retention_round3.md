# Spaciel – Hot Zone landmark retention, Round Three revision

Date: 10 November 2026. **Working 2D placement revision. Not a final 3D model.**

## Decision

Retain at least one large, intact building in the Hot Zone. Prefer the largest footprint from the earlier approved V10 layout rather than automatically clearing all the original large structures. The intended surroundings remain largely sparse and damaged.

## Selected earlier building

- Source: `Night_City_V10_Completed_Footprints.geojson` (previous approved building layout)
- Original footprint ID: `original-4125`
- Selection basis: largest ground-area polygon among the earlier V10 footprints overlapping the saved Hot Zone preservation outline (approx. **8,357 atlas px²**)
- Centre: approximately **(2426.23, 3741.77)** in 5175×7966 Atlas map pixels
- Road-centreline clearance: approximately **60.42 Atlas px** against the current V17 cleaned centreline graph
- Important: the **exact original SketchUp mesh and original building height are not authenticated**. Retaining the earlier footprint preserves a deliberate large-building landmark and its site; it is *not* a claim that its final SKP geometry has been reinstalled in the 3D renderer.

## Change to Round Three

- Baseline: 7,858 provisional source-derived building placements (6,257 from Round Two plus 1,601 Round Three additions).
- Remove 11 small placements that touch the original large footprint or its 2.5 Atlas px clearance zone.
- Reserve the historical footprint as one large protected landmark. No scaling of any existing SketchUp model.
- Updated provisional 2D count: **7,848 footprint objects** (7,847 existing source-derived buildings plus one preserved large-building footprint).
- **The other 7,847 placements are unchanged**. No road graph, districts, terrain, coastline, unrelated buildings or live website were altered.
- The retained footprint clears road centrelines and other remaining building outlines by the stated margin.

## Follow-on integration

In the 3D migration, use the retained outline as an authoritative *reserved landmark site*, recover the closest original V10/V19 massing or authentic SKP mesh for that specific building, and preserve its large silhouette. If no source mesh can be verified, keep a clearly marked provisional massing rather than fabricating a supposedly original SketchUp building. The user has not requested complete Hot Zone reconstruction or blanket infill.

## Files

- `data/landmarks/hotzone_largest_earlier_building_retained.geojson` — public geometry of the protected V10 planning footprint.
- Private Spaciel Library: the revised 7,848-object city 2D outline layer, standalone interactive review website, cropped before/after comparison, full-city preview, and list of removed smaller placements.