#!/usr/bin/env python3
"""Spaciel Draft 03: district-aware infill anywhere within the gold buildable regions.
Do NOT treat earlier footprints as individual slots. Preserve existing Draft 02.
All source geometry is kept in private outputs; only method and aggregate report for public repo.
"""
from pathlib import Path
import cv2, numpy as np, math, random, csv, json, zipfile, time, collections
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import shape, Polygon
from scipy.spatial import cKDTree
START=time.monotonic();import os
root=Path(os.environ.get('SPACIEL_WORK_ROOT','/mnt/data'));out=root/'spaciel_round2';out.mkdir(exist_ok=True)
RNG=random.Random(20451110+2)
goldimg=np.array(Image.open(root/'Spaciel_Building_Blocks_Only.png').convert('RGB'))
gold=np.all(goldimg==[219,168,107],axis=2).astype('uint8');H,W=gold.shape;SX=W/5175;SY=H/7966
allowed=gold.copy()  # Building frontage can approach the designated gold block boundary exactly
dgold=cv2.distanceTransform(gold,cv2.DIST_L2,3)
N,labels,region_stats,region_centroids=cv2.connectedComponentsWithStats(gold,connectivity=8)
region_area=np.bincount(labels.ravel(),minlength=N).astype('int32')
region_occ=np.zeros(N,np.int32)
# Existing accepted provisional geometries, never remodelled
v2=[ft for ft in json.loads((root/'spaciel_block_fill/Spaciel_Block_First_Assembly_02_PRIVATE.geojson').read_text())['features'] if ft['properties']['method']=='ORIGINAL_SKP_POSITION']
print('existing',len(v2),'regions',N-1,'area',gold.sum(),flush=True)
source_features=json.loads(zipfile.ZipFile(root/'Spaciel_Private_Original_SKP_Placement_Review.zip').read('native_original_buildings_atlas_hulls.geojson'))['features']
src=[]
for ft in source_features:
 p=shape(ft['geometry'])
 if p.geom_type!='Polygon' or not p.is_valid or p.area<=0:continue
 a=p.area*SX*SY
 if a<5 or a>4600:continue
 q=ft['properties'];cent=p.centroid
 pts=np.asarray(p.exterior.coords[:-1],np.float32)*np.array([SX,SY],np.float32)
 rel=pts-np.array([cent.x*SX,cent.y*SY],np.float32)
 # principal long axis in projected map units
 cov=rel.T@rel/max(1,len(rel));eigval,eigvec=np.linalg.eigh(cov);main=eigvec[:,-1];th=math.atan2(main[1],main[0])
 src.append(dict(iid=q['instance_id'],sid=q['source_native_id'],name=q['source_skp_name'],rel=rel,
                 area=a,theta=th,aspect=math.sqrt((eigval[-1]+1e-5)/(eigval[0]+1e-5)),
                 h=float(q['height_m']),w=float(q['width_m']),d=float(q['depth_m']),tris=int(q['source_triangles']),
                 orig=[cent.x*SX,cent.y*SY]))
print('original SKP source instances',len(src),flush=True)
# Style is inferred regionally from V10 coordinates, NEVER used as individual building destinations.
slots=json.loads((root/'files/Night_City_V10_Completed_Footprints.geojson').read_text())['features']
pts=[];styles=[]
for ft in slots:
 s=ft['properties'].get('style');
 if s:
  g=shape(ft['geometry']);pts.append((g.centroid.x*SX,g.centroid.y*SY));styles.append(s)
styletree=cKDTree(np.asarray(pts));del slots
style_ranges={ 'corporate':(38,125),'urban':(14,50),'mixed':(12,45),'combat':(8,35),
 'commercial':(7,37),'heritage':(6,25),'suburb':(4,15),'military':(6,25),
 'affluent':(9,43),'university':(8,36),'exec':(6,30),'amusement':(5,25),
 'port':(7,35),'hotzone':(8,55),'industrial':(8,45)}
# Halo occupancy targets by regional style: broad centre/urban frontage denser, Hot Zone deliberately sparse.
regional_limits={'corporate':.95,'urban':.95,'mixed':.93,'commercial':.93,
 'heritage':.90,'industrial':.89,'combat':.84,'university':.81,
 'port':.84,'amusement':.80,'military':.76,'suburb':.75,
 'affluent':.74,'exec':.66,'hotzone':.53}
NAMES=list(regional_limits)
centers={i:tuple(region_centroids[i]) for i in range(1,N) if region_area[i]>=40}
if centers:
 klist=list(centers);ktree=cKDTree(np.array([centers[k] for k in klist]));ind=styletree.query(np.array([centers[k] for k in klist]))[1]
 region_style={klist[j]:styles[int(ind[j])] for j in range(len(klist))}
else:region_style={}
# Rasterized occupancy with 1-pixel gap halo; keep original shapes unchanged.
occ=np.zeros_like(gold)
solid=np.zeros_like(gold)
halo_k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
records=[];usecnt=collections.Counter();use_by_source=collections.defaultdict(list)
style_counts=collections.Counter()
for ft in v2:
 r=ft['properties'].copy();rr=np.array(ft['geometry']['coordinates'][0][:-1],np.float32)
 px=np.rint(rr*np.array([SX,SY])).astype('int32');x0=max(0,int(px[:,0].min())-2);x1=min(W,int(px[:,0].max())+3);y0=max(0,int(px[:,1].min())-2);y1=min(H,int(px[:,1].max())+3)
 mm=np.zeros((y1-y0,x1-x0),np.uint8);cv2.fillPoly(mm,[px-np.array([x0,y0],np.int32)],1)
 pp=cv2.dilate(mm,halo_k)
 occ[y0:y1,x0:x1][pp>0]=1;solid[y0:y1,x0:x1][mm>0]=1
 region=int(labels[round(r['centre_atlas_y']*SY),round(r['centre_atlas_x']*SX)])
 region_occ[region]+=int(np.count_nonzero(pp))
 r['phase']=2;records.append((r,rr));usecnt[r['source_native_id']]+=1;style_counts[r['style']]+=1
 use_by_source[r['source_native_id']].append((r['centre_atlas_x']*SX,r['centre_atlas_y']*SY))
# Existing block occupancy may slightly overcount due to shared halo; safe to under-fill instead of overfilling.
orig_count=len(records)
area_sort=np.argsort([s['area'] for s in src]);aa=np.array([src[int(i)]['area'] for i in area_sort]);reuse_limit=16
checks=collections.Counter()

def select_sources(area,style,phase,limit=16):
 lo,hi=area*0.38,area*2.5
 if phase==3:lo,hi=max(5,area*.2),area*2.8
 a=np.searchsorted(aa,max(5,lo),'left');b=np.searchsorted(aa,min(4600,hi),'right')
 if b<=a:return []
 picks=RNG.sample(range(int(a),int(b)),min(72,int(b-a)))
 mn,mx=style_ranges.get(style,(8,50))
 def penalty(i):
  s=src[i];h=s['h'];height_pen=max(0,mn-h)/max(15,mn)+max(0,h-mx)/max(mx,25)
  repeat=min(usecnt[s['sid']],reuse_limit)
  return .8*abs(math.log(s['area']/area)) + .55*height_pen + .07*repeat + .25*max(0,s['aspect']-3) + RNG.random()*.4
 inds=[int(area_sort[k]) for k in picks];inds.sort(key=penalty)
 return inds[:limit]

def try_place(i,cx,cy,rot,sty,phase,region,frontage=False):
 s=src[i];z=s['rel'];c=math.cos(rot);ss=math.sin(rot)
 ar=z@np.array([[c,ss],[-ss,c]],np.float32)+[cx,cy]
 px=np.rint(ar).astype('int32')
 x0=max(0,int(px[:,0].min())-2);y0=max(0,int(px[:,1].min())-2);x1=min(W,int(px[:,0].max())+3);y1=min(H,int(px[:,1].max())+3)
 if x0==0 or y0==0 or x1==W or y1==H or x1<=x0 or y1<=y0:return False
 if (x1-x0)*(y1-y0)>14000:return False
 mm=np.zeros((y1-y0,x1-x0),np.uint8);cv2.fillPoly(mm,[px-np.array([x0,y0],np.int32)],1)
 if np.any((mm>0)&(allowed[y0:y1,x0:x1]==0)):
  checks['outside_gold']+=1;return False
 if np.any((mm>0)&(occ[y0:y1,x0:x1]>0)):
  checks['occupied']+=1;return False
 # Avoid repeated copies of the same source model immediately next to each other.
 for xx,yy in use_by_source[s['sid']]:
  if (xx-cx)**2+(yy-cy)**2<28**2:
   checks['duplicate_nearby']+=1;return False
 pp=mm if sty in ('corporate','urban','mixed','commercial','heritage','industrial') else cv2.dilate(mm,halo_k)
 if np.any((pp>0)&(occ[y0:y1,x0:x1]>0)):
  checks['halo_occupied']+=1;return False
 # Global region cap with a small allowance for a whole building.
 extra=int(np.count_nonzero(pp))
 limit=regional_limits.get(sty,.82)
 if region_area[region]>60 and (region_occ[region]+extra)/region_area[region]>limit+0.025:
  checks['region_target']+=1;return False
 occ[y0:y1,x0:x1][pp>0]=1;solid[y0:y1,x0:x1][mm>0]=1
 region_occ[region]+=extra
 pp_atlas=ar/np.array([SX,SY],np.float32)
 r={'placement_id':f'block-{len(records)+1}','source_instance_id':s['iid'],'source_native_id':s['sid'],
 'source_name':s['name'],'method':'ROUND_02_GOLD_BLOCK_INFILL','style':sty,'native_width_m':round(s['w'],2),
 'native_depth_m':round(s['d'],2),'native_height_m':round(s['h'],2),'source_triangles':s['tris'],
 'centre_atlas_x':round(cx/SX,2),'centre_atlas_y':round(cy/SY,2),
 'shift_atlas_x':round((cx-s['orig'][0])/SX,2),'shift_atlas_y':round((cy-s['orig'][1])/SY,2),
 'rotation_deg':round(math.degrees(rot),3),'natural_source_scale':True,'approved':False,
 'phase':3,'placement_kind':'road_frontage' if frontage else 'internal_infill','buildable_region_id':region}
 records.append((r,pp_atlas));usecnt[s['sid']]+=1;use_by_source[s['sid']].append((cx,cy));style_counts[sty]+=1
 return True

# Face edges from the actual buildable gold outline. Gradient of distance-to-edge aligns long axes with street-adjacent block boundary.
gx=cv2.Sobel(dgold,cv2.CV_32F,1,0,ksize=3);gy=cv2.Sobel(dgold,cv2.CV_32F,0,1,ksize=3)
# Stages favour the block frontages then fill internal vacancies, then small residual openings.
stages=[
 dict(name='major_streetfront_buildings',grid=10,near=(7.5,28),mind_free=7.5,area=(170,620),phase=2,tries=24),
 dict(name='regular_streetfront_buildings',grid=7,near=(4.2,20),mind_free=4.5,area=(60,310),phase=1,tries=24),
 dict(name='large_internal_buildings',grid=8,near=(6,60),mind_free=6.5,area=(95,380),phase=2,tries=24),
 dict(name='small_streetfront',grid=5,near=(2.8,18),mind_free=3.0,area=(25,140),phase=3,tries=24),
 dict(name='in-block_compact_infill',grid=6,near=(3.1,80),mind_free=3.3,area=(28,150),phase=3,tries=24),
 dict(name='last_residential_urban_edges',grid=4,near=(1.7,18),mind_free=2.2,area=(10,75),phase=3,tries=20),
]

for si,stage in enumerate(stages):
 empty=allowed.copy();empty[occ>0]=0
 dfree=cv2.distanceTransform(empty,cv2.DIST_L2,3)
 step=stage['grid'];cn=[]
 # Grid where blocks have clearance from roads and existing buildings.
 ox=RNG.randrange(step);oy=RNG.randrange(step)
 for y in range(oy+3,H-3,step):
  for x in range(ox+3,W-3,step):
   if not empty[y,x]:continue
   d0=dgold[y,x];d1=dfree[y,x]
   if d0<stage['near'][0] or d0>stage['near'][1] or d1<stage['mind_free']:continue
   reg=labels[y,x]
   if region_area[reg]<40:continue
   if region_occ[reg] / region_area[reg] >= regional_limits.get(region_style.get(reg,'mixed'),.85):continue
   # prioritise street frontage in first/third stage, internal free clearance in second/fourth
   score=(-d0+RNG.random()*4) if si in (0,1,3,5) else (d1+RNG.random()*3)
   cn.append((score,x,y))
 cn.sort(key=lambda v:v[0],reverse=True)
 accepted=0;attempted=0
 print('stage',stage['name'],'positions',len(cn),'existing',len(records),'elapsed',round(time.monotonic()-START,1),flush=True)
 for rank,(sc,x,y) in enumerate(cn):
  if occ[y,x] or not allowed[y,x]:continue
  reg=labels[y,x];style=region_style.get(reg)
  if not style:
   style=styles[int(styletree.query((x,y))[1])]
  if region_occ[reg]/max(region_area[reg],1)>=regional_limits.get(style,.83):continue
  d0=float(dgold[y,x]);d1=float(dfree[y,x]);
  if d1<stage['mind_free']*.7:continue
  # predict area to fit within available corridor, not to mimic old site sizes
  lo,hi=stage['area'];ideal=min(hi,max(lo,(min(d1,d0)+1.0)**2*(2.6 if si in (0,1,3,5) else 2.0)))
  # Keep variety, but try compact originals over very long outlines except industrial/port.
  cand=select_sources(ideal,style,stage['phase'],limit=stage['tries'])
  if not cand:continue
  # edge tangent at the local point, two cardinal rotations as fallback
  tangent=math.atan2(float(gy[y,x]),float(gx[y,x]))+math.pi/2
  for ix in cand:
   s=src[ix]
   if s['area']>min(650,(d1*4.3)**2*1.5) or s['area']<5:continue
   mn,mx=style_ranges.get(style,(6,45))
   if s['h']>mx*1.8 or (s['h']<mn*.5 and style in ('corporate','urban')):continue
   if s['aspect']>5.2 and style not in ('port','industrial','corporate'):continue
   # Rigid rotations; align longest axis with gold boundary, then try native orientation.
   angled=tangent-s['theta'];rotations=(angled, angled+math.pi/2,0,math.pi/2) if si in (0,1,3,5) else (0,angled,math.pi/2)
   for ang in rotations:
    attempted+=1
    if try_place(ix,x,y,ang,style,3,reg,frontage=si in (0,1,3,5)):
     accepted+=1;break
   else:continue
   break
 print('completed',stage['name'],'new',accepted,'total',len(records),'attempts',attempted,'elapsed',round(time.monotonic()-START,1),flush=True)

# Final exact polygon + gold-pixel audit, then discard only failing new candidate placements.
# Prevent tiny subpixel intersections generated by raster rounding from becoming final overlaps.
from shapely.strtree import STRtree
geom=[Polygon(np.asarray(poly,dtype=float).round(2).tolist()) for _,poly in records]
spatial=STRtree(geom)
reject=set(); reasons=collections.Counter()
for i,((rec,coords),g) in enumerate(zip(records,geom)):
 px=np.rint(np.asarray(coords,dtype=float).round(2)*[SX,SY]).astype('int32')
 x0=max(0,int(px[:,0].min())-1);y0=max(0,int(px[:,1].min())-1)
 x1=min(W,int(px[:,0].max())+2);y1=min(H,int(px[:,1].max())+2)
 mask=np.zeros((y1-y0,x1-x0),np.uint8);cv2.fillPoly(mask,[px-np.array([x0,y0])],1)
 if np.any((mask>0)&(gold[y0:y1,x0:x1]==0)):
  assert rec['phase']==3
  reject.add(i);reasons['outside_gold_rounding']+=1
for i,g in enumerate(geom):
 if i in reject:continue
 for j0 in spatial.query(g):
  j=int(j0)
  if j<=i or j in reject:continue
  a=g.intersection(geom[j]).area
  if a>0 and a/min(g.area,geom[j].area)>.005:
   # Prefer original SKP placement, otherwise prefer the earlier fitted candidate.
   ri,rj=records[i][0],records[j][0]
   loser=j if ri['phase']!=3 else (i if rj['phase']!=3 else j)
   reject.add(loser);reasons['exact_overlap_above_half_percent']+=1
if reject:
 records=[r for i,r in enumerate(records) if i not in reject]
 # Exact post-audit coverage. Dense frontage can share an edge; rural styles retain a narrow halo.
 solid[:]=0;occ[:]=0
 for rec,coords in records:
  px=np.rint(np.asarray(coords,dtype=float).round(2)*[SX,SY]).astype('int32')
  x0=max(0,int(px[:,0].min())-2);y0=max(0,int(px[:,1].min())-2)
  x1=min(W,int(px[:,0].max())+3);y1=min(H,int(px[:,1].max())+3)
  mm=np.zeros((y1-y0,x1-x0),np.uint8);cv2.fillPoly(mm,[px-np.array([x0,y0])],1)
  solid[y0:y1,x0:x1][mm>0]=1
  pp=mm if rec['phase']==3 and rec['style'] in ('corporate','urban','mixed','commercial','heritage','industrial') else cv2.dilate(mm,halo_k)
  occ[y0:y1,x0:x1][pp>0]=1
 style_counts=collections.Counter(r['style'] for r,_ in records)
print('Final geometry audit: dropped',len(reject),'reason counts',dict(reasons),flush=True)
physical=int(np.count_nonzero(solid & gold));halo=int(np.count_nonzero(occ & gold));gold_count=int(gold.sum());new=len(records)-orig_count
methods=collections.Counter(p['method'] for p,_ in records)
summary={'version':'Draft 03 — source-position-preserving complete block repack','retained_original_positions':orig_count,'round02_repacked_placements':new,'all_placements':len(records),
 'original_skp_source_position_retained':methods.get('ORIGINAL_SKP_POSITION',0),
 'native_sources_reused_elsewhere':len(records)-methods.get('ORIGINAL_SKP_POSITION',0),
 'new_road_frontage':sum(p.get('placement_kind')=='road_frontage' for p,_ in records),
 'new_interior_infill':sum(p.get('placement_kind')=='internal_infill' for p,_ in records),
 'distinct_original_source_definitions':len({r['source_native_id'] for r,_ in records}),
 'gold_mask_area_pixels':gold_count,'building_outline_area_pixels':physical,
 'building_outline_coverage_pct':round(100*physical/gold_count,2),'with_character_specific_spacing_pct':round(100*halo/gold_count,2),
 'residual_unoccupied_gold_pixels':gold_count-physical, 'style_placement_counts':dict(style_counts),
 'final_geometry_rejected_candidates':len(reject),'final_geometry_rejected_reasons':dict(reasons),
 'status':'UNAPPROVED 2D REPACK — 140 original SKP positions retained; old Draft 02 free placements re-evaluated; no mesh scaling',
 'regional_density_caps':'local character; deliberately sparse Hot Zone and Executive areas',
 'constraint_notes':['140 authentic original-position placements retained; other Draft 02 allocations were provisional and repacked without changing source geometry','Native source hulls translated/rotated, never resized',
                     'No hull allowed outside approved gold mask or touching another hull at working raster scale',
                     'No geometry overlaps at working raster resolution; original Draft 02 has 1px clearance; dense frontage may abut','Original V10 polygons never treated as individual destination slots',
                     'Full road widths/coast/terrain grade and final 3D mesh placement not yet verified']}
(out/'draft03_repack_summary.json').write_text(json.dumps(summary,indent=2))
# private geometry, never push source-derived hulls to public GitHub.
features=[]
for rec,p in records:
 coords=np.asarray(p,dtype=float).round(2).tolist()
 features.append({'type':'Feature','properties':rec,'geometry':{'type':'Polygon','coordinates':[coords+[coords[0]]]}})
geo={'type':'FeatureCollection','metadata':{'version':'draft03','approved':False,'original_skp':True,'source_publication_allowed':False},'features':features}
(out/'Spaciel_Block_Fill_Draft03_REPACK_PRIVATE.geojson').write_text(json.dumps(geo,separators=(',',':'),default=lambda v: v.item() if isinstance(v,np.generic) else str(v)))
# Review images use true solid footprint raster, not dilated halo
base=np.empty((H,W,3),np.uint8);base[:]=[13,21,31];base[gold>0]=[91,71,47]
for r,p in records:
 pix=np.rint(np.asarray(p)*[SX,SY]).astype(np.int32)
 col=(112,200,164) if r['method']=='ORIGINAL_SKP_POSITION' else ((224,181,108) if r['phase']==2 else (112,163,205))
 cv2.fillPoly(base,[pix],col)
 cv2.polylines(base,[pix],True,(35,48,55),1,cv2.LINE_AA)
Image.fromarray(base).save(root/'Spaciel_Block_Fill_Draft03_REPACK_Map.png')
preview=Image.fromarray(base);preview.thumbnail((1460,2350));ww,hh=preview.size
canvas=Image.new('RGB',(ww+48,hh+147),(13,21,31));canvas.paste(preview,(24,90));d=ImageDraw.Draw(canvas)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';big=ImageFont.truetype(font,24);small=ImageFont.truetype(font,14)
d.text((24,20),'SPACIEL   /   BUILDABLE BLOCK FILL · ROUND TWO',fill=(235,240,229),font=big)
d.text((24,58),'Gold unoccupied  •  Sand Draft 02  •  Sky blue added frontage / infill  •  Mint original SKP sites',fill=(185,200,198),font=small)
d.text((24,hh+112),f"{len(records):,} native-scale 2D placements · {summary['building_outline_coverage_pct']:.1f}% gold area physically covered · still provisional",fill=(180,195,199),font=small)
canvas.save(root/'Spaciel_Block_Fill_Draft03_REPACK_Preview.png')
print('SUMMARY',json.dumps(summary,indent=2),'elapsed',round(time.monotonic()-START,1),flush=True)