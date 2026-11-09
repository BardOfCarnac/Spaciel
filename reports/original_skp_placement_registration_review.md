# Spaciel — original SKP placement registration review

**Status (9 Nov 2026):** original source instances have been extracted, road registration replayed against current V17 linework using nine saved controls, and a non-destructive placement audit of 4,902 source building envelopes has been completed. This report changes none of the 11,508 approved V10 footprint shapes or positions.

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
- **Resolved:** `(1).skp` and `(2).skp` are byte-for-byte identical (SHA256 `17317588df75a4bea8a87ad86d0438ff112c693f6c54e4ca9da4fa4c53842ee0`). Their same map frame is established. Earlier placement-count differences reflect extraction methods.
- The raw source contains **16,499 unique top-level instances** linked to 13,697 distinct definition IDs, recovered with native transforms. The screened catalogue contains 4,462 complete building-envelope definitions. **4,902 placed top-level instances** use 4,427 of these definitions; 35 screened definitions are not top-level placed. The prior 1,520 geometry-fit proposals remain alternate architectural candidates, not original-location authentications.

## What is now ready

`audit_skp_original_placements.py` supports importing genuine original placed building polygons in either original SKP plan pixels or raw SKP-world XY inches (the latter via the archived source map conversion). It then:

1. Converts their geometry to the authoritative Atlas-pixel frame with V2.
2. Checks intersections and nearest distance to real V17 **road centrelines** (not road-edge buffers).
3. Finds overlapping approved V10 target polygons, listing coverage and IoU as **candidates**, not identifications.
4. Exports a non-destructive Atlas overlay, per-instance CSV review and summary counts.

It does **not** stretch models, move roads, authenticate the original identities, assign new locations, or accept a near polygon match as fact. The script deliberately has no automatically promoted final building placements.

## How to advance

**Recovered:** the actual original SKP in the user's Library (and its identical named copy). `extract_skp_original_instances.py` now recovers the instance IDs, definition IDs and native 13-value transformations. `build_original_placement_outlines.py` extracts the source vertex hulls, transforms them with the original component matrices, and projects them through the V2 road registration. It keeps private exact source-derived geometry out of the public repository.

The road and site audit of all 4,902 source building placements produces:

| QA classification | Original instances |
|---|---:|
| Direct V17 road-centreline intersections | 739 |
| Within 5 Atlas px of a centreline (no intersection) | 242 |
| Source polygon covers at least 50% of itself within an approved target, road clear | 271 |
| Some other target overlap, road clear | 445 |
| Road clear, target polygon within 5 px but not touching | 91 |
| Road clear, target polygon 5–10 px away | 51 |
| Road clear, target polygon 10–20 px away | 98 |
| No nearby approved target within 20 px and road clear | 2,965 |

These categories add to 4,902 and are **diagnostic**, not final move/keep decisions. There are **818** pairs of source convex hulls overlapping by at least 25% of the smaller shape, involving **955** source instances; some are nested architecture. There are **576** almost-contained pairs. Among the 271 high-overlap candidates, 224 avoid any 25%-overlap with another screened source instance; these span 137 distinct target sites. One candidate per target forms the first **137-site manual visual shortlist**.

**Caution:** convex hulls can exaggerate actual source geometry (courtyards/concavities) and the road data is centreline geometry, not road widths or shorelines. The project should visually inspect these 137 and then expand to small-jiggle candidates. The full SKP binary, source face meshes and private exact placed hulls were not uploaded to the public GitHub repository.

Next compare representative source buildings visually on the registered Atlas, including roads and waterfront; vet the 137 clean in-place shortlist first. Keep unmatched native architecture available for reuse; the 11,508 approved polygons remain layout guides, not moulds.

All the earlier cross-version figures in this report remain **working diagnostics**. They must not be read as evidence that source buildings already fit their original sites.
