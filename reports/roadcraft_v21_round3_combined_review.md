# Spaciel — Round Three Buildings + Roadcraft V21 Combined Inspection

Date: 10 November 2026. Status: **non-destructive review build**, not an approved road or building update.

## Preserved city geometry

- 7,847 previously placed native-source footprint outlines with reported source heights.
- One retained large Hot Zone footprint (`original-4125`), in its previously protected location. Because its exact SKP model is not authenticated, the viewer uses a **temporary illustrative 75 m vertical mass** for visual inspection only.
- No changes to placement coordinates, footprint polygons, source identifiers, district styles or road routing data.

## Road source and relationship to the atlas

- Latest road geometry: `experiment/roadcraft-v21-cartographic-grammar/experiments/roadcraft_v21_cartographic_grammar_viewer.html` in `BardOfCarnac/Spaciel` GitHub, data schema `spaciel-roadcraft-v21-stroke-width-review`.
- V21 contains 2,321 nonempty road chains (2,521 entries including empty ones), with 173 identified major corridors. The latest road data is held on an **experimental branch**, not certified against the official atlas.
- V21 coordinates are in the 792×1224 atlas-source-pixel frame; projected to the working 5175×7966 atlas pixel frame by independent x/y scale factors. This is a cartographic, not surveyed, registration.
- The combined HTML **loads V21 dynamically from the public Spaciel GitHub branch** while online. It has an embedded, fully offline V17 road fallback, and clearly indicates which one is currently visible. A reliable on-device live-network V21 fetch has not been independently verified in this environment.
- Primary roads are shown as approximate 15 m wide surfaces; local roads as approximately 9 m. These widths are a visual assumption, not official measured road edges.

## Road/building screening

A non-destructive independent check using the **actual V21 geometry fetched through the connected GitHub repository** flagged **607 of 7,848** footprint objects as potentially intersecting the estimated road ribbon plus a 1-atlas-pixel tolerance. `original-4125` is not flagged.

Using the same clearance assumptions with the earlier V17 centre-lines gave **zero flagged footprints**. That comparison is meaningful, but V21's route changes and incomplete atlas verification must be considered before interpreting any candidate as a definitive building-placement error. The map's 'Highlight possible road conflicts' toggle computes and marks tentative issues when road data loads.

Do not automatically relocate all 607: first inspect arterial continuity, whether any local road refit misread the source strokes, and the nearby protected/landmark buildings. Roads and existing footprints remain untouched in this review.

## Rendering scope

The viewer uses WebGL2 when supported and a working Canvas2D pseudo-3D fallback otherwise, with pan, zoom, orbit/tilt, top-down, Hot Zone shortcut, individual building inspection, and layer controls. The rendered building volumes are **extruded original-scale footprint polygons using retained height metadata**, *not* the complete original SketchUp meshes/faces. The next fully architectural 3D pass will need to map source model mesh IDs into these placements.

The atlas underlay was visually cleaned of its earlier road paint so that the V21 road layer can be distinguished from V17 imagery. The real terrain height mesh is **not** imported into this review build; ground is flat with the atlas as a coastline/reference texture.

## Files and distribution

- Private review website: `Spaciel_Round3_Buildings_Roadcraft_V21_3D_Review.html`
- Main screenshot: `Spaciel_Combined_Desktop_Preview.png`
- Supporting generator: `build_combined_v21.py` (uses private source placement GeoJSON locally)

Because the page embeds exact building footprint geometry derived from the source model, keep it in the private Spaciel Library rather than publishing to the public GitHub repository before source redistribution rights are verified. No public site has been deployed.