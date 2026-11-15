# V33 Road-edge / kerb zoom-detail proposal — 15 November 2026

Roadcraft V33 is the adopted working road geometry. The close-up rendering is a reversible **presentation treatment** layered over V33, not new roads and not measured pavements.

## Visual progression

- **Distant:** the perimeter of a V33 road ribbon reads as a thin, slightly illuminated outline.
- **Approaching a junction:** as the rendered road reaches roughly 9–27 screen pixels across, the perimeter gradually resolves into a kerb lip and a narrow pavement-coloured band outside the roadway.
- **Close street exploration:** a muted edge highlight/shadow distinguishes the kerb from the road and pavement. No new road junctions or navigation nodes are generated.

The same continuous centreline and individual width from V33 determine every stage. Use `roadDetailAtZoom(path, pixelsPerAtlasPixel)` from `viewer/src/road-kerb-lod.mjs` and `drawRoadsAtZoom(ctx, visibleRoads, pixelsPerAtlasPixel)` for the 2D reference renderer. A future curved-bowl/WebGL renderer can use the same measurements and fade law but will need native geometry/materials.

Street-level widths of sidewalks are **illustrative**, not present in the original source atlas; the road layer retains `edgeSamples` with explicit observed (`o`) versus modelled (`m`) evidence. No assumption that the constructed pavement is a measured object should enter routing, collision, or building-placement systems.

Draw adjoining roads in shared passes (pavement, kerb lip, road fill), so intersection joins form one surface. Keep curbs across true junction mouths absent once the roadway fills; finer intersection cut-outs should come from a junction-aware mesh once other app layers are integrated.

## Boundaries

Keep V23 as historical reference and preserve V33's current topology (1,390 nodes, 1,962 paths, 208 degree-one nodes, 11 approved joins). No change to buildings, terrain, water, camera design, or the published private V19 HTML is implied by this prototype.
