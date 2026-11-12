/**
 * Map canonical-ID private editorial/location data into either V19 or Modular pin objects.
 * Geometry, map category / subtype logic, icon sprites and animations are outside this module.
 *
 * Private payload schema: {records:{[id]:{n,d,s,g:[neighbourhood,district,region],
 *   k:'main'|'vendr_child',v?:[index,colour,subtype,tags,affiliations,secondary,context]}}}.
 */
export function geographyTrail(pin) {
  return [pin.neighbourhood, pin.district, pin.region]
    .filter(value => typeof value === 'string' && value.trim()).join(', ');
}
export function attachIconDetails(pins, payload, {requireComplete = true} = {}) {
  if (!Array.isArray(pins) || !payload || typeof payload.records !== 'object')
    throw new TypeError('Pin array and private details lookup are required');
  const seen = new Set();
  let mains = 0, outlets = 0, described = 0, extraTagged = 0;
  for (const pin of pins) {
    if (!pin || !pin.id || seen.has(pin.id)) throw new Error('Missing or duplicate pin ID: '+pin?.id);
    seen.add(pin.id);
    const info = payload.records[pin.id];
    if (!info || pin.name !== info.n) throw new Error('Canonical ID/name mismatch: '+pin.id);
    const child = pin.isVendrChild === true;
    if ((child ? 'vendr_child':'main') !== info.k) throw new Error('Main/outlet mismatch: '+pin.id);
    if (typeof info.d !== 'string' || !info.d.trim()) throw new Error('Unwritten description: '+pin.id);
    const [neighbourhood,district,region] = info.g;
    if (district !== pin.district) throw new Error('District mismatch: '+pin.id);
    pin.short_description = info.d;
    pin.shortDescription = info.d;
    pin.description = info.d;
    pin.descriptionStatus = info.s;
    pin.neighbourhood = neighbourhood || '';
    pin.region = region || '';
    pin.legacyDisplayTag = pin.displayTag || '';
    if (info.v) {
      if (child || pin.index !== info.v[0]) throw new Error('Sourcebook index mismatch: '+pin.id);
      pin.c = info.v[1];pin.sub = info.v[2];
      pin.tags = info.v[3].slice();
      pin.affiliations = info.v[4].slice();
      pin.secondaryFunctions = info.v[5].slice();
      pin.contextTags = info.v[6].slice();
    } else {
      if (!child) throw new Error('Missing 28-role classification: '+pin.id);
      pin.tags = [];
    }
    pin.displayTag = pin.tags.join(' · ');
    if (child) outlets++;else {mains++;if (pin.tags.length) extraTagged++;}
    described++;
  }
  if (requireComplete && (pins.length !== 661 || mains !== 556 || outlets !== 105 || described !== 661))
    throw new Error('Expected 556 main locations and 105 Vend-R pins');
  return {pins:pins.length,mains,outlets,described,extraTagged};
}
