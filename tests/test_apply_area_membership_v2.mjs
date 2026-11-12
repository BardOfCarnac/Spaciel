import assert from 'node:assert/strict';
import {test} from 'node:test';
import {applyAreaMembershipV2,areasForPin,pinsInArea,geographyFooter} from '../src/geography/apply-area-membership-v2.mjs';
const membership={
  areas:{
    'region:island':{name:'The Island',kind:'region'},
    'district:marina':{name:'Upper Marina',kind:'district',parent_id:'region:island'},
    'locality:floats':{name:'Marina FloatHomes',kind:'locality',parent_id:'district:marina'},
    'morph:new-harbor':{name:'New Harbor',kind:'working_morphology',parent_id:'district:marina'},
    'outside:outskirts':{name:'Outskirts',kind:'outside'},
  },
  by_pin:{
    a:{id:'a',name:'A',district:'Upper Marina',region:'The Island',neighbourhood:'Marina FloatHomes',neighbourhood_evidence:'attested_2045_named_locality',working_area_id:'morph:new-harbor',working_area:'New Harbor',working_area_status:'inside_working_polygon_provisional_registration',area_ids:['region:island','district:marina','locality:floats']},
    b:{id:'b',name:'B',district:'Upper Marina',region:'The Island',neighbourhood:'',neighbourhood_evidence:'none',working_area_id:'morph:new-harbor',working_area:'New Harbor',working_area_status:'near_working_polygon_boundary_review',area_ids:['region:island','district:marina']},
    c:{id:'c',name:'C',district:'Outskirts',region:'',neighbourhood:'',working_area_id:'',area_ids:['outside:outskirts']}
  },
  by_area:{'region:island':['a','b'],'district:marina':['a','b'],'locality:floats':['a'],'outside:outskirts':['c']},
  by_working_area_candidate:{'morph:new-harbor':['a','b']}
};
test('original approved area membership is not overwritten by conceptual polygon',()=>{
 const pins=[{id:'a',name:'A',district:'Upper Marina',region:'The Island',x:8,z:2,role:'living:homes'},
             {id:'b',name:'B',district:'Upper Marina',region:'The Island',x:2,z:5,role:'living:homes'},
             {id:'c',name:'C',district:'Outskirts',region:'',x:11,z:3,role:'work:industry'}];
 const old=structuredClone(pins);
 const result=applyAreaMembershipV2(pins,membership,{requireComplete:true});
 assert.deepEqual(result,{processed:3,city:2,outskirts:1,withNeighbourhood:1,workingCandidates:2});
 assert.equal(pins[0].neighbourhood,'Marina FloatHomes');
 assert.equal(pins[0].workingArea,'New Harbor');
 assert.equal(pins[1].neighbourhood,'');
 for(let i=0;i<3;i++)for(let key of ['id','name','district','region','x','z','role'])assert.equal(pins[i][key],old[i][key]);
 assert.deepEqual(geographyFooter(pins[0]),{heading:'NIGHT CITY',path:'Marina FloatHomes, Upper Marina, The Island'});
 assert.deepEqual(geographyFooter(pins[2]),{heading:'OUTSKIRTS',path:''});
});
test('area -> pins and pin -> areas are reciprocal, retaining provisional status',()=>{
 assert.deepEqual(pinsInArea(membership,'district:marina'),['a','b']);
 assert.deepEqual(pinsInArea(membership,'morph:new-harbor'),['a','b']);
 assert.deepEqual(pinsInArea(membership,'morph:new-harbor',{directOnly:true}),['a']);
 assert.equal(areasForPin(membership,'a').at(-1).evidence,'inside_working_polygon_provisional_registration');
 assert.equal(pinsInArea(membership,'unknown').length,0);
});
test('duplicate, missing or changed identities fail instead of guessing by name',()=>{
 const bad=[{id:'a',name:'Wrong',district:'Upper Marina',region:'The Island'}];
 assert.throws(()=>applyAreaMembershipV2(bad,membership),/identity/);
 const a={id:'a',name:'A',district:'Upper Marina',region:'The Island'};
 assert.throws(()=>applyAreaMembershipV2([a,a],membership),/duplicated/);
 assert.throws(()=>applyAreaMembershipV2([{id:'unknown',name:'X'}],membership),/Unregistered/);
});
