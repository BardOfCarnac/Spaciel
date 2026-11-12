import assert from 'node:assert/strict';
import {test} from 'node:test';
import {attachIconDetails,geographyTrail} from '../src/locations/pin-bubble-details-v1.mjs';

test('Optional tags remain optional and provenance is independent of description',()=>{
 const p=[
  {id:'m1',name:'Goosetopia',index:7,district:'Downtown',c:4,sub:2,x:10,z:20,displayTag:'Specialist retailer'},
  {id:'v1',name:'Named Shop',isVendrChild:true,district:'Downtown',c:4,sub:0,x:10,z:20,displayTag:'General retail'}];
 const snapshot=p.map(x=>({x:x.x,z:x.z}));
 const lookup={records:{
   m1:{n:'Goosetopia',d:'Upmarket shop selling collectable figurines.',s:'existing_vendr',g:['','Downtown','The Island'],k:'main',v:[7,4,2,[],[],[],[]]},
   v1:{n:'Named Shop',d:'Store selling interesting articles.',s:'draft_sourcebook_checked',g:['','Downtown','The Island'],k:'vendr_child'}
 }};
 const result=attachIconDetails(p,lookup,{requireComplete:false});
 assert.deepEqual(result,{pins:2,mains:1,outlets:1,described:2,extraTagged:0});
 assert.equal(p[0].displayTag,'');
 assert.equal(p[1].displayTag,'');
 assert.equal(p[0].description,'Upmarket shop selling collectable figurines.');
 assert.equal(geographyTrail(p[0]),'Downtown, The Island');
 assert.equal(p[0].x,snapshot[0].x);
 assert.equal(p[1].z,snapshot[1].z);
});
test('Neighbourhood first and missing geographic levels omitted',()=>{
 assert.equal(geographyTrail({neighbourhood:'The Warren',district:'Old Combat Zone',region:'The Island'}),'The Warren, Old Combat Zone, The Island');
 assert.equal(geographyTrail({district:'Outskirts'}),'Outskirts');
});
test('Bad joins are rejected rather than matched by name alone',()=>{
 const register={records:{m1:{n:'Correct',d:'Useful description.',g:['','Downtown','The Island'],k:'main',v:[0,4,2,[],[],[],[]]}}};
 assert.throws(()=>attachIconDetails([{id:'m1',name:'Incorrect',index:0,district:'Downtown'}],register,{requireComplete:false}),/mismatch/);
 assert.throws(()=>attachIconDetails([{id:'unknown',name:'Correct',index:0,district:'Downtown'}],register,{requireComplete:false}),/mismatch/);
});
