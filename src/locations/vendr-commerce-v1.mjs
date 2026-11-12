/**
 * Spaciel / Vend-R v1.3 commerce classification and discoverability.
 * This operates on existing canonical pins only. It never creates map markers.
 * Approved primary-role changes are separate from stock capability:
 * a pawnshop may sell weapons without becoming a Gear & Technology shop.
 */
const clean = value => String(value ?? '').normalize('NFKD')
  .replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
const GOODS_MODES = new Set(['DIRECT_SELLER','HYBRID_DIRECT_EVENT','EVENT_MARKET']);

export function departmentSearchTerms(index, departments) {
  const out = new Set();
  for (const name of departments || []) {
    out.add(String(name).replaceAll('-', ' '));
    for (const alias of index.aliases?.[name] || []) out.add(alias);
  }
  return [...out];
}

export function findVendrRetailers(index, department, {pinIds=null, includeSecondary=true}={}) {
  if (!index || !Array.isArray(index.records)) throw new TypeError('Vend-R index.records required');
  const requested = clean(department);
  const matching = Object.entries(index.aliases || {})
    .filter(([code,terms]) => requested === clean(code) ||
      requested === clean(code.replaceAll('-', ' ')) ||
      terms.some(term => requested === clean(term)))
    .map(([code]) => code);
  if (!matching.length || !requested) return [];
  const allowed = pinIds == null ? null : new Set([...pinIds].map(String));
  return index.records.filter(p => {
    if (!p.goods_offered || !GOODS_MODES.has(p.stock_mode)) return false;
    if (allowed && !allowed.has(String(p.id))) return false;
    const offered = includeSecondary ? [...p.primary_departments,...p.secondary_departments] : p.primary_departments;
    return matching.some(dep => offered.includes(dep));
  }).map(p => ({
    id:p.id, name:p.name, district:p.district, stock_mode:p.stock_mode,
    primary_archetype:p.primary_archetype, confidence:p.confidence,
    matched_departments:matching.filter(dep =>
      p.primary_departments.includes(dep) || (includeSecondary && p.secondary_departments.includes(dep)))
  }));
}

export function applyVendrCommerceV1(locations, overlay, index, {strict=true}={}) {
  if (!Array.isArray(locations)) throw new TypeError('locations must be array');
  if (!Array.isArray(index?.records)) throw new TypeError('Vend-R index.records required');
  if (!Array.isArray(overlay?.primary_role_changes) ||
      !Array.isArray(overlay?.possible_embedded_outlet_roles)) {
    throw new TypeError('V5 role overlay required');
  }
  const changeById = new Map(overlay.primary_role_changes.map(r => [r.id,r]));
  const outletById = new Map(overlay.possible_embedded_outlet_roles.map(r => [r.id,r]));
  const profiles = new Map(index.records.map(r => [r.id,r]));
  const seen = new Set();
  const changed = new Set(), outletChanged = new Set(), joined = new Set();
  function attach(location) {
    if (!location || typeof location !== 'object') return;
    const id = String(location.id || location.entity_id || '');
    if (!id || seen.has(location)) return;
    seen.add(location);
    const override = changeById.get(id);
    const outlet = outletById.get(id);
    if (override || outlet) {
      const current = location.role || '';
      const target = override?.to_role || outlet.recommended_role;
      // Primary roles only change within Shopping. The four main location
      // changes have preconditions; standalone embedded outlets can come
      // through any Shopping subtype before this normalization.
      const permitted = location.category === 'shopping' && (
        override ? (current === override.from_role || current === target)
                 : (!current || current.startsWith('shopping:'))
      );
      if (permitted && current !== target) {
        location.role = target;
        location.subtype = 'Gear & technology';
        (override ? changed : outletChanged).add(id);
      } else if (override && !permitted && strict) {
        throw new Error('Conflicting category/role for V5 role correction: ' + id);
      }
    }
    const p = profiles.get(id);
    if (p && p.goods_offered && GOODS_MODES.has(p.stock_mode)) {
      location.vendr_primary_departments = [...p.primary_departments];
      location.vendr_secondary_departments = [...p.secondary_departments];
      location.vendr_search_terms = departmentSearchTerms(index,
        [...p.primary_departments,...p.secondary_departments]);
      location.vendr_stock_mode = p.stock_mode;
      location.vendr_stock_confidence = p.confidence;
      joined.add(id);
    }
    // Parent bubbles may have embedded (unmapped) shops: annotate the shop,
    // never the parent as though it owns its child's inventory.
    for (const shop of location.shops || []) attach(shop);
  }
  for (const loc of locations) attach(loc);
  return {
    matching_merchants: joined.size,
    corrected_primary_gear_roles: changed.size,
    corrected_embedded_gear_roles: outletChanged.size,
    unmatched_merchants: index.records.filter(p => p.goods_offered && !joined.has(p.id)).length
  };
}
