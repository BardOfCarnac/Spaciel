/**
 * Spaciel bidirectional source-geography index.
 * Area membership must come from verified source declarations; never infer
 * locality from unregistered, conceptual, or historical polygon boundaries.
 * A location can have 0 or 1 locality, exactly 1 city district and region;
 * Outskirts are an explicit non-city classification.
 */
export function createAreaMembership({areaDefinitions,pins}) {
  if (!Array.isArray(areaDefinitions)||!Array.isArray(pins)) throw new TypeError('Arrays required');
  const areas=new Map(),byPin=new Map(),byArea=new Map();
  for(const area of areaDefinitions) {
    if(!area?.id||areas.has(area.id))throw new Error('Invalid/duplicate area ID');
    areas.set(area.id,structuredClone(area));
    byArea.set(area.id,[]);
  }
  for(const pin of pins) {
    if(!pin?.id||byPin.has(pin.id))throw new Error('Missing/duplicate pin ID');
    const ids=pin.outskirts ? ['outside:outskirts'] : [pin.region_id,pin.district_id,...(pin.locality_id?[pin.locality_id]:[])];
    for(const id of ids)if(!id||!areas.has(id))throw new Error('Unknown area for '+pin.id);
    if(pin.outskirts) {
      if(pin.region_id||pin.district_id||pin.locality_id)throw new Error('Outskirts not in Night City hierarchy: '+pin.id);
    } else {
      if(areas.get(pin.region_id).kind!=='region'||areas.get(pin.district_id).kind!=='district')
        throw new Error('Region/district type mismatch: '+pin.id);
      if(areas.get(pin.district_id).parent_id!==pin.region_id)throw new Error('District/region ancestry mismatch: '+pin.id);
      if(pin.locality_id && (areas.get(pin.locality_id).kind!=='locality'||areas.get(pin.locality_id).parent_id!==pin.district_id))
        throw new Error('Locality/district ancestry mismatch: '+pin.id);
    }
    const record={id:pin.id,name:pin.name||'',parent_id:pin.parent_id||'',kind:pin.kind||'main',area_ids:ids};
    byPin.set(pin.id,record);
    for(const aid of ids)byArea.get(aid).push(pin.id);
  }
  for(const record of byPin.values()){
    if(record.kind!=='vendr_child')continue;
    const parent=byPin.get(record.parent_id);
    if(!parent)throw new Error('Orphan outlet: '+record.id);
    if(record.area_ids[0]!==parent.area_ids[0]||record.area_ids[1]!==parent.area_ids[1])
      throw new Error('Child differs from parent district/region: '+record.id);
  }
  return {
    forPin(id){const p=byPin.get(id);return p?p.area_ids.map(aid=>({...areas.get(aid)})):[];},
    forArea(id){return(byArea.get(id)||[]).slice();},
    getLocation(id){const p=byPin.get(id);return p?structuredClone(p):null;},
    areasCount:areas.size,
    pinsCount:byPin.size
  };
}
