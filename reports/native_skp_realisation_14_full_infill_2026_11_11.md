# Spaciel Realisation 14 — citywide original-source infill

**Date:** 11 November 2026. **Status:** comprehensive **private**, reversible city-massing and source-architecture **review build**, not an approved final parcel/road survey.

## Result

Starting with the staged Realisation 13 skyline, the full infill pass preserved **all 7,367 existing building placements**, including the **399** newly reinstated large original-source models, the protective Hot Zone landmark and the intentionally sparse/ruined blocks. A new character-aware pass added or reinstalled **1,454** unscaled original-source building instances, bringing the working city to **8,821 building objects**. **8,810** have direct-face source mesh instances in **60** compressed spatial architecture tiles; the remaining **11** display provisional masses.

The 1,454 additions comprise **202 recovered identities** from the smaller-building infill reserve and **1,252 newly placed source-model uses**, including smaller source definitions recovered from the original user-supplied SketchUp archive. **824** previously reserved small-building placements were not forced back into sites where they could not fit and remain available in earlier private snapshots. No large skyline structure was moved or removed, and no source shape was stretched or rescaled.

## Geographic and stylistic constraints

The infill uses the previously approved buildable-footprint and road-separated character regions, not historical footprints as rigid one-building-per-slot parcels. The placement screens exclude the working coastline/water mask, preserved Hot Zone void, and V17 plus painted-atlas road bands. Dense streets can receive compact source architecture; lower-density Executive Zone, residential compounds, amusement/resort, docks, port, university, and military sites retain distinct breathing room rather than being filled uniformly.

**27 actual new source-model placements** were also identified for focused inspection as contextual exceptions: **10** waterfront-edge examples, **10** near V17 chain endpoints and **7** scattered peripheral instances. These are geographically screened examples, not an assertion that every chain endpoint is an official cul-de-sac or every waterfront site is an approved quay. Shipping-container infill has **not** been scattered city-wide; any container-focused development is to remain in designated coastal cargo sites.

## Source fidelity and validation

- All **1,454** new placements use direct-face geometry from the recovered original SketchUp catalogue. Their fallback 2D outlines were synchronized with the actual projected 3D mesh convex hull after placement, maintaining source shape, size and rigid transforms.
- Independent native-mesh clearance checks found **zero new collisions** against the 7,367 earlier building masses, other new direct-face mesh hulls, the reviewed water raster and atlas-painted road mask. No new mesh hull came within 2.5 atlas pixels of screened V17 road centrelines.
- Source-rendering assets and two-dimensional polygon registration use the same **5175×7966 atlas** frame; the 60 compressed architecture tiles, source template catalogue, provenance and per-placement records are bundled privately.
- Desktop and mobile **Canvas fallback** browser checks passed without JavaScript page errors: 8,821 building objects, all **556** tagged locations, unified search, infill overlay and working unusual-site navigation.
- **Limitations:** the automated road/water masks are approximate and cannot certify real kerb or parcel boundaries, V21 registration or all shoreline details. Full nested SketchUp architecture/materials and actual hardware **WebGL2** rendering are not validated. An attempt to browse the separate modular app over a locally intercepted hostname was blocked by the test environment's network policy, so no hosted/browser modular deployment is claimed.

## Private artifacts

In the user's private ChatGPT Library `/Spaciel/working-data/`:

- `Spaciel_Realisation_14_Full_City_Infill_Viewer.html` — standalone combined viewer (roads + terrain + buildings + 556 tagged locations and search)
- `Spaciel_Realisation_14_Complete_Private_Project.zip` — modular project, source-architecture tiles, full geometry, audit, before/after image, review scripts and README
- `Spaciel_R14_Full_Buildings_PRIVATE.geojson` and `Spaciel_R14_Infill_Only_PRIVATE.geojson` — registered polygon geometry with source provenance
- `Spaciel_R14_Integration_QA.json`, `Spaciel_R14_Native_Mesh_Clearance_QA_PRIVATE.json`, `Spaciel_R14_Special_Sites_PRIVATE.json`
- `Spaciel_Realisation_14_City_Comparison.png` and `Spaciel_Realisation_14_Unusual_Sites_Overview.png`

The prior Realisation 13 remains a reversible baseline. **None of the private SKP-derived meshes, polygon outlines, full viewer, source locations or tiles is published in this public repository** while source redistribution rights remain unclear.

## Future integration

Integrate the modular full-infill layer with the primary V19 optical viewer's approved category icon morph, bubbles, bottom colour bar, region/district ghost labels, unified map search and ocean shader. Validate WebGL2 and experimental V21 road geometry against the official atlas before replacing the current working snapshot.
