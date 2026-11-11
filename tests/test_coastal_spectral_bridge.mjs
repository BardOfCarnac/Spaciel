import assert from 'node:assert/strict';
import {referenceCoastalGains} from '../src/water/coastal_spectral_bridge_v1.mjs';
const near=(a,b,eps=1e-7)=>assert.ok(Math.abs(a-b)<eps,`Expected ${a} ≈ ${b}`);
for(const overrides of [
  {},{enabled:false},{influence:0},{swell:0,wind:0},
  {exposure:1,shelter:0,fetch:1},{exposure:0,shelter:1,fetch:0},
  {reservoir:true},{exposure:0.73,shelter:0.64,fetch:0.52}
]){
  const off=referenceCoastalGains({...overrides,enabled:false});
  near(off.swell,1);near(off.ripple,1);
  const offByInfluence=referenceCoastalGains({...overrides,influence:0});
  near(offByInfluence.swell,1);near(offByInfluence.ripple,1);
  const gains=referenceCoastalGains(overrides);
  assert.ok(Number.isFinite(gains.swell)&&Number.isFinite(gains.ripple));
  assert.ok(gains.swell>0&&gains.ripple>0);
}
const open=referenceCoastalGains({exposure:1,shelter:0,fetch:1});
const sheltered=referenceCoastalGains({exposure:0,shelter:1,fetch:0});
assert.ok(open.swell>sheltered.swell);
assert.ok(open.ripple>sheltered.ripple);
const noWind=referenceCoastalGains({exposure:1,shelter:0,fetch:0});
assert.ok(open.ripple>noWind.ripple);
const lake=referenceCoastalGains({reservoir:true,exposure:1,shelter:0,fetch:1});
assert.ok(lake.swell<open.swell);
const ratio=(open.swell-1)/(referenceCoastalGains({exposure:1,shelter:0,fetch:1,swell:.45}).swell-1);
near(ratio,2); // linear parameter response
console.log('Coastal spectral bridge reference checks passed');
