'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const SpacielSearch=require('../src/search/spaciel-search.js');
const geo=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/search/unified_geographic_v1.json'),'utf8'));
const locations=[
 {id:'pin-a',name:'Anjelika’s',district:'Charter Hill',source:'Night City 2045',
  x:1,z:2,shops:[{id:'venue-a',name:'Example Cyberware',kind:'Shop',ownPin:false}]},
 {id:'pin-b',name:'Another Place',district:'Kabuki',x:3,z:4}
];
const idx=SpacielSearch.createIndex({geography:geo,locations});
test('index retains 24 districts, 11 neighbourhoods and 527 traced street names',()=>{
 assert.equal(idx.counts.districts,24);
 assert.equal(idx.counts.neighbourhoods,11);
 assert.equal(idx.counts.streets,527);
 assert.ok(geo.streets.every(s=>Array.isArray(s.lines)&&s.lines.length>0));
});
test('district query prioritises the district over matching pins',()=>{
 const r=SpacielSearch.search(idx,'kabuki')[0];
 assert.equal(r.kind,'district');
 assert.equal(SpacielSearch.destination(r).frame,'district-prototype-900x1390');
});
test('neighbourhood search and destination are independent from pins',()=>{
 const r=SpacielSearch.search(idx,'wellsprings')[0];
 assert.equal(r.kind,'locality');
 assert.equal(SpacielSearch.destination(r).parentDistrict,'South Night City');
});
test('street query returns real traced polyline, not an invented pin',()=>{
 const r=SpacielSearch.search(idx,'zaragoza st')[0];
 assert.equal(r.kind,'street');
 const d=SpacielSearch.destination(r);
 assert.equal(d.frame,'v17-local-roads');
 assert.ok(d.lines[0].length>1);
});
test('location and nested Vend-R venue remain searchable',()=>{
 const pin=SpacielSearch.search(idx,'anjelika')[0];
 assert.equal(pin.kind,'pin');
 assert.equal(SpacielSearch.destination(pin).locationId,'pin-a');
 const shop=SpacielSearch.search(idx,'cyberware')[0];
 assert.equal(shop.kind,'venue');
 assert.equal(SpacielSearch.destination(shop).shopId,'venue-a');
});
test('query minimum length, context and accent folding are retained',()=>{
 assert.deepEqual(SpacielSearch.search(idx,'k'),[]);
 assert.ok(SpacielSearch.search(idx,'night city').some(r=>r.kind==='pin'));
 assert.equal(SpacielSearch.normalize('CAFÉ'),'cafe');
});
