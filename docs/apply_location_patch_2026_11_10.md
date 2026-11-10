# How to apply the 10 November 2026 Spaciel location corrections

This staged patch updates **556 existing point-of-interest records** without changing their positions, popup animations, roads, or building geometry.

1. Load the 556-record source dataset in the same order as the archived source register, *not* a filtered or resorted array.
2. Load [the patch](../data/locations/spaciel_locations_v19_patch_2026-11-10.json).
3. Call `applyLocationPatch(sourcePOIs, patchJson)` from [the migration helper](../scripts/apply_location_patch_2026_11_10.js).
4. Display `poi.name` and `poi.display_tag` in a location popup. Preserve `short_description` separately, since the previous Vend-R descriptions should not be discarded.
5. Confirm that the result has 556 unique IDs and nonempty display tags before swapping the map layer.

**Do not join on the original ID alone:** 12 Executive Zone residences had empty IDs, and three 'The Cells' markers shared the same original ID. `record_index` plus an exact name check is therefore required.

**No live viewer is modified by committing the patch or script.** Integration into an HTML build requires the renderer to load this JSON and call the helper. The standalone 31 MB viewer cannot simply import a repository file without suitable packaging.

The sourcebook's 51 numbered Playland attractions remain out of scope, pending later placement and unique registration.
