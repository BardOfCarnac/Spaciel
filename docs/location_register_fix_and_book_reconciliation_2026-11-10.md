# Spaciel 556-location corrections and sourcebook reconciliation (10 November 2026)

**Status:** corrected dataset committed; the existing V19 HTML map is **not** automatically patched.

## Completed corrections

- **556/556** mapped locations carry a non-empty `display_tag`.
- **38/38** reviewed records matched unique locations in the register and received their reviewed display tags.
- **23** role changes were applied; **15** reviewed locations retained their current role.
- **12** missing IDs were assigned stable local IDs for Executive Zone residences. Their original records had blank source/page fields, so these are **dataset IDs, not book marker IDs**.
- The three distinct **The Cells** map entries had shared one ID. Each now has a unique `-SITE-01`, `-SITE-02`, or `-SITE-03` suffix, with the original common ID preserved in `previous_id`.
- The pre-existing 28-role taxonomy is unchanged. All reviewed roles already exist in it.
- Every original coordinate and row order is preserved.

## Data files

- [Corrected full register (CSV)](../data/locations/spaciel_locations_556_corrected_2026-11-10.csv)
- [Corrected full register (JSON)](../data/locations/spaciel_locations_556_corrected_2026-11-10.json)
- [V19 display/classification patch (JSON)](../data/locations/spaciel_locations_v19_patch_2026-11-10.json)
- [Historical 38-place review](../data/decisions/location_tag_review_2026-11-10.json)

## 608 versus 556

The earlier **608** figure was cited in conversation but has not been validated as a complete unique-location census. The current mapped register contains 556 records.

The *Night City 2045* sourcebook has **51 numbered Playland by the Sea attractions**, spread across its Playland chapter (PDF pages 303–312). These individual attractions were deliberately deferred as an optional expansion; the user had requested not to place every individual attraction yet. This strongly suggests why most of the nominal **52-place difference** exists, but **the final 1 is not yet proven**. Do not fabricate a 52nd POI or coordinates. Also, Playland `#31` and `#39` need additional index/text verification if compiling a complete Playland sublocation catalogue.

**Coverage statement:** 100% of the existing 556 mapped records have tags and unique IDs after this migration. That is not a claim of 100% coverage of every sourcebook location.

## Integration precautions

- The file's `record_index` is an exact index for the 556-entry source register and is the safest migration key, particularly for missing/duplicate old IDs.
- Original IDs that were already unique remain unchanged. Do not join the three The Cells entries on their old shared ID alone.
- Apply role/category and display-tag changes together. Use the current icon family/subtype mappings, not a new set of glyphs.
- Keep the 51 Playland attractions in the deferred expansion backlog until individually registered against their official map; never place them using guessed coordinates.
- Existing map/animation sources (including V19 31 MB HTML) were **not overwritten** by this repository commit.
