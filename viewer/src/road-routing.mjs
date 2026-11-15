/** Spaciel road topology and snapping; all distances are ATLAS PIXELS, not metres.
 * Crossings are connected only where a graph node is shared.
 * Road-width geometry never creates routable links by visual overlap.
 */
const hypot = (a,b) => Math.hypot(a[0]-b[0],a[1]-b[1]);
const between = (a,b,t) => [a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])];

export function validateRoadcraftV33(graph, expected={}) {
  if(graph?.schema!=='spaciel.roads.runtime.v1'||graph.version!=='roadcraft-v33'||
     JSON.stringify(graph.frame)!=='[5175,7966]'||!graph.nodes||!Array.isArray(graph.paths))
    throw new Error('Unexpected V33 road graph or coordinate frame');
  const nodes=graph.nodes, keys=Object.keys(nodes), indices=new Set();
  if(expected.nodes&&keys.length!==expected.nodes) throw new Error('Incorrect V33 node count');
  if(expected.paths&&graph.paths.length!==expected.paths) throw new Error('Incorrect V33 path count');
  if(keys.some(k=>!Array.isArray(nodes[k])||nodes[k].length!==2||!nodes[k].every(Number.isFinite))) throw new Error('Invalid node position');
  for(const p of graph.paths){
    if(indices.has(p.id)||!Number.isInteger(p.id)) throw new Error('Nonunique route id');indices.add(p.id);
    if(!nodes[String(p.from)]||!nodes[String(p.to)]||!Array.isArray(p.points)||p.points.length<2)
      throw new Error('Road endpoints or polyline missing');
    if(!['local','medium','arterial'].includes(p.roadClass)||!(p.width>0)) throw new Error('Invalid road class or width');
    if(p.points.some(x=>!Array.isArray(x)||x.length!==2||!x.every(Number.isFinite))) throw new Error('Invalid road vertex');
    if(hypot(p.points[0],nodes[String(p.from)])>.12||hypot(p.points.at(-1),nodes[String(p.to)])>.12) throw new Error('Polyline does not touch graph node');
    if(!Array.isArray(p.edgeSamples)||p.edgeSamples.some(s=>!['o','m'].includes(s.e))) throw new Error('Edge evidence missing');
  }
  return graph;
}
function pathMeasures(points){const d=[0];for(let i=1;i<points.length;i++)d.push(d[i-1]+hypot(points[i],points[i-1]));return d;}
function pointAt(pts,d,s){
  if(s<=0)return pts[0].slice();if(s>=d.at(-1))return pts.at(-1).slice();
  let lo=0,hi=d.length-1;while(hi-lo>1){let m=(lo+hi)>>1;if(d[m]<=s)lo=m;else hi=m;}
  return between(pts[lo],pts[lo+1],(s-d[lo])/(d[lo+1]-d[lo]||1));
}
function subsection(path,d,a,b){
  if(a>b)return subsection(path,d,b,a).reverse();
  const pts=[pointAt(path,d,a)];
  for(let i=1;i<d.length-1;i++)if(d[i]>a+1e-7&&d[i]<b-1e-7)pts.push(path[i]);
  const q=pointAt(path,d,b);if(hypot(pts.at(-1),q)>1e-6)pts.push(q);
  return pts;
}
function addPoints(out,coords){for(const p of coords)if(!out.length||hypot(out.at(-1),p)>1e-5)out.push(p);}
class Heap{
  a=[];
  push(v){let i=this.a.length;this.a.push(v);while(i>0){let j=(i-1)>>1;if(this.a[j].cost<=v.cost)break;this.a[i]=this.a[j];i=j;}this.a[i]=v;}
  pop(){const a=this.a,ans=a[0],tail=a.pop();if(a.length){let i=0;while(2*i+1<a.length){let c=2*i+1,r=c+1;if(r<a.length&&a[r].cost<a[c].cost)c=r;if(tail.cost<=a[c].cost)break;a[i]=a[c];i=c;}a[i]=tail;}return ans;}
  get size(){return this.a.length}
}
export function createRoadRouter(graph){
  validateRoadcraftV33(graph);
  const measures=graph.paths.map(p=>pathMeasures(p.points));
  const lengths=measures.map(d=>d.at(-1));
  const adjacency=new Map(Object.keys(graph.nodes).map(k=>[k,[]]));
  graph.paths.forEach((p,i)=>{
    const a=String(p.from),b=String(p.to),length=lengths[i];
    adjacency.get(a).push({to:b,index:i,cost:length,forward:true});
    adjacency.get(b).push({to:a,index:i,cost:length,forward:false});
  });
  function snap(at,{maxDistancePx=Infinity,roadClasses=null}={}){
    const [x,y]=at;let best=null,limit=maxDistancePx**2;
    for(let i=0;i<graph.paths.length;i++){
      const path=graph.paths[i];if(roadClasses&&!roadClasses.includes(path.roadClass))continue;
      const pts=path.points,d=measures[i];
      for(let j=1;j<pts.length;j++){
        const a=pts[j-1],b=pts[j],dx=b[0]-a[0],dy=b[1]-a[1],lensq=dx*dx+dy*dy;
        if(!lensq)continue;
        const t=Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/lensq));
        const q=[a[0]+dx*t,a[1]+dy*t],err=(x-q[0])**2+(y-q[1])**2;
        if(err<limit){limit=err;best={position:q,distancePx:Math.sqrt(err),pathId:path.id,pathIndex:i,alongPx:d[j-1]+t*Math.sqrt(lensq),roadClass:path.roadClass,widthPx:path.width};}
      }
    }
    return best;
  }
  function route(from,to,options={}){
    const A=Array.isArray(from)?snap(from,options):from,B=Array.isArray(to)?snap(to,options):to;
    if(!A||!B)return null;
    const ia=A.pathIndex,ib=B.pathIndex,pa=graph.paths[ia],pb=graph.paths[ib],La=lengths[ia],Lb=lengths[ib];
    let best=null;
    if(ia===ib){best={distancePx:Math.abs(A.alongPx-B.alongPx),points:subsection(pa.points,measures[ia],A.alongPx,B.alongPx),pathIds:[pa.id]};}
    const dist=new Map(),parent=new Map(),heap=new Heap();
    for(const [key,cost] of [[String(pa.from),A.alongPx],[String(pa.to),La-A.alongPx]]){
      if(cost<(dist.get(key)??Infinity)){dist.set(key,cost);parent.set(key,null);heap.push({key,cost});}
    }
    const targets=[[String(pb.from),B.alongPx],[String(pb.to),Lb-B.alongPx]];
    while(heap.size){
      const cur=heap.pop();if(cur.cost>dist.get(cur.key)+1e-7)continue;
      if(best&&cur.cost>best.distancePx)break;
      for(const e of adjacency.get(cur.key)){
        const nc=cur.cost+e.cost;
        if(nc<(dist.get(e.to)??Infinity)-1e-7){dist.set(e.to,nc);parent.set(e.to,{from:cur.key,edge:e});heap.push({key:e.to,cost:nc});}
      }
    }
    for(const [target,terminalCost] of targets){
      const cost=(dist.get(target)??Infinity)+terminalCost;
      if(best&&cost>=best.distancePx-1e-7)continue;
      if(!Number.isFinite(cost))continue;
      const seq=[];let k=target;
      while(parent.get(k)){
        const step=parent.get(k);seq.push(step);k=step.from;
      }
      seq.reverse();let startNode=k,endNode=target;
      const points=[];
      addPoints(points,subsection(pa.points,measures[ia],A.alongPx,startNode===String(pa.from)?0:La));
      for(const step of seq){
        const p=graph.paths[step.edge.index];addPoints(points,step.edge.forward?p.points:p.points.slice().reverse());
      }
      addPoints(points,subsection(pb.points,measures[ib],endNode===String(pb.from)?0:Lb,B.alongPx));
      best={distancePx:cost,points,pathIds:[pa.id,...seq.map(s=>graph.paths[s.edge.index].id),pb.id]};
    }
    return best?{...best,start:A,end:B,units:'atlas-px'}:null;
  }
  return {graph,snap,route,adjacency,paths:graph.paths,counts:{nodes:Object.keys(graph.nodes).length,paths:graph.paths.length}};
}
