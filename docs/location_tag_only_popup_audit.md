# Spaciel V19 — tag-only location bubbles

Status: **tested formatter / integration instructions**, not yet merged into the private 29 MB V19 HTML viewer. No production map, Supabase table, or Vend-R copy has been modified.

## Audited source material

- Current V19 source: `Spaciel_V19_Name_Short_Description_Popups.html` (private Library).
- Category register: `Spaciel_556_Category_Register.csv` (private Library).
- Existing Vend-R source: `night_city_2045_vendr_database_v1_3.json` (private Library).
- Book checks: `RTG-CPR-Night_City_2045-600dpi.pdf` (private Library).

### Findings

- **556 parent map-point rows**; all 556 have one of seven categories, and all have one of **28 subtypes**.
- The V19 category/subtype integer pairs have been cross-checked against every category-register row: **556/556 exact label matches** in the formatter matrix.
- **138 subsidiary/embedded records** are currently declared in `GEO_SHOP_ROWS`. **46** have unresolved or unclassified type text; display a neutral `Venue` fallback until resolved rather than inventing a shop speciality.
- **12** reconstructed Executive Zone person/property labels have blank canonical `entity_id` fields. Their **map index** is still distinct; do not join those by empty ID or assume they are the same place.
- `The Cells` appears at **three map positions** with one shared place ID. Preserve the three point indices; if deduplication is required, use separate map-point IDs and a shared canonical entity ID.
- Existing review flags are stale for this purpose: **98** say `Needs description confirmation`, which is no longer a blocker for tag-only bubbles. **101** reconstructed entries still have generic review flags. **13** entries have more specific classification questions.

## Display policy

1. Popup has **name** and **one short classification** (not a prose description).
2. For a Vend-R profile actually linked by **entity_id**, prefer `display_tags.type[0]` (never a name join). If none, use the mapped Spaciel subtype.
3. For a subsidiary shop without a profile, use its known `kind` label if factual, otherwise its mapped subtype or neutral `Venue`.
4. Continue using the existing icon colours, bubble animation, and map geometry.
5. Keep old `short_description` in Vend-R; do not delete or overwrite it.
6. Do **not** display `source_blurb_raw`, security ratings, or inferred prose.

## Source-verified fixes

These overrides are in `scripts/location_tag_only_labels.js` and will affect colours **only after the integration call is made**.

| Place | Former primary subtype | Source-verified primary subtype |
|---|---|---|
| Toranoko Gakuen | Industry & utilities | Education & childcare (Tyger Claws orphanage) |
| The Night City Animal Shelter | Camps & shelters | Medical & cyberware (clinic for exotics) |
| University Cargo Bay | Education & childcare | Communities & estates (low-cost student housing) |
| Marina FloatHomes | Sport & recreation | Homes & apartments (floating houseboats) |
| The Forlorn Hope Wreckage | Bars & pubs | Culture & landmarks (destroyed bar / memorial site) |
| Graceland Medical | Security & faction facilities | Medical & cyberware (Father Grace's clinic within gang territory) |

The eight other flagged faction/security entries are **not** blindly recategorized: their physical function remains security/faction facilities until further source review.

## Minimal V19 integration

Place the complete script `scripts/location_tag_only_labels.js` **before** the inline scripts which create `GEO_POINTS`.

After the `GEO_POINTS=GEO_ROWS.map(...)` statement and before any rendering or category-dependent indexing:

```js
SPACIEL_TAG_ONLY.applyVerifiedCorrections(GEO_POINTS);
```

Inside the current `openGeoBubble(item,x,y,focusedShopId)` function, replace the short-description lookup and assignment with:

```js
const profileIndex = window.SPACIEL_VENDR_PROFILES_BY_ID || {};
const tag = SPACIEL_TAG_ONLY.label(item, selectedShop, profileIndex);
document.getElementById('geoBubbleShortDescription').textContent = tag;
```

The existing paragraph/ID and CSS can stay: they now hold a tag, not a description.

The offline fallback viewer contains its own separate `DATA` array and `show(p)` function. Apply overrides once after `const DATA=[...]`:

```js
SPACIEL_TAG_ONLY.applyVerifiedCorrections(DATA);
```

In `show(p)`, replace the description lookup with:

```js
const tag = SPACIEL_TAG_ONLY.label(p, null, window.SPACIEL_VENDR_PROFILES_BY_ID || {});
detail.innerHTML = '<button class="x" aria-label="Close location details" type="button">×</button>' +
                   '<strong>' + esc(p.name) + '</strong><p class="short-description">' +
                   esc(tag) + '</p>';
```

**Do not replace map arrays with only an entity-ID-keyed map**: the 12 blank IDs and the three multi-point `The Cells` records make that unsafe.

## Follow-up work

- Merge formatter into a regenerated **private V19 HTML** viewer once file-editing capability is available.
- Run mobile popup visual test and the fallback-renderer test.
- Keep 46 uncertain child venue types marked for source verification; do not fill them with invented detail.
