# Approved Ocean Optics 02 — viewer-centred body colour (12 Nov 2026)

**Design status: APPROVED / FROZEN mechanics.** The user selected the second of four ocean optical studies as Spaciel's baseline. **Implementation status: INTEGRATED PRIVATE REVIEW**, not WebGL2-certified. The private trial is `Spaciel_Modular_10_Ocean_Optics_02.html` and ZIP in ChatGPT Library `/Spaciel/working-data/`; Modular 09 remains rollback. Do not publish source-derived complete private HTML, licensed Night City atlas or original SketchUp models.

## Approved treatment

1. Ocean **body** progresses smoothly and cyclically: **black → very dark red → cola → green → blue → cola → very dark red → black**. Overall dark enough for distinct sunglints and visible terrain.
2. The viewer/camera centre shows the *actual current phase*. Screen-left water samples slightly **earlier** phases; screen-right samples slightly **later** phases. This is a **view-relative effect**, not a geographic east/west time map.
3. Modulate the shift with distance from the viewing centre as a simple proxy for obliquity in the convex bowl. Do not stretch the colour ramp to the edges of the water mask or change it merely because land occupies the right side of the screen.
4. Keep **sunglint independent**, governed by sun, normal/wave and camera relationships, using its separately approved light palette. Preserve existing glint geometry, depth/shelf/coastal response, shoreline mask and water movement while trialling body pigment.
5. **Ocean only**; reservoirs/lakes remain independently coloured until their surface datum is registered. Preserve the original October V7 24,303 vertices / 48,262 irregular Delaunay facets, including display-only marine shelf and translucent sea-level optical water from Modular 09.

## Initial editable integration values (not frozen final RGB)

- Working palette RGB stops at daily fractions `[0,.105,.205,.285,.385,.485,.575,.67,.75,.86,1]`, corresponding to `#020508 #1E0810 #3D1313 #4C2B15 #214124 #18523B #134C5F #18354E #472B19 #331217 #020508`. They came from the illustrative comparison study; final colours can be toned without overturning the approved behaviour.
- At screen coordinates `x,y∈[0,1]`, `nx=2x−1`, `ny=2y−1`, `rim=clamp(length(nx×.88,ny×.92),0,1)`. Phase offset in fraction of day: `0.15 × nx × (0.35 + 0.65 × rim) × strength`. Default `strength=.70`; maximum default edge shift ≈2.5 hours.
- Ocean clock is **not** the wave animation timer or sun azimuth clock. Full 24h loop continuously interpolates.
- Shader contract: `waterOpticsOn`, `waterCycleHour`, `waterBowlStrength`, `waterViewport`. In `wMaterial`, use cycle pigment for marine water as the base body colour, keeping the original depth contours, surface shading, wave texture, specular/glint and alpha composite. This is intentionally a screen-space viewing-angle approximation.

## Integration / verification

Modular 10 is derived from private Modular 09; it enables the separate optical water surface by default with a switch to compare legacy V3.4 pigment. The original coastline signed-distance coverage, water mesh, original regional terrain, V23 roads, 661-pin system, buildings, ghost labels, search and bottom UI are unchanged. It adds ocean-clock, progression-strength, on/off and animate-day controls under existing water controls. **37/37 Node regression tests pass.** Headless Chromium 2D fallback smoke test has no page errors, but does not support WebGL2 and therefore **does not verify the new shader on actual Android/desktop GPU**. Confirm real-device shoreline, left/centre/right progression, time playback and independent sun/glint before production release.

See the public [reference maths/palette module](../src/water/ocean-optics-v1.mjs).