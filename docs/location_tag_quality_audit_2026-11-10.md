# Spaciel location tags — QA pass 2 (10 November 2026)

**Status:** 556/556 display tags exist, but `273` entries originally inherited a generic role fallback. After this sourcebook-led QA pass, **255 generic fallbacks** remain. They are usable but not necessarily informative. This is **not** 100% independently verified semantic accuracy.

## Applied in staged register v2

- **18** sourcebook- or name-confirmed location tag improvements.
- **16** category/role corrections and **2** tag-wording refinements.
- **556** non-empty tags; **556** unique IDs; unchanged original coordinates and record order.
- The existing 38-location reviewed set and the original 556 corrected register remain archived unchanged.
- **The HTML V19 viewer was not changed.** No unlocated Playland attractions were introduced.

## Corrected cases

| Location | Previous role | New role | Display tag |
|---|---|---|---|
| The Crater | `work:offices` | `leisure:culture` | Arasaka HQ ruins |
| Herschel’s Crematorium | `civic:medical` | `civic:faith` | Crematorium |
| Trauma Team Corporate Living Center | `civic:medical` | `living:homes` | Employee accommodation |
| Digital Divinity Incorporated, NC | `civic:faith` | `civic:faith` | Corporate church |
| Albino Alligator Car Wash | `municipal:freight` | `municipal:infrastructure` | Gang-controlled water supply |
| The Grateful Crane | `leisure:parks` | `leisure:parks` | Guerrilla garden |
| Hunger Street | `leisure:parks` | `food:restaurants` | Street-food market |
| The Old Ironworks Building | `leisure:attractions` | `living:homes` | Converted industrial apartments |
| Salón de Valentino | `work:industry` | `civic:public` | Local government offices |
| The Terrace | `municipal:infrastructure` | `leisure:parks` | Unfinished public park |
| Main Gate | `leisure:parks` | `municipal:security` | Military checkpoint |
| Kiroshi | `work:warehouses` | `work:industry` | Cyberoptics factory |
| Medical Technologies | `work:warehouses` | `civic:medical` | Body bank / ripperdoc clinic |
| Petrochem CHOOH2 Station | `municipal:freight` | `shopping:services` | CHOOH2 fuel station |
| SovOil CHOOH2 Station | `municipal:freight` | `shopping:services` | CHOOH2 fuel station |
| Trauma Team Pharmaceutical Plant | `civic:medical` | `work:industry` | Pharmaceutical plant |
| Substation 12 | `work:industry` | `municipal:infrastructure` | Electrical substation |
| Upper Marina Substation 2 | `work:industry` | `municipal:infrastructure` | Electrical substation |

## What still needs checking

- **255 role-derived generic tags** still need further sourcebook/Vend-R refinement. Many are appropriate, but they provide less information than a place-specific type.
- The old register's `review_required` flags concern earlier description/source verification, not necessarily missing or bad display tags. Do not treat every flagged record as untagged.
- A smaller number of highly specific names can hide misleading classifications even when their tag looks plausible; the QA pass is not an exhaustive independent reread of all 556 entries.

## Reference data

- [Register v2](../data/locations/spaciel_locations_556_tag_qa_v2_2026-11-10.json)
- [V19 patch v2](../data/locations/spaciel_locations_v19_patch_v2_2026-11-10.json)
- [Original corrected register](../data/locations/spaciel_locations_556_corrected_2026-11-10.json)

Use `record_index` plus name matching when migrating because the source register originally had missing and repeated IDs. This v2 patch is self-contained for the full 556-record set; it supersedes the earlier patch when used with the identical source array. Never apply both patches sequentially without validating IDs and record order.

**Source:** *Night City 2045* (licensed book retained privately in the user's Library); no original sourcebook prose or artwork is reproduced here.
