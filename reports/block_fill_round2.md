# Spaciel — Round Two: building block repack

**Date:** 10 November 2026  
**Status:** Unapproved 2D assembly and review website. Source 3D meshes, roads and terrain remain unchanged.

## Why we changed the method

The earlier fixed-footprint matching approach was wrong for the user's intent: the **gold regions are shared buildable blocks**, not one-to-one destinations for the historical V10 building outlines. The original 11,508 footprint polygons define an approximate buildable mask and provide geographic character context only.

Draft 02 improved this by freely placing 3,571 source-scale SketchUp hulls within gold space. But it prioritised sites with large central clearance, leaving thin unused strips along block edges and producing an underpopulated street frontage. Draft 02 covered **30.3%** of gold area with building outlines.

Previous layout iterations taught us to preserve road edges, coastline and regional morphology; duplicate good original structures to fill gaps; keep major building fronts close to streets; avoid random vacant roadside blocks; keep substantial ruins/voids in the Hot Zone, and use more spaced residential layouts in suburban, affluent and executive neighbourhoods. Open spaces must be deliberate, not accidental scraps.

## Round Two changes

Rather than merely scattering smaller items into Draft 02's spaces, we **repacked the provisional non-original placements** while retaining **140 original-position buildings**. Placement is free anywhere inside the existing gold areas. Larger buildings were favoured first, especially along road-facing edges, followed by ordinary and compact infill. The longest source building axis may be rotated to follow a nearby gold-area edge, but model proportions are never changed.

Character-aware regional density caps limit development in the Hot Zone, Executive and other open districts. In denser urban/commercial/corporate blocks, touching sidewalls are allowed, which is more appropriate than forcing arbitrary gaps between row buildings. Source design reuse avoids putting duplicates immediately beside themselves. Buildings remain plain closed-source structures, as approved; window/facade detail is not an acceptance requirement.

## Outcome

| Measure | Draft 02 | Round Two |
| --- | ---: | ---: |
| Total SketchUp-derived placement hulls | 3,571 | **6,257** |
| Retained original positions | 140 | **140** |
| Repositioned original model instances | 3,431 | **6,117** |
| Distinct source designs | 2,501 | **2,930** |
| Physical building outline coverage of gold mask | 30.3% | **57.06%** |
| Coverage including style-specific separation buffers | 46.6% | **63.45%** |

Among the newly repacked proposals, **5,582** were placed in frontage-priority stages and **535** in internal-filling stages. Earlier Draft 02 positions (except the 140 original-source placements) are superseded, not presumed approved.

## Validation

- **6,257/6,257** placement hulls valid.
- **0** direct intersections with the cleaned V17 road centrelines.
- **0** hulls protruding beyond the gold mask at raster resolution.
- **0** building-pair overlaps greater than half of 1% of the smaller hull. There remain 66 tiny sub-threshold geometric intersections, with the largest **0.4677%** of the smaller hull.
- **12** automatically generated placements failed final geometric auditing and were rejected, rather than moving the fixed city boundaries.

These checks apply to **2D projected convex-hull approximations**, not full surveyed kerb widths or final 3D solids.

## District / block audit

Initial region-based occupancy analysis, using style estimated from nearest previous V10 footprint, shows approximately **63.7%** physical block coverage in corporate areas, **60.3%** in urban, **63.3%** in mixed-use, and **34.9%** in the Hot Zone. This approximates the intended contrast rather than making every gold area solid buildings.

Only **1** urban/commercial/corporate-style gold region(s) larger than 800 working pixels are below 35% built coverage. Such labels and gaps need manual map review before any permanent changes. Larger empty spaces in coastal/open districts are not automatically faults.

## Deliverables and protections

- **Private:** `Spaciel_Building_Blocks_Round_02.html`, interactive single-file website comparing Draft 02 and Round Two; `Spaciel_Block_Fill_Draft03_REPACK_PRIVATE.geojson` with exact source-derived hull placements; `Spaciel_Block_Fill_Round_Two_Comparison.png`.
- **Public GitHub:** the reproducible assembly algorithm (`scripts/assemble_native_buildings_block_round2.py`), this methodology report and aggregate audit summaries. Do not publicly commit exact SketchUp mesh geometry, source-derived hull polygons or licensed SKP binaries until redistribution rights are checked.

**Next:** inspect representative dense blocks and the remaining unusual coastal/large-gold regions in the viewer; verify full road surface widths, coastline and terrain foundations. Only then attach the approved original SketchUp 3D mesh geometry to these locations in the live city viewer. No website has been published.