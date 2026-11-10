# Spaciel — October 2026 building-area recovery (review only)

## Why this exists

Draft 03 placed 6,257 original-SKP building hulls inside the **gold** placement areas. Those gold areas were created from the *already approved V10 building footprints*, with some gap closure. They are not a citywide land-minus-roads construction envelope. Consequently sizeable plausible building land was excluded merely because our earlier footprints had not occupied it.

## Recovered source

An existing `Night_City_2045_V6_Frontage_Final_Viewer.html` from the original October 2026 morphology work contains **560 district-character block polygons** with style labels and historic density notes. These are in the **same 5175 × 7966 atlas-pixel coordinate frame** as current gold areas and cleaned road centrelines.

The earlier 560 polygons union to approximately **5,918,265 Atlas px²** (raw polygon areas sum to ~6,784,534 px²; they overlap one another). The newer 982 gold areas union to approximately **3,289,089 Atlas px²**. Intersection of older and gold is **2,740,507 Atlas px²**; approximately **3,177,758 Atlas px²** in the old character blocks is *not* represented by gold.

**Important:** Old polygons are **rough character/zoning areas, not road-cut buildable lots**. V6 acknowledged that some city areas had no full block representation. Original V6 polygons cross street centreline paths, and the city contains water, parks, intentional open areas and elevation differences. They cannot simply be dumped into the building packer.

## Provisional comparison

Subtract the current gold area and working buffered V17 road centreline corridors from older block coverage. The V17 source classifies roads with stylised 9 m local and 15 m major widths. For visual review only, their half widths were translated into atlas pixels (0.372 px/m) and given an extra **2 atlas pixels per side** margin. This produces about **2,250,095 Atlas px²** of candidate additional territory, before coastal, water, park and design exclusions. Neither stylised road widths nor this conversion certify physical road boundaries.

This recovered difference is large enough to explain the user's observation that the gold footprint-derived areas omit substantial land. It is **not a permission layer or an approved construction footprint**. The gold layer is unchanged. All current 6,257 placement proposals remain unchanged.

## Review and next steps

1. Visually compare the historic character blocks, existing gold areas, provisional road corridors and the up-to-date terrain/coastline in the private comparison website.
2. Replace provisional road buffers with the accepted road-surface envelope when available; make coastline, waterways, public parks, open plazas, the Hot Zone and military land explicit exclusions or density restrictions.
3. Derive the actual *land minus streets and deliberately protected space* envelope, and intersect this with the morphology/character definitions; **do not** derive future capacity from old individual V10 footprint slots.
4. Run another **block-first** SketchUp-native-scale placement pass across the enlarged eligible area, preserving meaningful voids and existing approved source positions and rejecting road/shoreline/building conflicts.

## Repository files

- `data/blocks/recovered_october_560_character_blocks.geojson` — exact recovered polygon planning areas and style names, **not** buildable plots
- `data/blocks/recovered_additional_territory_REVIEW_ONLY.geojson` — extra territory candidates after provisional road exclusion
- `data/roads/v17_road_width_classes_by_chain.csv` — class/width metadata keyed to cleaned road chains
- `scripts/recover_earlier_block_coverage.py` — regenerate candidate area for review

The offline comparison viewer and the V19 map image stay in the user's private Spaciel Library instead of being published as a website.