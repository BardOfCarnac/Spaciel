# Spaciel Realisation 12 — staged original-building restoration and local repack

11 November 2026 · **Private, reversible review build, not an approved map update**.

## Change from Realisation 11
The Realisation 11 28 original-instance urban restoration candidates were evaluated against the current 7,993-building geometry, with source location as a **rough starting point only**. Near-original footprint sites were searched with unscaled original source geometry and conservative road/coastline/other-building exclusions. Existing smaller buildings were eligible for a local rigid-translation repack. Candidates that could not fully repack their neighbours were held instead of forcibly inserted.

- **2** previously unplaced original-source SketchUp building definitions reinstated in a **staged alternate** viewer, at original-instance locations adjusted by small translations.
- **5** smaller existing source-architecture placements rigidly repositioned to clear the new sites; **none deleted, scaled or replaced**. Their original IDs and native source meshes are retained.
- Provisional alternate layout: **7,995** building objects (the original 7,993 are all retained), with **7,983** registered direct-face original-source mesh instances (previously 7,981). The 11 shoreline-held masses and the protected Hot Zone landmark remain unchanged.
- Restored original-source heights: **36 m** and **105 m**. The two new direct-face templates contribute **172** source triangles.
- The previous **60** architecture spatial tiles are retained and updated; the moved smaller buildings' mesh transforms, tile membership, and footprint positions are changed together.
- **26** urban original-instance candidates are explicitly held for visual review; the wider 633-model recovered-large-architecture catalogue remains available as before.
- **556** tagged places, roads, search and terrain remain unchanged in this experiment.

## Quantitative checks
- Reconstructed new source-face 3D mesh XY silhouettes match their original registered 2D source footprints at better than 99.98% intersection-over-union in the staged positions.
- All seven affected building footprints pass local post-change checks for overlapping other building footprints (1px proximity), V17 road centreline proximity (5.5 atlas px), and conservative water/atlas road-colour masks. **These are not certified kerb boundaries or a complete official coast survey**.
- Desktop/mobile portable-HTML browser fallback tests passed: 556 locations, 2 new staged major restorations, 5 moved smalls, camera focus and review-outline switch; no JavaScript errors.
- A served modular browser navigation test was blocked by this environment's administrator network policy. Actual GPU/WebGL2 original-architecture rendering and performance remain **unverified**.

## Review and rights
The preexisting **7,993-building layout remains available unchanged as Realisation 11**. This Realisation 12 version is a separate **staged/reversible** proposal, not the final city. Additional source-geometry nested component extraction, official atlas road alignment, the 11 shoreline exceptions, and visual frontage checks remain open. Do not automatically accept the other 26 anchors.

Private deliverables saved in ChatGPT Library `/Spaciel/working-data/`:
- `Spaciel_Realisation_12_Large_SKP_Repacked_Viewer.html` (standalone portable viewer)
- `Spaciel_Realisation_12_Private_Modular_and_Repack.zip` (modular project, private source assets and complete decisions)
- `Spaciel_Realisation_12_Before_After.png` (city atlas visual comparison)
- `Spaciel_R12_Repack_Proposals.json` / `Spaciel_R12_Staged_Large_Repacked_Placements_PRIVATE.geojson` / audits

This public record contains aggregate findings only. **Do not publish the private full viewer, meshes, polygon coordinates, source assets or original SketchUp file** until redistribution rights are checked.
