# Spaciel — area membership V2 review (12 November 2026)

**New private review viewer and reciprocal index are complete, not published to production.** Reuse the earlier district/subdivision decisions; do not invent a new hierarchy.

## Preserved authority
- Four project regions; **24 official Night City 2045 districts**; **11 adopted working subdivision schemes** (25 sectors); 13 districts deliberately left whole.
- **661 canonical pins**: 639 Night City, 22 Outskirts. All 639 city pins retain their recorded district and its authoritative region. The **105** separate Vend-R outlets inherit their physical parent site.
- **22** already source-evidenced neighbourhood pin assignments are retained.
- No icon position, pin ID, descriptions, parent-child link, category colour, 28 subtype roles, optional tags, footer typography or animation is changed.

## Geographic registration and confidence
- Old V19 provisional pin atlas and the larger source master have an **exact global affine relationship** in the existing 525-point alignment audit (RMSE 0.0136 source-master px over 479 matched records).
- The *second* transform into the 1396×1536 polygon atlas is calibrated from **23 district label anchors** and gently optimised against existing district declarations. The polygon layer itself is a draft, not ground-truth surveying.
- Under this provisional registration, **458 of 536 main city pins** fall in the polygon for their recorded district, up from 197 under the old naive direct scaling; 40 instead hit another district polygon and 38 hit no district polygon. **Do not overwrite the book-recorded district based on these mismatches.**
- Of 258 main city pins inside the **11 split districts**, 211 fall within a designated subdivision polygon, 18 are within 15px of one, and 29 are farther away. Only direct polygon hits are provisionally assigned as a displayed working subdivision, unless an attested place-specific locality already takes precedence.
- The displayed neighbourhood/working-area coverage rises from **22 to 263 of 639 city pins**: **241 new provisional working-subdivision assignments**; 22 previously source-attested assignments unaffected. 326 city pins belong to unsplit districts, so a missing neighbourhood is normally intentional, not a gap.
- Working-area **candidate** memberships exist for all pins in split districts, including those requiring geometry review. The inspector shows source-recorded and geometry-proposed lists separately.

## App contract
Use the [generic V2 membership loader](../src/geography/apply-area-membership-v2.mjs) with the private canonical-ID lookup. Reverse listings are obtained by the same lookup, not separately-maintained POI lists. The [tests](../tests/test_apply_area_membership_v2.mjs) check source-district immutability, provisional vs attested locality, Outskirts formatting and reciprocal access.

Main-city bubble footer (approved v07) is two lines: `NIGHT CITY` then `neighbourhood, district, region` with absent levels omitted. Outskirts does **not** claim to be in Night City.

## Private artifacts
The user-facing private files are:
- `Spaciel_Modular_07_661_Areas_Linked_V2.html` (integrated main viewer)
- `Spaciel_661_Area_Inspector_V2_Registered.html` (select regions/districts/working areas and check contained pins)
- `Spaciel_661_Geographic_Membership_V2_Registered_Review.json` (full reciprocal lookup with evidence flags)
- `Spaciel_661_Geographic_Membership_V2_Registered_Review.csv` (all 661 rows)
- `Spaciel_661_Geography_Reciprocal_V2_Review_Package.zip`

Syntax checked (23 viewer + 2 inspector JS scripts). The inspector interaction passed a headless browser test by direct page content. A Node VM test verified all 661 live bridge registrations and area reciprocity. Complete viewer WebGL2 rendering remains unverified.

**Do not automatically mark the 241 new area assignments as sourcebook-confirmed; they are approved names on provisional geometry.** A later independent road/coastline anchor registration should resolve the 47 split-district main pins whose sectors are not reliably intersected.
