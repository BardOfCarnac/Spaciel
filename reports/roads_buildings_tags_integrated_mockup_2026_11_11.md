# Spaciel — Roads + Buildings + Tags Integrated Mockup

Date: 11 November 2026. Status: **private review build**. Public repository record only.

## Baseline
- Combined Round Five geometry with V19 location/category data into a new review viewer; no original V19 or Round Five viewer was overwritten.
- **7,993** existing building placement objects preserved, including the protected Hot Zone landmark.
- **1,304** source-identified SketchUp mesh placements retained for WebGL2 rendering, with Canvas2D footprint fallback.
- Latest Roadcraft **V21** is requested from the experimental branch when online. Embedded **V17** lines (2,422 chains) are the local fallback. Road widths and road/building conflicts remain provisional.
- **556** named location pins, all with a display tag, distributed among **7** category colours; **138** linked Vend-r outlets are available within corresponding location bubbles.
- Search index: **527** street names, **24** official districts and **11** locality records, plus location names, district names, display tags, and linked outlet names.

## Registration
Existing viewers use different cartographic frames:
- V19 POI register: 3300 × 5100, scaled into the 5175 × 7966 Round Five atlas.
- V19 district/neighbourhood search labels: 792 × 1224, scaled to the same 5175 × 7966 atlas.
- V17 street-search index: already in 5175 × 7966 and not rescaled.
- Round Five buildings, roads and terrain: 5175 × 7966 working atlas.

## Test results
- Interactive review assembled in both one-file HTML and modular local source package.
- Desktop and mobile **Canvas fallback** smoke tests passed (7,993 building objects, 2,422 V17 road chains, 556 location records, name/tag bubble, search result and focus), no JavaScript errors.
- A WebGL2 context was unavailable in the test browser. The architectural WebGL2 route still requires real-device testing.
- V21 live-road retrieval is not established by offline tests; the working fallback is V17.
- Remaining review list: 11 uncertain shoreline placements and earlier road-placement conflicts. Do not treat the combined viewer as final or as a correction of those issues.

## Private assets and publication
The private combined HTML and multi-file package are saved in the **Spaciel/working-data** Library folder, with filenames:
- `Spaciel_Roads_Buildings_Tags_Integrated_Mockup.html`
- `Spaciel_Roads_Buildings_Tags_Modular_Private.zip`
- `Spaciel_Roads_Buildings_Tags_Integration_Notes.md`

The full viewer contains unredistributed original-source buildings and height/grid material. **Do not commit it to this public repository** until source rights are checked. This report deliberately contains no private footprints, SKP source meshes or embedded viewer payload.

## Next
Extract the reusable engine and pins UI to public source code without licensed data; verify WebGL, V21, POI registration and 11 shoreline exceptions before treating the viewer as a release candidate.
