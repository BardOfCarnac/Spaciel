# Spaciel Modular 09 — carry original adaptive triangles farther into shallows

**12 November 2026 — review build, not WebGL2-certified.** User approved the October 12 full regional V7 adaptive terrain in Modular 06 and asked for the triangulated ground to continue deeper under future water. The separate water material will be reworked in another conversation. Modular 08's provisional ocean shader led to a confusing visual result; this pass concentrates **only on the ground beneath it**.

## Implementation

- Original October 12 regional V7 **24,303 original vertices and 48,262 Delaunay faces** are preserved in source files and indices, source NPZ SHA-256 `fbac86f9f9d2e4cbde8c5e235e27f17fb737df34ddc4111bfc9bccd797c2550a`. This is the correct irregular adaptive terrain, not the V17 crater TIN or the V19 square grid.
- A separate **non-destructive marine display shelf** is constructed from Modular 07's repaired wet/dry shoreline classes and the original V7 DEM samples. The display-only derived vertex buffer gives submerged marine vertices a smooth additional fall of up to **12 metres over a 650-metre coastal reach**. The original elevations and height sampler remain untouched. This is a visual model, **not measured bathymetry**.
- **229 original vertex positions are adjusted only in the render buffer**, mean display lowering about 4.04 metres, maximum 12 m. **Zero land vertices** are displaced. Lakes/rivers are excluded. No additional faces or subdivisions are introduced.
- **562 source-mesh marine edge draws** within that nearshore reach are now visible (2.5% opacity). Land triangle edges remain at their approved 4% opacity. 219 fully submerged triangles receive a modest colour progression from original low-corner tint toward navy. Shore-straddling faces retain original colours.
- The current optical water surface is **off by default** until its replacement is designed; its legacy checkbox remains available solely for before/after comparison. Nothing in its light, glint or colour shader was redesigned here.
- Buildings (R14 source meshes), V23 roads, 661 pins, bubbles, category colours, camera, search and ghost geography are unchanged.

## QA / status

32 of 32 Node tests pass. All JavaScript files pass syntax checks. Archive integrity passes. The actual standalone viewer opens in Chromium's 2D fallback at mobile width, without JS page errors; shelf source is loaded and provisional water checkbox is off. **WebGL2 visual behaviour is unverified** in the available environment and requires user device review.

The private full viewer, model library and terrain payload are saved in the Spaciel Library under `/Spaciel/working-data/Spaciel_Modular_09_Portable.html` and `Spaciel_Modular_09_Private.zip`. Do not publish original map / licensed source models into public GitHub. Modular 08 remains available for rollback.
