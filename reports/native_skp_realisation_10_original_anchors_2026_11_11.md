# Spaciel Realisation 10 — original SKP placements as approximate anchors

Date: 11 November 2026. Status: **private review workbench**; no new city geometry approved.

## Decision

The approximate original SketchUp instance positions should guide restoration of the previously omitted large buildings, **not dictate exact approved placements**. Preserve each building's actual size and source-instance orientation, then translate/rotate judiciously to a plausible site that respects coastline, road widths and neighbouring structures. Do not reshape source models to fill a site.

## Working review UI

Realisation 10 extends the previous private large-model review with:
- A **Preview original SKP site** control that centres on the approximate registered source position.
- A **Next instance** control for models with multiple original placements.
- An original-instance outline preview that retains the **original SKP instance's orientation and dimensions** at its recorded anchor, with any subsequent rotation measured relative to that original.
- Draft export preserving model ID, original instance ID, approximate original atlas anchor, chosen draft position and additional rotation.

The workbench retains the 100 recovered large source models, 7,993 unchanged current building objects, 556 tagged places, V17 road fallback, and provisional V21 experiment. No large buildings were installed automatically.

## Important cautions

Original SKP-to-atlas registration is road-derived and approximate; several recorded positions are offshore or intersect painted streets or present-day footprints. A preliminary fully automatic 'nearest free spot' search was deliberately **not promoted**: the available older 560-block mask covers only part of the relevant urban area and the existing water and road colour masks do not certify a land parcel. A numerical zero-overlap score is not an authorised placement. Manual inspection and explicit clearance of roads, water, existing buildings and neighbourhood role remain required. Also check whether same-origin instance records represent stacked parts of one architectural structure.

## Private files

Saved in private ChatGPT Library `/Spaciel/working-data/`:
- `Spaciel_Realisation_10_Original_Anchors_Viewer.html`
- `Spaciel_Realisation_10_Private_Review.zip`
- `Spaciel_Realisation_10_Desktop_Preview.png`
- `Spaciel_Realisation_10_README.md`

Desktop/mobile self-contained viewer tests passed: 100 source models available, original anchor recentering, rotation interaction, and unchanged 556 locations, 7,981 registered meshes and 2,422 fallback road chains; zero JavaScript page errors. The separate modular browser test was restricted by this environment's local network policy; real-hardware WebGL remains to be checked.

**The private source-derived building geometry, source registered site polygons, GLBs, private viewer and archives remain unpublished** until redistribution rights are established.
