# Spaciel mainline viewer baseline — V19 (11 November 2026)

**Decision: the normal Spaciel application shell is the frozen approved V19 viewer, not the Realisation 09/10 building workbench or the Roadcraft V21 experiment.**

- Authoritative frozen private HTML: `/Spaciel/approved-baselines/Spaciel_Approved_Category_Morph_2026-11-11.html`
- SHA-256: `6cb84d3379e50ca17c4c518d44e2716622c3e61bf86fe39a21159ff5dcfc5d9f`
- Private rebase package: `/Spaciel/working-data/Spaciel_Mainline_01_Package.zip` (the HTML is byte-for-byte unchanged; the optional architecture and approved label files are **separate**, not yet integrated).
- WebGL2 automatic test was unavailable; V19 Canvas fallback opened, showed seven category buttons and handled search for Anjelika's with no JS page error.

## Required visual and interaction contract

Preserve V19 camera navigation, 661 pins (556 mapped places plus 105 individual Vend-R outlet pins), approved custom icons, bubble styling, 720 ms overlapping category transitions, spectrum bar, geographic search, street/district labels and search navigation. Do not replace the viewer with an R09/R10 inspection UI.

## Integration direction

1. Keep V19 source unchanged as the comparison reference. Every integration change goes to a new derived build, not the frozen source.
2. Add one shared atlas registration service with verified control points. Keep V17 offline linework until Roadcraft V21 is approved; expose V21 only as an optional reference layer while experimental.
3. Bring later building placement/mesh rendering from the *private* Realisation 10/09 tiled assets into the V19 WebGL renderer. Preserve source identity, 7,993 provisional placements, 11 coastline holds, protected Hot Zone landmark and 100 unplaced large SKP candidates. Do not blindly overlay a second full application.
4. Import the separately approved 24-district ghost label placement JSON by an audited mapping to the V19 geographical world. Avoid using the R09 workbench's rough district centroids as the new authority.
5. Integrate optical-water material only with the corrected authoritative shoreline and a world-space distance field. Avoid recreating the seam, dark patch or pixelated island edge.
6. Preserve V19's native full-app UI across desktop and mobile; test with real WebGL2 hardware as well as Canvas fallback.

## Distribution warning

V19 and native building assets contain licensed commercial/source-derived material. Keep complete viewer builds in private Library; this public repository contains documentation and source-independent code only. The rebase does **not** claim newer R09/R10 building geometry or V21 roads are already merged into V19.

## Why the change

The first two Integrated Review builds used Realisation 09 as the shell and consequently looked like an architecture inspection workbench, not the everyday Spaciel viewer the user expected. This entry prevents repeating that architectural mistake.
