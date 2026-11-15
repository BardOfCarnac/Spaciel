# Spaciel Roadcraft V33 — usable road layer (15 November 2026)

## Decision

The user accepted the **V33 conservative arterial refinements** as an improvement over V31 and wants to proceed with usability. V32 was rejected. This package makes V33 the **selected road geometry for new Spaciel builds**. It does **not** silently alter historical standalone HTML viewers, and it does not claim a full production deployment.

## Runtime contract

- Atlas-coordinate frame **5175 × 7966**, top-left origin, pixel distances only.
- 1,390 graph nodes, 1,962 paths, **one connected component**, 208 degree-one nodes.
- 11 user-approved V30 connections retained, 27 reviewed rejections and one uncertain endpoint retained as review records.
- 1,469 local, 169 medium, 324 arterial graph paths. Classes/widths are still provisional and should not be silently reclassified.
- 7,509 paired-edge sample records: 2,288 observed and **5,221 modelled**. Do not present estimated edges as verified.
- Crossings and side-by-side road paint do **not** create graph connections unless a shared graph node already exists.

## Files

- `data/roads/roadcraft_v33_usable.json` — streamlined offline/runtime road graph and edge evidence (use for loading and routing).
- `data/roads/roadcraft_v33_full_edge_evidence.json` — lossless original V33 review graph with full sampling and audit metadata.
- `data/roads/manifest.json` — `roadcraft-v33` as the new-build default; V23 still listed as historical reference.
- `viewer/src/road-network.js` — `loadSpacielRoads()` returns `{version, frame, roads, graph, router}`.
- `viewer/src/road-routing.mjs` — snap to a polyline, route via the actual graph (Dijkstra), and validate topology.
- `private_demo/Spaciel_Roadcraft_V33_Usable_Explorer.html` — **offline** exploration / two-tap routing demo with embedded clean atlas reference.
- `tests/roadcraft-v33-default.test.mjs` — deterministic graph, loader, snap and routing tests.

## Integration in a modular viewer

```js
import {loadSpacielRoads} from './viewer/src/road-network.js';
const layer = await loadSpacielRoads();

for (const road of layer.roads) {
  drawPolyline(road.points, {widthAtlasPx: road.widthPx, className: road.roadClass});
}
// For two picked atlas coordinates (x,y), choose nearest existing road:
const start = layer.router.snap([xStart, yStart]);
const end = layer.router.snap([xEnd, yEnd]);
const result = layer.router.route(start, end);
if(result) drawHighlightedRoute(result.points);
```

Road selection/route coordinates are in *atlas pixels*. This module neither computes metres/travel times nor assumes road direction, traffic laws, or separate carriageways. All edges in the graph are currently navigable in both directions because no one-way metadata is established. Do not mistake this for turn-by-turn road navigation.

## Known limitations

1. **V33 edges are not uniformly verified.** Measured and estimated sample sections are kept separate. A nominal `widthPx` does not imply surveyed boundary accuracy.
2. Route intersections are topological: if two drawn roads cross but do not share a node, the router does not invent a connection.
3. Street names are not attached to this graph; the existing geographic street search layer needs an explicit names-to-road-geometry reconciliation.
4. Old private V19/V21/WebGL viewers will continue to use embedded prior road arrays until rebuilt using this loader. This package is a drop-in data contract and **working demo**, not a completed original viewer rebuild.
5. No atlas image should be included in the public repository without confirming redistribution rights. The offline HTML demo embeds an earlier cleaned atlas as a private review reference; **keep that HTML private**, outside the public GitHub tree.

## QA / regression policy

```bash
node --test tests/roadcraft-v33-default.test.mjs
```

Preserve the V23 file untouched. Do not use V32 geometry as fallback. The user-approved V30 graph connection decisions may only change upon explicit subsequent review. For a future build, compare both left and right edge evidence before moving centreline geometry.
