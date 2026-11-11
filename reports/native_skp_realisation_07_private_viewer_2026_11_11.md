# Spaciel — Original SketchUp direct-face architecture (Realisation 07)

Date: 11 November 2026 · **private working review build**, not a public viewer or certified final city.

## Result
- Existing **7,993** building placements, roads and locations remain unchanged.
- Native **direct-face architecture** was reconstructed from the exact original user-supplied Night City SketchUp source for **3,079 source definitions**. Their original per-instance SKP transforms were combined with their saved atlas placement transforms.
- **7,981** building placements now have registered source faces for the WebGL2 review renderer (**335,192 original-source face triangles**). **11 shoreline holds** intentionally stay in massing, as does **one protected Hot Zone landmark**, whose exact source identity remains unauthenticated.
- **1,717** of the 7,981 placements were previously screened source-mesh fits; **6,264** are newly recovered registrations. A viewer toggle separates the two.
- Median native mesh hull overlap against the saved placement polygon is ~**99.96%**, while median original-to-current footprint registration residual is ~**0.003 atlas px**. Direct-source faces may occupy less than the full footprint hull at a handful of sites.
- **No building site was moved or deleted**, and no roads or geotags were replaced.

## Final-viewer preparation
- Spatial assets are partitioned into **60 atlas tiles** (512 × 512 atlas px), with a separate shared definition catalogue and checksummed tile manifest. This is a data layout for later viewport loading; the current review mockup still embeds the full architecture payload.
- Public code for a neutral tile loader is in `viewer/src/native-architecture-tiles.js`. It contains no source model geometry.
- The viewer retains the V17 offline road fallback, experimental online V21 attempt, **556 tagged locations** and unified place/street/district search.
- Desktop/mobile Canvas2D fallback smoke tests passed; a separate JavaScript construction check produced all **335,192 finite triangles** without errors. Live GPU WebGL2 rendering on a user's device is **not independently verified**.

## Fidelity and unresolved review
The extraction recovers the original source's **direct definition faces**; it is **not an assertion of complete SketchUp models with every nested component, original material or texture**. Height uses retained native building height and saved atlas terrain baselines. The older painted-road alignment shortlist (980 potential overlaps) remains provisional; V21 geometry and 11 shoreline sites still need review. The protected Hot Zone landmark is deliberately not assigned an unverified source mesh.

## Private deliverables
Saved under `/Spaciel/working-data/` in the private ChatGPT Library:
- `Spaciel_Realisation_07_Native_SKP_City.html` — self-contained interactive mockup
- `Spaciel_Realisation_07_Complete_Private_Viewer.zip` — modular viewer, architecture tile manifest/data, audit, preview
- `Spaciel_Realisation_07_Original_SKP_Model_Library.zip` — all 3,079 direct-face source-definition GLBs
- `Spaciel_Realisation_07_Source_Registration_QA.json` — per-placement numeric checks

**Copyright boundary:** no raw SketchUp file, derived source mesh, full viewer HTML, private tile catalogue or placement geometry is published to GitHub while redistribution rights are unresolved. Only this aggregate report and generic loader source are public.

## Next step
Validate WebGL2 on an actual GPU device, inspect the 11 held coast sites, reconcile confirmed road conflicts, and wire view-frustum/tile loading into the main Spaciel UI without changing the V19 pin morph and optical-water behaviours.
