# California terrain underneath Spaciel — real geographical reference v1
Created 11 November 2026. **Not Cyberpunk 2045 canon and not a change to the main V19 viewer.**

The [27 real-place GNIS reference points](../data/geography/real_california_dem_reference_v1.geojson) overlay the original USGS `USGS_1_n36w121.tif` elevation source using its existing full-DEM registration.

## Registration
- Original DEM tile covers approximately 35°–36° N and 120°–121° W, around 90 × 111 km at this latitude.
- The registered Night City **atlas rectangle** is approximately 13.9 × 21.4 km and is rotated 11.274° clockwise.
- Rectangle corners in the legacy 2400 × 2400 DEM overview are stored in metadata.
- Marker coordinates are the GNIS place names and point locations, not outlines of a valley, mountain chain, reservoir, park, or watershed.
- The `under_2045_atlas_rectangle` flag is simply a reference-map spatial test: real features covered by an engineered fictional city can be altered/absent in Night City 2045.
- The larger source DEM is **not proof** that all this land is rendered in the user's private V19 viewer.

## Findings
Fourteen of the 27 **point anchors** fall within the registered atlas quadrilateral. Examples are Morro Rock, Whale Rock Reservoir, Black Hill, Cerro Cabrillo, Hollister Peak, Los Osos Valley and Los Osos. Cerro Alto, Bishop Peak and the Irish Hills lie outside that quadrilateral but remain inside the larger DEM source tile.

## Review deliverables
A private **standalone** review was derived from the user's original `spaciel_full_dem_registration_check.html`, preserving the embedded terrain and atlas references:
- `Spaciel_Real_California_Terrain_Overlay_v1.html`: interactive canvas, pan/zoom, original map opacity, terrain footprint and geographic name toggles.
- `Spaciel_Real_California_Terrain_Review_v1.png`: static detail view.
- `spaciel_real_terrain_names_v1.geojson`: self-contained version of reference points and metadata.

These standalone files include original source-derived imagery and **must remain private**. Do not commit the HTML, PNG or source DEM imagery to this public repository. The georeferenced label points, registration metadata and this report are safe derived working data.

## Sources
USGS Geographic Names Information System (GNIS), TopoQuest USGS map indexes for Morro Bay South and San Luis Obispo, plus Morro Bay National Estuary Program watershed map. Coordinates are GNIS feature points / NAD83, treated as effectively equivalent to WGS84 at the scale of this review. A line or polygon feature needs an authoritative shape before we draw a named *region*.

## Remaining checks
Use a verified modern DEM crop as the common terrain reference and audit each candidate label against engineered coastline and crater. For true large-area labels (Chorro Valley, Irish Hills, Los Osos Valley), trace or obtain confirmed boundaries; do not turn a GNIS centroid into a made-up polygon. The fictional 2045 names must stay in a distinct layer.
