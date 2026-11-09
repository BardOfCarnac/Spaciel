#!/usr/bin/env python3
"""Non-destructive Spaciel source-building placement audit.

Inputs:
 - source features: GEOJSON *actual placed outlines*; polygons already transformed by
   the original SketchUp instance transform, not local definition hulls.
 - V10 approved target polygons in Atlas pixel coordinates.
 - V17 cleaned road centrelines in Atlas pixel coordinates.

No geometry is changed other than a frame conversion. Does not certify historical
identity, road width, ownership, elevation, bridge grade or building materials.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from shapely.geometry import shape, mapping
from shapely.affinity import affine_transform
from shapely.strtree import STRtree
from shapely.validation import explain_validity

HERE = Path(__file__).resolve().parent.parent
REG = HERE/'data/registration/atlas_skp_roads_v2.json'

def read_geojson(path):
    d=json.loads(Path(path).read_text(encoding='utf-8'))
    if d.get('type')!='FeatureCollection': raise ValueError(f'Expected GeoJSON FeatureCollection: {path}')
    return d['features']

def matrix_to_shapely(mat):
    """[ [a,b,xoff], [d,e,yoff] ] → Shapely [a,b,d,e,xoff,yoff]."""
    return [mat[0][0],mat[0][1],mat[1][0],mat[1][1],mat[0][2],mat[1][2]]

def transform_poly(poly,frame,config):
    if frame=='atlas_px':return poly
    if frame=='skp_world_inches':
        p=config['skp_world_xy_inches_to_skp_plan_px']
        poly=affine_transform(poly,[p['px_per_inch'],0,0,-p['px_per_inch'],p['offset_x_px'],p['offset_y_px']])
    return affine_transform(poly,matrix_to_shapely(config['skp_plan_to_atlas_matrix_3x3']))

def audit(source,sites,roads,frame,config):
    site_polys=[];site_ids=[]
    for s in sites:
        p=shape(s['geometry'])
        if p.is_empty:continue
        if not p.is_valid:p=p.buffer(0)   # index-only repair; input preserved
        if p.is_empty:continue
        site_polys.append(p);site_ids.append(str(s.get('properties',{}).get('id',s.get('id',''))))
    road_polys=[shape(r['geometry']) for r in roads if r.get('geometry') and shape(r['geometry']).geom_type in ('LineString','MultiLineString')]
    if not road_polys: raise ValueError('Road linework is empty')
    si=STRtree(site_polys);ri=STRtree(road_polys)
    out=[];features=[]
    for i,f in enumerate(source):
        props=f.get('properties',{}) or {}
        g=shape(f['geometry'])
        if g.geom_type not in ('Polygon','MultiPolygon'):raise ValueError(f'Source feature {i} must be a Polygon/MultiPolygon (got {g.geom_type})')
        if not g.is_valid: raise ValueError(f'Source feature {i} has invalid placed outline: {explain_validity(g)}')
        if g.is_empty or g.area<=0:raise ValueError(f'Source feature {i} has empty / zero-area geometry')
        p=transform_poly(g,frame,config)
        # Treat nearest lines as centreline diagnostics, NOT measured road widths.
        near=ri.nearest(p);near_d=float(p.distance(road_polys[int(near)]))
        cross=[int(j) for j in ri.query(p) if p.intersects(road_polys[int(j)]) and p.intersection(road_polys[int(j)]).length>1e-8]
        # One source model can cover several proposed plots. Record all overlaps.
        matches=[]
        for j in si.query(p):
            idx=int(j); s=site_polys[idx];inter=p.intersection(s).area
            if inter<=1e-8:continue
            union=p.area+s.area-inter
            matches.append((inter/p.area,inter/s.area,inter/union,site_ids[idx]))
        matches.sort(key=lambda x:(x[0],x[2]),reverse=True)
        best=matches[0] if matches else (0,0,0,'')
        decision='ROAD_CENTRELINE_CONFLICT' if cross else ('ROAD_NEAR_5PX_REVIEW' if near_d<5 else ('PLOT_REVIEW' if not matches else 'VISUAL_KEEP_CANDIDATE'))
        # 'VISUAL_KEEP_CANDIDATE' is NOT an approved keep or evidence of source identity.
        row={
            'instance_id':str(props.get('instance_id',props.get('id',i))),
            'source_native_id':str(props.get('source_native_id',props.get('native_id',''))),
            'source_revision':str(props.get('source_revision','UNKNOWN')),
            'native_frame':frame,
            'atlas_cx':round(p.centroid.x,3),'atlas_cy':round(p.centroid.y,3),
            'atlas_area_px2':round(p.area,3),
            'nearest_road_centerline_px':round(near_d,3),
            'road_centerline_crossings':len(cross),
            'overlapping_target_count':len(matches),
            'best_candidate_v10_id':best[3],
            'fraction_of_source_inside_best_target':round(best[0],4),
            'fraction_of_target_covered':round(best[1],4),
            'best_target_iou':round(best[2],4),
            'all_candidate_v10_ids':';'.join(m[3] for m in matches[:12]),
            'audit_flag':decision,
            'verification_status':'UNVERIFIED',
        }
        out.append(row)
        features.append({'type':'Feature','geometry':mapping(p),'properties':{**row,'original_skp_properties':props}})
    return out,features

def run(input_path,frame,targets,roads,output_dir,source_revision):
    config=json.loads(REG.read_text());source=read_geojson(input_path)
    if source_revision=='2':
        revision_warning='The saved (1).skp and (2).skp source files have identical SHA256. V2 road registration is source-frame consistent but each original site match is still only a candidate.'
    else: revision_warning='Source map placement frame should be confirmed against SKP road controls before approval.'
    rows,features=audit(source,read_geojson(targets),read_geojson(roads),frame,config)
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    file=output_dir/'source_building_position_review.csv'
    fields=['instance_id','source_native_id','source_revision','native_frame','atlas_cx','atlas_cy','atlas_area_px2',
    'nearest_road_centerline_px','road_centerline_crossings','overlapping_target_count','best_candidate_v10_id',
    'fraction_of_source_inside_best_target','fraction_of_target_covered','best_target_iou','all_candidate_v10_ids',
    'audit_flag','verification_status']
    with file.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    (output_dir/'source_building_registered_atlas.geojson').write_text(json.dumps({
        'type':'FeatureCollection','name':'unverified_native_building_placements_in_atlas','features':features},separators=(',',':')))
    from collections import Counter
    summary={'source_features_processed':len(rows),'counts_by_review_flag':dict(Counter(r['audit_flag'] for r in rows)),
      'frame_conversion':frame,'source_revision_given':source_revision,'warning':revision_warning,
      'does_not_change_site_or_road_files':True,'no_historical_identities_authenticated':True,
      'road_measurement':'centreline only; not a measured right of way'}
    (output_dir/'registration_review_summary.json').write_text(json.dumps(summary,indent=2))
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True,help='Actual placed source-building polygons GeoJSON')
    p.add_argument('--frame',choices=['skp_map_px','skp_world_inches','atlas_px'],default='skp_map_px')
    p.add_argument('--source-revision',choices=['1','2','unknown'],default='unknown')
    p.add_argument('--targets',default=str(HERE/'data/footprints/v10_approved_building_slots.geojson'))
    p.add_argument('--roads',default=str(HERE/'data/roads/v17_cleaned_road_centerlines.geojson'))
    p.add_argument('--output-dir',default='output/source_position_review')
    a=p.parse_args()
    print(json.dumps(run(a.source,a.frame,a.targets,a.roads,a.output_dir,a.source_revision),indent=2))
if __name__=='__main__':main()
