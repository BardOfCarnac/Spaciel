# Spaciel location classification QA v3 — 11 November 2026

**Status:** Staged in repository. The 661-pin HTML preview remains a private Library file, and no production viewer or Supabase data is altered by this repository commit.

This revision builds on the 556-row QA-v2 register. It **does not replace the seven established colour families or 28 existing category/subtype roles**, and it explicitly rejects the abandoned exercise of inventing 74 specialised tag labels.

## Corrections

| Location | Previous role | Existing role to use | Reusable display label | Basis |
|---|---|---|---|---|
| Snack & Shack | `food:restaurants` | `shopping:general` | General retailer | Vend-R v1.3 high-confidence direct-seller profile describes a bodega; rental rooms are secondary |
| Midnight Arms Regional Office | `work:offices` | `shopping:specialist` | Specialist retailer | Vend-R v1.3 high-confidence direct-seller profile describes a weapons retail outlet |
| Harbor Patrol HQ | `work:offices` | `municipal:security` | Security / faction facility | Location name and source register identify harbour patrol headquarters, not a corporate workplace |

The first two are grounded in high-confidence Vend-R v1.3 direct-selling profiles; Harbor Patrol HQ is an explicit function-based correction of the erroneous “Corporate headquarters” type.

## Preservation

The complete 556-place V3 register and V19 patch include the 38 earlier primary/secondary review decisions and the 18 November-10 sourcebook QA refinements. The 556 canonical IDs are unique. Names, coordinates, heights, provenance, earlier correction decisions, description fields, and order are retained. There are 7 colour families and 28 role codes. No new custom subtype is introduced.

The 661-pin private V19 preview was separately aligned with those staged classifications, restoring the 12 missing and 3 duplicated IDs from the older V19 source without changing the 105 individual Vend-R outlet positions or interactions. Commercial descriptions remain descriptions, not map subtype codes.

## Still for manual primary-function review

- Cyborg Station: cyberware shop versus fitting/clinical service.
- Matsura Food Products and Murakami Suiun Imports: trade versus industry/freight.
- Northern Light Supplies: office versus distribution operation.
- Fashion Cuts: clinical/cosmetic care versus grooming.
- University Cubes: educational site versus student housing.
- Coronado Dam and Quaid Winston Memorial De-Salinization Plant: industry/utility versus civic infrastructure.
- Tyger Works Tower, Chrome Cross, and Tartarus: previously noted occupant affiliation versus main use.

These unresolved cases are **not changed automatically**.

## Files

- [556-location staged register V3](../data/locations/spaciel_locations_556_category_qa_v3_2026-11-11.json)
- [V19 staged patch V3](../data/locations/spaciel_locations_v19_patch_v3_2026-11-11.json)
- [Prior QA-v2 audit](location_tag_quality_audit_2026-11-10.md)

**Validation:** 556 records; 556 distinct IDs; 556 nonempty display labels; roles all conform to seven families and 28 existing subtypes; exactly three edits beyond V2.