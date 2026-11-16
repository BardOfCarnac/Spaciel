// Spaciel coastal -> spectral surface adapter v1
// WebGL2 / GLSL ES 3.00. Include once ABOVE the original surface wave loop.
// Contract: p is V19 world X/Z in metres (NOT atlas pixels).
// Inputs are the native 1112x1392, 20 m shoreline-registered PNGs from Coastal Masks V1.
// RGBA mask: R inferred shallow shelf, G west swell exposure, B lee shelter, A water-valid.
// RGB fetch: R W (270 deg), G NW (315 deg), B SW (225 deg); normalized to 4 km.
// No surveyed bathymetry, hydrodynamic refraction or calibrated wave heights implied.
#ifndef SPACIEL_COASTAL_SPECTRAL_BRIDGE_V1
#define SPACIEL_COASTAL_SPECTRAL_BRIDGE_V1
uniform sampler2D uCoastalMask;
uniform sampler2D uCoastalFetch;
uniform int uCoastReady, uCoastEnabled;
uniform float uCoastInfluence, uCoastSwell, uCoastWind, uWindFrom;

struct CoastalWaveField {
  float swell;
  float ripples;
  float shelf;
  float exposure;
  float shelter;
  float directionalFetch;
  float wet;
};

const vec2 SP_COAST_ORIGIN=vec2(-11098.46,-13918.137);
const vec2 SP_COAST_DIM=vec2(1112.0,1392.0);
const float SP_COAST_M_PER_TEXEL=20.0;

// With V19 UNPACK_FLIP_Y_WEBGL=false: texel centres align to the shoreline-class grid.
vec2 spCoastUV(vec2 worldXZ){
  return ((worldXZ-SP_COAST_ORIGIN)/SP_COAST_M_PER_TEXEL+vec2(.5))/SP_COAST_DIM;
}

CoastalWaveField spCoastSample(vec2 worldXZ, bool isReservoir){
  CoastalWaveField r;
  r.swell=1.0; r.ripples=1.0;
  r.shelf=0.0; r.exposure=0.0; r.shelter=0.0;
  r.directionalFetch=0.0; r.wet=0.0;
  if(uCoastReady!=1)return r;
  vec2 uv=spCoastUV(worldXZ);
  if(any(lessThan(uv,vec2(0.0)))||any(greaterThan(uv,vec2(1.0))))return r;
  vec4 g=texture(uCoastalMask,uv);
  if(g.a<=.5)return r;
  vec3 f=texture(uCoastalFetch,uv).rgb;
  float deg=clamp(uWindFrom,225.0,315.0);
  float fetch=deg<=270.0
    ?mix(f.b,f.r,clamp((deg-225.0)/45.0,0.0,1.0))
    :mix(f.r,f.g,clamp((deg-270.0)/45.0,0.0,1.0));
  r.wet=1.0;
  r.shelf=g.r;
  r.exposure=g.g;
  r.shelter=g.b;
  r.directionalFetch=fetch;
  float swellTarget=clamp(.16+.98*g.g*(1.0-.37*g.b),.13,1.15);
  float rippleTarget=clamp(.20+1.02*sqrt(max(fetch,0.0))*(1.0-.25*g.b),.16,1.16);
  // Laguna Reservoir has no incoming Pacific swell.
  if(isReservoir){swellTarget=.12;rippleTarget=.24;}
  float influence=uCoastEnabled==1?clamp(uCoastInfluence,0.0,1.0):0.0;
  r.swell=mix(1.0,swellTarget,influence*clamp(uCoastSwell,0.0,1.0));
  r.ripples=mix(1.0,rippleTarget,influence*clamp(uCoastWind,0.0,1.0));
  return r;
}

// Multiply each EXISTING spectral component weight by this factor.
// Does not alter phase, wave position, wavelength, speed, steering or LOD.
// family: 0 long swell, 1 cross swell, 2 multidirectional fine chop.
float spCoastBandGain(CoastalWaveField coast, int family, float wavelengthMetres){
  float longFraction=family==2?0.0:smoothstep(70.0,600.0,wavelengthMetres);
  return mix(coast.ripples,coast.swell,longFraction);
}
#endif
