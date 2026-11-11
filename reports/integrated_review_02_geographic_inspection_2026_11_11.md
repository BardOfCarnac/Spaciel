# Spaciel Integrated Review 02 — geographic inspection

Date: 11 November 2026  
Status: **private, non-destructive review build; not a certified geometry correction or public app**.

## Preserved source

This review extends the existing **Integrated Review 01** and retains the private Realisation 09 building layout, tiled architectural model data, V17 road fallback, V19 Contour glyph artwork, approved overlapping filter animations, 556 tagged places, linked venue search, and existing 100-large-model placement review. All source snapshots remain unchanged.

Private saved deliverables in ChatGPT Library `/Spaciel/working-data/`:
- `Spaciel_Integrated_Review_02.html` — single-file viewer
- `Spaciel_Integrated_Review_02.zip` — HTML, notes, geometry QA
- `Spaciel_Review_02_Geometry_QA.json` — private per-site candidate details
- `Spaciel_Review_02_Notes.md` — test log and limitations

These contain source-derived geometry; **do not put them in the public GitHub repository** pending source redistribution checks.

## Review 02 changes

- V17 is the startup road default; V21 is loaded only on explicit user request. This prevents changing to an experimental alignment silently.
- The 24 **manually approved V02** district ghost-label placements replace untouched Study 02 defaults. Their offsets are projected relative to corresponding district anchor centroids; cartographic registration remains approximate.
- Fixed the extra icon/label vertical offset conversion to use the same metres-to-atlas-height factor as the source viewer.
- Added independently switchable diagnostic overlays for the atlas grid, significant under-building slope changes, 11 shoreline building holds, road/building conflict candidates, low-surface and out-of-frame location anchors, V17 reference roads, and ghost-text anchor locations.
- Added focus commands and export of the unapproved QA report without mutating map geometry.
- Kept ocean effects separate until the coastline SDF, high-resolution shore and water seam are validated.

## Initial geometry checks

Using the embedded 520×800 V17 sampled terrain grid and all 7,993 source placement footprints:

- **128** footprints span more than 5 atlas-height units between vertices (about 13.4 metres using the viewer conversion).
- **18** span more than 10 height units (about 26.9 metres).
- **11** source placements remain held for shoreline review; one large Hot Zone landmark is protected.
- Four Outskirts POIs have x beyond the 5,175-pixel atlas edge; they may be legitimate mapped outlying sites, not necessarily errors.
- 44 of the 556 main location pins sample below two atlas-height units; some are legitimate docks/waterfront sites.

These are diagnostics, **not automatic correction instructions**. No building placements, road coordinates, or POI coordinates were modified.

## Test status

Browser tests using in-memory HTML rendered desktop and mobile Canvas2D fallbacks, confirming 7,993 placements, 2,422 V17 road chains, 556 locations, 24 approved ghost labels, active category filtering and the inspection panel; no JavaScript page errors were observed. File/localhost navigation was blocked in the automated browser and testing used in-memory HTML. A WebGL2 graphics context was unavailable even with the software renderer, so native source-face appearance/performance still require actual hardware verification.

## Outstanding

True adaptive irregular triangulated terrain mesh, proper ocean SDF/glint integration, official-road registration review, high-gradient building sites, 11 coastal holds, 100 unplaced large originals, device WebGL2 test and 105 extra standalone V19 Vend-R pins are separate tasks.

See [the integration inventory](../docs/integration-inventory-2026-11-11.md) for full source paths and coordinate-contract notes.
