# Spaciel Modular 01 — source viewer preservation and core bridge

**11 November 2026 — foundational implementation.**

## Real viewer chosen
Private source is `Spaciel_V19_Roads_Water_01.html` (SHA-256 `ba3a12c318110c8910a35e70606871611cda38ab81ef83d6b8a71072a8b78820`). This is the **actual V19 application**, not the separate Realisation architectural workbench or search-control mock-up.

The private build retains 661 live pins (556 main + 105 direct Vend-R outlets), seven-colour filters and bubble morphs, district ghost labels, 7,981 native-source-face building placements, 2,422 V17 road chains, and registered V3.4 optical water.

## What the modular build actually does
- Extracts original ten ordered JavaScript slots and nine CSS cascade slots into individual files, preserving execution and display semantics. The 28 MB original renderer remains a single **legacy renderer** file for now; this is not yet a full refactor of internal rendering passes.
- Introduces source-independent `events`, `coordinates`, `camera`, `layers`, and `core` modules, loaded before the existing V19 renderer.
- Uses the **original** V19 3304×5100 bitmap / 900×1390 district prototype registration for reversible world transforms. Named V17 road-surface, V21 experimental road-surface and provisional search-road frames are separate on purpose: none is GPS.
- Observes the existing V19 renderer camera and gives other components one adapter for target X/Y/Z, distance, bearing and pitch. No parallel/competing GPU camera.
- Registers seven existing display layers: terrain, water, roads, architecture, ghost labels, locations and interface. Water, roads, buildings and pins delegate visibility to existing controls; terrain, ghost labels and UI are read-only. Layer `order` is composition metadata, **not** a change to the established GL drawing order.

## Source/storage boundary
The runnable modular package and portable viewer are private artifacts, **not committed to this public repository**: they contain book/map and SketchUp-derived commercial assets. The public repository retains architectural contracts, documentation, and source-independent geometry / UI work. Do not publish the 34 MB viewer or private architecture tiles without verifying redistribution rights.

## QA performed
- Syntax checks for 10 legacy + 5 new JS files: pass.
- Four Node tests: reversible coordinate transform, named frame handling, camera observer/command adapter, real layer delegation/read-only guards: 4/4 pass.
- Chromium with WebGL disabled opened the **actual portable viewer**, with the original Night City map, spectrum bar, 661 pins and no page errors.
- The extracted-folder URL could not be browsed in this environment because of browser administrator restrictions. A complete real-hardware WebGL2 certification remains pending; original source road, water and building drawing code was preserved rather than rewritten.


## User validation and terrain caveat — 11 November 2026

The user has now opened the modular viewer and confirmed **the combined systems are cooperating**. This is acceptance of the **integration foundation**, **not** acceptance of the current terrain's resolution or fidelity. The displayed terrain is **not the approved full-resolution terrain**. Do not mark high-resolution terrain integration as complete, or treat the current sampled/base terrain as an approved replacement.

**Next terrain milestone:** locate the approved full-resolution terrain asset and its original atlas registration; integrate through a replaceable terrain adapter without changing the functioning water, road, building, location, UI, or shared camera modules. Verify coast and crater profiles, height alignment, seams, zoom detail, and performance on real WebGL2 hardware. Preserve this build as a fallback baseline before any terrain change.

The private working package and portable HTML have been saved in the user's Spaciel Library under `/Spaciel/working-data/`.

## Deliberately staged for the next integration pass
1. Inspect modular V19 on a GPU-enabled device; verify road/water/native-architecture toggles and camera commands in the actual GL session.
2. Integrate the newly approved **left-anchored, rightward expanding** magnifier field, using the existing module and preserving the exact search icon/alignment.
3. Bring the approved unified search dataset (24 districts, 11 neighbourhoods, 527 named streets and linked venues) into this real viewer, not just a search-only demo.
4. Review Realisation 12's two restored larger SKP sources and provisional moved buildings before adding them to the main viewer.
5. Migrate renderer subsystems into dedicated modules one at a time, with private assets kept off public GitHub.

**Design rule:** preserve every approved 2045 Spaciel behaviour unless its own change has been explicitly reviewed and accepted.