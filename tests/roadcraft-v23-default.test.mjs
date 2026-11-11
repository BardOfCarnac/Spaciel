import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

test('V23 is the checked-in working road baseline, with valid connected topology', async () => {
  const root = new URL('../data/roads/', import.meta.url);
  const manifest = JSON.parse(await readFile(new URL('manifest.json', root), 'utf8'));
  assert.equal(manifest.current.version, 'roadcraft-v23');
  const graph = JSON.parse(await readFile(new URL(manifest.current.file, root), 'utf8'));
  assert.equal(graph.schema, manifest.current.graph_schema);
  assert.deepEqual(graph.frame, [5175, 7966]);
  assert.equal(graph.width_px, 22);
  const nodes = graph.nodes, paths = graph.paths;
  assert.equal(Object.keys(nodes).length, manifest.checks.nodes);
  assert.equal(paths.length, manifest.checks.paths);
  const adj = new Map(Object.keys(nodes).map(k => [String(k), []]));
  for (const path of paths) {
    const a = String(path.from), b = String(path.to), coords = path.coords;
    assert.ok(adj.has(a) && adj.has(b), 'road endpoints exist');
    assert.ok(Array.isArray(coords) && coords.length >= 2);
    for (const p of coords) assert.ok(p.length === 2 && p.every(Number.isFinite));
    assert.ok(Math.hypot(coords[0][0]-nodes[a][0],coords[0][1]-nodes[a][1]) < .11);
    const e=coords.at(-1);
    assert.ok(Math.hypot(e[0]-nodes[b][0],e[1]-nodes[b][1]) < .11);
    adj.get(a).push(b);adj.get(b).push(a);
  }
  const seen = new Set();
  let components=0;
  for(const start of adj.keys()) {
    if(seen.has(start)) continue;
    components++;
    const stack=[start];seen.add(start);
    while(stack.length) for(const v of adj.get(stack.pop())) if(!seen.has(v)){
      seen.add(v);stack.push(v);
    }
  }
  assert.equal(components, 1);
  assert.equal(paths.length - adj.size + components, manifest.checks.cycle_rank);
});
