# V19 Native Architecture 01 — private integration review

**Date:** 11 November 2026  
**Status:** integrated private HTML created; Canvas fallback tested; actual WebGL2 rendering NOT yet verified on hardware.

## Decision

Spaciel's **approved V19 map remains the primary viewer**. The Realisation 09 source-derived architecture has been integrated as a **WebGL2 building layer in V19's own scene**; the Realisation 09 workbench and its UI were not embedded. Source-approved V19 remains unchanged and preserved privately.

## Private deliverables

Stored in ChatGPT Library `/Spaciel/working-data/`:

- `Spaciel_V19_Native_Architecture_01.html` — offline standalone V19 shell with private geometry tiles.
- `Spaciel_V19_Native_Architecture_01.zip` — HTML, README, QA manifest.
- `Spaciel_V19_Native_Architecture_01_README.md`
- `Spaciel_V19_Native_Architecture_01_QA.json`

**Do not commit these files to the public Spaciel repository.** Their embedded original-source geometric data and atlas assets have unresolved redistribution rights.

## Scope

- Retained approved V19 terrain, registered coastline, search, 661 POIs, category icons, bubble morph, spectrum bar, geographic ghost lettering and canvas fallback.
- Added **7,981** registered **original direct-SKP-definition face placements** from Realisation 09, with **3,079** reused source definitions, partitioned into **60** compressed spatial tiles. The native model layer draws source-face triangles using the **existing V19 WebGL2 GL context, VP camera and registered terrain height grid**.
- The **11 shoreline holds** and **one protected Hot Zone original mass** remain provisional mesh masses, not substituted with guessed SKP identities. Total layout: **7,993** placements. **100 recovered large original source definitions remain unplaced and are NOT installed here.**
- Added a compact architecture-source selector to V19 building controls: automatic detail / source faces / original V19 outlines. At city scale the V19 overview massing remains; close up, native geometry is loaded as camera-nearby tiles, with old V19 buildings used during tile loading or on unsupported devices.
- No automatic relocation of buildings, streets or location pins. No change to the experimental Roadcraft V21 or polychromatic ocean work.

## Registration and QA

- Verified registration of **541 uniquely identified** place locations shared by V19 and the architecture atlas. Maximum residual approximately **0.031 metres**, at the precision of serialized coordinates. Legacy blank location IDs and three duplicate `The Cells` marker IDs were excluded from this strict unique-ID check; those are not registration failures.
- All 60 source-model tiles and layout indices decoded and count-checked.
- Static JavaScript syntax checks passed.
- WebGL-path simulation successfully loaded 12 camera-near tiles into buffers and issued the expected draw calls; it is **not a real shader/GPU test**.
- Chromium desktop Canvas fallback showed the regular V19 UI, 661 pins, search and filters, without JavaScript page errors.
- **Outstanding:** real-device WebGL2 shader/face appearance, GPU performance and terrain clipping; verify before treating as a certified 3D viewer.

## Next step

Open the HTML on hardware that supports WebGL2, zoom into a dense district and inspect source-face placement and fidelity, compare with the built-in original V19 outlines mode, then assess shoreline and unplaced landmark candidates. Preserve the frozen original V19 reference.

See also [the mainline decision](../docs/mainline-viewer-baseline-v19.md) and [the integration inventory](../docs/integration-inventory-2026-11-11.md).
