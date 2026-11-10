# Spaciel — Location category and display-tag review (10 November 2026)

**Status:** Review decisions archived; **not yet applied** to the live V19 map/database.

**Related data:** [`data/decisions/location_tag_review_2026-11-10.json`](../data/decisions/location_tag_review_2026-11-10.json).

## Purpose

Preserve the 38 location classification / subtype exceptions reviewed for the Night City 2045 Spaciel map. These labels distinguish a **broad map category / icon colour** from a more precise **short display tag** for the pop-up. This is a reference and proposed migration input, not a replacement of any current map file.

## Review summary

- 38 flagged places reviewed. The prior review summarised **23 category changes** and **15 retained broad categories**; those counts are historical review conclusions rather than independently recalculated against a versioned before/after map.
- Each proposed `suggested_role` below uses `category:subtype` syntax; this file does not assert that those strings are already supported by the live icon registry.
- **Do not join solely by display name**: first match each place to a canonical location ID, taking care with duplicated and missing IDs in Spaciel's registers.
- No coordinates, glyph geometry, icon colours, popup animation, or POI data have been modified by this commit.

## Reviewed records

| Location | Proposed role | Pop-up display tag |
| --- | --- | --- |
| Anjelika’s | `food:bars` | Host bar |
| Guns & Dolls | `shopping:specialist` | Gun shop / adult club |
| Munch Munch Munch | `food:clubs` | Private members’ club |
| Firebird Tearoom & Steam Baths | `food:cafes` | Tearoom / steam baths |
| Zhirafa Office Park | `work:offices` | Corporate offices / factories |
| Toranoko Gakuen | `civic:education` | Orphanage / vocational school |
| Tyger Works Tower | `municipal:security` | Gang-operated office tower |
| Chrome Cross | `municipal:security` | Red Chrome Legion hangout |
| The Forlorn Hope Wreckage | `leisure:culture` | Ruined bar / memorial |
| The Seep | `leisure:culture` | Flooded temple sinkhole |
| Bristol Business Park | `work:offices` | Offices / events complex |
| The Night City Animal Shelter | `civic:medical` | Exotic clinic / bodysculpting |
| Jesse James’ Kosher Deli | `food:bars` | Pub / martial arts studio |
| The Bodukkan | `municipal:security` | Kimen-Gumi headquarters |
| Honest Hiro’s Used Cars | `shopping:specialist` | Used-car dealership |
| Oni-Yama Jail | `municipal:security` | Gang-run jail |
| Tartarus | `municipal:security` | Gang-controlled mall |
| The Island | `municipal:security` | Voodoo Boys headquarters |
| Minimallism | `shopping:general` | Fixer-run mall / market |
| Skinny James’ Lot | `municipal:freight` | Nomad cargo broker |
| Container Mart | `shopping:general` | Container shopping plaza |
| University Cargo Bay | `living:homes` | Student container housing |
| EEC Consulate | `civic:public` | Consulate |
| Japanese Consulate | `civic:public` | Consulate |
| Mexican Consulate | `civic:public` | Consulate |
| Pacifica Confederation Offices | `civic:public` | Government offices |
| Organization of American States Mission | `civic:public` | Diplomatic mission |
| United States Consulate | `civic:public` | Consulate |
| Carriage Street Books/Afterwords Café | `food:cafes` | Bookshop / café |
| The Forge | `work:industry` | Chrome refurbishment works |
| GraffitiX | `leisure:culture` | Art gallery |
| Great River Storehouse | `work:warehouses` | Drone fulfilment warehouse |
| Marina FloatHomes | `living:homes` | Floating residences |
| Canadian Consulate | `civic:public` | Consulate |
| The Obituary | `municipal:security` | Dragula Racers headquarters |
| Turbo Neon Motors | `shopping:services` | Custom vehicle workshop |
| Graceland Medical | `civic:medical` | Community medical clinic |
| Totentanz | `food:clubs` | Maelstrom nightclub |

## Important interpretation notes

- **Guns & Dolls:** combined gun store and adult club, not a medical service.
- **The Night City Animal Shelter:** clinic and bodysculpting for exotics; not a general animal shelter.
- **University Cargo Bay:** inexpensive student container accommodation, not a freight depot.
- **GraffitiX:** the gallery function should drive its primary icon despite retail activity.
- **Great River Storehouse:** distribution / drone fulfilment operation rather than conventional walk-in retail.
- **Graceland Medical:** local medical care despite gang control.
- **The Forge:** industrial chrome refurbishment operation; preserve its industrial role.
- **Jesse James’ Kosher Deli:** bar/pub function remains relevant alongside its martial arts studio.

## Provenance and integration notes

Compiled from the 10 November 2026 user-approved Spaciel location review, with sourcebook and Vend-R comparisons. Specific sourcebook page checks included **Guns & Dolls** (PDF page 86), **Graceland Medical** (PDF page 94), **University Cargo Bay** (PDF page 147), **The Night City Animal Shelter** (PDF page 251), and **Toranoko Gakuen** (PDF page 207) of *Night City 2045*. The sourcebook is commercial; its text and original assets are not uploaded to this public repository.

To integrate: resolve canonical IDs → compare with the current 556-place source register → validate `suggested_role` against the active category/icon vocabulary → apply display tags → visually check icons and pop-ups → update the status in a new decision record. Do not silently mutate this historical archive.
