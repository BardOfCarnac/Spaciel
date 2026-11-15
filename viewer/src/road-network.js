/** Canonical V33 road loader; atlas-based yellow paint and 20px width, topology unchanged. */
import {validateRoadcraftV33,createRoadRouter} from './road-routing.mjs';
import {applyAtlasRoadPaintStyle} from './road-paint-style.mjs';
export {validateRoadcraftV33,createRoadRouter} from './road-routing.mjs';
export {applyAtlasRoadPaintStyle} from './road-paint-style.mjs';
export const SPACIEL_ROADS_MANIFEST_URL=new URL('../../data/roads/manifest.json',import.meta.url);
async function loadJson(url,fetchImpl){const res=await fetchImpl(url);
  if(!res.ok)throw Error('Spaciel road load failed: '+res.status+' ('+url+')');return res.json();}
export function validateSpacielRoadGraph(graph,expected={}){
  if(graph?.schema==='spaciel.roads.runtime.v1')return validateRoadcraftV33(graph,expected);
  throw Error('Unexpected road graph schema');
}
export async function loadSpacielRoads({manifestUrl=SPACIEL_ROADS_MANIFEST_URL,fetchImpl=fetch}={}){
  const url=new URL(manifestUrl,import.meta.url),manifest=await loadJson(url,fetchImpl);
  if(manifest.schema!=='spaciel.roads.manifest.v1'||manifest.current?.version!=='roadcraft-v33')throw Error('Incompatible road manifest');
  const original=validateSpacielRoadGraph(await loadJson(new URL(manifest.current.file,url),fetchImpl),manifest.checks);
  const style=await loadJson(new URL(manifest.current.paint_style_file,url),fetchImpl);
  const graph=applyAtlasRoadPaintStyle(original,style),router=createRoadRouter(graph);
  return {version:graph.version,frame:graph.frame,graph,router,
    widthPx:22, // backwards-compatible nominal fallback only; use roads[].widthPx
    paintPolicy:graph.paintLayer,
    roads:graph.paths.map(p=>({id:p.id,from:p.from,to:p.to,points:p.points,
      roadClass:p.roadClass,widthPx:p.width,major:p.isYellowRoad,isYellowRoad:p.isYellowRoad,
      paintStatus:p.paintStatus,isApprovedV30Join:p.join,edgeSamples:p.edgeSamples}))};
}
