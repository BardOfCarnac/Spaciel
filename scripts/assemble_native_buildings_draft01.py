#!/usr/bin/env python3
"""Non-destructive trial: preserve native-source building proportions and site character.

Public repository stores summary and generative code, not original SKP source-derived polygons.
"""
from __future__ import annotations
from pathlib import Path
import csv, json, math, time, zipfile, random, itertools, bisect, collections, base64
import numpy as np
import cv2
from shapely.geometry import shape, mapping, LineString, box, Polygon
from shapely.ops import unary_union
from shapely.affinity import rotate, translate
from shapely.strtree import STRtree
from PIL import Image, ImageDraw, ImageFont

HOME=Path('/mnt/data'); SRC=HOME/'files'; OUT=HOME/'spaciel_assembly'; OUT.mkdir(exist_ok=True)
TM=time.time();RNG=random.Random(2045)

def loadgeo(path): return json.loads(Path(path).read_text())['features']
slots=loadgeo(SRC/'Night_City_V10_Completed_Footprints.geojson')
T=[shape(f['geometry']) for f in slots];TP=[f['properties'] for f in slots]
roadfeat=loadgeo(SRC/'night_city_2045_cleaned_display_lines.geojson')
roads=[shape(f['geometry']) for f in roadfeat]
roadtree=STRtree(roads)
slotree=STRtree(T)
zipf=zipfile.ZipFile(HOME/'Spaciel_Private_Original_SKP_Placement_Review.zip')
origfeatures=json.loads(zipf.read('native_original_buildings_atlas_hulls.geojson'))['features']
SRC_POLY=[shape(f['geometry']) for f in origfeatures]
SRC_PROPS=[f['properties'] for f in origfeatures]
source_id_to_idx={p['instance_id']:i for i,p in enumerate(SRC_PROPS)}
shortlist=set()
with zipf.open('source_building_position_review.csv') as f:
    prior={r['instance_id']:r for r in csv.DictReader((x.decode() for x in f))}
for inst,r in prior.items():
    if float(r['fraction_of_source_inside_best_target'])>=.5 and int(r['road_centerline_crossings'])==0 and float(r['nearest_road_centerline_px'])>=5:
       shortlist.add(inst)
# More specific earlier 137 candidates if available from Github cached? use current private stats in file system.

# Atlas working envelopes: tiny gaps closed, roads remain separate.
# Geometry union is only used to determine overall placement coverage, NOT a new official district boundary.
print('Creating approved plot unions...',flush=True)
union_envelope=unary_union([p.buffer(1.7) for p in T]).buffer(-1.7)
# Need road safety buffer based on centreline (not definitive road width)
roadbuffer=unary_union(roads).buffer(2.6)
print('Inputs',len(T),'sites',len(SRC_POLY),'original instances',len(roads),'road chains',round(time.time()-TM,1),'sec',flush=True)

# spatial-grid for dynamic accepted building collision queries
CELL=65.0
placed=[];placed_poly=[];spgrid=collections.defaultdict(list)
def cells(bounds):
 a,b,c,d=bounds
 for i in range(int(math.floor(a/CELL)),int(math.floor(c/CELL))+1):
  for j in range(int(math.floor(b/CELL)),int(math.floor(d/CELL))+1):
   yield (i,j)
def colliders(poly):
 cand=set()
 for k in cells(poly.bounds): cand.update(spgrid.get(k,()))
 return cand

def near_roads(poly,clearance=2.6):
 # Zero means actual centreline intersection. Otherwise conservative approximate setback buffer.
 g=poly.buffer(clearance)
 for idx in roadtree.query(g):
  if g.intersects(roads[int(idx)]): return True
 return False

def can_place(poly,clearance=2.6,overlap_frac=0.025):
 if poly.is_empty or poly.area<5 or not poly.is_valid: return False
 if near_roads(poly,clearance): return False
 for idx in colliders(poly):
  p=placed_poly[idx]
  if not p.bounds[2]>=poly.bounds[0] or p.bounds[0]>poly.bounds[2]:continue
  if not p.bounds[3]>=poly.bounds[1] or p.bounds[1]>poly.bounds[3]:continue
  if not p.intersects(poly):continue
  if p.intersection(poly).area/min(poly.area,p.area)>overlap_frac:return False
 return True

def add(poly,source_index,placement_type,site_idx=None,dx=0,dy=0,rot=0,source_coverage=None):
 prop=SRC_PROPS[source_index]
 st=TP[site_idx] if site_idx is not None else {}
 record={'placement_id':f'build-{len(placed)+1}',
         'source_instance_id':prop['instance_id'], 'source_native_id':prop['source_native_id'],
         'source_skp_name':prop.get('source_skp_name',''), 'source_guid':prop.get('source_skp_guid',''),
         'placement_type':placement_type,'target_site_id':st.get('id',''),
         'target_origin':st.get('origin',''), 'style':st.get('style') or 'retained-context',
         'character_area':st.get('character_area') or '',
         'native_width_m':round(prop['width_m'],2),'native_depth_m':round(prop['depth_m'],2),
         'native_height_m':round(prop['height_m'],2),
         'source_triangles':prop.get('source_triangles',0),
         'atlas_cx':round(poly.centroid.x,3),'atlas_cy':round(poly.centroid.y,3),
         'translated_x_atlas_px':round(dx,3),'translated_y_atlas_px':round(dy,3),'rotation_deg':round(rot,3),
         'projected_footprint_area_atlas_px2':round(poly.area,2),
         'source_fraction_in_approved_envelope':round(source_coverage,3) if source_coverage is not None else '',
         'source_geometry_preserved':True,'placement_approved':False,'review_status':'AUTOMATIC_TRIAL',
         }
 placed.append(record);placed_poly.append(poly)
 ix=len(placed)-1
 for k in cells(poly.bounds):spgrid[k].append(ix)
 return record

# 1: retain viable original locations, preferring the best overlap with planned sites and the cleanest geometry.
print('Selecting original placements...',flush=True)
originals=[]
for i,poly in enumerate(SRC_POLY):
 if poly.area<=6 or not poly.is_valid: continue
 if near_roads(poly,2.6): continue
 covered=poly.intersection(union_envelope).area/poly.area
 if covered<0.72: continue
 nearby=slotree.query(poly)
 choices=[]
 for idx in nearby:
  j=int(idx);inter=poly.intersection(T[j]).area
  if inter>0:
   choices.append((inter/poly.area, j, inter/T[j].area))
 if not choices:continue
 choices.sort(reverse=True)
 fit,j,targfrac=choices[0]
 # Retain original position even when it covers only part of a large V10 building area.
 score=covered*2+min(1,fit)+.15*min(1,targfrac/.3)+min(1,poly.area/500)*.1
 if SRC_PROPS[i]['instance_id'] in shortlist:score+=.35
 originals.append((score,i,j,covered,fit))
originals.sort(reverse=True)
for score,i,j,covered,fit in originals:
 poly=SRC_POLY[i]
 if can_place(poly,clearance=2.6,overlap_frac=.015): add(poly,i,'ORIGINAL_POSITION',j,source_coverage=covered)
print('Original locations kept',len(placed),'from',len(originals),'viable candidates',round(time.time()-TM,1),'s',flush=True)

# Faster whole-city infill screen with atlas-pixel raster occupancy and road masks.
# The exact original-source polygons are saved, not rasterised, in the output manifest.
print('Rasterising road and accepted-source exclusions...',flush=True)
WAT,HAT=5175,7966
occupied=np.zeros((HAT,WAT),np.uint8)
roadmask=np.zeros_like(occupied)
for road in roads:
    for line in ([road] if road.geom_type=='LineString' else list(road.geoms)):
        a=np.rint(np.asarray(line.coords)).astype(np.int32)
        cv2.polylines(roadmask,[a],False,255,2)
roadmask=cv2.dilate(roadmask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))

def shape_roi(points):
    """Raster polygon in tightly clipped ROI, also return bounding origin."""
    pp=np.rint(points).astype(np.int32)
    x0=max(0,int(pp[:,0].min())-1);y0=max(0,int(pp[:,1].min())-1)
    x1=min(WAT,int(pp[:,0].max())+2);y1=min(HAT,int(pp[:,1].max())+2)
    if x0>=x1 or y0>=y1: return None
    out=np.zeros((y1-y0,x1-x0),np.uint8)
    cv2.fillPoly(out,[pp-np.array([x0,y0],np.int32)],255)
    return (x0,y0,x1,y1,out)

for poly in placed_poly:
    xx=shape_roi(np.asarray(poly.exterior.coords));
    if xx:
       x0,y0,x1,y1,mask=xx
       occupied[y0:y1,x0:x1][mask>0]=255

source_areas=np.array([p.area for p in SRC_POLY]);source_heights=np.array([p['height_m'] for p in SRC_PROPS])
valid_source=[i for i,p in enumerate(SRC_POLY) if p.is_valid and 10<=p.area<6000]
valid_source.sort(key=lambda i:source_areas[i]);sorted_areas=[source_areas[i] for i in valid_source]
use_count=collections.Counter(p['source_native_id'] for p in placed)
styles={
 'corporate':(38,125), 'urban':(14,50),'mixed':(12,45),
 'combat':(8,35),'commercial':(7,37),'heritage':(6,25),
 'suburb':(4,15),'military':(6,25),'affluent':(9,43),
 'university':(8,36),'exec':(6,30),'amusement':(5,25),
 'port':(7,35),'hotzone':(8,55),'industrial':(8,45),
}
# Keep each model's source size, shift its source centroid to the target and optionally rotate.
cache={}
def proto(i):
    if i in cache:return cache[i]
    p=SRC_POLY[i];cx,cy=p.centroid.coords[0]
    arr=np.array(p.exterior.coords[:-1],np.float64)
    rel=arr-np.array([cx,cy]);
    # Dominant direction from longest source edge
    edges=np.diff(np.vstack([arr,arr[0]]),axis=0);v=max(edges,key=lambda v:v@v)
    alpha=math.atan2(v[1],v[0])
    cache[i]=(rel,alpha)
    return cache[i]

def angle_for_site(p):
    # Dominant direction of longest edge approximates frontage/plot axis
    a=np.asarray(p.exterior.coords)
    e=np.diff(a,axis=0);v=max(e,key=lambda z: z@z)
    return math.atan2(v[1],v[0])

counts=collections.Counter();reasons=collections.Counter();trials=0
order=list(range(len(T)));order.sort(key=lambda i:(TP[i].get('origin')!='retained-original',-T[i].area))
for n,ti in enumerate(order):
    target=T[ti];tarea=target.area
    if tarea<22: reasons['target too small']+=1;continue
    txy=np.asarray(target.exterior.coords)
    target_roi=shape_roi(txy)
    if target_roi is None: reasons['off map']+=1;continue
    tx0,ty0,tx1,ty1,tm=target_roi
    area_pixels=np.count_nonzero(tm)
    if area_pixels==0: reasons['raster too small']+=1;continue
    existing=int(np.count_nonzero((occupied[ty0:ty1,tx0:tx1]>0)&(tm>0)))
    if existing/area_pixels>0.42:
        counts['already substantially occupied']+=1
        continue
    style=TP[ti].get('style') or 'urban'
    hmin,hmax=styles.get(style,(6,45))
    desired=min(tarea*.72,900.0)
    if tarea>1000:desired=min(tarea*.36,850.0)
    lo=max(10,desired*.30);hi=min(tarea*.99,desired*1.8)
    left=bisect.bisect_left(sorted_areas,lo);right=bisect.bisect_right(sorted_areas,hi)
    if left>=right:reasons['no native model in size range']+=1;continue
    pool=valid_source[left:right]
    if len(pool)>45: pool=RNG.sample(pool,45)
    def priority(k):
       ht=source_heights[k]
       hp=0 if hmin<=ht<=hmax else min(abs(ht-hmin),abs(ht-hmax))/max(15,hmax-hmin)
       ap=abs(math.log(max(1,source_areas[k])/desired))
       return hp*.9+ap*.8+.045*use_count[SRC_PROPS[k]['source_native_id']]+RNG.random()*.16
    pool.sort(key=priority)
    cx,cy=target.centroid.coords[0];ta=angle_for_site(target)
    found=False
    for k in pool[:8]:
       rel,a=proto(k)
       ang=(ta-a+math.pi/2)%math.pi-math.pi/2
       cosa,sina=math.cos(ang),math.sin(ang)
       pts=rel@np.array([[cosa,sina],[-sina,cosa]])+np.array([cx,cy])
       xx=shape_roi(pts)
       if xx is None:continue
       x0,y0,x1,y1,mask=xx
       npx=np.count_nonzero(mask)
       if npx<8:continue
       trials+=1
       # Require most source hull inside its target footprint for this conservative pass
       # Reuse full target mask even if it only partly covers the candidate rectangle.
       sx0=max(x0,tx0);sy0=max(y0,ty0);sx1=min(x1,tx1);sy1=min(y1,ty1)
       if sx0>=sx1 or sy0>=sy1: continue
       sub=mask[sy0-y0:sy1-y0,sx0-x0:sx1-x0]
       target_inside=tm[sy0-ty0:sy1-ty0,sx0-tx0:sx1-tx0]
       covered=np.count_nonzero((sub>0)&(target_inside>0))
       if covered/npx<.83:continue
       if np.any((mask>0)&(roadmask[y0:y1,x0:x1]>0)):continue
       conflicts=np.count_nonzero((mask>0)&(occupied[y0:y1,x0:x1]>0))
       if conflicts/npx>.015:continue
       # source polygon translated/rotated only, never scaled
       source_center=SRC_POLY[k].centroid
       dx=cx-source_center.x;dy=cy-source_center.y
       final=Polygon(pts)
       if not final.is_valid or final.area<5:continue
       add(final,k,'RELOCATED_NATIVE_UNSCALED',ti,dx,dy,math.degrees(ang))
       occupied[y0:y1,x0:x1][mask>0]=255
       use_count[SRC_PROPS[k]['source_native_id']]+=1
       counts['new fill']+=1;found=True;break
    if not found:reasons['no safe source fit']+=1
    if (n+1)%2000==0:print('Processed',n+1,'targets, placed',len(placed),'trial count',trials,'elapsed',round(time.time()-TM,1),'s',flush=True)
print('Placed total',len(placed),'new fill',counts['new fill'],'unsatisfied',dict(reasons),'trials',trials,round(time.time()-TM,1),'s',flush=True)
# Raster filters already exclude road buffer and collisions. Keep final count for reporting.
validatoroad=0;badpairs=set();chosen_sites=counts;failreason=reasons
# Independent exact-coordinate audit: the 1-pixel raster can admit tiny subpixel overlaps.
# Prefer the exact original-source position when a later infill hull clips it.
exact_tree=STRtree(placed_poly)
drop=set();minor_conflicts=[]
for i,p in enumerate(placed_poly):
 if i in drop:continue
 for j0 in exact_tree.query(p):
  j=int(j0)
  if j<=i or j in drop:continue
  q=placed_poly[j]
  if not p.intersects(q):continue
  frac=p.intersection(q).area/min(p.area,q.area)
  if frac>.013:
   keep_i=placed[i]['placement_type']=='ORIGINAL_POSITION'
   keep_j=placed[j]['placement_type']=='ORIGINAL_POSITION'
   rejected = j if keep_i or not keep_j else i
   drop.add(rejected)
   minor_conflicts.append([i,j,round(frac,4),rejected])
   if rejected==i:break
if drop:
 chosen_sites['new fill']-=sum(placed[i]['placement_type']=='RELOCATED_NATIVE_UNSCALED' for i in drop)
 placed=[p for i,p in enumerate(placed) if i not in drop]
 placed_poly=[p for i,p in enumerate(placed_poly) if i not in drop]
 failreason['removed by exact-coordinate overlap QA']=len(drop)
print('Final exact-coordinate collision cleanup',minor_conflicts,'remaining',len(placed),flush=True)

# Save full private manifest with exact source-derived hull geometry for review.
result={'type':'FeatureCollection', 'name':'Spaciel_native_scale_assembly_draft_01',
        'metadata':{'status':'AUTOMATIC_TRIAL_UNAPPROVED','road_buffer_atlas_px':2.6,'no_scale_change':True,'retains_v10_target_footprints':True,
          'source':'Original SKP direct instance and building definition; target site V10; V17 cleaned roads',
          'geometry_note':'Convex-hull plan projections derived from original models. Not exact building solid faces.'},
        'features':[{'type':'Feature','properties':p,'geometry':mapping(g)} for p,g in zip(placed,placed_poly)]}
(OUT/'Spaciel_Native_Building_Placement_Draft01_PRIVATE.geojson').write_text(json.dumps(result,separators=(',',':')))
with (OUT/'Spaciel_Native_Building_Placement_Draft01_PRIVATE.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(placed[0]));w.writeheader();w.writerows(placed)
# Counts by style and type, not exact source geometry for public project tracking
by_style={x:dict(collections.Counter(p['placement_type'] for p in placed if p['style']==x)) for x in sorted(set(p['style'] for p in placed))}
ids={p['target_site_id'] for p in placed if p['target_site_id']}
summary={'name':'Spaciel native-scale building placement draft 01',
 'status':'UNAPPROVED WORKING PLACEMENTS; NO LIVE CITY ALTERED',
 'approved_target_footprints':len(T),'skp_source_instance_envelopes':len(SRC_POLY),
 'placed_total':len(placed),'original_positions_retained':sum(p['placement_type']=='ORIGINAL_POSITION' for p in placed),
 'native_reuse_unsized_translations':sum(p['placement_type']=='RELOCATED_NATIVE_UNSCALED' for p in placed),
 'unique_approved_target_slots_served':len(ids),
 'unused_approved_target_slots':len(T)-len(ids),
 'unique_source_definition_ids':len({p['source_native_id'] for p in placed}),
 'skp_instances_used':len({p['source_instance_id'] for p in placed}),
 'road_centerline_buffer_px':2.6,'road_buffer_intersections':validatoroad,'significant_placed_poly_overlaps':len(badpairs),
 'infill_attempted_target_slots':len(T),'candidate_tests':trials,
 'target_site_coverage_notes':dict(chosen_sites),'unfilled_reason_counts':dict(failreason),
 'by_character_style':by_style,
 'limits':['No building faces/meshes merged into 3D viewer yet; placements are a source-ID + geometric-hull manifest.',
           'No district-by-district visual artistic review; model dimensions preserved, height selected by style heuristic.',
           'Road checks use 2.6 atlas-pixel centreline safety margin, not surveyed road surface width.',
           'Water/coast and individual foundations not separately validated beyond requiring target envelope coverage.',
           'Convex-hull proxies can overestimate concave building outlines.',
           'Native source model assignments are proposed; confirm landmarks and fit before publishing.']}
(OUT/'Spaciel_Native_Building_Placement_Draft01_Report.json').write_text(json.dumps(summary,indent=2))

# Render legible deterministic overlay, not generated artwork.
W,H=1650,2548
scaleX=W/5175;scaleY=H/7966
frame=np.full((H,W,3),(14,20,30),np.uint8)
# original working block mask as subtle neutral
bm=np.array(Image.open(HOME/'Spaciel_Building_Blocks_Only.png').convert('RGB'))
bm=cv2.resize(bm,(W,H),interpolation=cv2.INTER_AREA)
mask=(bm[:,:,0]>70)
frame[mask]=(45,55,65)
# drawn placement hulls in non-overlapping contrasting colors
for rec,poly in zip(placed,placed_poly):
 if poly.geom_type!='Polygon':continue
 xy=np.round(np.array(poly.exterior.coords)*[scaleX,scaleY]).astype(np.int32)
 color=(112,196,161) if rec['placement_type']=='ORIGINAL_POSITION' else (216,172,91)
 cv2.fillPoly(frame,[xy],color)
for r in roads:
 for l in ([r] if r.geom_type=='LineString' else list(r.geoms)):
  a=np.round(np.array(l.coords)*[scaleX,scaleY]).astype(np.int32)
  cv2.polylines(frame,[a],False,(61,67,76),1,cv2.LINE_AA)
img=Image.fromarray(frame)
fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F=ImageFont.truetype(fontfile,23);Sf=ImageFont.truetype(fontfile,17)
canvas=Image.new('RGB',(W+64,H+170),(14,20,30));canvas.paste(img,(32,104))
d=ImageDraw.Draw(canvas)
d.text((32,24),'SPACIEL  /  NATIVE BUILDING ASSEMBLY  —  DRAFT 01',font=F,fill=(244,232,209))
d.text((32,67),'Green: original position  ·  Gold: native-scale reuse  ·  Grey: empty planned areas',font=Sf,fill=(188,200,210))
d.text((32,H+121),f'{len(placed):,} provisional placements  ·  Source geometry never stretched  ·  Road-centreline check',font=Sf,fill=(188,200,210))
canvas.save(HOME/'Spaciel_Native_Building_Assembly_Draft01_Preview.png',optimize=True)

# Self-contained private interactive HTML using canvas for pan/zoom and model selection, no source-mesh public release.
# Embed smaller overview as backdrop and detailed transformed 2D hulls as private geometry.
thumb=Image.open(HOME/'Spaciel_Building_Blocks_Only.png').convert('RGB')
thumb.thumbnail((1100,1800))
from io import BytesIO
bio=BytesIO();thumb.save(bio,format='PNG',optimize=True)
bg64=base64.b64encode(bio.getvalue()).decode('ascii')
# Main review layer points abbreviated for load, but full polygons retained (screen uses exact native outline)
geo=[]
for rec,poly in zip(placed,placed_poly):
 c=np.array(poly.exterior.coords)
 geo.append({'p':np.round(c,1).tolist(),'t':0 if rec['placement_type']=='ORIGINAL_POSITION' else 1,
             'id':rec['placement_id'],'src':rec['source_native_id'],'inst':rec['source_instance_id'],'site':rec['target_site_id'],
             'style':rec['style'],'height':rec['native_height_m'],'wd':[rec['native_width_m'],rec['native_depth_m']],
             'dx':rec['translated_x_atlas_px'],'dy':rec['translated_y_atlas_px'],'angle':rec['rotation_deg']})
# visually preserve districts by style filter, type; editable interaction to mark manual decisions
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spaciel — Original SketchUp Assembly Draft 01</title><style>
:root{color-scheme:dark;font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:#0e141e;color:#e7ebee}
*{box-sizing:border-box}body{margin:0}header{display:flex;align-items:center;justify-content:space-between;padding:12px 17px;border-bottom:1px solid #354252;gap:12px;flex-wrap:wrap}
h1{font-size:17px;letter-spacing:.08em;margin:0}.sub{color:#aab7c5;font-size:12px}.shell{display:grid;grid-template-columns:minmax(0,1fr) 315px;height:calc(100dvh - 65px);min-height:530px}
.panel{background:#101925;border-left:1px solid #354252;overflow:auto;padding:17px}main{position:relative;overflow:hidden;background:#0c131e;touch-action:none}canvas{width:100%;height:100%;display:block;touch-action:none}
button,select,input{background:#1c2938;border:1px solid #516073;color:#edf3f7;border-radius:7px;padding:8px 10px;font:inherit;font-size:13px}button{cursor:pointer}button:hover{background:#334357}select{width:100%}
.ctrl{position:absolute;left:12px;top:12px;display:flex;gap:6px;z-index:2}.stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0}.stat{padding:11px;background:#1e2a38;border-radius:7px;font-size:11px;color:#b7c5d2}.stat b{display:block;font-size:24px;color:#f2f5f7}
.row{display:flex;gap:8px;align-items:center;margin:12px 0;font-size:13px}label{cursor:pointer}.light{color:#9eafc0}.val{font-weight:700;color:#e4f0f3}.legend{margin:8px 0 15px;font-size:12px;color:#b5c5d0;line-height:1.9}.dot{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px}
#detail{font-size:13px;line-height:1.7;overflow-wrap:anywhere}#detail strong{color:#c9eee1}.action{display:flex;flex-wrap:wrap;gap:5px;margin:10px 0}#message{font-size:12px;color:#9db1c4}
@media(max-width:740px){.shell{grid-template-columns:1fr;grid-template-rows:minmax(330px,60dvh) auto;height:auto}.panel{border-left:0;border-top:1px solid #354252}header{padding:10px}h1{font-size:14px}.ctrl button{padding:7px}}
</style></head><body><header><div><h1>SPACIEL / NATIVE-SCALE BUILDING ASSEMBLY</h1><div class="sub">Draft 01 — original SketchUp proportions and target site character. Nothing approved or deployed.</div></div><div class="sub">Independent 2D review · not the live 3D viewer</div></header>
<div class="shell"><main id="map"><canvas id="c"></canvas><div class="ctrl"><button id="zin" title="Zoom in">+</button><button id="zout" title="Zoom out">−</button><button id="reset">Overview</button></div></main><aside class="panel">
<div class="stats"><div class="stat">Original positions<b id="n0">—</b></div><div class="stat">Reused, no scaling<b id="n1">—</b></div><div class="stat">Visible on map<b id="nShown">—</b></div><div class="stat">Total provisional<b id="nall">—</b></div></div>
<div class="legend"><span class="dot" style="background:#70c4a1"></span>Original SKP position<br><span class="dot" style="background:#d8ac5b"></span>Native-scale reused building<br><span class="dot" style="background:#2d3741"></span>Remaining target placement area</div>
<div class="row"><label><input type="checkbox" id="show0" checked> Original positions</label><label><input type="checkbox" id="show1" checked> Reuse/infill</label></div>
<div class="row"><label><input type="checkbox" id="showBack" checked> Building blocks</label><label><input type="checkbox" id="showRoads"> Roads</label></div>
<div style="font-size:12px;color:#99a9bb;margin:14px 0 5px">District character / style</div><select id="style"><option value="all">All styles</option></select>
<div style="font-size:12px;color:#99a9bb;margin:14px 0 5px">Jump to source model or target ID</div><input id="find" placeholder="e.g. original-1 / source ID" style="width:100%">
<div id="detail"><p class="light">Tap or click a building to inspect its original source ID, dimensions and placement.</p></div>
<div class="action"><button data-choice="keep">Mark keep</button><button data-choice="move">Mark adjust</button><button data-choice="reject">Mark reject</button><button id="export">Export review decisions</button></div>
<div id="message">Local review labels; export before closing. This trial has not changed the city geometry.</div>
</aside></div>
<script>const DATA=__GEO__;const B64='__BG__';const c=document.getElementById('c'),ct=c.getContext('2d');const map=document.getElementById('map');let W=0,H=0,scale=0,offX=0,offY=0,selected=-1,drag=null,moved=false,showBack=true,showRoads=false;const states={},styles=[...new Set(DATA.map(x=>x.style))].sort();const styl=document.getElementById('style');for(const s of styles){const o=document.createElement('option');o.value=s;o.textContent=s;styl.appendChild(o)}
const bg=new Image();bg.src='data:image/png;base64,'+B64;bg.onload=()=>draw();
function resize(){const r=map.getBoundingClientRect();W=r.width;H=r.height;const dpr=window.devicePixelRatio||1;c.width=Math.round(W*dpr);c.height=Math.round(H*dpr);ct.setTransform(dpr,0,0,dpr,0,0);if(!scale)fit();draw()}
function fit(){scale=Math.min((W-30)/5175,(H-30)/7966);offX=(W-5175*scale)/2;offY=(H-7966*scale)/2}
function filt(x){return (x.t===0?document.getElementById('show0').checked:document.getElementById('show1').checked)&&(styl.value==='all'||styl.value===x.style)}
function polygon(a){ct.beginPath();for(let i=0;i<a.length;i++){const x=offX+a[i][0]*scale,y=offY+a[i][1]*scale;i?ct.lineTo(x,y):ct.moveTo(x,y)}ct.closePath()}
function draw(){ct.clearRect(0,0,W,H);ct.fillStyle='#0c131e';ct.fillRect(0,0,W,H);if(showBack&&bg.complete){ct.globalAlpha=.76;ct.drawImage(bg,offX,offY,5175*scale,7966*scale);ct.globalAlpha=1}
let shown=0;for(let i=0;i<DATA.length;i++){const x=DATA[i];if(!filt(x))continue;shown++;const ax=x.p;if(!ax.length)continue;const xx=offX+ax[0][0]*scale,yy=offY+ax[0][1]*scale;if(xx< -100||xx>W+100||yy<-100||yy>H+100){let visible=false;for(const [px,py] of ax){let qx=offX+px*scale,qy=offY+py*scale;if(qx>=0&&qx<=W&&qy>=0&&qy<=H){visible=true;break}}if(!visible)continue}
polygon(ax);ct.fillStyle=x.t===0?'#70c4a1':'#d8ac5b';ct.globalAlpha=.91;ct.fill();ct.globalAlpha=1;if(i===selected){ct.lineWidth=2.2;ct.strokeStyle='#ffffff';ct.stroke()}}
if(showRoads){ct.strokeStyle='#8b96a9';ct.globalAlpha=.6;ct.lineWidth=1;const r=__ROADS__;for(const seq of r){ct.beginPath();seq.forEach((p,i)=>{let x=offX+p[0]*scale,y=offY+p[1]*scale;i?ct.lineTo(x,y):ct.moveTo(x,y)});ct.stroke()}ct.globalAlpha=1}
document.getElementById('nShown').textContent=shown.toLocaleString()}
const lens=[DATA.filter(x=>x.t===0).length,DATA.filter(x=>x.t===1).length];document.getElementById('n0').textContent=lens[0].toLocaleString();document.getElementById('n1').textContent=lens[1].toLocaleString();document.getElementById('nall').textContent=DATA.length.toLocaleString();
function zoom(f,cx=W/2,cy=H/2){let n=Math.max(.022,Math.min(3.5,scale*f));let x=(cx-offX)/scale,y=(cy-offY)/scale;scale=n;offX=cx-x*scale;offY=cy-y*scale;draw()}
function inside(pt,p){let v=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const a=p[i],b=p[j];if((a[1]>pt[1])!==(b[1]>pt[1])&&pt[0]<(b[0]-a[0])*(pt[1]-a[1])/(b[1]-a[1])+a[0])v=!v}return v}
function inspect(i){selected=i;const div=document.getElementById('detail');if(i<0){div.innerHTML='<p class="light">Click a building to inspect it.</p>';draw();return}const x=DATA[i],status=states[x.id]||'not reviewed';div.innerHTML='<hr style="border:0;border-top:1px solid #405064;margin:19px 0"><strong>'+x.id+'</strong><div>Source: <span class="val">'+x.src+'</span> (instance '+x.inst+')</div><div>Slot: <span class="val">'+x.site+'</span></div><div>Style: '+x.style+'</div><div>Native size: '+x.wd[0]+' × '+x.wd[1]+' × '+x.height+' metres</div><div>Position: '+(x.t===0?'original source position':'translated without scaling')+'</div><div>Shift: '+x.dx+', '+x.dy+' atlas px; rotate '+x.angle+'°</div><div>Decision: <strong>'+status+'</strong></div>';draw()}
map.addEventListener('pointerdown',e=>{map.setPointerCapture(e.pointerId);drag={x:e.clientX,y:e.clientY,ox:offX,oy:offY};moved=false});map.addEventListener('pointermove',e=>{if(!drag)return;let dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>4)moved=true;offX=drag.ox+dx;offY=drag.oy+dy;draw()});map.addEventListener('pointerup',e=>{if(!drag)return;drag=null;if(moved)return;const rect=c.getBoundingClientRect();const a=[(e.clientX-rect.left-offX)/scale,(e.clientY-rect.top-offY)/scale];for(let i=DATA.length-1;i>=0;i--){const x=DATA[i];if(filt(x)&&inside(a,x.p)){inspect(i);return}}inspect(-1)});
map.addEventListener('wheel',e=>{e.preventDefault();const b=c.getBoundingClientRect();zoom(e.deltaY>0?.81:1.23,e.clientX-b.left,e.clientY-b.top)},{passive:false});
document.getElementById('zin').onclick=()=>zoom(1.4);document.getElementById('zout').onclick=()=>zoom(1/1.4);document.getElementById('reset').onclick=()=>{fit();draw()};
for(const id of ['show0','show1','style'])document.getElementById(id).addEventListener('change',draw);document.getElementById('showBack').onchange=e=>{showBack=e.target.checked;draw()};document.getElementById('showRoads').onchange=e=>{showRoads=e.target.checked;draw()};
document.getElementById('find').addEventListener('change',e=>{const q=e.target.value.toLowerCase().trim();let i=DATA.findIndex(x=>x.src.toLowerCase()===q||x.inst.toLowerCase()===q||x.id.toLowerCase()===q||x.site.toLowerCase()===q);if(i>=0){const x=DATA[i],p=x.p,mid=p[Math.floor(p.length/2)];scale=Math.max(scale,.24);offX=W/2-mid[0]*scale;offY=H/2-mid[1]*scale;inspect(i)}});
for(const b of document.querySelectorAll('[data-choice]'))b.addEventListener('click',()=>{if(selected<0)return;states[DATA[selected].id]=b.dataset.choice;inspect(selected)});
document.getElementById('export').onclick=()=>{let payload={review_type:'Spaciel_native_assembly_draft01',author_review_decisions:states,exported_at:new Date().toISOString()};let blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});let a=document.createElement('a');a.download='spaciel_native_assembly_review_decisions.json';a.href=URL.createObjectURL(blob);a.click();URL.revokeObjectURL(a.href)};
window.addEventListener('resize',resize);resize();</script></body></html>'''
# For performance avoid road overlay until toggled; simple coord transforms in JS.
roadjs=[]
for r in roads:
 geoms=[r] if r.geom_type=='LineString' else list(r.geoms)
 for line in geoms:
  roadjs.append(np.round(np.array(line.coords),1).tolist())
html=html.replace('__GEO__',json.dumps(geo,separators=(',',':'))).replace('__BG__',bg64).replace('__ROADS__',json.dumps(roadjs,separators=(',',':')))
(HOME/'Spaciel_Native_Building_Assembly_Draft01.html').write_text(html)
print('Website and private manifest ready:',round(time.time()-TM,1),'s',len(html),'html bytes',flush=True)