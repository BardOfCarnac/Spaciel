import test from 'node:test';
import assert from 'node:assert/strict';
import {roadDetailAtZoom} from '../viewer/src/road-kerb-lod.mjs';
const path = {roadClass:'local',width:12};
test('far zoom only shows road boundary, not extra pavement', () => {
  const d=roadDetailAtZoom(path,.1);assert.equal(d.status,'edges');assert.equal(d.pavementAtlasPx,0);
});
test('pavement and kerb emerge smoothly, with fixed road width', () => {
  const a=roadDetailAtZoom(path,1.0),b=roadDetailAtZoom(path,3.0);
  assert.ok(a.pavementAtlasPx > 0 && b.pavementAtlasPx > a.pavementAtlasPx);
  assert.equal(a.roadwayWidthAtlasPx,12);assert.equal(b.roadwayWidthAtlasPx,12);
  assert.equal(b.status,'kerbs-and-pavement');
});
test('detail is presentation only and enforces positive widths and zoom',()=>{
  assert.throws(()=>roadDetailAtZoom({width:0},1));
  assert.throws(()=>roadDetailAtZoom(path,0));
  assert.equal(roadDetailAtZoom(path,.1,'kerbs').reveal,1);
});
test('node degree utilities count real graph endpoints, not geometry crossings',async()=>{
 const {roadNodeDegrees}=await import('../viewer/src/road-kerb-lod.mjs');
 const ds=roadNodeDegrees([{from:1,to:2},{from:2,to:3},{from:2,to:4}]);
 assert.equal(ds.get('2'),3);assert.equal(ds.get('1'),1);
});
