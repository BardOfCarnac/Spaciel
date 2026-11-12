import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {test} from 'node:test';
import {createRequire} from 'node:module';
import {applyVendrCommerceV1, findVendrRetailers} from '../src/locations/vendr-commerce-v1.mjs';
const require = createRequire(import.meta.url);
const SpacielSearch = require('../src/search/spaciel-search.js');
const read = path => JSON.parse(readFileSync(new URL('../' + path, import.meta.url),'utf8'));
const v4 = read('data/locations/spaciel_locations_556_optional_tags_v4_2026-11-11.json');
const v5 = read('data/locations/spaciel_locations_556_gear_v5_2026-11-12.json');
const roles = read('data/locations/spaciel_gear_role_overlay_v5_2026-11-12.json');
const vendr = read('data/search/spaciel_vendr_merchandise_index_v1_2026-11-12.json');

test('source population and merchandise search counts do not confuse stock with dedicated stores', () => {
  assert.equal(vendr.records.length, 150);
  assert.equal(vendr.records.filter(x=>x.goods_offered).length,100);
  assert.equal(findVendrRetailers(vendr,'weapons').length,21);
  assert.equal(findVendrRetailers(vendr,'guns').length,21);
  assert.equal(findVendrRetailers(vendr,'armour').length,18);
  assert.equal(findVendrRetailers(vendr,'body armor').length,18);
  assert.equal(new Set([...findVendrRetailers(vendr,'weapons'),...findVendrRetailers(vendr,'armor')].map(x=>x.id)).size,29);
  assert.equal(findVendrRetailers(vendr,'weapons',{includeSecondary:false}).length,14);
  assert.equal(findVendrRetailers(vendr,'unrecognized query').length,0);
  assert.equal(vendr.records.filter(x=>x.primary_archetype==='weapons-dealer').length,9);
  assert.ok(vendr.records.some(x=>x.name==='Midnight Arms Regional Office'&&x.primary_departments.includes('weapons')));
});

test('only four approved primary roles change across existing 556 records', () => {
  const original = structuredClone(v4.records), rows=structuredClone(original);
  const result=applyVendrCommerceV1(rows, roles, vendr);
  assert.equal(result.corrected_primary_gear_roles, 4);
  assert.equal(result.matching_merchants, 52);
  assert.equal(new Set(rows.map(x=>x.category)).size,7);
  assert.equal(new Set(rows.map(x=>x.role)).size,28);
  assert.deepEqual(rows.map(x=>x.id),original.map(x=>x.id));
  for(let i=0;i<rows.length;i++){
    const before=original[i],after=rows[i];
    for(const key of ['id','name','category','district','x','z','height','source','display_tag'])
      assert.deepEqual(after[key],before[key],before.name+' changed '+key);
    if(after.role!==before.role) assert.ok(roles.primary_role_changes.some(x=>x.id===after.id));
  }
  for(const name of ['Guns & Dolls','Sanroo Neuro-land','Pursuit Security Inc Showroom','Midnight Arms Regional Office']){
    assert.equal(rows.find(x=>x.name===name).role,'shopping:gear');
  }
  // Mixed-purpose shops retain primary role but gain searchable departments.
  const pawn=rows.find(x=>x.name==='Moleharty’s Books & Antiques');
  assert.equal(pawn.role,'shopping:specialist');
  assert.ok(pawn.vendr_secondary_departments.includes('weapons'));
  assert.ok(pawn.vendr_search_terms.includes('guns'));
  // A second application must not change the same roles again.
  assert.equal(applyVendrCommerceV1(rows,roles,vendr).corrected_primary_gear_roles,0);
});

test('canonical V5 register matches applying the overlay to V4', () => {
  const expected=structuredClone(v4.records);
  applyVendrCommerceV1(expected,roles,vendr);
  assert.equal(v5.records.length,556);
  assert.equal(v5.counts.role_changes_in_vendr_gear_v5,4);
  for(let i=0;i<556;i++){
    const a=v5.records[i],b=expected[i],c=v4.records[i];
    for(const key of ['id','name','district','category','role','subtype','x','z','height','display_tag','source']) {
      assert.deepEqual(a[key],b[key],a.name+' canonical mismatch: '+key);
    }
    assert.deepEqual(a.tags,c.tags);
    assert.deepEqual(a.secondary_functions,c.secondary_functions);
  }
});

test('embedded sellers are only updated when existing matching pins are present', () => {
  const wanted=vendr.records.find(x=>x.name==='Cheek Turn');
  const mixed=vendr.records.find(x=>x.name==='Armory Pawn Shop');
  const locs=[
    {id:wanted.id,name:wanted.name,category:'shopping',role:'shopping:specialist'},
    {id:mixed.id,name:mixed.name,category:'shopping',role:'shopping:specialist'}
  ];
  const stats=applyVendrCommerceV1(locs,roles,vendr);
  assert.equal(stats.corrected_embedded_gear_roles,1);
  assert.equal(locs[0].role,'shopping:gear');
  assert.equal(locs[1].role,'shopping:specialist');
  assert.ok(locs[1].vendr_search_terms.includes('guns'));
  assert.equal(findVendrRetailers(vendr,'gun',{pinIds:[wanted.id]}).length,1);
  assert.equal(findVendrRetailers(vendr,'gun',{pinIds:['unmapped-nonexistent']}).length,0);
  assert.equal(locs.length,2); // Absolutely no new pin geometry.
});

test('standard unified place search discovers stock without changing destinations', () => {
  const rows=structuredClone(v4.records);
  applyVendrCommerceV1(rows,roles,vendr);
  const index=SpacielSearch.createIndex({locations:rows});
  const names=SpacielSearch.search(index,'weapons',{limit:200}).map(x=>x.name);
  assert.ok(names.includes('Midnight Arms Regional Office'));
  assert.ok(names.includes('Moleharty’s Books & Antiques')); // secondary department
  assert.ok(names.includes('GunMart')); // V4 optional tag even without Vend-R stock profile
  const hit=SpacielSearch.search(index,'midnight arms')[0];
  assert.equal(hit.kind,'pin');
  const dest=SpacielSearch.destination(hit);
  const source=rows.find(x=>x.id===dest.locationId);
  assert.equal(dest.point[0],source.x);
  assert.equal(dest.point[1],source.z);
});

test('category edits and legacy conflicts are rejected',()=>{
  const row=structuredClone(v4.records.find(x=>x.name==='Guns & Dolls'));
  row.category='civic';
  assert.throws(()=>applyVendrCommerceV1([row],roles,vendr),/Conflicting category/);
});
