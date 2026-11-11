# Spaciel — real California regional labels v2

**Draft geographic reference, 11 November 2026.** This is NOT a change to Night City 2045 canon, the approved V19 viewer, or any fictional district boundaries.

## Why

The first 27 real-world landmarks were too sparse for the original full 1° USGS elevation tile. The second pass covers **79 named features**, adding **52**. Priority is given to **broad regions** (valleys, mountain ranges, viticultural areas and watersheds), **reservoirs** and **major sites** (quarries, landfills, energy generation, airports and military installations), with towns and minor peaks available optionally. It does **not** attempt a detailed contemporary California street/business map.

The [full 79-feature register](../data/geography/real_california_dem_reference_v2.geojson) is derived from the existing 27-feature v1 and verified sources including USGS GNIS / TopoQuest, Mapcarta's GNIS/OSM features, San Luis Obispo County, Monterey County Water Resources Agency, the US Nuclear Regulatory Commission and the Paso Robles AVA Alliance.

## What the expanded set contains

- 22 `region` candidates on top of v1's Irish Hills, Los Osos Valley and other topographical labels: Santa Lucia Range, La Panza Range, Chorro Valley, San Luis Range, Edna Valley, Arroyo Grande Valley, Adelaida District, Templeton Gap, El Pomar, Creston District, Upper Salinas Valley, Paso Robles Basin, etc.
- 7 additional reservoir/lake anchors: Nacimiento, San Antonio, Santa Margarita, Lopez, Atascadero, Laguna and intermittent Clear Lake.
- 9 industrial/infrastructure anchors: Diablo Canyon Nuclear Power Plant, **historic** Morro Bay Power Plant, two quarries, two landfills, Camp Roberts, and two airports.
- Two additional headlands: Point Buchon and Point San Luis.
- A few additional towns for geographical orientation, **not** automatically displayed in the primary low-density view.

**Precision:** published reference points are coordinates for sites; all approximate broad-area text centres are explicitly labelled `approx_cartographic_label_anchor`. A point does not define a valley, mountain-range, vineyard region, forest, waterbody polygon or administrative boundary.

## Coordinates and visual implementation

- USGS original `USGS_1_n36w121.tif`: approximately 35°–36°N, 120°–121°W.
- Reuse the existing original 2400 × 2400 reference display's georeferencing and the original registered city quadrilateral, with no adjustment to terrain geometry.
- **Do not confuse** the atlas's 14 × 21 km legacy rectangle with the actual fictional built city, and **do not infer** from the whole DEM tile that all its terrain is visible in V19.
- Maintain the reference overlay separate from 2045 labels, locations, real estate, roads, water and the 661-pin viewer. Initial toggles: *Regions*, *Reservoirs*, *Industrial/landmarks* ON; *Towns*, *Peaks/minor* OFF; *Include atlas area* OFF.
- Large subdued green regional text is hierarchy level 1. Blue reservoir and amber facility markers are a secondary readable level. Smaller towns/peaks only at higher detail.
- Original-DEM overview image and self-contained interactive HTML are **private working artifacts**, not committed to this public repo due to source-image rights.

## Quality / caveats

- Some AVA regions are **legally defined winegrowing appellations**, not general governmental regions; they are placed as a real-world regional reference only.
- Morro Bay Power Plant is historic/decommissioned: not an operating 2026 power plant.
- Clear Lake is intermittent; do not depict it as permanently flooded.
- Spaciel's fictional Night City locations may overwrite, remove or alter physical real-world features. Real labels must not appear in the fictional 2045 layer without a setting-specific conversion.
- Future work: acquire real vector polygons for forest, AVAs and watersheds (or derive named relief region placement), then manually refine label placement and collision against the **current** high-resolution terrain and coast. Do not invent boundaries from a point.

## Source examples

- SLO County water bodies: https://www.slocounty.ca.gov/departments/public-works/our-divisions/water-information-directory/lakes%2C-creeks-and-beaches
- SLO municipal water sources: https://www.slocity.org/government/department-directory/utilities-department/water/water-sources/surface-water
- Paso Robles AVA regions: https://pasowine.com/paso-robles/ava/
- US NRC Diablo Canyon: https://www.nrc.gov/node/2148776
- SLO waste facilities: https://www.iwma.com/landfills-and-transfer-stations
- USGS Salinas Valley reference: https://pubs.usgs.gov/publication/sir20265005/full
