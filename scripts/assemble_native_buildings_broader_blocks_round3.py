#!/usr/bin/env python3
"""Spaciel Round 3: infill inside recovered broad 2045 road-block regions.
Never uses the old building footprints as individual destinations.
Round Two source-based outlines are retained. New model outlines are never scaled,
only moved and rotated. This is an unapproved 2D placement experiment.
"""
from pathlib import Path
import json, zipfile, math, random, collections, time, csv, io, base64
import cv2, numpy as np
from shapely.geometry import Polygon, shape, LineString, mapping
from shapely.ops import unary_union
from shapely.strtree import STRtree
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import cKDTree

ROOT=Path('/mnt/data'); OUTPUT=ROOT/'spaciel_round3'; OUTPUT.mkdir(exist_ok=True)
START=time.monotonic(); RNG=random.Random(2045_1110+3)
W,H=3304,5100; AX=W/5175; AY=H/7966

def readgeo(p):return json.loads(Path(p).read_text())
def outlines(g):
 if g.is_empty:return
 if g.geom_type=='Polygon':yield g
 elif hasattr(g,'geoms'):
  for p in g.geoms:yield from outlines(p)
def poly2pix(p):return np.round(np.asarray(p.exterior.coords[:-1],dtype=np.float32)*[AX,AY]).astype(np.int32)
def rast_polygon(img,p,color):
 pts=poly2pix(p)
 if len(pts)>=3:cv2.fillPoly(img,[pts],color)
 for ring in p.interiors:
  rr=np.round(np.asarray(ring.coords[:-1],np.float32)*[AX,AY]).astype(np.int32)
  if len(rr)>=3:cv2.fillPoly(img,[rr],0)

def raster_union(geo):
 a=np.zeros((H,W),dtype=np.uint8)
 for p in outlines(geo):
  if p.area>=5:rast_polygon(a,p,1)
 return a

# Broader recovered 560 city blocks, Gold previously approved mask. New placements
# are drawn only from the additional old-block territory, minus roads/water/Hot Zone.
broadgeo=readgeo(ROOT/'Spaciel_Candidate_Buildable_Blocks_Road_Exclusion_v2.geojson')
goldgeo=readgeo(ROOT/'files/Spaciel_Gold_Buildable_Regions_v1.geojson')
blockgeo=[shape(f['geometry']).buffer(0) for f in broadgeo['features']]
broad_union=unary_union(blockgeo)
gold_union=unary_union([shape(f['geometry']).buffer(0) for f in goldgeo['features']])
extra_geo=broad_union.difference(gold_union)
gold=np.all(np.array(Image.open(ROOT/'Spaciel_Building_Blocks_Only.png').convert('RGB')) == [219,168,107],axis=2).astype('uint8')
broad=raster_union(broad_union)
extra=raster_union(extra_geo)
# Area not previously filled is the only new placing region; retain all old source outlines.
print('shape',gold.shape,'broad',int(broad.sum()),'extra',int(extra.sum()),flush=True)

# Reconstruct V17 stylised road exclusion by chain with an additional atlas-pixel margin.
roads=readgeo(ROOT/'files/night_city_2045_cleaned_display_lines.geojson')['features']
v17=readgeo(ROOT/'files/night_city_2045_visual_road_layer_v17.geojson')['features']
roadprops={f['properties']['chain_id']:f['properties'] for f in v17}
roadmask=np.zeros((H,W),np.uint8)
for ft in roads:
 chain=ft['properties']['chain_id'];p=roadprops.get(chain,{})
 width=float(p.get('width_m',9)); thickness=max(4,math.ceil((width*.372+2*2.6)*AX))
 pp=np.asarray(ft['geometry']['coordinates'],np.float32)*[AX,AY]
 if len(pp)>1:cv2.polylines(roadmask,[np.rint(pp).astype(np.int32)],False,1,thickness,lineType=cv2.LINE_8)

# Original preserved Hot Zone polygon from older road-block placement experiment.
s=(ROOT/'files/night_city_2045_city_first_pass.html').read_text();i=s.index('const D=')+len('const D=');original=json.JSONDecoder().raw_decode(s[i:])[0]
hot=np.zeros((H,W),np.uint8)
rast_polygon(hot,Polygon(original['hotzone']).buffer(0),1)
# High-saturation cyan/blue and green atlas areas are water / landscape, not building lots.
arr=np.asarray(Image.open(ROOT/'files/spaciel_v19_atlas_high_res_2.png').convert('RGB'))
red,green,blue=arr[:,:,0],arr[:,:,1],arr[:,:,2]
water=((red<80)&(green>70)&(blue>72)&(blue>red+32)).astype(np.uint8)
water=cv2.dilate(water,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
allowed=extra.copy(); allowed[roadmask>0]=0;allowed[hot>0]=0;allowed[water>0]=0
# Reject any new positions around existing sources; preserve the previous layout exactly.
old=readgeo(ROOT/'files/Spaciel_Round_02_Native_Placements_PRIVATE.geojson')['features']
assert len(old)==6257
occup=np.zeros((H,W),dtype=np.uint8)
existingids=collections.Counter();originalpositions=0;old_area_pixel=np.zeros((H,W),dtype=np.uint8)
for feat in old:
 p=shape(feat['geometry']);pp=poly2pix(p)
 if len(pp)<3:continue
 cv2.fillPoly(old_area_pixel,[pp],1)
 cv2.fillPoly(occup,[pp],1)
 existingids[str(feat['properties'].get('source_native_id',''))]+=1
 if feat['properties'].get('method')=='ORIGINAL_SKP_POSITION':originalpositions+=1
# Dilate existing occupancy to maintain separation from placed buildings.
occup=cv2.dilate(occup,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))

# Per-block local character assigned from the V6 historical morphology review.
v6s=(ROOT/'files/Night_City_2045_V6_Frontage_Final_Viewer.html').read_text();i=v6s.index('const DATA=')+len('const DATA=');v6=json.JSONDecoder().raw_decode(v6s[i:])[0]
styles=[b[2] for b in v6['blocks']]
stylemask=np.zeros((H,W),dtype=np.uint16)
for bi,p in enumerate(blockgeo):
 if not p.is_empty:rast_polygon(stylemask,p,bi+1)

# Native SKP hulls (kept outside public GitHub). Rigid 2D transformations only.
z=zipfile.ZipFile(ROOT/'Spaciel_Private_Original_SKP_Placement_Review.zip')
sources_geo=json.loads(z.read('native_original_buildings_atlas_hulls.geojson'))['features']
sources=[]
for ft in sources_geo:
 p=shape(ft['geometry'])
 if p.geom_type!='Polygon' or not p.is_valid or p.area<=0:continue
 pr=ft['properties'];area=p.area*AX*AY
 if not (9<=area<=1400):continue
 c=p.centroid
 pp=poly2pix(p).astype(np.float32)
 rel=pp-[c.x*AX,c.y*AY]
 if len(rel)<3:continue
 cov=(rel.T@rel)/len(rel);eigval,eigvec=np.linalg.eigh(cov);main=eigvec[:,-1]
 angle=math.atan2(main[1],main[0]);aspect=math.sqrt((eigval[-1]+1e-5)/(eigval[0]+1e-5))
 if aspect>8:continue
 sources.append({'iid':str(pr['instance_id']),'sid':str(pr['source_native_id']),'name':pr['source_skp_name'],
 'width':float(pr['width_m']),'depth':float(pr['depth_m']),'height':float(pr['height_m']),
 'triangles':int(pr['source_triangles']),'rel':rel.astype('float32'),
 'origin':(c.x*AX,c.y*AY),'angle':angle,'aspect':aspect,'area':area})
sources.sort(key=lambda s:s['area']);areas=np.array([s['area'] for s in sources]);print('sources',len(sources),flush=True)
# Style-specific ranges are guidance, never geometry editing.
style_limits={'corporate':(.60,36,125),'urban':(.62,14,60),'mixed':(.57,12,60),'commercial':(.57,8,44),
 'heritage':(.57,6,30),'industrial':(.53,8,55),'combat':(.45,8,40),'university':(.47,8,40),
 'port':(.48,8,50),'amusement':(.42,5,30),'military':(.38,6,30),'suburb':(.36,4,20),
 'affluent':(.35,8,48),'exec':(.29,6,38),'hotzone':(.03,8,50)}

# Label *connected* recovered areas, so coverage can be controlled without requiring 1 building per slot.
components,labels,stats,centroids=cv2.connectedComponentsWithStats(allowed,connectivity=8)
region_area=stats[:,cv2.CC_STAT_AREA]
regstyle={}
for r in range(1,components):
 if region_area[r]<50:continue
 x,y=map(int,centroids[r]);ind=int(stylemask[min(H-1,y),min(W-1,x)])
 regstyle[r]=styles[ind-1] if 1<=ind<=len(styles) else 'mixed'
regused=np.zeros(components,np.int32)
newmask=np.zeros((H,W),np.uint8);count=collections.Counter();new=[];reuse=collections.Counter(existingids)
source_last=collections.defaultdict(list)
# collect already placed locations so repeated instances of same definition aren't placed next-door
for f in old:
 p=f['properties'];source_last[str(p['source_native_id'])].append((p['centre_atlas_x']*AX,p['centre_atlas_y']*AY))

# Distance to edge and road to favour frontage rather than centre-only random scatter.
dist=cv2.distanceTransform(allowed,cv2.DIST_L2,3)
gradx=cv2.Sobel(dist,cv2.CV_32F,1,0,ksize=3)
grady=cv2.Sobel(dist,cv2.CV_32F,0,1,ksize=3)
# compact small shapes and mid-size source buildings are prioritized; large buildings can still fit
# wherever a bigger free region exists.

def try_build(s,cx,cy,ang,reg,style,stage):
 rr=s['rel'];co=math.cos(ang);sn=math.sin(ang)
 xy=rr@np.array([[co,sn],[-sn,co]],np.float32)+[cx,cy]
 pix=np.rint(xy).astype(np.int32)
 x0=max(0,int(pix[:,0].min())-2);y0=max(0,int(pix[:,1].min())-2)
 x1=min(W,int(pix[:,0].max())+3);y1=min(H,int(pix[:,1].max())+3)
 if x0<=1 or y0<=1 or x1>=W-1 or y1>=H-1:return False
 if (x1-x0)*(y1-y0)>7000:return False
 q=pix-[x0,y0];local=np.zeros((y1-y0,x1-x0),np.uint8)
 cv2.fillPoly(local,[q],1)
 if np.any((local>0)&(allowed[y0:y1,x0:x1]==0)):return False
 if np.any((local>0)&(occup[y0:y1,x0:x1]>0)):return False
 area_px=int(local.sum())
 target=style_limits.get(style,(.5,8,45))[0]
 if region_area[reg]<100 or (regused[reg]+area_px)/(region_area[reg])>target+.05:return False
 # For houses and parks prefer 1px separation: refuse near occupied after dilate.
 if style not in ('urban','corporate','commercial','mixed','heritage','industrial'):
  expanded=cv2.dilate(local,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
  if np.any((expanded>0)&(occup[y0:y1,x0:x1]>0)):return False
 if any((xx-cx)**2+(yy-cy)**2<34**2 for xx,yy in source_last[s['sid']][-24:]):return False
 # Commit raster + geometry, leaving source geometry untouched.
 cv2.fillPoly(newmask,[pix],1)
 cv2.fillPoly(occup,[pix],1)
 # full occupancy with 1px gap around candidate
 occregion=occup[y0:y1,x0:x1];dil=cv2.dilate(local,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
 occregion[dil>0]=1
 regused[reg]+=area_px
 source_last[s['sid']].append((cx,cy));reuse[s['sid']]+=1
 pxy=(xy/np.array([AX,AY])).round(2).tolist()
 coords=pxy+[pxy[0]]
 rec={'placement_id':f'round3-new-{len(new)+1}','source_instance_id':s['iid'],'source_native_id':s['sid'],'source_name':s['name'],
  'method':'ROUND_03_RECOVERED_ROAD_BLOCK_INFILL','style':style,'native_width_m':round(s['width'],2),
  'native_depth_m':round(s['depth'],2),'native_height_m':round(s['height'],2),'source_triangles':s['triangles'],
  'centre_atlas_x':round(cx/AX,2),'centre_atlas_y':round(cy/AY,2),
  'rotation_deg':round(math.degrees(ang),3),'natural_source_scale':True,'approved':False,'phase':4,
  'placement_kind':stage,'broader_buildable_region_id':int(reg),'source_geometry_private':True}
 new.append({'type':'Feature','properties':rec,'geometry':{'type':'Polygon','coordinates':[coords]}});count[style]+=1
 return True

# Stage candidates in permitted extra area. Prioritise frontages first and then internal gaps;
# styles maintain deliberate open space. Re-use naturally scaled SketchUp originals as needed.
stages=[
 {'name':'major_frontage','step':9,'area':(140,650),'depth':(6.0,40),'minfree':6.5,'num':10},
 {'name':'regular_frontage','step':7,'area':(65,350),'depth':(3.8,26),'minfree':4,'num':9},
 {'name':'interior_midrise','step':8,'area':(90,450),'depth':(5.0,80),'minfree':5,'num':9},
 {'name':'edge_infill','step':6,'area':(28,140),'depth':(3.1,25),'minfree':3.1,'num':8},
 {'name':'interior_infill','step':7,'area':(35,200),'depth':(3.1,95),'minfree':3.2,'num':8},
 {'name':'compact_frontage','step':5,'area':(15,95),'depth':(2.2,20),'minfree':2.2,'num':6},
]
# Don't iterate every masked pixel at the full image resolution: grid scan and sample by region.
for si,stage in enumerate(stages):
 free=allowed.copy();free[occup>0]=0
 dfree=cv2.distanceTransform(free,cv2.DIST_L2,3)
 step=stage['step'];ox=RNG.randrange(step);oy=RNG.randrange(step)
 arr=[]
 for yy in range(oy+2,H-2,step):
  mask=(free[yy,ox+2:W-2:step]>0)
  xs=np.arange(ox+2,W-2,step)[mask]
  if len(xs)==0:continue
  d0=dist[yy,xs];d1=dfree[yy,xs]
  good=(d0>=stage['depth'][0])&(d0<=stage['depth'][1])&(d1>=stage['minfree'])
  for xx in xs[good]:
   reg=int(labels[yy,xx])
   if region_area[reg]<150:continue
   style=regstyle.get(reg,'mixed');lim=style_limits.get(style,(.5,8,45))[0]
   if regused[reg]/region_area[reg]>=lim:continue
   # broad blocks are more valuable: first place substantive buildings; near road is priority
   score=(25-float(dist[yy,xx]) if si in (0,1,3,5) else float(dfree[yy,xx]))+RNG.random()*3
   arr.append((score,int(xx),int(yy)))
 arr.sort(reverse=True)
 accepted=0;attempted=0
 print('stage',stage['name'],'candidates',len(arr),'elapsed',round(time.monotonic()-START,1),flush=True)
 for _,xx,yy in arr:
  if occup[yy,xx] or not allowed[yy,xx]:continue
  reg=int(labels[yy,xx]);style=regstyle.get(reg,'mixed');target=style_limits.get(style,(.5,8,45))
  if regused[reg]/region_area[reg]>=target[0]:continue
  clearance=float(dfree[yy,xx]);edge=float(dist[yy,xx]);
  if clearance<stage['minfree']*.8:continue
  mn,mx=stage['area'];ideal=min(mx,max(mn,(min(clearance,edge)+1)**2*(2.1 if si in (0,1,3,5) else 1.9)))
  ia=int(np.searchsorted(areas,max(9,ideal*.25),'left'));ib=int(np.searchsorted(areas,min(1400,ideal*3.5),'right'))
  if ib<=ia:continue
  picks=RNG.sample(range(ia,ib),min(36,ib-ia))
  def rank(k):
   s=sources[k];h=s['height'];mnH,mxH=target[1:]
   penalty=max(0,mnH-h)/max(mnH,10)+max(0,h-mxH)/max(mxH,20)
   return abs(math.log(max(9,s['area'])/ideal))*.65+penalty*.42+min(25,reuse[s['sid']])*.035+max(0,s['aspect']-3)*.17+RNG.random()*.12
  picks.sort(key=rank)
  edge_tangent=math.atan2(float(grady[yy,xx]),float(gradx[yy,xx]))+math.pi/2
  made=False
  for k in picks[:stage['num']]:
   s=sources[k]
   if s['height']>target[2]*1.8 or (s['height']<target[1]*.5 and style in ('corporate','urban')):continue
   if s['area']>min(mx*2.5,(clearance*4.0)**2*2):continue
   a=edge_tangent-s['angle']
   angles=[a,a+math.pi/2,0,math.pi/2] if si in (0,1,3,5) else [0,a,math.pi/2]
   for ang in angles:
    attempted+=1
    if try_build(s,xx,yy,ang,reg,style,stage['name']):
     accepted+=1;made=True;break
   if made:break
 print('stage_complete',stage['name'],'added',accepted,'total_new',len(new),'attempts',attempted,'elapsed',round(time.monotonic()-START,1),flush=True)

# Exact Shapely audit of NEW candidates vs each other and existing; reject any
# new shapes that intersect anything or lie outside allowed area; keep Round Two untouched.
old_polys=[shape(ft['geometry']).buffer(0) for ft in old]
new_polys=[shape(ft['geometry']).buffer(0) for ft in new]
old_tree=STRtree(old_polys);n_tree=STRtree(new_polys)
reject=set();reasons=collections.Counter()
# New source polygons may be slightly outside mask due to raster rounding. Use mostly mask,
# and exact V17 geometry setback to ensure no crossings at geometry precision.
road_lines=[LineString(ft['geometry']['coordinates']) for ft in roads]
road_tree=STRtree(road_lines)
for i,g in enumerate(new_polys):
 if g.is_empty or not g.is_valid:
  reject.add(i);reasons['invalid_geometry']+=1;continue
 # direct older-building crossing check
 for j in old_tree.query(g):
  if g.intersection(old_polys[int(j)]).area>0.005:
   reject.add(i);reasons['old_overlap']+=1;break
 if i in reject:continue
 for j in n_tree.query(g):
  j=int(j)
  if j>=i or j in reject:continue
  if g.intersection(new_polys[j]).area>0.005:
   reject.add(i);reasons['new_overlap']+=1;break
 if i in reject:continue
 # actual road centreline plus a minimum clearance, without declaring kerb width
 for j in road_tree.query(g.buffer(2.6)):
  if g.distance(road_lines[int(j)])<2.6:
   reject.add(i);reasons['road_clearance']+=1;break
 if i in reject:continue
 # exact broader-area containment, excludes extents beyond recovered road blocks
 if g.difference(broad_union).area>0.2:
  reject.add(i);reasons['outside_broad_region']+=1
kept=[x for i,x in enumerate(new) if i not in reject]
print('Exact audit rejected',len(reject),dict(reasons),'keep new',len(kept),flush=True)

# Final artwork at true raster scale.
new_final=np.zeros((H,W),np.uint8)
for ft in kept:cv2.fillPoly(new_final,[poly2pix(shape(ft['geometry']))],1)
oldcount=int(old_area_pixel.sum());newcount=int(new_final.sum());recovered_count=int(allowed.sum())
physfinal=cv2.bitwise_or(old_area_pixel,new_final)
all_area=np.bitwise_or(gold,broad)
results={'version':'Spaciel Round Three Draft 04 — broader road-block infill','baseline_existing_round_two':len(old),
 'retained_original_position_count':originalpositions,'new_rigid_sketchup_placements':len(kept),'all_source_derived_placements':len(old)+len(kept),
 'new_source_models_unique':len({f['properties']['source_native_id'] for f in kept}),
 'all_source_definitions_unique':len({f['properties']['source_native_id'] for f in old+kept}),
 'new_by_neighborhood_style':dict(collections.Counter(f['properties']['style'] for f in kept)),
 'new_by_placement_stage':dict(collections.Counter(f['properties']['placement_kind'] for f in kept)),
 'atlas_area_m2_not_applicable':True,'all_area_pixels_at_review_resolution':int(all_area.sum()),
 'additional_review_area_pixels_after_road_hotzone_water_exclusions':recovered_count,
 'new_physical_roof_outline_pixels':newcount,'round_two_roof_outline_pixels':oldcount,
 'combined_roof_outline_pixels':int(physfinal.sum()),
 'combined_coverage_of_gold_plus_recovered_pct':round(100*physfinal.sum()/max(1,all_area.sum()),2),
 'new_placement_coverage_of_reviewable_extra_pct':round(100*newcount/max(1,recovered_count),2),
 'excluded_road_pixels_in_extra':int(np.count_nonzero(extra & roadmask)),
 'excluded_hot_zone_pixels_in_extra':int(np.count_nonzero(extra & hot)),
 'excluded_water_or_park_pixels_in_extra':int(np.count_nonzero(extra & water)),
 'exact_rejections':dict(reasons),'status':'Provisional 2D, no final 3D / terrain / coast certification',
 'note':'Broader V2 legacy road blocks are approximate. New placements preserve native model proportions. Original Round Two placements unchanged. Precise shoreline, park boundaries, actual road edges, visual composition and foundations require verification before city integration.'}
(OUTPUT/'round3_summary.json').write_text(json.dumps(results,indent=2))
(OUTPUT/'Round03_New_Placements_Private.geojson').write_text(json.dumps({'type':'FeatureCollection','metadata':{'status':'private-source-derived','source':'Original SketchUp mesh outlines; preserve commercial model rights'},'features':kept},separators=(',',':')))
(OUTPUT/'Round03_All_Placements_Private.geojson').write_text(json.dumps({'type':'FeatureCollection','metadata':{'status':'private-source-derived; REVIEW ONLY'},'features':old+kept},separators=(',',':')))

# Render citywide static map and side-by-side comparison of Round Two and Round Three.
canvas=np.empty((H,W,3),np.uint8);canvas[:]=(13,21,31)
canvas[all_area>0]=(49,62,54)
canvas[gold>0]=(82,68,42)
canvas[allowed>0]=(38,75,73)
canvas[roadmask>0]=(19,29,39)
canvas[old_area_pixel>0]=(197,160,103) # sand older
canvas[new_final>0]=(94,207,195)   # teal round three
# interior restricted zones dark
canvas[(hot>0)&(old_area_pixel==0)]=(24,28,39)
# main map saved
Image.fromarray(canvas).save(OUTPUT/'Spaciel_Round03_City_Assembly_Map.png',optimize=True)
# previous comparison: round 2 map drawn on same background.
base=np.empty((H,W,3),dtype=np.uint8);base[:]=(13,21,31)
base[all_area>0]=(40,53,47);base[gold>0]=(82,68,42);base[roadmask>0]=(19,29,39)
base[old_area_pixel>0]=(197,160,103)
source=Image.fromarray(base).resize((1050,1621),Image.Resampling.LANCZOS)
newim=Image.fromarray(canvas).resize((1050,1621),Image.Resampling.LANCZOS)
C=Image.new('RGB',(2166,1815),(11,18,28));d=ImageDraw.Draw(C)
try:
 big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
 small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
except:big=small=ImageFont.load_default()
d.text((33,22),'SPACIEL   /   ROUND THREE · RECOVERED BUILDABLE TERRITORY',fill=(238,242,242),font=big)
d.text((33,68),'ROUND TWO · 6,257 ORIGINAL-SOURCE BUILDINGS',fill=(230,183,106),font=small)
d.text((1116,68),f'ROUND THREE · {len(old)+len(kept):,} ORIGINAL-SOURCE BUILDINGS',fill=(105,213,196),font=small)
C.paste(source,(33,102));C.paste(newim,(1116,102))
d.text((33,1744),f'{len(kept):,} additional rigid source-model placements in formerly unused block territory',fill=(223,232,232),font=small)
d.text((33,1770),'Gold/sand: previous areas and placements · Teal: new allowable areas and original-SKP placements · All provisional',fill=(170,189,199),font=small)
C.save(OUTPUT/'Spaciel_Round03_Comparison.png',optimize=True)

# Export sanitized aggregate non-source-placement report for public project.
md=f'''# Spaciel — broader-block packing, Round Three / Draft 04

**Status:** Provisional 2D working layout, NOT an approved final map or a published source-model asset.

## Design decision

The historic V10 building footprints are not parcels to fill one by one. Round Two preserved 6,257 source-scale model footprints in a footprint-derived gold region, while the older October 560 road-separated urban blocks cover much more of Night City. This pass leaves the 6,257 previous placements untouched and fills additional *reviewable* area in the recovered older road-block geography.

## Output

- Previously placed: **{len(old):,}**, preserved.
- Newly placed, rigid transformations without stretching: **{len(kept):,}**.
- Total provisional building outlines: **{len(old)+len(kept):,}**.
- Distinct original SketchUp model source definitions across the combined draft: **{results['all_source_definitions_unique']:,}**.
- Coverage of the union of current gold and recovered broad blocks at 3304×5100 working raster: **{results['combined_coverage_of_gold_plus_recovered_pct']}%**. (Not comparable to Round Two gold-only percentage without noting the larger denominator.)
- Roof-outline coverage within the specifically approved-for-trial *extra* review area: **{results['new_placement_coverage_of_reviewable_extra_pct']}%**. Remaining space includes intentional gaps and candidates not verified safe.

## Constraints / QA

- No original-source geometry was rescaled, enlarged or stretched; only translation and rotation.
- Road corridor exclusion is based on current V17 cleaned lines with stylized 9–15 m width estimates and a minimum extra margin, **not certified kerb boundaries**.
- A recovered Hot Zone preserve polygon is withheld from new placements; its existing sparse Round Two treatment is unchanged.
- Highly saturated atlas water/landscape colours are conservatively excluded from new placements. This is not a complete shoreline polygon or park masterplan.
- All new polygons passed coarse mask and occupancy tests, and a post-placement source-polygon audit against existing models, other new models and road-line proximity. Unresolved tolerances and areas need a visual check.
- Source model IDs, model polygon outlines and placements remain private because the SketchUp source's redistribution rights were not established. Only aggregate counts and this method are committed publicly.

## Important limitations

This is a citywide **infill trial**, not a fully repacked skyline. Some old V10 gold polygons lie outside the recovered 560 blocks. The combined preview keeps those previous buildings but does not imply all polygon combinations are certified land. Water, actual coastlines, grades, fine road widths, and neighbourhood-scale aesthetic review remain open. No 3D viewer was altered.
'''
(OUTPUT/'round3_report.md').write_text(md)
print('SUMMARY',json.dumps(results,indent=2),'elapsed_sec',round(time.monotonic()-START,1),flush=True)