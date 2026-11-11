# Spaciel Modular 05 — genuine R14 buildings and original V17/V6 terrain

**11 November 2026, private device-review candidate.** The user's prior Modular 04 screenshot showed architecture and terrain that were not the approved native assets. This update keeps the main V19-based viewer and corrects both layers rather than substituting a different standalone viewer.

## True SketchUp-derived native architecture

The private **Spaciel Realisation 14** source contains **8,821 placed objects**, of which **8,810** refer to original source-face geometry derived from **3,813 SketchUp definitions**. Original native model vertices were transformed using their saved source-to-atlas placement transforms into the current V19 native GPU tiling format (60 compressed geographic tiles; no re-scaling, boxes or extruded-footprint substitutes). Building source geometry persists at close zoom and does not switch to legacy representations.

A cross-check against the staged Roadcraft V23 centreline network found exactly three footprint crossings. For this review, only the three visible instances `block-5057`, `round3-new-475`, and `round3-new-1073` are withheld from GPU tiles; originals remain untouched for later review. The other **8,807 native mesh instances**, totalling **365,004 source triangles**, remain. The 11 R14 objects without original source faces are not fabricated as new meshes.

## True native adaptive terrain

The newer **V17 crater V6 local patch** is the authoritative native triangle source for this build: **12,884 irregular native triangles**, retaining original vertices, normals, elevations, lowest-corner face colours, and subtle 4% original edge lines. Relative to the earlier 12,728-face original native mesh, the V6 patch keeps 12,658 earlier faces, replaces 70 and adds 226 around the Hot Zone. This is **not** the old V19 20m square grid, and is **not** a uniform subdivision of native triangles into 206,144 synthetic facets.

The source 520×800 V17 registered elevation grid drives draping/camera heights. A V17→V19 world affine maps native geometry into the same camera, buildings, roads and pin universe as the existing viewer. Existing V19 classification and optical water remains preserved; coastline height seams require device review.

## Preserved modules

Approved 661 location pins, V07 location bubbles, closing animation, unified search and top-left expanding magnifier, approved exact-icon-RGB spectrum focus, V23 road candidate (1,992 paths) and older road comparison layer, registered water shaders, modular camera, coordinates and layer manager. Modular 04 remains the rollback baseline.

## Verification and remaining uncertainty

All **20/20 Node regression tests** and JavaScript syntax checks pass; all original R14 packed tile lengths and terrain mesh buffer sizes have been audited; ZIP integrity passes. A Playwright `set_content` test loaded the **actual portable HTML** in the browser's **2D fallback**, inspected active native counts and the expanded search, with no JavaScript page errors. However, **WebGL2 is unavailable in this test environment**: no honest claim of GPU-rendered 3D visual certification can be made. The user must inspect close native building faces, street clearance, Hot Zone, terrain-water boundaries, geometry colour/lighting and camera near-plane on GPU hardware before acceptance.

Private full source assets and runnable files are saved to the user's Spaciel Library under `/Spaciel/working-data/Spaciel_Modular_05_Private.zip` and `Spaciel_Modular_05_Portable.html`. Commercial map/SketchUp-derived mesh data should not be published in this public repository without appropriate redistribution rights.
