
import test from 'node:test';import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {applyAtlasRoadPaintStyle} from '../viewer/src/road-paint-style.mjs';
import {applyGreyRoadWidthStyle} from '../viewer/src/road-grey-widths.mjs';
import {createRoadRouter} from '../viewer/src/road-routing.mjs';
const root=new URL('../data/roads/',import.meta.url);
const src=JSON.parse(await readFile(new URL('roadcraft_v33_usable.json',root),'utf8'));
const yellow=JSON.parse(await readFile(new URL('v33_yellow_paint_style_v1.json',root),'utf8'));
const grey=JSON.parse(await readFile(new URL('v33_grey_width_style_v1.json',root),'utf8'));
const graph=applyGreyRoadWidthStyle(applyAtlasRoadPaintStyle(src,yellow),grey);
test('grey size bands plus fixed yellow widths',()=>{
  assert.equal(graph.paths.length,1962);
  assert.deepEqual(graph.greyWidthLayer.widthBandsAtlasPx,{narrow:9,regular:12,wide:17});
  assert.equal(graph.paths.filter(x=>x.widthClass==='narrow'&&x.width===9).length,501);
  assert.equal(graph.paths.filter(x=>x.widthClass==='regular'&&x.width===12).length,753);
  assert.equal(graph.paths.filter(x=>x.widthClass==='wide'&&x.width===17).length,68);
  assert.equal(graph.paths.filter(x=>x.widthClass==='yellow'&&x.width===20).length,394);
  assert.equal(graph.paths.filter(x=>x.widthClass==='review').length,246);
});
test('geometry and physical edge measurements remain identical',()=>{
  assert.deepEqual(graph.nodes,src.nodes);
  for(let i=0;i<src.paths.length;i++){
    const a=src.paths[i],b=graph.paths[i];
    assert.deepEqual([a.id,a.from,a.to,a.points,a.join],[b.id,b.from,b.to,b.points,b.join]);
    assert.deepEqual(a.edgeSamples.filter(x=>x.e==='o'),b.edgeSamples.filter(x=>x.e==='o'));
  }
  assert.equal(graph.paths.filter(p=>p.join).length,11);
  assert.ok(createRoadRouter(graph));
});
