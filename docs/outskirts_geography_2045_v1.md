# Spaciel 2045 Outskirts geography — first named-area registration

Status: **DRAFT, anchor registration validated; actual ghost-text placement, terrain clearance and region extents NOT validated** (11 November 2026).

The names are registered in [`data/geography/outskirts_2045_labels_v1.json`](../data/geography/outskirts_2045_labels_v1.json). This is a **non-destructive overlay candidate**, not a change to the frozen V19 application, existing 24 city districts, 11 neighbourhoods, or 556 mapped location coordinates.

## 2045 first-pass name hierarchy

| Name | Entity type | Existing sourcebook location used for anchor | Intended map behaviour |
| --- | --- | --- | --- |
| Outskirts | Broad sourcebook geographical context | None; not a defined polygon | Distant-zoom regional text only |
| Badlands | Landscape descriptor | None; not a defined polygon | Distant-zoom landscape text, never a city district |
| Northern Oil Fields | Named geographical region | Northern Oil Fields (Night City 2045, p. 297) | Regional-scale ghost text |
| Jackson Plains | Named geographical region | Jackson Plains Regional Airport (p. 296) | Regional-scale ghost text; airport is NOT centre/boundary |
| Pol-Bud Miasto | Company town, NOT a region | Pol-Bud Miasto (p. 298) | Settlement-scale text, using existing pin |
| Laguna Bend | Town in 2045, NOT an inundated town | Laguna Bend (p. 296) | Settlement-scale text, using existing pin |
| Laguna Reservoir | 2045 waterbody | Laguna Bend is **proximity only** | Withhold waterbody text until checked against 2045 shoreline |

**Temporal safeguards:** the later **Rocky Ridge** ghost town should not replace the 2045 settlement **Pol-Bud Miasto**; the larger **Laguna Bend Reservoir** was created in 2062 and must not replace the earlier Laguna Reservoir on a 2045 map.

## Later-setting geographical names — research candidates, not 2045 labels

Red Peaks, Rocky Ridge Plains, Sierra Sonora, Vasquez Pass, Biotechnica Flats, Rattlesnake Creek, Eastern Wastelands, Southern Desert. They are useful research cues from 2077-era geography but the 2045 name/extent should not be inferred from proximity alone. These are recorded with `render_in_2045: false`.

The name of a **business** called Rocky Ridge does not independently establish an official 2045 *region* named Rocky Ridge Plains.

## Map anchoring and registration

The authoritative current public location register is `data/locations/spaciel_locations_556_corrected_2026-11-10.json`; it has 20 `Outskirts` records. Each named 2045 anchor points to that source record by persistent ID. We do not duplicate or change pin coordinates.

The public register's world `x,z` coordinates can be mapped into the private integration viewer's 5175 × 7966 working atlas coordinates using a 2D affine transform, derived from matching **four independent registered locations** against the private Realisation viewer:

- Northern Oil Fields: (1971.550, 861.999)
- Pol-Bud Miasto: (4812.280, 3745.551)
- Laguna Bend: (4759.055, 5524.530)
- Jackson Plains Regional Airport: (2749.023, 7027.355)

The three-point affine solve predicts the fourth match to within **0.006 working-atlas pixels**. The coefficients and each control residual are saved in JSON. This supports *registration of points*, not validity of broad region shapes.

These coordinates are **not** interchangeable with the 1396 × 1536 ghost-label study, 900 × 1390 prototype district search frame, terrain 780 × 1200 historical frame, or the 792 × 1224 map-art frame. Use the central V19/Modular coordinate adapter.

## Before showing labels in V19

1. Overlay the two regional point anchors, two settlement anchors and proposed Laguna Reservoir zone on the 2045 *actual* terrain/water mask and sourcebook Outskirts map. Reject water or building overlaps.
2. Choose the final large-letter ghost-text positions **away from pins**; do not treat the pin coordinate as a region's visual centre or invent boundaries.
3. Verify the old Laguna Reservoir shape and suppress any 2062-flood-era water polygon.
4. Integrate the approved name types into the existing label/search hierarchy without touching the frozen V19 661-pin baseline, seven-colour category bar, water, roads or city ghost labels.
5. Only after page-level confirmation, consider adopting any later-setting Badlands names into 2045, with distinct source-era and confidence fields.

## Setting-source cross-checks

- *Night City 2045* (R. Talsorian Games), Outskirts chapter, pp. 293–299, and individual pin source-page references in the map register.
- [Cyberpunk Wiki — Northern Oil Fields](https://cyberpunk.fandom.com/wiki/Northern_Oil_Fields)
- [Cyberpunk Wiki — Jackson Plains](https://cyberpunk.fandom.com/wiki/Jackson_Plains)
- [Cyberpunk Wiki — Pol-Bud Miasto](https://cyberpunk.fandom.com/wiki/Pol-Bud_Miasto)
- [Cyberpunk Wiki — Laguna Bend](https://cyberpunk.fandom.com/wiki/Laguna_Bend)
- [Cyberpunk Wiki — 2077-area fast travel geography](https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Fast_Travel/Dataterms)

**No new administrative district boundaries have been invented; no viewer build has been deployed.**
