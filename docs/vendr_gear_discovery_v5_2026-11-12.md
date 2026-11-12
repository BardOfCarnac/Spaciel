# Spaciel V5 — Vend-R merchandise discovery and primary Gear classification

**Decision:** 12 November 2026. **Status:** Approved data + reusable integration committed to the public Spaciel repository; the private 661-pin portable viewer and any Supabase deployment have **not** been rebuilt or altered.

## Why

The older 556-place Spaciel register had only eight explicit `Weapons` optional-tag assignments, misleadingly suggesting only eight shops. The independent Vend-R v1.3 stock profile database identifies **21 sellers whose stock model includes weapons** and **18 including armour**; **29** distinct sellers have at least one of those departments. Of the 21 weapons-capable vendors, nine have the primary `weapons-dealer` archetype. These counts describe cataloguing/supply capability, **not a promise of live stock**, and include embedded stores / mixed retailers.

## Classification policy

- Preserve the **seven existing category colours and 28 existing icon role codes**.
- **Shopping → Gear & technology (`shopping:gear`)** is the primary icon for dedicated combat/equipment retailers, including weapons and dedicated netrunning-hardware sellers. Apply role correction only to **confirmed existing pins**.
- **Shopping → Specialist retail**, **Shopping → General retail** etc. remain valid for pawnshops, general shops, markets, and fashion sellers even if their Vend-R merchandise can include guns or armour.
- Every inventory-bearing merchant may be *found* through its Vend-R `primary_departments` and `secondary_departments`, including the weapons, armour, ammunition, netrunning, cyberware and general-equipment groups. These searchable capabilities **are not Spaciel's optional display tags**. Never create a generic display tag because a department happens to be present.
- **Civic → Medical & cyberware** stays unchanged, including ripperdocs and clinics; a vendor that *sells* components and one that *implants* components may have different primary roles. This pass deliberately makes no medical corrections.
- Factories, security armouries, market parent buildings and other non-retail places do not automatically become equipment shops.
- Keep source/provenance uncertainty; no invented coordinates, entrances, map pins or inventory claims.

## Actual main-register changes

Only four existing sourcebook records change primary role from `shopping:specialist` to `shopping:gear`:
1. Guns & Dolls
2. Sanroo Neuro-land
3. Pursuit Security Inc Showroom
4. Midnight Arms Regional Office

Existing Gear retailers such as GunMart, Smithery, Bladeware, Faisal's Customs and Morgan's keep their classification. The original 556-place V4 register is retained as rollback; **V5 is the new staged working register**, with all original IDs, categories, coordinates, source pages, optional tags and geographic fields preserved.

The Vend-R catalogue also recognizes four dedicated **embedded-outlet** role candidates: **Cheek Turn, YoBro!, Cybershack, Eggheadz**. `applyVendrCommerceV1` will assign Gear only when an existing exact-ID Shopping outlet object is supplied; it never adds phantom pins. Sourcebook entities without corresponding pins remain in the index, but cannot be shown on the map until their actual geometry is verified.

## Population accounting and join behaviour

- 150 stock profiles from the Vend-R v1.3 merchandise dataset.
- 100 inventory-capable goods sellers with nonempty merchandise departments under `DIRECT_SELLER`, `HYBRID_DIRECT_EVENT`, or `EVENT_MARKET`. This excludes service-only providers and aggregate containers from standalone sellers.
- 21 with weapons, 18 with armour, 29 in the union; nine primary weapons dealers.
- 52 of the goods-seller profiles directly match exact IDs in the 556-place V4/V5 main register. Others may be separately pinned outlet children, mentioned outlets, or unlocated businesses. **Do not substitute guessed name-based joins.**
- A category icon change and a merchandise search match are independent; a pawnshop can appear in a "guns" search without its pawnshop primary icon changing.
- Users may search `weapons`, `guns`, `firearms`, `ammo`, `armour`, `body armor`, `cyberdeck`, `equipment` or standard department names. Matching is based on controlled department aliases rather than generated description prose.

## Files

- [556-place V5 working register](../data/locations/spaciel_locations_556_gear_v5_2026-11-12.json)
- [Small V5 overlay and rationale](../data/locations/spaciel_gear_role_overlay_v5_2026-11-12.json)
- [Canonical-ID-indexed Vend-R merchandise records](../data/search/spaciel_vendr_merchandise_index_v1_2026-11-12.json)
- [Reusable helper](../src/locations/vendr-commerce-v1.mjs) to attach departments to existing locations and normalize approved roles
- [Unified search](../src/search/spaciel-search.js) now consumes optional `vendr_search_terms` (and genuine V4 `tags`) from pin / child-venue objects, without changing destinations
- [Regression tests](../tests/test_vendr_gear_discovery_v5.mjs)

## Integration sequence (next portable viewer rebuild)

```js
import {applyVendrCommerceV1} from './src/locations/vendr-commerce-v1.mjs';
// Use the V5 556-place classification dataset as the main-source input.
// First create/restore GEO_POINTS and the existing Vend-R child objects;
// preserve all established icon colour and bubble animations.
const [gearOverlay, merchandise] = await Promise.all([
  fetch('data/locations/spaciel_gear_role_overlay_v5_2026-11-12.json').then(r=>r.json()),
  fetch('data/search/spaciel_vendr_merchandise_index_v1_2026-11-12.json').then(r=>r.json())
]);
applyVendrCommerceV1(GEO_POINTS, gearOverlay, merchandise);
const searchIndex = SpacielSearch.createIndex({geography, locations:GEO_POINTS});
// Build icon glyphs from the now-normalized roles; SpacielSearch.search()
// will also find mixed-purpose merchants by their controlled Vend-R departments.
```

Run `node --test tests/test_vendr_gear_discovery_v5.mjs` in a checked-out repository. Do not run the V4 role-invariance test against V5 as if V5 were V4; V4 remains immutable. Existing terrain, coast, roads, buildings, map movements, water optics, palette and bubble typography are outside this change.

## Review candidates

The protected/armoured-fashion shop **Gibson Battlegear Outlet** is still `shopping:general` in the main map and a `fashion-boutique` primary archetype in Vend-R, with fashion and armour departments. That is an appropriate **manual review candidate**, not an automatic weapons-dealer role correction. Stock candidates absent from Vend-R's 150 profile rows—such as the separately tagged **GunMart** and **Bladeware**—remain discoverable via the existing V4 `Weapons` tags in the unified search once the tag-bearing main records are loaded.
