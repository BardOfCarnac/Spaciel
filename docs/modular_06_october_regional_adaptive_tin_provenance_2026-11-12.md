# Modular 06 — recovery of the ACTUAL October 12 adaptive regional terrain

**Review build, not user-approved or hardware-verified.** The previous Modular 05 terrain claim was incorrect: it used the V17 Hot Zone local-study mesh with 12,884 triangles, not the approved original October adaptive triangulation. Do not repeat that identification.

## Original approved source

- October 12 archive: `spaciel_full_regional_adaptive_bundle.zip`, containing `build_spaciel_regional_adaptive.py` and `spaciel_regional_adaptive_mesh.npz` (**24,274 vertices / 48,204 adaptive faces**).
- Later October 12 coastline correction: `spaciel_regional_v7_corrected_bay_bundle.zip`, including `build_spaciel_regional_adaptive_v7.py`, `spaciel_regional_v7_adaptive_mesh.npz` (**24,303 vertices / 48,262 original adaptive faces**) and the **3604 × 3604** editable `n36w121_night_city_del_coronado_bay_v7.tif` source DEM.
- The method is genuine **roughness-, relief- and coastal-proximity-weighted Delaunay TIN**, not square/grid triangulation or uniform subdivision. Face colours use the **minimum of the original three source elevations**, charcoal-to-slate palette, directional NW relief lighting and **4%** triangle edge opacity.
- V7 source NPZ SHA256: `fbac86f9f9d2e4cbde8c5e235e27f17fb737df34ddc4111bfc9bccd797c2550a`.

## Modular 06 implementation

The private V19-based viewer now gets the exact **V7 48,262 original Delaunay face indices** and their original 24,303 vertices and elevations, registered via the documented V5 lon/lat affine to V19 bitmap-to-world mapping. No generated or subdivided replacement triangles are used. A separate 1112×1392 road/camera height sampler is calculated directly from the original V7 georeferenced DEM; that sample grid is **not** the rendered triangle topology. Preserve R14 native source-model buildings, candidate V23 roads, water, pins, v07 bubbles, search and spectrum focus.

The private package contains the original NPZ, source script, V7 settings and registration spec. The separately stored source GeoTIFF is referenced but not duplicated. The source archive uses approximately 25–31m per raster pixel over the 1-degree regional tile; do not claim this is the raw 1m LiDAR dataset.

## Outstanding limits

20/20 Node regression tests and all JS syntax checks passed; private ZIP integrity checked. Full-page browser 3D testing timed out in the available environment, **so do not describe this as WebGL2 or visual approval**. The V17 V6 crater treatment is a later local intervention and has **not** been merged into the recovered October regional TIN. Road/building clearance can differ from the later engineered V19 elevations; needs real-device inspection.

Private artifacts archived at `/Spaciel/working-data/Spaciel_Modular_06_Private.zip` and `Spaciel_Modular_06_Portable.html`. Modular 05 remains the rollback. Do not upload privately licensed map or SketchUp geometry to public GitHub.
