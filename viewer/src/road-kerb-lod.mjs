/** Spaciel V33 - one fixed-width road corridor, different visual readings at distance.
 * Pavements/kerbs are illustrative styling; they are not traced or navigable geometry.
 */
export function clamp01(n) { return Math.max(0, Math.min(1, n)); }
export function smoothstep(a, b, x) {
  const t = clamp01((x - a) / (b - a));
  return t * t * (3 - 2 * t);
}
export function roadDetailAtZoom(path, zoomPxPerAtlasPx, mode = 'adaptive') {
  if (!(zoomPxPerAtlasPx > 0) || !Number.isFinite(zoomPxPerAtlasPx)) throw new Error('Positive zoom required');
  if (!(path?.width > 0) || !Number.isFinite(path.width)) throw new Error('V33 width required');
  const projectedWidth = path.width * zoomPxPerAtlasPx;
  const reveal = mode === 'edges' ? 0 : mode === 'kerbs' ? 1 : smoothstep(9, 27, projectedWidth);
  const pavement = { local:2.8, medium:3.7, arterial:5.6 }[path.roadClass] ?? 2.8;
  return {
    projectedWidthPx: projectedWidth,
    reveal, roadwayWidthAtlasPx: path.width,
    pavementAtlasPx: pavement * reveal,
    status: reveal < .2 ? 'edges' : reveal < .83 ? 'emerging-kerbs' : 'kerbs-and-pavement'
  };
}
export function roadNodeDegrees(paths) {
  const result = new Map();
  for (const p of paths) {
    for (const id of [p.from, p.to]) result.set(String(id), (result.get(String(id)) ?? 0) + 1);
  }
  return result;
}
function stroke(ctx, pts, width, colour, opacity = 1) {
  if (!pts || pts.length < 2 || !(width > 0)) return;
  ctx.globalAlpha = opacity;ctx.strokeStyle = colour;ctx.lineWidth = width;
  ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);
  for (let i=1;i<pts.length;i++)ctx.lineTo(pts[i][0],pts[i][1]);ctx.stroke();
}
function offsetBoundary(pts, lateralOffset, trimStart, trimEnd) {
  if (pts.length < 2) return [];
  const distances = [0], offset = [];
  for (let i=1;i<pts.length;i++) distances.push(distances.at(-1) + Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));
  const length = distances.at(-1), a=Math.min(length,trimStart), b=Math.max(0,length-trimEnd);
  if (b-a < Math.max(2,Math.abs(lateralOffset)*.4)) return [];
  for (let i=0;i<pts.length;i++) {
    const prev=pts[Math.max(0,i-1)],next=pts[Math.min(pts.length-1,i+1)];
    const dx=next[0]-prev[0],dy=next[1]-prev[1],mag=Math.hypot(dx,dy)||1;
    offset.push([pts[i][0]-dy/mag*lateralOffset,pts[i][1]+dx/mag*lateralOffset]);
  }
  function at(distance) {
    let j=1;while(j<distances.length-1&&distances[j]<distance) j++;
    const t=(distance-distances[j-1])/(distances[j]-distances[j-1]||1);
    return [offset[j-1][0]+(offset[j][0]-offset[j-1][0])*t,offset[j-1][1]+(offset[j][1]-offset[j-1][1])*t];
  }
  const result=[at(a)];
  for (let i=1;i<pts.length-1;i++)if(distances[i]>a+1e-4&&distances[i]<b-1e-4)result.push(offset[i]);
  result.push(at(b));return result;
}
/** Draws V33's unchanged centreline/width in three visual passes:
 * pavement background, asphalt, two external edge lines.
 * Incoming kerb lines are trimmed near 3+ arm junctions; no circular kerb caps.
 * The `degrees` map should be calculated once from the FULL graph, even if paths here are culled.
 * The caller sets ctx transformation into the atlas frame.
 */
export function drawRoadsAtZoom(ctx, visiblePaths, zoom, {mode='adaptive', degrees=null}={}) {
  if (!Array.isArray(visiblePaths) || !(zoom>0)) throw new Error('Road array and positive zoom required');
  const ds=degrees ?? roadNodeDegrees(visiblePaths);
  const old={alpha:ctx.globalAlpha,cap:ctx.lineCap,join:ctx.lineJoin};
  ctx.lineJoin='round';ctx.lineCap='round';
  const info=visiblePaths.map(p=>roadDetailAtZoom(p,zoom,mode));
  visiblePaths.forEach((p,i)=>{
    const d=info[i];if(d.pavementAtlasPx>.025){
      stroke(ctx,p.points,p.width+2*d.pavementAtlasPx+1.5/zoom,'#16252e',.72*d.reveal);
      stroke(ctx,p.points,p.width+2*d.pavementAtlasPx,'#586e73',.71*d.reveal);
    }
  });
  visiblePaths.forEach(p=>stroke(ctx,p.points,p.width,p.roadClass==='arterial'?'#33444a':'#27363f',1));
  ctx.lineCap='butt';
  visiblePaths.forEach((p,i)=>{
    const d=info[i], a=(ds.get(String(p.from))??0)>=3?p.width*.55:0;
    const b=(ds.get(String(p.to))??0)>=3?p.width*.55:0;
    for(const side of [-1,1]){
      const edge=offsetBoundary(p.points,side*p.width*.5,a,b);
      stroke(ctx,edge,Math.max(.48,1.15/zoom)*(.5+.5*d.reveal),'#b3d0cc',.43+.47*d.reveal);
    }
  });
  ctx.globalAlpha=old.alpha;ctx.lineCap=old.cap;ctx.lineJoin=old.join;
}
