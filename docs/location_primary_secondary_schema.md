# Primary classification and secondary facets

**Status (10 November 2026):** canonical-ID reviewed overlay committed; migration/export helper committed. **Not deployed to the V19 viewer, Supabase or a public map.** This repo is a working archive, not the live viewer.

## Rule

Each POI has one primary map category/role and independently stored descriptive facets:

- `category`: the *single* existing colour family (seven families; no new colours).
- `role`: the existing `category:subtype` key that determines the pictogram.
- `display_tag`: short on-screen label. Not used to choose a map colour.
- `secondary_functions`: additional services/activities (e.g., adult club, bookshop, steam baths).
- `affiliations`: verified organisations controlling or occupying the place (e.g., Voodoo Boys, Maelstrom).
- `context_tags`: current physical/operating state (e.g., ruined, flooded, gang-controlled).
- `needs_function_validation`: the primary-function-vs-occupier interpretation deserves another close read; do not auto-switch based on an affiliation.

**Examples:** Guns & Dolls is a specialist shop with adult entertainment as a secondary function. The Night City Animal Shelter is a medical/bodysculpting clinic, not ordinary animal housing. University Cargo Bay is student housing despite its name. The Forlorn Hope Wreckage is a ruined landmark, not an active bar. Totentanz is a nightclub with a separate Maelstrom affiliation.

## Data and usage

The [38-record overlay](../data/decisions/location_primary_secondary_v1.json) links reviewed decisions to **unique canonical IDs** in the 556-row source register. It also includes the 28 supported role-to-subtype strings. It supersedes earlier working spreadsheet suggestions *for these reviewed records*, while preserving the [historical review archive](../data/decisions/location_tag_review_2026-11-10.json).

From the repository root, with the 556-row CSVs available locally (the full proprietary-source derived master register is not committed):

```bash
python scripts/apply_location_primary_secondary.py \
  --register Spaciel_556_Category_Register.csv \
  --display-audit Spaciel_556_Display_Tag_Audit.csv \
  --overlay data/decisions/location_primary_secondary_v1.json \
  --out-dir export/
python -m unittest discover -s tests -p 'test_location_primary_secondary.py'
```

The helper exports a new 556-row CSV/JSON and an ID QA report. It **does not edit the source CSV or live viewer**. It leaves unreviewed locations' existing category/role intact; their tags come from the display-tag audit when supplied. It updates a reviewed location's subtype using the approved 28-role vocabulary. All source coordinate and description fields are retained. The helper raises an error on stale reviewed classifications, missing reviewed locations, or audit-order differences rather than guessing.

## Known source-register issues

- 12 rows have no canonical location ID (Executive Zone).
- Three distinct `The Cells` rows share one canonical ID (University District). Those all need unique IDs before full key-based integration.
- Three reviewed records retain a question about which *function* is most appropriate as their primary: **Tyger Works Tower**, **Chrome Cross**, **Tartarus**. Their archived roles are retained pending review. Other affiliation tags must not overrule functional classification.

## Integration when the viewer is available

1. Import the exported JSON/CSV by canonical ID; do not perform a name-only join.
2. Bind icon family/colour to `category` and icon subtype to `role` as before. Secondary facets and faction affiliations must not affect these.
3. Render the place name and its short description (the earlier pop-up design decision); show `display_tag` only where the UI calls for a type label. Do not replace the description with the tag.
4. Optionally expose facet filters and a separate organisation overlay later.
5. Visually QA representative hybrids, category colours, the 38 changed/retained records, and the 15 ID-problem rows.
6. Only after passing QA, record the viewer/data version to which the export was applied.

Commercial sourcebook text and original assets are not checked into this public repository.
