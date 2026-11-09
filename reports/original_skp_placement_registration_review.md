# Spaciel — original SKP placement registration review

**Status:** working alignment validated against saved road checkpoints; **original building instances are not yet independently registered**. This report does not change the existing 11,508 V10 footprint shapes or their locations.

## Why this matters

The old V1 uniform-image fit is not adequate to place source buildings. An already archived **V2 road-derived affine transform** (from the original `Night+City2045_2 (1).skp` map image) accounts for different X/Y map scale. The V2 SKP-plan→Atlas formula is:

```
x_atlas = 1.0956952680760181*x_skp - 0.00036675251033988057*y_skp - 1430.5202834740833
y_atlas = 0.00028172297856186564*x_skp + 1.426397634249643*y_skp + 746.1248161129311
```

The transform coefficients, prior residuals and inverse are preserved machine-readably at `data/registration/atlas_skp_roads_v2.json`.

## Replay against our current V17 road linework

Nine saved road points, identified as Watson Blvd (2), Kennedy Ave (3) and Marina Blvd (4), were projected into current V17 *Atlas-pixel* road-centreline coordinates and checked against the nearest road line. This is a useful **cross-version consistency check**, not a new independent survey.

| Check | Maximum nearest-road-centreline distance | Meaning |
|---|---:|---|
| Old V1 uniform map fit | 119.2 atlas px | Wrong for source placement |
| V2 road-derived affine fit | **2.6 atlas px** | Good match to current V17 linework at 9 saved checkpoints |

The earlier V2 registration had separate residual measurements against the SKP road traces (mean about 3.1–8.6 SKP px across the three named roads; maximum 12.8 SKP px). Replayed nearest-road distances are not identical to named-road trace residuals, and a nearest-road match alone is insufficient to certify site identity.

**Important:** `night_city_2045_visual_road_layer_v17.geojson` uses *local 3D world kilometres* (about -5..10), not Atlas pixels. We use `v17_cleaned_road_centerlines.geojson`, the 2,422-chain cleaned Atlas-pixel display layer. Confusing the two creates false failures.

## Important source-version distinction

- The V2 alignment and the original 6930×5562 SKP plan-image projection were recorded for `Night+City2045_2 (1).skp` (16,383 placements in the older extraction metadata).
- The 4,462 usable source-envelope catalogue and newer native geometry were extracted from `Night+City2045_2 (2).skp` (16,499 top-level instances reported in prior reconciliation, including non-buildings).
- **We have not yet proved that (2) uses the same SKP plan pixel frame as (1)** or recovered a per-instance placed-footprint file with native placement IDs in that frame.
- A catalogue of *definitions* and their sizes is not equivalent to the original *placed instances* and transforms. The 1,520 previous verified geometry choices are suitable architectural candidates, but do **not** authenticate any original SKP building location.

## What is now ready

`audit_skp_original_placements.py` supports importing genuine original placed building polygons in either original SKP plan pixels or raw SKP-world XY inches (the latter via the archived source map conversion). It then:

1. Converts their geometry to the authoritative Atlas-pixel frame with V2.
2. Checks intersections and nearest distance to real V17 **road centrelines** (not road-edge buffers).
3. Finds overlapping approved V10 target polygons, listing coverage and IoU as **candidates**, not identifications.
4. Exports a non-destructive Atlas overlay, per-instance CSV review and summary counts.

It does **not** stretch models, move roads, authenticate the original identities, assign new locations, or accept a near polygon match as fact. The script deliberately has no automatically promoted final building placements.

## How to advance

Next input required: actual **original per-instance footprints** or native instance transforms exported from `Night+City2045_2 (2).skp`, with stable IDs, original world coordinates, orientation and definition references. A raw SketchUp file is not currently present in this session's accessible working files. The already archived V19 SketchUp wireframe can help visually, but its separate lines alone do not recover all definition/group IDs.

Before running the city-wide keep/jiggle/reuse classification, compare at least 3 widely separated **road junctions** and 3 recognizable **source building landmarks** in (2) against the registered Atlas. Preserve unmatched structures for reusing as assets; use the 11,508 approved polygons as a layout guide, not a mould.

All the earlier cross-version figures in this report remain **working diagnostics**. They must not be read as evidence that source buildings already fit their original sites.