# Spaciel Coastal × Cross-Swell bridge V1
11 November 2026 · **experimental integration, additive, main viewer unchanged**

## What is working
- Took the existing **Cross-Swell / Cola & Sunset** material study (24 components, 3 wave families, quasi-periodic regional steering, 8 physical wavelength bands from 1,650 m to 2.15 m).
- Added **native, registered, 1112 × 1392 V19 coastal masks** derived from the approved 20 m shoreline classes; *not* a rescaled image of the decorative atlas.
- Geographical effect is applied as a **per-component slope/motion amplitude multiplier**. Wave domain, wavelength, frequency, phase, direction steering, and pixel-footprint LOD **remain the original implementation**. Panning/zoom do not restart or translate the pattern.
- The volume colour, sun glint material, polychromatic shading, and terrain geometry remain independent.
- Added toggles for coastal influence, swell/ripple gains, directional SW/W/NW fetch, and diagnostics.
- Explicit outside-water background (and no inferred bathymetry) in the standalone demo.

## Files
- [Interactive standalone V19 coastal × Cross-Swell demo](../../experiments/water/coastal_cross_swell_bridge_v1.html)
- [GLSL bridge](coastal_spectral_bridge_v1.glsl)
- [WebGL2 adapter](coastal_spectral_bridge_v1.mjs)
- [Embedded approved V19 PNG mask sources](coastal_mask_embedded_v1.mjs)
- [Reference gain tests](../../tests/test_coastal_spectral_bridge.mjs)

## How to plug into the main map
```js
import {SpacielCoastalSpectralBridge} from './src/water/coastal_spectral_bridge_v1.mjs';
import {COAST_V19_MASK_DATA_URI, COAST_V19_FETCH_DATA_URI} from './src/water/coastal_mask_embedded_v1.mjs';
const coast = new SpacielCoastalSpectralBridge(gl, {
  maskUrl: COAST_V19_MASK_DATA_URI,
  fetchUrl: COAST_V19_FETCH_DATA_URI,
  maskUnit: 4, fetchUnit: 5
});
await coast.load(); // no changes to the underlying surface if loading fails
coast.configure({enabled:true, influence:1, swell:.9, wind:.9, windFrom:270});
coast.bind(existingWaterProgram); // once per draw, AFTER binding the program
```

In the **spectral fragment shader**, paste/include `coastal_spectral_bridge_v1.glsl` before the original 24-component wave loop and sample once per pixel:

```glsl
CoastalWaveField geo = spCoastSample(worldXZ, isReservoir);
for (int i=0; i<24; ++i) {
  // The existing wave normal and phase calculations are unchanged.
  int family = i / 8;
  int band = i - family * 8;
  float waveLength = spectralWL(band);
  float weight = originalSpectralWeight;
  weight *= spCoastBandGain(geo, family, waveLength);
  slope += originalWaveDirection * cos(originalPhase) * weight;
}
```

**Important:** `worldXZ` must be the existing V19 world-space position in **metres**, with the shoreline grid defined by origin `(-11098.46, -13918.137)`, cell size `20 m`, size `1112 × 1392`. This is not the 3,300 × 5,100 decorative atlas coordinate frame. The water surface requires the authoritative V19 wet classification to decide whether a pixel is rendered; do not infer land/water from the depth bands.

The standalone lab preserves the original wave shader exactly except for (a) sampling the V19 geographic fields, (b) early land/background return, (c) per-component weight multiplication, and (d) diagnostic output. The result can be visually compared with the influence toggle off (while retaining the same coastline).

## Geographic channels
| Source | Channel | Description |
|---|---|---|
| `uCoastalMask` RGBA8 | R | Inferred shelf/shallow proximity (illustrative, **not surveyed**) |
|  | G | Western swell exposure |
|  | B | Lee shelter |
|  | A | Wet/valid mask |
| `uCoastalFetch` RGB8 | R | W/270° directional fetch |
|  | G | NW/315° directional fetch |
|  | B | SW/225° directional fetch |

### Weight transfer
```glsl
longFraction = family == 2 ? 0.0 : smoothstep(70.0, 600.0, wavelengthMetres);
weight *= mix(geo.ripples, geo.swell, longFraction);
```

That preserves the identity of the original wave bands while making longer swells respond more to ocean exposure and finer wave bands respond more to local fetch. Geography does **not** bend/advance the phase and does not numerically simulate diffraction or refraction. These will require their own physically considered steering pass.

## Guardrails and limitations
- No edits to roads, terrain, buildings, coastline, or shoreline raster. Neither the main V19 viewer nor its existing shaders are replaced in this branch.
- Original wave field is independent from geography. Setting `enabled=false`, `influence=0`, or both gains=0 yields the unchanged original component weights.
- Use non-premultiplied, non-colour-converted PNG uploads (`UNPACK_COLORSPACE_CONVERSION_WEBGL=NONE`) so encoded mask values are sampled as data, not sRGB colour art.
- Mask sampler uses `LINEAR` and `CLAMP_TO_EDGE`, coordinates based on the V19 texel centres, `UNPACK_FLIP_Y_WEBGL=false` to match the source convention.
- No coverage beyond the mapped grid; the lab renders an explicit dark background outside wet pixels. A production water renderer should use its **existing** approved wet region geometry.
- Current directional wind fetch is only supported for **225°–315°**; outside this sector requires additional masks rather than blind extrapolation.
- Reservoir treatment is exposed in the GLSL adapter, but the standalone Cross-Swell lab only has the source's general wet alpha and cannot itself distinguish the reservoir's class 3. The **main V19 renderer must pass `isReservoir` from shoreline class 3**. Do not claim the lake independently has its own calibrated behaviour yet.
- Standalone demo samples its native 20 m masks, not a synthetic shoreline. The final water surface can render at higher pixel density while geography changes only as finely as the source data permits.
- This branch **has not been independently WebGL-rendered in a live browser in the current tool session**. Requires a device visual pass (coastline orientation, PNG upload readiness, wave glint contrast, masking around bridge/harbour) before approving for main.
- Not the final hierarchical zoom/morph refinement from the subsequent water-surface discussion. The bridge is intentionally a *multiplier interface* so it can be reused unchanged when the surface algorithm is upgraded.
- The previous V3.6 water shader's glints are disabled; this lab uses the glints of the existing Cross-Swell surface. Avoid double reflections when combining with the separate body-colour renderer.

## Quick acceptance tests
1. Start the standalone HTML; mask status must say `V19 coast ready`.
2. Switch on/off “Coastline influence” without camera motion. Glint structures should stay in the same world-space positions while local amplitude changes.
3. Pan and zoom through Morro Rock and Del Coronado Bay. No coast seams, animated texture resets or fixed-grid stripes.
4. Set strength to 0; surface within water must recover exactly the original wave-band weights.
5. Set wind from SW, W, NW. Only short-ripple gains shift; large swell gains should not depend on wind direction.
6. Check shoreline class 3 is separately handled in the main viewer, not treated like Pacific water.
7. Verify using device GPU WebGL2. Tests in `tests/test_coastal_spectral_bridge.mjs` cover the reference gain rules.
