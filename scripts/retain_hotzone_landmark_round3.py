#!/usr/bin/env python3
"""Non-destructive Round 03 Hot Zone landmark retention, on top of existing placements.
Retain the largest approved V10 Hot Zone footprint as reserved original massing.
Do NOT assert that its exact original SketchUp model is identified.
"""
from pathlib import Path
import json, collections, math, io, base64
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import shape, Polygon, LineString, mapping
from shapely.ops import unary_union
from shapely.strtree import STRtree

ROOT=Path('/mnt/data');OUT=ROOT/'spaciel_hotzone';OUT.mkdir(exist_ok=True)
V10=json.loads((ROOT/'files/Night_City_V10_Completed_Footprints.geojson').read_text())
source=next(f for f in V10['features'] if f['properties']['id']=='original-4125')
landmark=shape(source['geometry']);assert landmark.is_valid and landmark.area>8000
oldfc=json.loads((ROOT/'spaciel_round3/Round03_All_Placements_Private.geojson').read_text())
assert len(oldfc['features'])==7858
buf=2.5
removed=[];keep=[]
for feat in oldfc['features']:
    if shape(feat['geometry']).intersects(landmark.buffer(buf)):
        removed.append({'id':feat['properties']['placement_id'],'method':feat['properties'].get('method',''),'source_native_id':feat['properties']['source_native_id']})
    else:keep.append(feat)
print('Removed',len(removed),'kept',len(keep))
# Avoid inventing original model identity or elevation; exact building source remains unresolved.
props={
 'placement_id':'landmark-hotzone-largest-retained',
 'historic_footprint_id':'original-4125',
 'landmark_kind':'largest approved V10 Hot Zone footprint by mapped ground area',
 'method':'RETAIN_PREVIOUS_LARGE_HOT_ZONE_MASSING',
 'native_skp_source_verified':False,
 'geometry_source':'Night_City_V10_Completed_Footprints.geojson',
 'footprint_area_atlas_px2':round(landmark.area,1),
 'nominal_height_m':None,
 'visual_status':'original large-building outline reserved; detailed 3D model assignment pending',
 'approved_position':True,
 'protected_from_automatic_infill':True,
 'note':'Keep distinctive major building; use historical silhouette, not a new stretched SKP model.'}
f={'type':'Feature','id':'landmark-hotzone-largest-retained','properties':props,'geometry':source['geometry']}
features=keep+[f]
summary={
 'phase':'Round Three landmark retention revision',
 'baseline_placements':7858,
 'small_source_placements_removed_for_landmark_clearance':len(removed),
 'removed_ids':[x['id'] for x in removed],
 'retained_source_buildings':len(keep),
 'protected_large_hot_zone_landmarks':1,
 'revised_total_footprint_objects':len(features),
 'protected_landmark_id':'original-4125',
 'protected_landmark_area_atlas_px2':round(landmark.area,1),
 'building_to_building_clearance_atlas_px':buf,
 'landmark_true_native_skp_mesh_identified':False,
 'existing_3d_city_modified':False,
 'status':'working 2D placement map; not yet converted into existing 3D geometry'
}
# Verify graph centerline clearance, no significant overlaps with landmark
roadsj=json.loads((ROOT/'files/night_city_2045_cleaned_display_lines.geojson').read_text())
roads=[LineString(v['geometry']['coordinates']) for v in roadsj['features']]
summary['road_centerline_clearance_atlas_px']=round(min(x.distance(landmark) for x in roads),2)
assert summary['road_centerline_clearance_atlas_px']>8
assert not any(shape(x['geometry']).intersects(landmark.buffer(buf-1e-6)) for x in keep)

(ROOT/'spaciel_hotzone_landmark_restored_footprint.geojson').write_text(json.dumps({'type':'FeatureCollection','metadata':{'source':'Previously approved V10 largest Hot Zone footprint','rights':'derived planning geometry, not private SKP meshes','status':'landmark reserve; review source-model assignment'},'features':[f]},separators=(',',':')))
(OUT/'Spaciel_Round03_With_HotZone_Landmark_PRIVATE.geojson').write_text(json.dumps({'type':'FeatureCollection','metadata':summary,'features':features},separators=(',',':')))
(OUT/'hotzone_retention_summary.json').write_text(json.dumps(summary,indent=2))
(OUT/'hotzone_removed_buildings.json').write_text(json.dumps(removed,indent=2))

# Browser source layers use 3304x5100 atlas-aligned raster, downsize to HTML assets.
W,H=3304,5100; SW=1450; SH=round(H*SW/W);SX=W/5175;SY=H/7966
old_buildings=np.zeros((H,W,4),np.uint8)
new_buildings=np.zeros_like(old_buildings)
landmark_layer=np.zeros_like(old_buildings)
road_layer=np.zeros_like(old_buildings)

def topts(feat):return np.rint(np.asarray(feat['geometry']['coordinates'][0],float)*[SX,SY]).astype(np.int32)
for feat in keep:
    q=topts(feat)
    color=(93,214,192,250) if feat['properties'].get('method','').startswith('ROUND_03_') else (230,181,102,255)
    layer=new_buildings if feat['properties'].get('method','').startswith('ROUND_03_') else old_buildings
    cv2.fillPoly(layer,[q],color)
    cv2.polylines(layer,[q],True,(32,52,56,255),1,cv2.LINE_AA)
cv2.fillPoly(landmark_layer,[topts(f)],(251,231,182,255))
cv2.polylines(landmark_layer,[topts(f)],True,(247,105,75,255),5,cv2.LINE_AA)
for road in roadsj['features']:
    q=np.rint(np.asarray(road['geometry']['coordinates'],float)*[SX,SY]).astype(np.int32)
    if len(q)>1:cv2.polylines(road_layer,[q],False,(126,153,180,155),2,cv2.LINE_AA)

atlas=Image.open(ROOT/'files/spaciel_v19_atlas_high_res_2.png').convert('RGB')
base=atlas.resize((SW,SH),Image.Resampling.LANCZOS)
comp=Image.blend(Image.new('RGB',base.size,(9,17,29)),base,.33).convert('RGBA')
old_img=Image.fromarray(old_buildings,'RGBA').resize((SW,SH),Image.Resampling.LANCZOS)
new_img=Image.fromarray(new_buildings,'RGBA').resize((SW,SH),Image.Resampling.LANCZOS)
land_img=Image.fromarray(landmark_layer,'RGBA').resize((SW,SH),Image.Resampling.LANCZOS)
road_img=Image.fromarray(road_layer,'RGBA').resize((SW,SH),Image.Resampling.LANCZOS)
# composite citywide
result=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(comp,road_img),old_img),new_img),land_img)
result.save(OUT/'Spaciel_Round03_HotZone_Landmark_Citywide.png',optimize=True)
# Crop visible to just Hot Zone neighbourhood
xmin,ymin,xmax,ymax=(1990,3180,3000,4070)
x0=int(xmin/5175*SW);y0=int(ymin/7966*SH);x1=int(xmax/5175*SW);y1=int(ymax/7966*SH)
scale_crop=3
before=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(comp,road_img),old_img),new_img).crop((x0,y0,x1,y1)).resize(((x1-x0)*scale_crop,(y1-y0)*scale_crop),Image.Resampling.LANCZOS)
after=result.crop((x0,y0,x1,y1)).resize(((x1-x0)*scale_crop,(y1-y0)*scale_crop),Image.Resampling.LANCZOS)
# At zoom, labels
Wc,Hc=before.size
pad=18;gap=20;top=78;bottom=70
sheet=Image.new('RGB',(Wc*2+2*pad+gap,Hc+top+bottom),(10,18,29));d=ImageDraw.Draw(sheet)
try:
 bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
 sm=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
except: bold=sm=ImageFont.load_default()
d.text((pad,13),'HOT ZONE: BEFORE — smaller infill',font=bold,fill=(226,185,112))
d.text((pad+Wc+gap,13),'AFTER — largest earlier landmark retained',font=bold,fill=(243,225,185))
d.text((pad,48),'Round Three baseline',font=sm,fill=(175,189,202))
d.text((pad+Wc+gap,48),'Original-4125 large footprint protected',font=sm,fill=(175,189,202))
sheet.paste(before.convert('RGB'),(pad,top));sheet.paste(after.convert('RGB'),(pad+Wc+gap,top))
d.text((pad,top+Hc+18),f'{len(removed)} competing small placements removed; all remaining placements preserved',font=sm,fill=(218,226,234))
d.text((pad,top+Hc+41),'Exact SketchUp mesh for the retained landmark still needs matching.',font=sm,fill=(175,189,202))
sheet.save(OUT/'Spaciel_HotZone_Largest_Building_Before_After.png',optimize=True)

# Single-file lightweight review, not published; visual layer toggles and Hot Zone jump.
def as_data(im,ext='PNG'):
    b=io.BytesIO();im.save(b,format=ext,optimize=True,quality=75)
    return f'data:image/{ext.lower()};base64,'+base64.b64encode(b.getvalue()).decode()
imgs={'terrain':as_data(base,'JPEG'),'old':as_data(old_img),'new':as_data(new_img),'landmark':as_data(land_img),'roads':as_data(road_img)}
points=[]
for feat in keep:
    p=feat['properties'];points.append([round(float(p['centre_atlas_x']),1),round(float(p['centre_atlas_y']),1),p['placement_id'],p.get('source_native_id',''),p.get('method','')])
points.append([round(landmark.centroid.x,1),round(landmark.centroid.y,1),'landmark-hotzone-largest-retained','original-4125','RETAIN_PREVIOUS_LARGE_HOT_ZONE_MASSING'])
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Spaciel · Hot Zone landmark retained</title><style>
*{box-sizing:border-box}html,body{margin:0;height:100%;overflow:hidden;background:#09131f;color:#e8f0f5;font:13px system-ui}canvas{position:fixed;inset:0;width:100%;height:100%;touch-action:none;cursor:grab}.panel{position:fixed;z-index:4;top:12px;left:12px;width:min(350px,calc(100% - 24px));background:#102133ef;border:1px solid #456072;border-radius:12px;padding:14px;box-shadow:0 10px 25px #0007}.panel h1{font-size:15px;margin:0 0 6px}.sub{color:#bbcad4;font-size:11px;line-height:1.5}.tog{display:flex;align-items:center;gap:7px;margin:8px 0}.tog input{accent-color:#e8b777}.swatch{width:11px;height:11px;border-radius:2px}button{color:#e9f4fa;background:#244158;border:1px solid #597487;border-radius:7px;padding:8px 9px;margin:4px 4px 0 0;cursor:pointer}.foot{font-size:10px;color:#a4b8c8;line-height:1.4;margin-top:11px}.inspector{position:fixed;right:12px;bottom:12px;background:#102133ed;border:1px solid #456072;border-radius:11px;padding:12px;display:none;z-index:4;max-width:320px}@media(max-width:680px){.panel{top:auto;bottom:10px;left:10px;width:calc(100% - 20px);padding:10px}.sub,.foot{display:none}.tog{display:inline-flex;margin-right:10px;font-size:11px}.panel h1{font-size:13px}.inspector{bottom:auto;top:12px}}
</style></head><body><canvas id="map"></canvas><div class="panel"><h1>SPACIEL · HOT ZONE LANDMARK</h1><p class="sub">Round Three with the largest earlier Hot Zone building footprint retained. Unchanged SketchUp layouts everywhere else.</p>
<label class="tog"><input type="checkbox" data-layer="old" checked><span class="swatch" style="background:#e6b566"></span>Round Two</label>
<label class="tog"><input type="checkbox" data-layer="new" checked><span class="swatch" style="background:#5dd6c0"></span>Round Three</label>
<label class="tog"><input type="checkbox" data-layer="landmark" checked><span class="swatch" style="background:#fbe7b6"></span>Hot Zone landmark</label>
<label class="tog"><input type="checkbox" data-layer="roads"><span class="swatch" style="background:#8ea5b7"></span>Roads</label>
<button id="jump">View Hot Zone</button><button id="whole">Whole city</button><button id="before">Before / after</button><button id="zin">+</button><button id="zout">−</button>
<p class="foot">7,858 baseline placements. '''+str(len(removed))+''' smaller placements removed; one large historic footprint retained. Its exact original SKP mesh is not yet authenticated.</p></div><div class="inspector" id="info"></div><script>
const IMGS='''+json.dumps(imgs,separators=(',',':'))+''';const POINTS='''+json.dumps(points,separators=(',',':'))+''';const WW='''+str(SW)+''',HH='''+str(SH)+''';const cv=document.getElementById('map'),ctx=cv.getContext('2d'),imgs={},flags={old:true,new:true,landmark:true,roads:false};let zoom=1,xoff=0,yoff=0,winW=innerWidth,winH=innerHeight,pts=new Map(),lastdist=0,dragged=false;
for(const k in IMGS){const im=new Image();im.onload=draw;im.src=IMGS[k];imgs[k]=im}
function resize(){winW=innerWidth;winH=innerHeight;const pr=Math.min(devicePixelRatio||1,2);cv.width=Math.round(winW*pr);cv.height=Math.round(winH*pr);fitCity()}
function fitCity(){zoom=Math.min((winW-18)/WW,(winH-18)/HH);xoff=(winW-WW*zoom)/2;yoff=(winH-HH*zoom)/2;draw()}
function focus(cx,cy,wide=950,high=900){zoom=Math.min((winW-24)/(WW*wide/5175),(winH-24)/(HH*high/7966));xoff=winW/2-(cx/5175)*WW*zoom;yoff=winH/2-(cy/7966)*HH*zoom;draw()}
function draw(){const pr=Math.min(devicePixelRatio||1,2);ctx.setTransform(pr,0,0,pr,0,0);ctx.fillStyle='#09131f';ctx.fillRect(0,0,winW,winH);ctx.save();ctx.translate(xoff,yoff);ctx.scale(zoom,zoom);for(const [k,a] of [['terrain',.34],['roads',flags.roads?1:0],['old',flags.old?1:0],['new',flags.new?1:0],['landmark',flags.landmark?1:0]]){const im=imgs[k];if(a&&im&&im.complete&&im.naturalWidth){ctx.globalAlpha=a;ctx.drawImage(im,0,0,WW,HH)}}ctx.restore();ctx.globalAlpha=1}
function zoomAt(f,cx=winW/2,cy=winH/2){let z=Math.max(.06,Math.min(50,zoom*f));let fact=z/zoom;xoff=cx-(cx-xoff)*fact;yoff=cy-(cy-yoff)*fact;zoom=z;draw()}
for(const inp of document.querySelectorAll('input[data-layer]'))inp.onchange=()=>{flags[inp.dataset.layer]=inp.checked;draw()};document.getElementById('jump').onclick=()=>focus(2460,3590,970,880);document.getElementById('whole').onclick=fitCity;document.getElementById('zin').onclick=()=>zoomAt(1.5);document.getElementById('zout').onclick=()=>zoomAt(.65);document.getElementById('before').onclick=()=>{flags.landmark=!flags.landmark;document.querySelector('input[data-layer=landmark]').checked=flags.landmark;draw()};
cv.onpointerdown=e=>{cv.setPointerCapture(e.pointerId);pts.set(e.pointerId,[e.clientX,e.clientY]);dragged=false};cv.onpointermove=e=>{if(!pts.has(e.pointerId))return;let p=pts.get(e.pointerId),dx=e.clientX-p[0],dy=e.clientY-p[1];pts.set(e.pointerId,[e.clientX,e.clientY]);if(Math.abs(dx)+Math.abs(dy)>3)dragged=true;if(pts.size===1){xoff+=dx;yoff+=dy}else{const all=[...pts.values()],dist=Math.hypot(all[0][0]-all[1][0],all[0][1]-all[1][1]);if(lastdist)zoomAt(dist/lastdist,(all[0][0]+all[1][0])/2,(all[0][1]+all[1][1])/2);lastdist=dist}draw()};cv.onpointerup=e=>{if(!dragged&&pts.size===1){let x=(e.clientX-xoff)/zoom/WW*5175,y=(e.clientY-yoff)/zoom/HH*7966;let best=null,bd=1e9;for(const pt of POINTS){const d=(pt[0]-x)**2+(pt[1]-y)**2;if(d<bd){bd=d;best=pt}}if(best&&Math.sqrt(bd)<Math.max(18,22/Math.max(.5,zoom))){const isLand=best[2].startsWith('landmark-');const info=document.getElementById('info');info.style.display='block';info.textContent=isLand?'Original-4125 · historic largest Hot Zone footprint (SKP model pending)':best[2]+' · Original source '+best[3]}}pts.delete(e.pointerId);lastdist=0};cv.onpointercancel=e=>{pts.delete(e.pointerId);lastdist=0};cv.addEventListener('wheel',e=>{e.preventDefault();zoomAt(e.deltaY>0?.82:1.22,e.clientX,e.clientY)},{passive:false});document.getElementById('info').onclick=()=>document.getElementById('info').style.display='none';window.onresize=resize;resize();focus(2460,3590,970,880);
</script></body></html>'''
(OUT/'Spaciel_Round03_HotZone_Landmark_Review.html').write_text(html)
print(json.dumps(summary,indent=2))