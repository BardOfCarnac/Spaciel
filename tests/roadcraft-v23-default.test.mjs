import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

test('V23 is preserved as the unchanged legacy road graph while V33 is current',async()=>{
  const root=new URL('../data/roads/',import.meta.url);
  const manifest=JSON.parse(await readFile(new URL('manifest.json',root),'utf8'));
  assert.equal(manifest.current.version,'roadcraft-v33');
  assert.equal(manifest.legacy.v23,'roadcraft_v23_default_width22.json');
  const graph=JSON.parse(await readFile(new URL(manifest.legacy.v23,root),'utf8'));
  assert.equal(graph.schema,'spaciel-roadcraft-v23-parallel-corridor-review');
  assert.deepEqual(graph.frame,[5175,7966]);
  assert.equal(graph.width_px,22);
  assert.equal(Object.keys(graph.nodes).length,1436);
  assert.equal(graph.paths.length,1992);
});
