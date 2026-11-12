# Spaciel — 661 icon descriptions and geographic bubble footers (12 November 2026)

**State:** integrated in a **private Modular 07 review build**, not deployed to a live service.

This integration uses the newest existing `Spaciel_Modular_07_Portable.html` viewer rather than replacing its architecture or terrain, with the approved v07 Chakra Petch/Oxanium bubble composition and 720 ms icon morph preserved.

## Data and integrity

- Exact canonical-ID join for **556 main locations** and **105 individual Vend-R outlets**, **661 short descriptions available**.
- **140** Vend-R edited descriptions retained; **521** original sourcebook summary drafts (pending editorial approval) attached. Descriptions are not invented from generic subtype labels.
- Restored **12 missing Executive Zone IDs and 3 duplicated Cells IDs** in **both** embedded 556-place source arrays. Same names and coordinates, unchanged outlets and source-page references.
- V4 canonical tags: **194** main places have nonredundant optional tags; the rest have none. All 7 category colours and 28 subtype icon codes preserved. No generic role/tag fallback in the header.
- The on-click icon detail bubble's white content displays the one-line description; clicking a Vend-R child shows *that* child’s authored description, not merely its parent’s label.
- Geography footer: **NIGHT CITY** on the first line, then **neighbourhood, district, region** in that order on one comma-separated line using only verified fields. For the 24 official districts the parent regions are taken from the user-approved locked 2045 hierarchy. 639 pin records have a mapped region; 22 Outskirts records have no official city region and show Outskirts without an invented ancestor.
- Neighbourhoods are attached only to location pins *explicitly corresponding to attested local communities* or their directly linked child outlets. 22 are currently supported this way; unplaced 11-scheme boundaries are **not** used to invent a neighbourhood for other pins.

Both the WebGL/DOM bubble and 2D canvas fallback use the same mapping and geographic ordering; the 2D canvas wraps descriptions up to four lines within its white panel, displays NIGHT CITY and the geographic trail separately.

The 661-line editorial payload and full private 40+ MB HTML remain outside public GitHub. Reusable helper: [`src/locations/pin-bubble-details-v1.mjs`](../src/locations/pin-bubble-details-v1.mjs); tests: [`tests/test_pin_bubble_details_v1.mjs`](../tests/test_pin_bubble_details_v1.mjs).

**QA:** 661 distinct exact ID joins, complete nonblank descriptions, 556 unique records in both 3D and 2D source arrays, 194 correctly tagged main pins, 24 region-district mappings, 22 explicit neighbourhood pins, and syntax checks of all 22 embedded JavaScript blocks. Browser-based full WebGL/device acceptance remains outstanding because local navigation is blocked by the test environment. No Supabase update was made.
