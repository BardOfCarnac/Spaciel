# Spaciel — California regional terrain, expanded edges (v3)

**Review-only, 11 November 2026.** The 2045 mainline V19 viewer, fictional geography, 661 pins and label standard are unchanged.

## Deliverables

- [`data/geography/real_california_dem_reference_v3.geojson`](../data/geography/real_california_dem_reference_v3.geojson): 106 real named features, 27 additional to v2's 79, all in latitude/longitude with mapped 2400 × 2400 original USGS reference-tile coordinates and source URLs.
- Private self-contained review artifacts: `Spaciel_Real_California_Regional_Overlay_v3.html`, `Spaciel_California_Full_Region_Atlas_v3.png` and `Spaciel_California_Regions_Edge_Review_v3.png`, in working files. They reuse the real embedded DEM reference and atlas overlay; **do not commit source-licensed imagery into the public repository**.

## Explicit focus: edges left relatively empty by v2

**North:** Salinas Valley, Nacitone Watershed, Cholame Hills, Cholame Creek Watershed, Eagle Hills, Cholame Valley and Estrella River Valley; additional source-site labels: San Ardo Oil Field, San Antonio River, Nacimiento Dam and San Antonio Dam; towns hidden by default.

**East:** Upper San Juan Creek Watershed, San Juan Hills, Machesna Mountain Wilderness, Huer Huero Creek Watershed, San Juan Valley. The **Carrizo Plain** is important context, but the primary plain and Soda Lake locations lie outside the east edge of the 120°–121°W source tile. Show `TOWARDS CARRIZO PLAIN →` as a **directional outside-source annotation**, not a falsely placed region inside the DEM. Similarly `TOWARDS CALIENTE RANGE →` on the southeastern border.

**South:** Huasna Valley, Alamo Creek Watershed, Nipomo Mesa, Santa Maria River Valley, Guadalupe–Nipomo Dunes and Cuyama River Watershed. A small Oso Flaco Lake reference is included, with a less certain point anchor.

## Geographical hierarchy

1. **Context / super-region:** *California Coast Ranges*, or *Central Coast* when a neutral geographical title is needed. A super-region is a small, subdued distant-zoom label, not 106 copies of `Badlands`.
2. **Macro named landscape:** Salinas Valley, Santa Lucia Range, Cholame Hills, San Juan Hills, La Panza Range, Huasna Valley, Nipomo Mesa, Santa Maria River Valley.
3. **Medium region:** Cholame Valley, Eagle Hills, Estrella River Valley, San Juan Creek watershed, Machesna Mountain Wilderness, Edna Valley, San Luis Range and existing regional labels.
4. **Discrete features:** reservoirs, dams, quarries, landfills, historic power facilities, oilfield, military land, airports and headlands.
5. **Towns / peaks:** optional detail; default hidden to avoid an artificial population of every settlement.

All source coordinates for broad regions are **proposed text locations, not legal or natural polygons**. For area labels, the GNIS coordinate can indicate the high point or valley mouth rather than its geometric centre. Some watershed names are real official drainage designations but **not necessarily ordinary local place names**. Do not attach such names to the 2045 fictional world without deliberate conversion.

## Preserve coordinate scope

- Source `USGS_1_n36w121.tif`, 35–36°N and 120–121°W, approx 90 × 111 km.
- Original registered 2045 atlas quadrilateral is about 14 × 21 km within the full DEM tile.
- The source tile is **larger than the actively rendered 2045 V19 viewer area**. An overlay on this full tile is not an added terrain asset and does not expand the viewer.
- Reuse original DEM/atlas georeferencing. Do not apply names from California terrain to the fictional map by default.

## Source verification

- [USGS Cambria quadrangle](https://pubs.usgs.gov/sim/3287/): southern Santa Lucia Range and adjacent northeastern valleys.
- [San Luis Obispo County north watersheds](https://www.slocounty.ca.gov/departments/public-works/current-public-works-projects/slo-watershed/watersheds/north-county): Cholame, Estrella, Huer Huero, Salinas and San Juan drainage names.
- [San Luis Obispo County south watersheds](https://www.slocounty.ca.gov/departments/public-works/current-public-works-projects/slo-watershed/watersheds/south-county): Huasna, Alamo, Cuyama and Santa Maria drainage names.
- [Monterey County Nacitone Watershed](https://www.rcdmonterey.org/nacitone): Nacimiento and San Antonio drainage systems.
- [BLM Carrizo Plain](https://www.blm.gov/visit/carrizo-plain-national-monument) and [USGS regional geology](https://geo-nsdi.er.usgs.gov/metadata/open-file/99-14/).
- [US Fish & Wildlife Service Guadalupe–Nipomo Dunes](https://www.fws.gov/refuge/guadalupe-nipomo-dunes/about-us).
- Site-level links in each GeoJSON record.

## Next practical improvement

Inspect labels inside the latest **private** Spaciel V19 terrain crop and current coastline, rather than the full USGS tile. Then choose area-specific names compatible with the alternate Cyberpunk 2045 map, and disallow overlap with official city district ghost text. The review's point anchors alone do not establish mountain or valley boundaries.
