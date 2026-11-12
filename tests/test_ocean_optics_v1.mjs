import test from "node:test";
import assert from "node:assert/strict";
import {OCEAN_OPTICS_V1,viewerPhaseOffset,sampleOceanBodyRgb} from "../src/water/ocean-optics-v1.mjs";
test("centre true, sides opposed and continuous",()=>{
  assert.equal(viewerPhaseOffset(.5,.5,.7),0);
  const l=viewerPhaseOffset(.1,.5,.7),r=viewerPhaseOffset(.9,.5,.7);
  assert.ok(l<0&&r>0);assert.ok(Math.abs(l+r)<1e-12);
});
test("zero strength removes bowl shift",()=>{
  for(const x of [0,.2,.5,.8,1])assert.ok(Math.abs(viewerPhaseOffset(x,.9,0))===0);
});
test("dark body cycle closes at midnight",()=>{
  const a=sampleOceanBodyRgb(0),b=sampleOceanBodyRgb(24);
  assert.deepEqual(a,b);assert.deepEqual(a,[2,5,8]);
});
test("viewer-shifted sampling gives different left and right pigments",()=>{
  const left=sampleOceanBodyRgb(11.5,.05,.5),centre=sampleOceanBodyRgb(11.5,.5,.5),right=sampleOceanBodyRgb(11.5,.95,.5);
  assert.notDeepEqual(left,centre);assert.notDeepEqual(right,centre);
  assert.ok(OCEAN_OPTICS_V1.paletteStops.length>=10);
});