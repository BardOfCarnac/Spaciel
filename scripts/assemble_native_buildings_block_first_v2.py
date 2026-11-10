#!/usr/bin/env python3
"""Place unchanged original SketchUp building-hull shapes anywhere inside gold buildable blocks.
The V10 individual polygons are NOT target slots. No matching to individual footprints.
No geometry is published by this script to public GitHub; outputs remain private.
"""
import csv, json, math, random, zipfile, time, collections, base64
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import cKDTree
from shapely.geometry import shape, mapping, Polygon

START=time.time();RNG=random.Random(20451110)
ROOT=Path('/mnt/data'); FILE=ROOT/'files'; OUT=ROOT/'spaciel_block_fill';OUT.mkdir(exist_ok=True)
W,H=Image.open(ROOT/'Spaciel_Building_Blocks_Only.png').size
SX=W/5175;SY=H/7966
r=np.array(Image.open(ROOT/'Spaciel_Building_Blocks_Only.png').convert('RGB'))
gold=np.all(r==np.array([219,168,107]),axis=2).astype('uint8')
GOLD_COUNT=int(np.count_nonzero(gold)); print('Gold area px',GOLD_COUNT, 'dimensions', W,H,flush=True)
# A thin outline buffer prevents roundoff from leaving the gold areas.
allowed=cv2.erode(gold,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
dist=cv2.distanceTransform(allowed,cv2.DIST_L2,3)
# The map's existing neighbourhood style assignments are *guidance only*; not individual target sites.
slots=json.loads((FILE/'Night_City_V10_Completed_Footprints.geojson').read_text())['features']
stylesrc=[];stylenames=[]
for f in slots:
 style=f['properties'].get('style')
 if not style:continue
 g=shape(f['geometry']); stylesrc.append((g.centroid.x*SX,g.centroid.y*SY));stylenames.append(style)
style_tree=cKDTree(np.asarray(stylesrc));del slots
style_ranges={
 'corporate':(38,125),'urban':(14,50),'mixed':(12,45),'combat':(8,35),
 'commercial':(7,37),'heritage':(6,25),'suburb':(4,15),'military':(6,25),
 'affluent':(9,43),'university':(8,36),'exec':(6,30),'amusement':(5,25),
 'port':(7,35),'hotzone':(8,55),'industrial':(8,45),}
style_colors={
 'corporate':(104,180,197),'urban':(221,185,125),'mixed':(200,172,135),
 'combat':(181,128,130),'commercial':(233,188,131),'heritage':(166,181,144),
 'suburb':(134,189,150),'military':(155,162,134),'affluent':(140,178,181),
 'university':(170,173,203),'exec':(164,185,192),'amusement':(201,147,182),
 'port':(135,177,188),'hotzone':(179,117,106),'industrial':(165,151,126)}
# Authentic original SKP source envelopes. Reuse original geometry, including scale, dimensions and orientation.
z=zipfile.ZipFile(ROOT/'Spaciel_Private_Original_SKP_Placement_Review.zip')
features=json.loads(z.read('native_original_buildings_atlas_hulls.geojson'))['features']
source=[]
for f in features:
 p=shape(f['geometry'])
 if p.geom_type!='Polygon' or not p.is_valid or p.area<12:continue
 prop=f['properties']; center=p.centroid
 points=np.array(p.exterior.coords[:-1],dtype=np.float32)
 if len(points)<3: continue
 rel=(points-np.array([center.x,center.y],np.float32))*np.array([SX,SY],np.float32)
 # Actual polygon area in gold-mask coordinate system; preserve geometry's original physical scale.
 area=float(p.area*SX*SY)
 if area<5 or area>4600:continue
 source.append(dict(iid=prop['instance_id'],sid=prop['source_native_id'],name=prop['source_skp_name'],h=float(prop['height_m']),w=float(prop['width_m']),d=float(prop['depth_m']),area=area,rel=rel,orig=(center.x*SX,center.y*SY),tris=int(prop['source_triangles'])))
print('Source screened',len(source),flush=True)
# Source model dimensions are not changed; use neighbouring building-style ranges as simple initial heuristic.
source_areas=np.array([s['area'] for s in source]);sorder=np.argsort(source_areas);sortedareas=source_areas[sorder]
usecnt=collections.Counter();placed=[];occ=np.zeros_like(gold,dtype=np.uint8)
# Each placed outline has a 1-pixel safety spacer so two shapes do not touch.
spacer_kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
# Candidate placement raster check: exact selected source convex hull must be fully within gold mask.
checks=collections.Counter()

def propose(i,cx,cy,angle,kind,style):
 s=source[i]; rr=s['rel'];c=math.cos(angle);ss=math.sin(angle)
 pts=rr@np.array([[c,ss],[-ss,c]],np.float32)+np.array([cx,cy],np.float32)
 px=np.rint(pts).astype(np.int32)
 x0=int(max(0,np.min(px[:,0])-2));y0=int(max(0,np.min(px[:,1])-2));x1=int(min(W,np.max(px[:,0])+3));y1=int(min(H,np.max(px[:,1])+3))
 if x0==0 or y0==0 or x1==W or y1==H or x1<=x0 or y1<=y0:return False
 if (x1-x0)*(y1-y0)>15000:return False
 mask=np.zeros((y1-y0,x1-x0),np.uint8)
 cv2.fillPoly(mask,[px-np.array([x0,y0],np.int32)],1)
 # No source-hull pixel may leave allowed gold region (including morphological padding).
 inside=allowed[y0:y1,x0:x1];occupied=occ[y0:y1,x0:x1]
 if np.any((mask>0)&(inside==0)):checks['not_inside_gold']+=1;return False
 if np.any((mask>0)&(occupied>0)):checks['building_collision']+=1;return False
 # Apply a tiny spacing halo when adding buildings, not to original geometry.
 psp=cv2.dilate(mask,spacer_kernel)
 occ[y0:y1,x0:x1][psp>0]=1
 native_pts=pts/np.array([SX,SY],np.float32)
 rec={'placement_id':f'block-{len(placed)+1}', 'source_instance_id':s['iid'],'source_native_id':s['sid'],
      'source_name':s['name'],'method':kind,'style':style,'native_width_m':round(s['w'],2),
      'native_depth_m':round(s['d'],2),'native_height_m':round(s['h'],2),
      'source_triangles':s['tris'],'centre_atlas_x':round(cx/SX,2),'centre_atlas_y':round(cy/SY,2),
      'shift_atlas_x':round((cx-s['orig'][0])/SX,2),'shift_atlas_y':round((cy-s['orig'][1])/SY,2),
      'rotation_deg':round(math.degrees(angle),3),'natural_source_scale':True,'approved':False,
      'geometry':native_pts.tolist()}
 placed.append(rec); usecnt[s['sid']]+=1
 return True

# 1. Original positions first, where they are genuinely inside buildable gold areas.
orig_candidates=[]
for i,s in enumerate(source):
 x,y=s['orig'];xi=int(round(x));yi=int(round(y))
 if xi<=2 or xi>=W-2 or yi<=2 or yi>=H-2 or dist[yi,xi]<3:continue
 sty=stylenames[style_tree.query([x,y])[1]]
 hmin,hmax=style_ranges.get(sty,(5,60))
 if s['h']>hmax*1.8: continue
 orig_candidates.append((s['area'],i,x,y,sty))
orig_candidates.sort(reverse=True)
for area,i,x,y,sty in orig_candidates:
 propose(i,x,y,0,'ORIGINAL_SKP_POSITION',sty)
print('Originals kept inside blocks',len(placed), 'checks',dict(checks),flush=True)

# 2. Free packing within *gold masks*, NOT V10 polygon centroids. Build grid of points across the actual gold area.
# Four stages favour a varied city, then progressively smaller infill buildings for remaining spaces.
passes=[(13,7,320,0.70),(10,6,175,0.66),(8,5,105,0.67),(6,4,65,0.73)]

# Density tuning follows local district character, not any single V10 slot.
def height_penalty(style,h):
 lo,hi=style_ranges.get(style,(6,40))
 if h<lo:return (lo-h)/max(lo,10)
 if h>hi:return (h-hi)/max(hi,15)
 return 0

def choose_candidates(area,style,limit=12):
 # Filter physical source sizes using source footprint area (in the raster coordinate frame).
 import bisect
 lo=max(6,area*.35);hi=min(2900,area*2.2)
 a=int(np.searchsorted(sortedareas,lo,'left')); b=int(np.searchsorted(sortedareas,hi,'right'))
 if a>=b:return []
 # Cheap reproducible variety, no dominance by one design.
 picks=RNG.sample(range(a,b),min(28,b-a))
 candidates=[int(sorder[n]) for n in picks]
 candidates.sort(key=lambda i: (.9*abs(math.log(source[i]['area']/area))+.65*height_penalty(style,source[i]['h'])+.10*min(usecnt[source[i]['sid']],12)+RNG.random()*.35))
 return candidates[:limit]

# Distances computed once per stage, including spacing placed during previous passes.
for step,minD,desired,fac in passes:
 free=allowed.copy();free[occ>0]=0
 dd=cv2.distanceTransform(free,cv2.DIST_L2,3)
 points=[]
 for y in range(RNG.randrange(3,step),H-3,step):
  for x in range(RNG.randrange(3,step),W-3,step):
   jx=x+RNG.randint(-step//3,step//3); jy=y+RNG.randint(-step//3,step//3)
   if jx<5 or jx>W-5 or jy<5 or jy>H-5:continue
   d=dd[jy,jx]
   if d<minD:continue
   # Higher clearance priority first, to retain more coherent large sites.
   points.append((float(d)+RNG.random()*5,jx,jy))
 RNG.shuffle(points)
 # sort with light region preference
 points.sort(reverse=True,key=lambda p:p[0])
 print('Stage',step,'centres',len(points),'time',round(time.time()-START,1),flush=True)
 success=0; checked=0
 for d,x,y in points:
  if occ[y,x] or not allowed[y,x]:continue
  if d<minD:continue
  # Use height character from nearest planned location, never try to match its individual polygon.
  sty=stylenames[style_tree.query([x,y])[1]]
  # Fit building scale to nearby free space; sample combinations, retain original proportions.
  target_area=min(desired*(0.72+RNG.random()*.8),math.pi*(d*.75)**2*fac)
  candidates=choose_candidates(target_area,sty,limit=10)
  if not candidates:continue
  # nearby block axis approximation: native cardinal plus 90-degree turns.
  for i in candidates:
   s=source[i]
   if s['area']>math.pi*(d*1.25)**2:continue
   if height_penalty(sty,s['h'])>1.8:continue
   # Original rotation preserved except optional quarter-turns; no scaling.
   angles=(0,math.pi/2,-math.pi/2,math.pi)
   for ang in angles[:2]:
    checked+=1
    if propose(i,x,y,ang,'BLOCK_FREELY_PACKED_UNSCALED',sty):success+=1;break
   else:continue
   break
 print('Stage complete',step,'added',success,'placed',len(placed),'attempts',checked,'elapsed',round(time.time()-START,1),flush=True)

# 3. Validate using the exact map mask and measure union area (raster non-overlap).
area_used=int(np.count_nonzero(occ&gold));ratio=area_used/GOLD_COUNT
sumbytype=dict(collections.Counter(p['method'] for p in placed))
sumstyle=dict(collections.Counter(p['style'] for p in placed))
summary={'draft':'Spaciel block-first placement 02','status':'UNAPPROVED NONDESTRUCTIVE 2D TRIAL',
 'principle':'Gold regions are free buildable blocks; V10 individual building polygons are not target slots.',
 'buildable_block_mask_pixels':GOLD_COUNT,'occupied_with_spacing_pixels':area_used,'occupied_fraction_including_spacing':round(ratio,4),
 'placements':len(placed),'by_method':sumbytype,'distinct_original_skp_source_definitions':len(set(p['source_native_id'] for p in placed)),
 'style_counts':sumstyle,'road_clearance_rule':'Buildable gold mask already excludes cleaned road centrelines; placements cannot leave inner gold mask.',
 'original_geometry_unchanged':'No scaling; source geometric footprint rotated or translated as a rigid shape.',
 'source_hull_note':'Convex-hull approximations of SKP shape; does not prove actual face geometry or construction.',
 'limitations':['Gold blocks created by morphological closure of V10 approved building masks, not independently surveyed block polygons.',
                'District style is nearest earlier V10 styled polygon; final district boundaries need verifying.',
                'Road surface widths, coastline water geometry and terrain foundation grades not independently validated.',
                '2D placement suggestions are not actual 3D mesh integrations; all unapproved.']}
(OUT/'block_first_placement_summary.json').write_text(json.dumps(summary,indent=2))
# Private exact placement geometry only, not public-source models.
geo={'type':'FeatureCollection','metadata':{'status':summary['status'],'method':'pack within contiguous gold buildable masks',
    'footprints_are_slots':False,'source_geometry_sketch_up_provenance':'private'},
    'features':[{'type':'Feature','properties':{k:v for k,v in item.items() if k!='geometry'},'geometry':{'type':'Polygon','coordinates':[item['geometry']+[item['geometry'][0]]]}} for item in placed]}
(OUT/'Spaciel_Block_First_Assembly_02_PRIVATE.geojson').write_text(json.dumps(geo,separators=(',',':')))
with open(OUT/'Spaciel_Block_First_Assembly_02_PRIVATE.csv','w',newline='') as f:
 fields=[k for k in placed[0] if k!='geometry'];dw=csv.DictWriter(f,fieldnames=fields);dw.writeheader();dw.writerows([{k:v for k,v in p.items() if k!='geometry'} for p in placed])
# Presentation: gold background, original positions mint, freely packed sky blue, no old footprint outlines.
back=np.empty((H,W,3),np.uint8);back[:]=[13,21,31];back[gold>0]=[78,63,44]
for p in placed:
 a=np.rint(np.asarray(p['geometry'])*[SX,SY]).astype(np.int32)
 col=(112,200,164) if p['method']=='ORIGINAL_SKP_POSITION' else (225,180,109)
 cv2.fillPoly(back,[a],col)
 # Only faint edges; simplify rendered shapes at citywide scale.
 cv2.polylines(back,[a],True,(42,50,58),1,cv2.LINE_AA)
preview=Image.fromarray(back);preview.thumbnail((1650,2540))
PW,PH=preview.size
canvas=Image.new('RGB',(PW+64,PH+164),(13,21,31));canvas.paste(preview,(32,100));draw=ImageDraw.Draw(canvas)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';heading=ImageFont.truetype(font,25);small=ImageFont.truetype(font,16)
draw.text((32,24),'SPACIEL   /   BUILDING BLOCK ASSEMBLY 02',font=heading,fill=(235,233,225))
draw.text((32,64),'Gold: unfilled buildable area   ·   Mint: original locations   ·   Sand: freely placed SKP shapes',font=small,fill=(181,193,200))
draw.text((32,PH+118),f'{len(placed):,} native-scale provisional buildings  ·  {ratio*100:.1f}% gold-area coverage including spacing  ·  No original site-matching',font=small,fill=(181,193,200))
canvas.save(ROOT/'Spaciel_Block_First_Assembly_02_Preview.png')
# Clean no-captions map with gold and buildings
Image.fromarray(back).save(ROOT/'Spaciel_Block_First_Assembly_02_Map.png')
print('DONE',json.dumps(summary,indent=2), 'elapsed',round(time.time()-START,1),'s',flush=True)