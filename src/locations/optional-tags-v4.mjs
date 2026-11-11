/**
 * Spaciel V4 — Optional additional tags, independent of the seven map colours
 * and 28 roles. Accept the canonical-ID-indexed V4 lookup JSON.
 * Do not infer tags from role/subtype, retailer descriptions, or affiliations.
 */
export function applyOptionalTagsV4(locations, lookup, options = {}) {
  if (!Array.isArray(locations)) throw new TypeError('locations must be an array');
  const byId = lookup?.by_id;
  if (!byId || typeof byId !== 'object') throw new TypeError('V4 lookup.by_id required');
  const strict = options.strict !== false;
  const seen = new Set();
  let main = 0, tagged = 0, children = 0;
  for (const item of locations) {
    if (!item || typeof item !== 'object') throw new TypeError('invalid location');
    const child = item.isVendrChild === true || item.is_vendr_child === true;
    const id = String(item.id || '');
    if (!child && (!id || seen.has(id))) {
      if (strict) throw new Error('missing or duplicated canonical ID: ' + id);
      continue;
    }
    if (!child) seen.add(id);
    if (item.legacy_display_tag === undefined) {
      item.legacy_display_tag = item.display_tag ?? item.displayTag ?? '';
    }
    if (child) {
      // Outlet type is retained as description; do not misuse it as a tag.
      item.tags = [];
      item.display_tag = '';
      item.displayTag = '';
      children++;
      continue;
    }
    const ref = byId[id];
    if (!ref) {
      if (strict) throw new Error('V4 tag lookup lacks canonical ID: ' + id);
      continue;
    }
    const tags = ref.tags;
    if (!Array.isArray(tags) || tags.some(t => typeof t !== 'string' || !t.trim())) {
      throw new Error('Invalid V4 tags for ' + id);
    }
    item.tags = [...new Set(tags)];
    item.display_tag = item.tags.join(' · ');
    item.displayTag = item.display_tag;
    item.secondary_functions = [...(ref.secondary_functions || [])];
    item.affiliations = [...(ref.affiliations || [])];
    item.context_tags = [...(ref.context_tags || [])];
    // category, role, coordinates, names, descriptions and icons are unchanged.
    main++; if (item.tags.length) tagged++;
  }
  if (strict && options.requireComplete && main !== lookup.count) {
    throw new Error(`Expected ${lookup.count} canonical places, received ${main}`);
  }
  return {main, with_tags:tagged, without_tags:main-tagged, vendr_children:children};
}
