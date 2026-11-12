/**
 * Integrate a private, read-only one-line description register by canonical pin ID.
 * No place-name matching, no subtype/tag fallbacks, no change to map geometry.
 * Pass in the owner-supplied 661-pin description JSON from a private source.
 */
export function loadOneLineDescriptions(register) {
  if (!register || !Array.isArray(register.records)) throw new TypeError("Description register records required");
  if (register.records.length !== register.count) throw new Error("Description count mismatch");
  const byId = new Map();
  for (const row of register.records) {
    if (typeof row?.id !== "string" || !row.id.trim()) throw new Error("Missing canonical pin ID");
    if (byId.has(row.id)) throw new Error("Duplicate canonical pin ID: " + row.id);
    if (!["existing_vendr","draft_sourcebook_checked","missing"].includes(row.description_status))
      throw new Error("Invalid description status");
    if (typeof row.description !== "string") throw new TypeError("Description must be a string");
    if (row.description_status === "missing" && row.description) throw new Error("Missing status has nonempty description");
    if (row.description_status !== "missing" && !row.description) throw new Error("Existing/draft status has empty description");
    byId.set(row.id,row);
  }
  return byId;
}
export function applyOneLineDescriptions(locations, byId, {requireComplete = false} = {}) {
  if (!Array.isArray(locations) || !(byId instanceof Map)) throw new TypeError("Locations array and ID lookup required");
  const seen = new Set();
  const result = {matched:0,described:0,missing:0,unmatched:0};
  for (const loc of locations) {
    if (!loc || typeof loc.id !== "string" || !loc.id) throw new Error("Location without ID");
    if (seen.has(loc.id)) throw new Error("Duplicate location ID: " + loc.id);
    seen.add(loc.id);
    const row=byId.get(loc.id);
    if (!row) {
      result.unmatched++;
      if (requireComplete) throw new Error("Missing description register entry for " + loc.id);
      continue;
    }
    if (row.name !== loc.name) throw new Error("ID/name mismatch: " + loc.id);
    loc.short_description=row.description;
    loc.description_status=row.description_status;
    // Do not replace category, role, subtype, tags, affiliations, name or position.
    result.matched++;
    if (row.description) result.described++;
    else result.missing++;
  }
  if (requireComplete && result.matched !== byId.size) throw new Error("Incomplete 661-pin description join");
  return result;
}
