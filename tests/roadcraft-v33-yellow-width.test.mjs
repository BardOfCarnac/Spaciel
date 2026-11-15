import test from 'node:test';import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {applyAtlasRoadPaintStyle} from '../viewer/src/road-paint-style.mjs';
import {createRoadRouter} from '../viewer/src/road-routing.mjs';
const root=new URL('../data/roads/',import.meta.url);
const graph=JSON.parse(await readFile(new URL('roadcraft_v33_usable.json',root),'utf8'));
const style=JSON.parse(await readFile(new URL('v33_yellow_paint_style_v1.json',root),'utf8'));
const result=applyAtlasRoadPaintStyle(graph,style);
test('confirmed yellow roads share one 20 atlas-pixel width',()=>{
  assert.equal(result.paths.filter(p=>p.isYellowRoad).length,394);
  assert.ok(result.paths.filter(p=>p.isYellowRoad).every(p=>p.width===20&&p.major));
  assert.equal(result.paths.filter(p=>p.paintStatus==='review').length,191);
});
test('routing coordinates and measured edges are untouched',()=>{
  assert.deepEqual(result.nodes,graph.nodes);
  for(let i=0;i<graph.paths.length;i++){
    const a=graph.paths[i],b=result.paths[i];
    assert.deepEqual([b.from,b.to,b.points,b.join],[a.from,a.to,a.points,a.join]);
    assert.deepEqual(b.edgeSamples.filter(s=>s.e==='o'),a.edgeSamples.filter(s=>s.e==='o'));
  }
  assert.ok(createRoadRouter(result));
});
