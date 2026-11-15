/** Canonical Spaciel road loader: V33 for new builds, with graph-aware routing.
 * This replaces the V23-only loader; old V23 data remains archived unchanged.
 */
import {validateRoadcraftV33,createRoadRouter} from './road-routing.mjs';
export {validateRoadcraftV33,createRoadRouter} from './road-routing.mjs';
export const SPACIEL_ROADS_MANIFEST_URL=new URL('../../data/roads/manifest.json',import.meta.url);

async function loadJson(url,fetchImpl){
  const res=await fetchImpl(url);
  if(!res.ok)throw Error(`Spaciel road load failed: ${res.status} (${url})`);
  return res.json();
}
export function validateSpacielRoadGraph(graph, expected={}){
  if(graph?.schema==='spaciel.roads.runtime.v1')return validateRoadcraftV33(graph,expected);
  throw Error('Legacy graph cannot be loaded by the V33 runtime. Use V33 manifest or an explicit legacy adapter.');
}
export async function loadSpacielRoads({manifestUrl=SPACIEL_ROADS_MANIFEST_URL,fetchImpl=fetch}={}){
  const url=new URL(manifestUrl,import.meta.url),manifest=await loadJson(url,fetchImpl);
  if(manifest.schema!=='spaciel.roads.manifest.v1'||manifest.current?.version!=='roadcraft-v33')throw Error('Incompatible road manifest');
  const graph=validateSpacielRoadGraph(await loadJson(new URL(manifest.current.file,url),fetchImpl),manifest.checks);
  const router=createRoadRouter(graph);
  return {
    version:graph.version,frame:graph.frame,graph,router,
    widthPx:22, // legacy nominal default only; render each road using its individual widthPx instead
    roads:graph.paths.map(p=>({id:p.id,from:p.from,to:p.to,points:p.points,roadClass:p.roadClass,
      widthPx:p.width,major:p.major,isApprovedV30Join:p.join,edgeSamples:p.edgeSamples}))
  };
}
