import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {test} from 'node:test';
import {applyOptionalTagsV4} from '../src/locations/optional-tags-v4.mjs';
const pathFromRoot = (p) => new URL('../' + p, import.meta.url);
const read = (p) => JSON.parse(readFileSync(pathFromRoot(p),'utf8'));
const v3 = read('data/locations/spaciel_locations_556_category_qa_v3_2026-11-11.json');
const v4 = read('data/locations/spaciel_locations_556_optional_tags_v4_2026-11-11.json');
const lookup = read('data/locations/spaciel_location_additional_tags_lookup_v4_2026-11-11.json');
test('556 places preserve seven families, 28 roles and original provenance', () => {
  const rows = structuredClone(v3.records);
  const result = applyOptionalTagsV4(rows,lookup,{requireComplete:true});
  assert.equal(result.main,556);
  assert.equal(result.with_tags,194);
  assert.equal(result.without_tags,362);
  assert.equal(new Set(rows.map(x=>x.id)).size,556);
  assert.equal(new Set(rows.map(x=>x.category)).size,7);
  assert.equal(new Set(rows.map(x=>x.role)).size,28);
  for(let i=0;i<556;i++){
    const a=v3.records[i],b=rows[i],c=v4.records[i];
    for(const key of ['id','name','district','category','role','x','z','height','source','sourcebook_basis']){
      assert.equal(a[key],b[key],`${a.name}: ${key}`);
      assert.equal(a[key],c[key],`${a.name}: V4 ${key}`);
    }
    assert.deepEqual(b.tags,c.tags);
    assert.equal(b.display_tag,c.display_tag);
    assert.deepEqual(b.affiliations,c.affiliations);
  }
});
test('redundant tag removed, useful tags optional, affiliations separate', () => {
  const rows=structuredClone(v3.records);
  applyOptionalTagsV4(rows,lookup);
  const byName=(name)=>rows.find(x=>x.name===name);
  assert.deepEqual(byName('Goosetopia').tags,[]);
  assert.equal(byName('Goosetopia').display_tag,'');
  assert.deepEqual(byName('Totentanz').tags,['Nightclub']);
  assert.deepEqual(byName('Totentanz').affiliations,['Maelstrom']);
  assert.deepEqual(byName('Tyger Dojo/Tora-no-Ana').tags,['Martial arts']);
  assert.deepEqual(byName('Firebird Tearoom & Steam Baths').tags,['Tearoom','Bathing']);
  assert.ok(!rows.some(x=>x.tags.includes('Collectible figurine shop') || x.tags.includes('Specialist retailer') || x.tags.includes('Maelstrom nightclub')));
});
test('Vend-R children keep descriptions but no forced generic tag', () => {
  const child={id:'vendr-child',isVendrChild:true,category:'shopping',role:'shopping:general',short_description:'General retailer selling household items.',displayTag:'General retail'};
  const r=applyOptionalTagsV4([child],lookup);
  assert.equal(r.vendr_children,1);
  assert.equal(child.display_tag,'');
  assert.deepEqual(child.tags,[]);
  assert.equal(child.legacy_display_tag,'General retail');
  assert.equal(child.short_description,'General retailer selling household items.');
  assert.equal(child.category,'shopping');
});
test('duplicate sourcebook IDs are rejected instead of silently cross-wiring', () => {
  const a=structuredClone(v3.records[0]);
  assert.throws(()=>applyOptionalTagsV4([a,a],lookup),/duplicated canonical ID/);
});
