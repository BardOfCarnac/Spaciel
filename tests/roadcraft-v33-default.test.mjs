import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {validateRoadcraftV33,createRoadRouter} from '../viewer/src/road-routing.mjs';
import {loadSpacielRoads} from '../viewer/src/road-network.js';
const base=new URL('../',import.meta.url);
const data=JSON.parse(await readFile(new URL('data/roads/roadcraft_v33_usable.json',base),'utf8'));
const manifest=JSON.parse(await readFile(new URL('data/roads/manifest.json',base),'utf8'));

test('V33 selected, V23 remains named legacy reference',()=>{
 assert.equal(manifest.current.version,'roadcraft-v33');
 assert.equal(manifest.current.graph_schema,data.schema);
 assert.equal(manifest.legacy.v23,'roadcraft_v23_default_width22.json');
 assert.deepEqual(data.frame,[5175,7966]);
});
test('all roads and endpoints match registered coordinates',()=>{
 assert.doesNotThrow(()=>validateRoadcraftV33(data,manifest.checks));
 assert.equal(data.paths.length,1962);assert.equal(Object.keys(data.nodes).length,1390);
 const observed=data.paths.flatMap(x=>x.edgeSamples).filter(s=>s.e==='o').length;
 const modeled=data.paths.flatMap(x=>x.edgeSamples).filter(s=>s.e==='m').length;
 assert.equal(observed,2288);assert.equal(modeled,5221);
});
test('topology connected, degree-1 ends and approved joins preserved',()=>{
 const R=createRoadRouter(data);const seen=new Set(), stack=[Object.keys(data.nodes)[0]];
 while(stack.length){const u=stack.pop();if(seen.has(u))continue;seen.add(u);for(const e of R.adjacency.get(u))stack.push(e.to);}
 assert.equal(seen.size,1390);
 assert.equal([...R.adjacency.values()].filter(a=>a.length===1).length,208);
 assert.equal(data.paths.filter(p=>p.join).length,11);
 assert.equal(data.review.preservedRejectedEndpointIds.length,27);
 assert.equal(data.review.preservedUncertainEndpointIds.length,1);
});
test('snap to a road interior, not merely a nearby junction',()=>{
 const R=createRoadRouter(data),p=data.paths[0],q=p.points[5];
 const snap=R.snap(q,{maxDistancePx:2});
 assert.ok(snap&&snap.distancePx<1e-4);
 assert.ok(snap.alongPx>0&&snap.alongPx<350);
});
test('routing follows graph geometry and honours mid-road starts',()=>{
 const R=createRoadRouter(data),p=data.paths[0];
 const a=R.snap(p.points[7],{maxDistancePx:2}),b=R.snap(p.points[20],{maxDistancePx:2});
 assert.ok(a&&b);
 const r=R.route(a,b);
 assert.ok(r.distancePx>5 && r.distancePx<500);
 assert.ok(r.points.length>=2);
 assert.ok(Math.hypot(...r.points[0].map((v,i)=>v-a.position[i]))<.01);
 assert.ok(Math.hypot(...r.points.at(-1).map((v,i)=>v-b.position[i]))<.01);
 assert.equal(r.units,'atlas-px');
});
test('cross-city routing can find a path through existing junctions',()=>{
 const R=createRoadRouter(data),a=data.nodes['1696'],b=data.nodes['4545'];
 const route=R.route(a,b);
 assert.ok(route&&route.distancePx>0);
 assert.ok(route.distancePx<350,'approved connection should be short');
});
test('unconnected visual line crossing does not create a node',()=>{
 const R=createRoadRouter(data);
 const n=Object.keys(data.nodes).length;
 R.snap([3000,3000]);
 assert.equal(R.adjacency.size,n);
});
test('loader exports renderable road widths, edge provenance and a router',async()=>{
 const fetchImpl=async(url)=>({ok:true,json:async()=>JSON.parse(await readFile(url,'utf8'))});
 const loaded=await loadSpacielRoads({manifestUrl:new URL('data/roads/manifest.json',base),fetchImpl});
 assert.equal(loaded.version,'roadcraft-v33');assert.equal(loaded.roads.length,1962);
 assert.ok(loaded.roads.every(p=>p.widthPx>0&&Array.isArray(p.edgeSamples)));
 assert.equal(typeof loaded.router.route,'function');
});
