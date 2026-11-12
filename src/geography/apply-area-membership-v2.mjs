/**
 * Spaciel geography V2: apply source-record district/region and provisional
 * working-sector membership by canonical pin ID.
 *
 * This module deliberately includes no private sourcebook or atlas geometry.
 * Locality and working-sector assignments are different evidence classes.
 */
export function applyAreaMembershipV2(pins, membership, opts={}) {
  if(!Array.isArray(pins)||!membership?.by_pin||!membership?.areas)throw new TypeError('V2 membership and pin array required');
  const strict=opts.strict!==false;
  const seen=new Set();
  const out={processed:0,city:0,outskirts:0,withNeighbourhood:0,workingCandidates:0};
  for(const p of pins){
    if(!p?.id||seen.has(p.id))throw new Error('Missing/duplicated pin ID');
    seen.add(p.id);
    const r=membership.by_pin[p.id];
    if(!r){if(strict)throw new Error('Unregistered pin: '+p.id);continue}
    if(p.name!==r.name||p.district!==r.district||p.region!==r.region)
      throw new Error('Pinned identity or source-record geography changed: '+p.id);
    p.neighbourhood=r.neighbourhood||'';
    p.neighbourhoodEvidence=r.neighbourhood_evidence||'none';
    p.workingAreaId=r.working_area_id||'';
    p.workingArea=r.working_area||'';
    p.workingAreaStatus=r.working_area_status||'';
    if(p.district==='Outskirts'){
      if(p.region||p.neighbourhood)throw new Error('Outside pin has Night City geographic labels: '+p.id);
      out.outskirts++;
    } else {
      out.city++;
      if(p.neighbourhood)out.withNeighbourhood++;
      if(p.workingAreaId)out.workingCandidates++;
    }
    out.processed++;
  }
  if(strict&&opts.requireComplete&&out.processed!==Object.keys(membership.by_pin).length)
    throw new Error('Incomplete full-location geography join');
  return out;
}
export function areasForPin(membership,id){
  const p=membership.by_pin[id];if(!p)return [];
  const ids=p.area_ids.slice();
  if(p.working_area_id&&!ids.includes(p.working_area_id))ids.push(p.working_area_id);
  return ids.map(id=>({id,...membership.areas[id],evidence:id===p.working_area_id?p.working_area_status:'recorded_hierarchy'}));
}
export function pinsInArea(membership,id,{directOnly=false}={}){
  if(!membership.areas[id])return [];
  if(id.startsWith('morph:')){
    const pins=membership.by_working_area_candidate?.[id]||[];
    return directOnly?pins.filter(pinId=>membership.by_pin[pinId].working_area_status==='inside_working_polygon_provisional_registration'):pins.slice();
  }
  return (membership.by_area?.[id]||[]).slice();
}
export function geographyFooter(pin){
  if(pin.district==='Outskirts')return {heading:'OUTSKIRTS',path:''};
  return {heading:'NIGHT CITY',path:[pin.neighbourhood,pin.district,pin.region].filter(Boolean).join(', ')};
}
