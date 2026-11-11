/** Load the user-selected default Spaciel roads from the checked-in manifest.
 * Data and coordinates are already in the registered 5175×7966 atlas-pixel frame.
 * Use this in future modular viewers in place of hardcoded V17/V21 URLs.
 */
export const SPACIEL_ROADS_MANIFEST_URL =
  new URL('../../data/roads/manifest.json', import.meta.url);

async function loadJson(url, fetchImpl) {
  const response = await fetchImpl(url);
  if (!response.ok) throw new Error('Spaciel road load failed: ' + response.status + ' (' + url + ')');
  return response.json();
}

export function validateSpacielRoadGraph(graph, expected = {}) {
  if (graph?.schema !== 'spaciel-roadcraft-v23-parallel-corridor-review' ||
      !Array.isArray(graph.frame) || graph.frame[0] !== 5175 ||
      graph.frame[1] !== 7966 || !Array.isArray(graph.paths) ||
      !graph.nodes || typeof graph.nodes !== 'object') {
    throw new Error('Unexpected Spaciel road graph format / atlas frame');
  }
  if (expected.nodes && Object.keys(graph.nodes).length !== expected.nodes) {
    throw new Error('Spaciel road node count differs from manifest');
  }
  if (expected.paths && graph.paths.length !== expected.paths) {
    throw new Error('Spaciel road path count differs from manifest');
  }
  for (const path of graph.paths) {
    const a = graph.nodes[String(path.from)], b = graph.nodes[String(path.to)];
    if (!a || !b || !Array.isArray(path.coords) || path.coords.length < 2) {
      throw new Error('Road path missing its registered endpoint');
    }
    if (path.coords.some(p => p.length !== 2 || !p.every(Number.isFinite))) {
      throw new Error('Road path contains invalid coordinates');
    }
    for (const [p,q] of [[path.coords[0],a],[path.coords.at(-1),b]]) {
      if (Math.hypot(p[0]-q[0],p[1]-q[1]) > 0.11) {
        throw new Error('Road path geometry endpoint does not match node');
      }
    }
  }
  return graph;
}

export async function loadSpacielRoads({
  manifestUrl = SPACIEL_ROADS_MANIFEST_URL,
  fetchImpl = fetch
} = {}) {
  const url = new URL(manifestUrl, import.meta.url);
  const manifest = await loadJson(url, fetchImpl);
  if (manifest.schema !== 'spaciel.roads.manifest.v1' ||
      manifest.current?.version !== 'roadcraft-v23') {
    throw new Error('Incompatible Spaciel road manifest');
  }
  const dataUrl = new URL(manifest.current.file, url);
  const graph = validateSpacielRoadGraph(
    await loadJson(dataUrl, fetchImpl), manifest.checks
  );
  return {
    version: manifest.current.version,
    frame: graph.frame,
    widthPx: graph.width_px,
    graph,
    // Directly usable by a flat-road renderer; do not infer route links from stroke overlaps.
    roads: graph.paths.map(p => ({
      from: p.from, to: p.to, points: p.coords, major: Boolean(p.major)
    }))
  };
}
