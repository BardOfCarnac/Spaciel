# Spaciel — block-first native building assembly, Draft 02

**Status:** Provisional 2D placement draft, no 3D viewer or source geometry modified.

## Correct placement principle

**The contiguous gold areas represent buildable space; they are not individual building-footprint slots.** The older 11,508 V10 footprint polygons were only used to establish the gold areas and offer a *broad* neighbourhood-character guide. We do **not** try to place one SKP building per V10 polygon or demand that a model cover a named footprint. Large gold regions may contain dozens of original-model buildings, small buildings may share a region, and unfilled spaces are allowed.

## Inputs and method

- Gold block mask from previously approved `Spaciel_Building_Blocks_Only.png` (3304 × 5100). This mask was earlier derived by small-gap closure of approved V10 polygons with cleaned road corridors preserved.
- Original user-supplied SketchUp-derived, native-scale model hulls (4,902 original placements in private archive). Source polygons are source-geometry convex-hull plan projections, not full face meshes.
- Source placements are kept at their original 2D positions when fully within the gold area and free of overlaps. Otherwise buildings are **translated or rotated as rigid shapes**, never scaled or stretched. Their native source IDs and full native metric dimensions are preserved.
- Candidate location centres are **free-grid samples in the gold areas**, never the old footprint centres. Broad architectural styles come from nearest earlier styled V10 polygons. An inset gold mask and occupancy halo stop candidate building polygons from crossing block edges or overlapping other placed polygons at working raster precision.
- These do not constitute reconstructed original historical positions, cadastral blocks, or full 3D mesh integration.

## Preliminary draft counts

| Metric | Result |
|---|---:|
| Total provisional native-source instances | **3,571** |
| Original-position building instances kept | **140** |
| Models rigidly reused within gold areas | **3,431** |
| Different native source designs | **2,501** |
| Gold area occupied by building hulls (no spacing) | **30.3%** |
| Gold area reserved by buildings **and** a narrow spacing halo | **46.6%** |
| Exact Shapely overlaps over 0.5% of smaller hull | **0** |
| Exact Shapely crossings of cleaned road centrelines | **0** |
| Invalid placed polygon hulls | **0** |

Coverage is based on source convex hulls and does not constitute final solid roof coverage. Gold occupancy is not the same as the number of V10 footprint IDs; there is **no intended 11,508-building quota**.

## Review priorities

1. Compare appearance and density block by block, particularly central corporate districts versus suburb/port/industrial areas.
2. Re-run infill passes using still smaller source models where visually too empty; retain space for courtyards and vacant lots where appropriate.
3. Validate true coastline/water, actual roads/kerbs and slopes. Current mask reflects only the earlier road-centreline-protection layer and is not surveyed road width.
4. Integrate 3D SketchUp face meshes only after approving candidate source IDs and placements.
5. Keep source-derived exact geometries, original SKP library and the private interactive HTML outside the public GitHub repo pending model redistribution rights.

## Versioning

**Draft 01 (8,618 placements) is superseded for placement logic:** it incorrectly treated each old approved footprint as an individual destination. It remains as an audit of that failed approach, not an architectural layout approval. The gold buildable areas are now the single source of truth for placement allowance.

`data/blocks/gold_buildable_regions_v1.geojson` provides approximate editable vector outlines of the gold mask; mask-pixel geometry remains the working placement authority. No previous road, terrain, district, SKP source or approved block dataset is overwritten by Draft 02.