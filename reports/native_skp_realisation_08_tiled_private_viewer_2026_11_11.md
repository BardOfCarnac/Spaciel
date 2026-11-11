# Spaciel — Realisation 08: private tiled native architecture viewer

11 November 2026 · Status: **private working mockup**, not a final release.

## Architecture
- 7,993 preserved source-derived building footprint positions, including a protected provisional Hot Zone landmark.
- 7,981 source-registered SketchUp **direct-face** building placements in the private architecture tile library (1,717 previously screened and 6,264 newer registrations).
- 11 shoreline-held building masses and one protected landmark continue to use provisional massing.
- 3,079 source definition IDs packaged as shared direct-face mesh templates; every registered instance appears exactly once in the **60** spatial tiles.
- Source geometry is **not** necessarily full nested SketchUp components, complete materials, accessories or textures; it is a reconstruction of direct definition faces.

## Realisation 08 changes
- New modular viewer fetches only the compressed geometry tiles near the camera, reusing the registered 5175×7966 atlas frame.
- **Up to 16 GPU architecture tiles** are retained at a time. As the camera moves, old tile GPU buffers are discarded and nearby tiles replace them; zoomed-out views display lighter original-footprint masses.
- Portable one-file viewer embeds the same private tile data and lazily assembles GPU geometry when zoomed in.
- Existing location pins and search are retained: 556 tagged locations, location bubbles, streets and district search.
- Roads remain V17 (offline) with experimental online V21; terrain/placement registration not reworked in this pass.
- Original Realisation 07 and V19 remain untouched.

## QA
- Source archive manifest has **60** valid tiles, **7,981** unique placement indices and **3,079** native templates.
- Desktop/mobile Canvas2D browser smoke tests passed: location search, tags, 2,422 V17 road chains and UI startup without JavaScript errors.
- Independent simulated WebGL2 constructor executed the tiled geometry upload path with no JS errors. At the initial focus, **16 / 16** selected tiles were prepared; after a camera move, old buffers were released and 16 new nearby tiles remained.
- **A real GPU/WebGL2 device test has not yet been performed.** These tests verify program flow and geometry handling, not successful GPU drawing, performance, appearance, or source-face material fidelity.

## Outstanding work
1. Test on actual desktop/mobile hardware using WebGL2 and inspect source geometry visually.
2. Reconcile the 11 shoreline holds and the previously flagged candidate road collisions (do not automatically move/delete buildings).
3. Restore the approved V19 bubble-morph animation, optical water, geographic ghost labels and complete UI in the final viewer.
4. Verify and integrate any useful nested SketchUp components (rather than inventing details).
5. Check redistribution rights before publishing source-derived viewer data.

## Storage and copyright
Saved privately under ChatGPT Library path `/Spaciel/working-data/`:
- `Spaciel_Realisation_08_Portable_Native_Tiles.html`
- `Spaciel_Realisation_08_Private_Tiled_Viewer.zip`
- `Spaciel_Realisation_08_README.md`

**Do not commit the private HTML, original SKP, compressed model templates, spatial tile files, placements or GLBs to this public repository.** Only generic, source-independent viewer code and aggregate QA are appropriate here.
