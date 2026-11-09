#!/usr/bin/env python3
"""Recover original placed building polygons from the EXACT saved SKP source.

Writes original-geometry-derived polygon outlines to PRIVATE folder only;
never upload source meshes / raw outlines to a public code repository without
clearing the redistribution rights of the original SketchUp architecture.

Output Atlas polygons are observational QA, not final site assignments.
"""
from __future__ import annotations
import argparse,csv,zipfile,json,sys,struct
from pathlib import Path
import numpy as np
from shapely.geometry import MultiPoint,mapping
from shapely.affinity import affine_transform
HERE=Path(__file__).resolve().parent.parent
from extract_skp_original_instances import chunks,first_child,nested_id,EXPECTED_HASH
import hashlib
from audit_skp_original_placements import transform_poly

def main():
    p=argparse.ArgumentParser();p.add_argument('--instances',default=str(HERE/'private/native_original_top_level_instances.csv'))
    p.add_argument('--screen-package',required=True,help='Private screening package; do not publish source geometry')
    p.add_argument('--skp',required=True,help='Exact user-supplied original SKP binary')
    p.add_argument('--output',default=str(HERE/'private/native_original_buildings_atlas_hulls.geojson'))
    args=p.parse_args()
    raw=list(csv.DictReader(open(args.instances)))
    with zipfile.ZipFile(args.screen_package) as z:
        screens={int(r['source_native_id']):r for r in csv.DictReader(z.read('Native_SKP_Building_Screen_4470.csv').decode().splitlines())}
    approved={k:v for k,v in screens.items() if v.get('building_envelope_pass')=='True'}
    registered=json.loads((HERE/'data/registration/atlas_skp_roads_v2.json').read_text())
    if hashlib.sha256(Path(args.skp).read_bytes()).hexdigest()!=EXPECTED_HASH:
        raise ValueError('Unexpected SKP source hash; original instance placements not verified for this input')
    with zipfile.ZipFile(args.skp) as z: data=z.read('model.dat')
    root={t:(p,n) for t,p,n in chunks(data,6,len(data))}
    defsec=first_child(data,*first_child(data,*root[0x1f9],0x1770),0x1771)
    # Cache only direct XY vertex coordinates for screened source definitions.
    # Closed-building-envelope screening was completed independently in the source catalogue.
    vertex_shapes={}
    for tag,st,ln in chunks(data,defsec[0],defsec[0]+defsec[1]):
        if tag!=0x157c:continue
        container=first_child(data,st,ln,0x1388)
        if not container:continue
        properties={t:(p,n) for t,p,n in chunks(data,container[0],container[0]+container[1])}
        if 0x7d0 not in properties or 0x1389 not in properties:continue
        sid=nested_id(data,*properties[0x7d0])
        if sid not in approved:continue
        vp,vlen=properties[0x1389]
        xy=[]
        for _,vst,vln in chunks(data,vp,vp+vlen):
            fields={t:(p,n) for t,p,n in chunks(data,vst,vst+vln)}
            if 0x9c5 in fields and fields[0x9c5][1]==24:
                x,y,z=struct.unpack_from('<3d',data,fields[0x9c5][0]);xy.append((x,y))
        poly=MultiPoint(xy).convex_hull if len(xy)>=3 else None
        vertex_shapes[sid]=poly if poly and poly.geom_type=='Polygon' and poly.area>1e-3 else None
    cached=vertex_shapes;features=[];skipped=[]
    for i,r in enumerate(raw):
        k=int(r['source_native_id']);
        if k not in approved:continue
        hull=cached.get(k)
        if hull is None:continue
        m=[float(r[x]) for x in ('m00','m01','m10','m11','world_x_inches','world_y_inches')]
        world=affine_transform(hull,m)
        atlas=transform_poly(world,'skp_world_inches',registered)
        if atlas.area<1e-10 or not atlas.is_valid:continue
        vals={
          'instance_id':str(r['instance_id']), 'source_native_id':str(k),
          'source_revision':'(2).skp, SHA256 identical to (1).skp',
          'source_skp_name':approved[k].get('skp_name',''),
          'source_skp_guid':approved[k].get('skp_guid',''),
          'width_m':float(approved[k]['width_m']),
          'depth_m':float(approved[k]['depth_m']),
          'height_m':float(approved[k]['height_m']),
          'source_triangles':int(approved[k]['triangles']),
          'geometry_detail':approved[k]['geometry_detail'],
          'source_polygon_type':'convex hull of all definition vertices, after native original instance affine transform',
          'original_instance_transform_retained':True,
          'historical_site_identity_authenticated':False,
        }
        features.append({'type':'Feature','geometry':mapping(atlas),'properties':vals})
        if (i+1)%4000==0: print('processed',i+1,'of',len(raw),'accepted',len(features),flush=True)
    out={'type':'FeatureCollection','name':'PRIVATE_exact_source_placed_hulls_in_atlas_px','features':features}
    Path(args.output).parent.mkdir(exist_ok=True,parents=True)
    Path(args.output).write_text(json.dumps(out,separators=(',',':')))
    print(json.dumps({'usable_source_definition_ids':len(approved),'placed_usable_original_instances':len(features),
        'distinct_placed_usable_definitions':len({f['properties']['source_native_id'] for f in features}),
        'screened_definitions_unplaced':len(set(approved)-{int(f['properties']['source_native_id']) for f in features}),
        'screened_geometry_extraction_failed':len(skipped),
        'output_file_private':args.output},indent=2))
if __name__=='__main__':main()
