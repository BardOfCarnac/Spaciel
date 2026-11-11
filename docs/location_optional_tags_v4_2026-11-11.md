# Spaciel V4 — optional additional tags (11 November 2026)

**Status:** Staged, non-destructive. The V3 location register is retained and unchanged. The 661-pin V19 private preview is separate from the repository and is not a production deployment.

## Rule
- Primary `category`: one of seven established families, determines colour.
- Primary `role`: one of 28 established subtypes, determines glyph.
- Optional `tags: string[]`: only meaningful cross-cutting or more precise reusable functions **not duplicated by the primary subtype**. Empty `[]` is normal.
- `affiliations`: organisations and factions; **not** tags.
- `context_tags`: physical / operational state; distinct from tags.
- `secondary_functions`: source-reviewed secondary uses; retained even when not promoted to a tag.
- Specific descriptions and original source notes remain descriptions. Never generate prose from a tag.
- `legacy_display_tag` and `legacy_tag_basis` retain previous wording for auditing, but never render as current tags.
- `display_tag` is a compatibility alias of `tags.join(" · ")`, blank when the tag array is empty. No fallback to subtype labels.

## Counts
- 556 sourcebook locations; 194 with additional tags and 362 needing none.
- 93 reusable tag values / 198 assignments; seven colour families and 28 unchanged role codes.
- 38 reviewed primary/secondary records contribute verified affiliations, secondary functions and context.
- 105 separately positioned Vend-R children remain outside the 556-row migration; V19 previews retain them, without misclassifying parent pins.

## Examples
| Place | Primary role | Optional tags | Affiliation |
|---|---|---|---|
| Goosetopia | shopping:specialist | none | — |
| Totentanz | food:clubs | Nightclub | Maelstrom |
| Tyger Dojo/Tora-no-Ana | leisure:sport | Martial arts | — |
| Firebird Tearoom & Steam Baths | food:cafes | Tearoom, Bathing | — |

## Inputs and integration
- [Source V3](../data/locations/spaciel_locations_556_category_qa_v3_2026-11-11.json) retained as rollback.
- [V4 register](../data/locations/spaciel_locations_556_optional_tags_v4_2026-11-11.json)
- [V4 by-ID lookup](../data/locations/spaciel_location_additional_tags_lookup_v4_2026-11-11.json)
- [Policy / controlled vocabulary](../data/decisions/location_additional_tag_policy_v4.json)

Use canonical IDs for joining. Viewer tag display must read `tags`; if empty, omit the entire tag line, **not** display a generic role fallback. Search should index only actual tags alongside name/district/role and descriptions where separately permitted. Do not show legacy label values or treat affiliations as tags. Preserve colour filters and bubble/icon animations.

This pass does **not** claim sourcebook validation of old role-fallback labels, invent 74 new bespoke location descriptors, or change any of the three unresolved affiliation-versus-primary questions.
