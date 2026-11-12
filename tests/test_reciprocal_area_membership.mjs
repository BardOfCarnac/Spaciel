import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createAreaMembership} from '../src/geography/reciprocal-area-membership.mjs';
const areas=[
 {id:'reg:island',name:'The Island',kind:'region',parent_id:null},
 {id:'dist:marina',name:'Upper Marina',kind:'district',parent_id:'reg:island'},
 {id:'loc:harbour',name:'Marina FloatHomes',kind:'locality',parent_id:'dist:marina'},
 {id:'outside:outskirts',name:'Outskirts',kind:'outside',parent_id:null}
];
const pins=[
 {id:'primary',kind:'main',name:'Primary',region_id:'reg:island',district_id:'dist:marina',locality_id:'loc:harbour'},
 {id:'shop',kind:'vendr_child',parent_id:'primary',name:'Child',region_id:'reg:island',district_id:'dist:marina',locality_id:'loc:harbour'},
 {id:'badlands',kind:'main',outskirts:true,name:'Outside'}
];
test('pin-to-area and area-to-pin agree, including child pins',()=>{
 const x=createAreaMembership({areaDefinitions:areas,pins});
 assert.deepEqual(x.forArea('dist:marina'),['primary','shop']);
 assert.deepEqual(x.forPin('primary').map(v=>v.name),['The Island','Upper Marina','Marina FloatHomes']);
 assert.deepEqual(x.forPin('badlands').map(v=>v.name),['Outskirts']);
 assert.equal(x.forArea('outside:outskirts').length,1);
 assert.equal(x.forArea('unknown').length,0);
 assert.equal(x.pinsCount,3);
});
test('rejects invalid districts, children and duplicate IDs',()=>{
 assert.throws(()=>createAreaMembership({areaDefinitions:areas,pins:[pins[0],pins[0]]}),/duplicate pin/i);
 assert.throws(()=>createAreaMembership({areaDefinitions:areas,pins:[pins[1]]}),/Orphan/);
 assert.throws(()=>createAreaMembership({areaDefinitions:areas,pins:[{...pins[0],district_id:'dist:wrong'}]}),/Unknown area/);
 assert.throws(()=>createAreaMembership({areaDefinitions:areas,pins:[{...pins[2],district_id:'dist:marina'}]}),/Outskirts not in Night City/);
});
