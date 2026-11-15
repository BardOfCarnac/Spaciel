/** A conservative atlas-derived paint style overlay for the approved V33 routing graph. */
export function applyAtlasRoadPaintStyle(graph,style) {
  if(style?.schema!=='spaciel.roads.yellow-paint-style.v1'||style.sourceVersion!==graph.version||
     style.frame?.[0]!==graph.frame?.[0]||style.frame?.[1]!==graph.frame?.[1])throw Error('Wrong V33 paint layer');
  const width=style.widthPolicy?.yellowRoadWidthAtlasPx;
  if(!Number.isFinite(width)||width<=0)throw Error('Invalid yellow width');
  const yellow=new Set(style.yellowPathIds),review=new Set(style.reviewPathIds);
  const ids=new Set(graph.paths.map(p=>p.id));
  if(yellow.size!==style.yellowPathIds.length||review.size!==style.reviewPathIds.length||
     [...yellow].some(id=>review.has(id))||[...yellow,...review].some(id=>!ids.has(id))||
     style.greyPathCount!==graph.paths.length-yellow.size-review.size)throw Error('Invalid paint mapping');
  return {...graph,paintLayer:{schema:style.schema,widthAtlasPx:width,yellowPaths:yellow.size,reviewPaths:review.size},
    paths:graph.paths.map(p=>{
      const isYellowRoad=yellow.has(p.id),paintStatus=isYellowRoad?'yellow':review.has(p.id)?'review':'grey';
      const next={...p,originalWidthPx:p.width,originalMajorFlag:p.major,originalRoadClass:p.roadClass,
        width:isYellowRoad?width:p.width,roadClass:isYellowRoad?'arterial':p.roadClass,
        major:isYellowRoad,isYellowRoad,paintStatus};
      // Measured ('o') edges are evidence; do not re-position them to suit display styling.
      if(isYellowRoad&&p.edgeSamples?.length)next.edgeSamples=p.edgeSamples.map(s=>{
        if(s.e==='o'||!Array.isArray(s.c))return s;
        const [tx,ty]=nearestTangent(p.points,s.c),nx=-ty,ny=tx;
        const r=v=>Math.round(v*100)/100;
        return {...s,l:[r(s.c[0]+nx*width/2),r(s.c[1]+ny*width/2)],
                     r:[r(s.c[0]-nx*width/2),r(s.c[1]-ny*width/2)]};
      });
      return next;
    })};
}
function nearestTangent(pts,c){
  let dist=Infinity,tx=1,ty=0;
  for(let i=1;i<pts.length;i++){
    const a=pts[i-1],b=pts[i],dx=b[0]-a[0],dy=b[1]-a[1],m=dx*dx+dy*dy;
    if(m<1e-9)continue;
    const t=Math.max(0,Math.min(1,((c[0]-a[0])*dx+(c[1]-a[1])*dy)/m));
    const d=(a[0]+t*dx-c[0])**2+(a[1]+t*dy-c[1])**2;
    if(d<dist){dist=d;tx=dx/Math.sqrt(m);ty=dy/Math.sqrt(m);}
  }
  return [tx,ty];
}
