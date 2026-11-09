#!/usr/bin/env python3
"""Recheck 9 previously saved named-road V2 SKP-frame checkpoints against V17 Atlas roads.

This is a replay of previously recorded road samples, not an independent survey.
V17 centreline geometry is in Atlas px; do NOT use `night_city_2045_visual_road_layer_v17.geojson`
which is expressed in local 3D world kilometres.
"""
from __future__ import annotations
from pathlib import Path
import argparse,csv,json,statistics
from shapely.geometry import Point,shape
from shapely.strtree import STRtree
BASE=Path(__file__).resolve().parent.parent
SAMPLES={
 'Watson Blvd': [(3496.797,1326.224,0.266),(3510.226,1292.987,11.465)],
 'Kennedy Ave': [(3707.079,1296.212,4.248),(3679.848,1287.045,4.452),(3676.126,1283.433,0.718)],
 'Marina Blvd': [(3779.745,1850.800,5.692),(3784.080,1849.981,6.630),(3805.065,1829.646,9.396),(3813.886,1824.562,12.796)]}

def run(roads,output_csv):
    lines=[]
    for f in json.loads(Path(roads).read_text())['features']:
        g=shape(f['geometry'])
        if g.geom_type in ('LineString','MultiLineString'):lines.append(g)
    if not lines:raise ValueError('Atlas road lines are empty; did you accidentally supply 3D kilometre coordinates?')
    bounds=(min(p.bounds[0] for p in lines),min(p.bounds[1] for p in lines),max(p.bounds[2] for p in lines),max(p.bounds[3] for p in lines))
    if not(500 < bounds[2] < 20000 and 500 < bounds[3] < 20000):raise ValueError('Road coordinates must be Atlas pixels, not kilometres/metres')
    t=STRtree(lines)
    reg=json.loads((BASE/'data/registration/atlas_skp_roads_v2.json').read_text())
    m=reg['skp_plan_to_atlas_matrix_3x3']
    data=[]
    for road,points in SAMPLES.items():
        for i,(sx,sy,skp_resid) in enumerate(points,1):
            ax=m[0][0]*sx+m[0][1]*sy+m[0][2]
            ay=m[1][0]*sx+m[1][1]*sy+m[1][2]
            oldx=64.552809+.695716713*sx
            oldy=2076.549160+.695716713*sy
            def nearest(x,y):
                q=Point(x,y)
                return q.distance(lines[int(t.nearest(q))])
            data.append({'road':road,'checkpoint':i,'original_skp_plan_x_px':round(sx,3),
              'original_skp_plan_y_px':round(sy,3),'atlas_v2_x_px':round(ax,3),'atlas_v2_y_px':round(ay,3),
              'v2_nearest_v17_centerline_px':round(nearest(ax,ay),3),
              'v1_nearest_v17_centerline_px':round(nearest(oldx,oldy),3),
              'prior_v2_nearest_skp_road_trace_px':skp_resid,
              'independent_control':'No — saved V2 reference-point replay'})
    Path(output_csv).parent.mkdir(parents=True,exist_ok=True)
    with open(output_csv,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    return {'checkpoints':len(data),'max_v2_nearest_v17_atlas_px':max(x['v2_nearest_v17_centerline_px'] for x in data),
     'max_v1_nearest_v17_atlas_px':max(x['v1_nearest_v17_centerline_px'] for x in data),
     'mean_v2_nearest_v17_atlas_px':round(statistics.mean(x['v2_nearest_v17_centerline_px'] for x in data),3),
     'note':'Saved source-road controls replayed on current V17 centreline graph; does not prove a new source SKP revision uses same frame.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--roads',default=str(BASE/'data/roads/v17_cleaned_road_centerlines.geojson'))
    p.add_argument('--output',default=str(BASE/'data/registration/v2_named_road_checkpoints_against_v17.csv'))
    a=p.parse_args();print(json.dumps(run(a.roads,a.output),indent=2))