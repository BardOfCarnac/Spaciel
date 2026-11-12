# Spaciel geography: reciprocal area membership — 12 November 2026

**Baseline:** 24 official 2045 city districts, four regions, and a separate Outskirts category. Future builds should use the same canonical-ID-indexed membership in **both** directions (pin → areas and area → pins), without duplicating handwritten location lists.

## Verified source-record join
- All **661** pin records (556 main + 105 Vend-R outlets) have an assigned district or Outskirts label.
- The **639 city pins** each map to one of the 24 districts and via the locked 2045 hierarchy to one of four regions; **22 Outskirts pins** are outside Night City.
- All **105** outlet records have existing parents in the same district.
- **28** 2045-attested neighbourhood/community/ruin-sector labels occur in geography V0.7, but only **22** individual pins currently have supported locality assignments. Do **not** fill the others from names or guesses.

## Geometry QA is not yet passed
The private atlas-morphology layer is a 38-polygon working layout (24 traced district footprints, 25 conceptual subdivisions and 13 unsplit districts). Under a **non-verified direct-coordinate scaling** from the V19 3300×5100 fallback map to the 1396×1536 polygon atlas, of 536 main city points:

| Comparison | Count |
|---|---:|
| Within recorded district polygon | 197 |
| Within different traced district | 260 |
| Outside traced polygons | 79 |

**These numbers reveal a likely coordinate registration issue, not 339 proven erroneous district assignments.** An exploratory affine fit to existing district labels improved apparent matches to around 431, but it is circularly fitted and is **not** a defensible map registration. Keep all conflicts in review, retain source-recorded district labels, and never auto-promote proposed / historical / 2077 neighbourhood names.

## Integration
- Import [reciprocal-area-membership.mjs](../src/geography/reciprocal-area-membership.mjs) and construct the two-way lookup with confirmed area IDs and canonical pin IDs, including known parent-child relationships. [Tests](../tests/test_reciprocal_area_membership.mjs) verify symmetry and guard against orphan shops/invalid ancestry.
- The **private** full 661-place review viewer supports `spacielAreasForPin(id)` and `spacielPinsInArea(areaId)`; detailed polygon diagnostic results and annotated location IDs remain private, not committed to this public repository.
- City bubbles retain the two-line footer: `NIGHT CITY`, then available `neighbourhood, district, region`. Outskirts bubbles show `OUTSKIRTS` instead of an incorrect city heading.
- No source coordinates, district declarations, descriptions, tag choices, or animations were changed.

**Next:** independently register the two atlas images with shared control points, audit traced boundary lines and only then use geometry to auto-populate neighbourhood membership.
