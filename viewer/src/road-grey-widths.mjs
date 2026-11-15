
/** V33 grey road width standardisation. Does not alter road nodes, centreline or observed edges. */
function expandRanges(s){const ids=[];for(const part of s.split(',')){
  const [a,b=a]=part.split('-').map(Number);
  if(!Number.isInteger(a)||!Number.isInteger(b)||b<a)throw Error('Invalid grey evidence range');
  for(let n=a;n<=b;n++)ids.push(n);
}return ids;}
function nearestTangent(pts,c){let best=Infinity,tx=1,ty=0;
  for(let i=1;i<pts.length;i++){
    const a=pts[i-1],b=pts[i],dx=b[0]-a[0],dy=b[1]-a[1],m=dx*dx+dy*dy;if(m<1e-9)continue;
    const t=Math.max(0,Math.min(1,((c[0]-a[0])*dx+(c[1]-a[1])*dy)/m));
    const d=(a[0]+t*dx-c[0])**2+(a[1]+t*dy-c[1])**2;
    if(d<best){best=d;tx=dx/Math.sqrt(m);ty=dy/Math.sqrt(m);}
  }return [tx,ty];}
export function applyGreyRoadWidthStyle(graph,style){
  if(graph?.version!=='roadcraft-v33'||graph.paintLayer?.schema!==style?.requiresYellowStyleSchema||
    style.schema!=='spaciel.roads.grey-width-style.v1'||style.sourceVersion!==graph.version||
    JSON.stringify(style.frame)!==JSON.stringify(graph.frame))throw Error('Mismatched V33 grey style');
  const bands=style.widthBandsAtlasPx,review=new Set(style.greyReviewIds);
  const idsEvidence=expandRanges(style.dualAtlasEvidenceIdsRle),supported=new Set(idsEvidence);
  if(review.size!==style.greyReviewIds.length||supported.size!==idsEvidence.length)throw Error('Duplicate evidence IDs');
  const ids=new Set(graph.paths.map(p=>p.id));
  if([...review,...supported].some(id=>!ids.has(id)))throw Error('Unknown road id');
  const counts={narrow:0,regular:0,wide:0,greyReview:0,dual:0,provisional:0,yellow:0,yellowReview:0,changed:0};
  const paths=graph.paths.map(p=>{
    if(p.isYellowRoad){counts.yellow++;return {...p,widthClass:'yellow',greyEvidenceStatus:'yellow_confirmed'};}
    if(p.paintStatus!=='grey'){counts.yellowReview++;return {...p,widthClass:'review',greyEvidenceStatus:'unresolved'};}
    const w=p.width;let band=null;
    if(!review.has(p.id)){
      if(w>=7.4&&w<=10.4)band='narrow';
      else if(w>10.4&&w<=14.0)band='regular';
      else if(w>14.0&&w<=19.3)band='wide';
    }
    if(!band){counts.greyReview++;return {...p,widthClass:'review',greyEvidenceStatus:'unresolved'};}
    counts[band]++;if(supported.has(p.id))counts.dual++;else counts.provisional++;
    const width=bands[band];if(!Number.isFinite(width)||width<=0)throw Error('Invalid standard width');
    if(Math.abs(p.width-width)>.01)counts.changed++;
    const road={...p,width,widthClass:band,originalV33WidthPx:p.originalWidthPx,
      greyEvidenceStatus:supported.has(p.id)?'dual_atlas':'nominal_provisional',
      roadClass:band==='wide'?'medium':'local'};
    if(p.edgeSamples?.length)road.edgeSamples=p.edgeSamples.map(s=>{
      if(s.e==='o'||!Array.isArray(s.c))return s;
      const [tx,ty]=nearestTangent(p.points,s.c),nx=-ty,ny=tx,r=x=>Math.round(x*100)/100;
      return {...s,l:[r(s.c[0]+nx*width/2),r(s.c[1]+ny*width/2)],
        r:[r(s.c[0]-nx*width/2),r(s.c[1]-ny*width/2)]};
    });return road;
  });
  for(const [key,n] of Object.entries({yellow:style.counts.yellowLocked,
    yellowReview:style.counts.yellowReviewHeld,narrow:style.counts.greyNarrow,
    regular:style.counts.greyRegular,wide:style.counts.greyWide,
    greyReview:style.counts.greyHeldForReview,dual:style.counts.greyDualAtlasSupported,
    provisional:style.counts.greyNominalProvisional,changed:style.counts.greyWidthsChanged})){
    if(counts[key]!==n)throw Error('V33 grey width count drift: '+key+' '+counts[key]+'!='+n);
  }
  return {...graph,greyWidthLayer:{schema:style.schema,widthBandsAtlasPx:bands,
    narrowPaths:counts.narrow,regularPaths:counts.regular,widePaths:counts.wide,
    reviewPaths:counts.greyReview,observedEvidencePaths:counts.dual,provisionalPaths:counts.provisional},paths};
}
