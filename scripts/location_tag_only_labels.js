/* Spaciel tag-only bubble labels (audit draft, 10 November 2026).
   Integrates with GEO_POINTS and GEO_SHOP_ROWS in the V19 HTML viewer.
   Does not alter sourcebook prose, Vend-R profiles, coordinates, or buildings.
   Exposes window.SPACIEL_TAG_ONLY for the two popup renderers. */
(function (root) {
  'use strict';

  // Indices are the existing V19 (category, subtype) pairs, not a new taxonomy.
  const FAMILIES = [
    'Work & Industry', 'Leisure & Culture', 'Food & Nightlife',
    'Living & Lodging', 'Shopping & Services', 'Municipal', 'Civic & Care'
  ];
  const SUBTYPES = [
    ['Offices & professional', 'Media & broadcasting', 'Industry & utilities', 'Warehouses & research'],
    ['Attractions & games', 'Sport & recreation', 'Culture & landmarks', 'Parks & open spaces'],
    ['Restaurants', 'Cafés & bakeries', 'Bars & pubs', 'Clubs & nightlife'],
    ['Homes & apartments', 'Communities & estates', 'Hotels & short stays', 'Camps & shelters'],
    ['General retail', 'Gear & technology', 'Specialist retail', 'Services & repair'],
    ['Passenger transport', 'Freight & vehicle services', 'Security & faction facilities', 'City infrastructure'],
    ['Medical & cyberware', 'Education & childcare', 'Faith & memorials', 'Government, aid & emergency']
  ];

  // Individually checked against Night City 2045. The source register remains untouched.
  // Value: [V19 category, V19 subtype].
  const VERIFIED_CORRECTIONS = Object.freeze({
    'NC2045-LOC-KABUKI-206-TORANOKO-GAKUEN': [6, 1], // Orphanage / vocational education
    'NC2045-LOC-NORTH-HEYWOOD-250-THE-NIGHT-CITY-ANIMAL-SHELTER': [6, 0], // Exotic medical clinic
    'NC2045-LOC-SOUTH-NIGHT-CITY-146-UNIVERSITY-CARGO-BAY': [3, 1], // Student housing
    'NC2045-LOC-UPPER-MARINA-073-MARINA-FLOATHOMES': [3, 0], // Houseboats
    'NC2045-LOC-LITTLE-CHINA-098-THE-FORLORN-HOPE-WRECKAGE': [1, 2], // Ruins, no longer a bar
    'NC2045-LOC-THE-HOT-ZONE-093-GRACELAND-MEDICAL': [6, 0] // Mobile healthcare within faction facility
  });

  function categoryOf(location) {
    const override = location && location.id && VERIFIED_CORRECTIONS[location.id];
    return {
      c: override ? override[0] : (location?.c ?? location?.cat ?? null),
      sub: override ? override[1] : (location?.sub ?? null)
    };
  }

  function fromTaxonomy(location) {
    const { c, sub } = categoryOf(location);
    if (Number.isInteger(c) && Number.isInteger(sub) && SUBTYPES[c]?.[sub]) return SUBTYPES[c][sub];
    return Number.isInteger(c) ? FAMILIES[c] || null : null;
  }

  function vendorType(profile) {
    const type = profile?.display_tags?.type;
    if (Array.isArray(type)) return type.find(x => typeof x === 'string' && x.trim())?.trim() || null;
    return typeof type === 'string' && type.trim() ? type.trim() : null;
  }

  function meaningfulShopType(shop) {
    const value = typeof shop?.kind === 'string' ? shop.kind.trim() : '';
    if (!value || /unresolved|unclassified|not.confirmed|^site\s*\/|^commercial or/i.test(value)) return null;
    return value.replace(/\s*\(Vend-R audited note\)\s*$/, '');
  }

  /** Return a single concise classification, never prose or source text.
   * @param {object} location - Parent GEO_POINTS entry or standalone map point.
   * @param {object|null} shop - Optional focused GEO_SHOP_ROWS child record.
   * @param {object} profilesById - Optional Vend-R profiles keyed by entity_id.
   */
  function label(location, shop = null, profilesById = {}) {
    const chosen = shop || location;
    const specific = chosen?.id && vendorType(profilesById[chosen.id]);
    if (specific) return specific;
    if (shop) return meaningfulShopType(shop) || fromTaxonomy(shop) || 'Venue';
    return fromTaxonomy(location) || 'Location';
  }

  /** Apply verified primary categories to both WebGL map points and fallback DATA.
   * The underlying source register is intentionally not edited by this display helper.
   */
  function applyVerifiedCorrections(points) {
    for (const p of points || []) {
      const fix = p?.id && VERIFIED_CORRECTIONS[p.id];
      if (!fix) continue;
      p.c = fix[0];
      p.sub = fix[1];
    }
    return points;
  }

  root.SPACIEL_TAG_ONLY = Object.freeze({
    FAMILIES, SUBTYPES, VERIFIED_CORRECTIONS, categoryOf, label, applyVerifiedCorrections
  });
})(typeof window === 'undefined' ? globalThis : window);
