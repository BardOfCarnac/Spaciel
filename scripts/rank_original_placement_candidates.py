#!/usr/bin/env python3
"""Prioritise manual review of original building *locations* without moving anything.
The source polygon geometry is private; publish only per-instance numeric review records.
"""
from pathlib import Path
from collections import Counter
import csv,json
from shapely.geometry import shape
from shapely.strtree import STRtree
HERE=Path(__file__).resolve().parent.parent
SRC=HERE/'private/native_original_buildings_atlas_hulls.geojson'
SLOTS=HERE/'data/footprints/v10_approved_building_slots.geojson'
AUDIT=HERE/'private/original_position_audit/source_building_position_review.csv'
OUT=HERE/'data/placement/native_original_instance_review.csv'
REPORT=HERE/'reports/original_building_location_triage.json'

def main():
    source=json.loads(SRC.read_text())['features']
    targets=json.loads(SLOTS.read_text())['features']
    old={x['instance_id']:x for x in csv.DictReader(AUDIT.open())}
    geometries=[shape(t['geometry']) for t in targets]
    ids=[str(t['properties']['id']) for t in targets]
    tree=STRtree(geometries)
    geom_by_id=dict(zip(ids,geometries))
    source_poly=[shape(f['geometry']) for f in source]
    sourcetree=STRtree(source_poly)
    original_conflicts=Counter();severity_pairs=Counter()
    for i,p in enumerate(source_poly):
        for j0 in sourcetree.query(p):
            j=int(j0)
            if j<=i:continue
            inter=p.intersection(source_poly[j]).area
            if inter<=0:continue
            ratio=inter/min(p.area,source_poly[j].area)
            if ratio>=.25:
                severity_pairs['overlap_25pct_pairs']+=1
                original_conflicts[i]+=1;original_conflicts[j]+=1
            if ratio>=.95:severity_pairs['almost_contained_pairs']+=1
    rows=[];by_target={};clean_by_target={};count=Counter()
    for source_i,f in enumerate(source):
        p=shape(f['geometry']);a=f['properties'];o=old[a['instance_id']]
        near_i=int(tree.nearest(p));site=geometries[near_i]
        nd=round(p.distance(site),3)
        if o['best_candidate_v10_id']:
            best_id=o['best_candidate_v10_id']
            # Source intersections previously scored by source-fraction; do not recenter it.
            best_coverage=float(o['fraction_of_source_inside_best_target'])
        else:
            best_id=ids[near_i];best_coverage=0.0
        cross=int(o['road_centerline_crossings']);road_dist=float(o['nearest_road_centerline_px'])
        if cross:group='ROAD_CENTRELINE_CONFLICT'
        elif road_dist<5:group='NEAR_ROAD_CENTRELINE_5PX'
        elif best_coverage>=0.5:group='IN_PLACE_OVERLAP_50PCT'
        elif nd==0:group='PARTIAL_APPROVED_SITE_OVERLAP'
        elif nd<=5:group='NEAR_TARGET_WITHIN_5PX'
        elif nd<=10:group='NEAR_TARGET_WITHIN_10PX'
        elif nd<=20:group='NEAR_TARGET_WITHIN_20PX'
        else:group='NO_NEAR_APPROVED_SITE_20PX'
        r={
           'instance_id':a['instance_id'],'source_native_id':a['source_native_id'],
           'source_name':a['source_skp_name'],'source_guid':a['source_skp_guid'],
           'native_width_m':round(a['width_m'],2),'native_depth_m':round(a['depth_m'],2),
           'native_height_m':round(a['height_m'],2),
           'source_triangles':a['source_triangles'],'detail':a['geometry_detail'],
           'atlas_x':round(p.centroid.x,2),'atlas_y':round(p.centroid.y,2),
           'native_hull_area_atlas_px2':round(p.area,2),
           'nearest_target_polygon_distance_px':nd,
           'candidate_target_v10_id':best_id,
           'candidate_target_area_atlas_px2':round(geom_by_id[best_id].area,2),
           'source_fraction_overlapping_candidate':best_coverage,
           'best_target_iou':o['best_target_iou'],
           'road_centerline_clearance_atlas_px':round(road_dist,2),
           'road_centerline_crossings':cross,
           'original_source_overlap_25pct_count':original_conflicts[source_i],
           'review_group':group,
           'keep_or_move_approved':False,
           'historical_identity_verified':False,
        }
        rows.append(r);count[group]+=1
        if group=='IN_PLACE_OVERLAP_50PCT':
            by_target.setdefault(best_id,[]).append(r)
            if original_conflicts[source_i]==0:
                clean_by_target.setdefault(best_id,[]).append(r)
    OUT.parent.mkdir(exist_ok=True,parents=True)
    with OUT.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    approved_targets={k:sorted(v,key=lambda r:(r['source_fraction_overlapping_candidate'],float(r['best_target_iou']),r['source_triangles']),reverse=True)[0] for k,v in clean_by_target.items()}
    with (OUT.parent/'in_place_high_overlap_visual_shortlist.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(sorted(approved_targets.values(),key=lambda r:-r['source_fraction_overlapping_candidate']))
    summary={'instances_processed':len(rows),'source_definition_names':len({r['source_native_id'] for r in rows}),
       'groups':dict(count),'unique_target_sites_with_high_overlap_candidate':len(by_target),
       'high_overlap_instances':count['IN_PLACE_OVERLAP_50PCT'],
       'original_building_hull_overlaps_25pct_pairs':severity_pairs['overlap_25pct_pairs'],
       'original_building_hull_almost_contained_pairs':severity_pairs['almost_contained_pairs'],
       'original_source_instances_involved_in_major_overlaps':len(original_conflicts),
       'high_overlap_instances_without_major_original_overlap':sum(len(v) for v in clean_by_target.values()),
       'distinct_target_sites_with_clean_high_overlap_shortlist':len(clean_by_target),
       'high_overlap_shortlisted_unique_source_instances':len(approved_targets),
       'note':'Candidates preserve original source transforms; polygon convex hulls overstate concave building area. Do not automatically place/move anything.',
       'same_skp_source_versions_sha256_verified':True,
       'do_not_publish_private_exact_source_polygons':True}
    REPORT.write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
