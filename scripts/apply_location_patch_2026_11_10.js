/**
 * Spaciel V19 POI migration helper, 2026-11-10.
 * Does not alter map positions, other POI fields, or the source array.
 * Usage:
 *   import { applyLocationPatch } from "./apply_location_patch_2026_11_10.js";
 *   const corrected = applyLocationPatch(originalPOIs, patchJson);
 * Render corrected[i].display_tag in the popup, not the older generic subtype.
 */
export function applyLocationPatch(originalPOIs, patch) {
  if (!Array.isArray(originalPOIs) || originalPOIs.length !== 556) {
    throw new Error("Expected the original 556-record V19 POI array.");
  }
  if (!patch || !Array.isArray(patch.by_record_index) ||
      patch.by_record_index.length !== originalPOIs.length) {
    throw new Error("Location correction patch length mismatch.");
  }
  const norm = value => String(value ?? "").toLowerCase()
    .normalize("NFKD").replace(/[’‘]/g, "'")
    .replace(/[^a-z0-9]+/g, " ").trim();
  const output = originalPOIs.map(poi => ({ ...poi }));
  const seen = new Set();
  const ids = new Set();
  for (const correction of patch.by_record_index) {
    const i = correction.record_index;
    if (!Number.isInteger(i) || i < 0 || i >= output.length || seen.has(i)) {
      throw new Error("Invalid or repeated record_index: " + i);
    }
    const poi = output[i];
    if (norm(poi.name) !== norm(correction.match_name)) {
      throw new Error("Unsafe location ordering: expected " +
        correction.match_name + " at index " + i);
    }
    poi.id = correction.location_id;
    poi.category = correction.category;
    poi.role = correction.role;
    poi.subtype = correction.subtype;
    poi.display_tag = correction.display_tag;
    // Preserve short_description and source coordinates unchanged.
    if (!poi.display_tag || ids.has(poi.id)) {
      throw new Error("Missing tag or repeated location ID at " + i);
    }
    seen.add(i);
    ids.add(poi.id);
  }
  if (seen.size !== 556 || ids.size !== 556) {
    throw new Error("Incomplete patch.");
  }
  return output;
}
