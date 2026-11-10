#!/usr/bin/env python3
"""Rebuild a NON-AUTHORITATIVE review layer of earlier city-block coverage.

Requires: shapely. Input GeoJSONs/CSV are kept in the Spaciel repo.
Does not change approved building positions or plot assignments.
"""
import csv
import json
from pathlib import Path
from shapely.geometry import shape, LineString, mapping
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT/'data/blocks/recovered_october_560_character_blocks.geojson'
GOLD = ROOT/'data/blocks/gold_buildable_regions_v1.geojson'
ROADS = ROOT/'data/roads/v17_cleaned_road_centerlines.geojson'
WIDTHS = ROOT/'data/roads/v17_road_width_classes_by_chain.csv'
OUT = ROOT/'data/blocks/recovered_additional_territory_REVIEW_ONLY.geojson'
PX_PER_M = 0.372  # working V17 map-to-atlas scale, not a surveyed metric
EXTRA_MARGIN_PX = 2.0  # provisional, per side
MIN_POLY_AREA_PX2 = 20

def parts(geometry):
    if geometry.is_empty:return
    if geometry.geom_type == 'Polygon':yield geometry
    elif geometry.geom_type in ('MultiPolygon','GeometryCollection'):
        for member in geometry.geoms:yield from parts(member)

def main():
    src=json.loads(LEGACY.read_text());gold=json.loads(GOLD.read_text());roads=json.loads(ROADS.read_text())
    source_union=unary_union([shape(f['geometry']).buffer(0) for f in src['features']])
    gold_union=unary_union([shape(f['geometry']).buffer(0) for f in gold['features']])
    widths={int(r['chain_id']):float(r['width_m']) for r in csv.DictReader(WIDTHS.open())}
    line_exclusions=[]
    for feature in roads['features']:
        k=int(feature['properties']['chain_id'])
        line=shape(feature['geometry'])
        if line.is_empty: continue
        assert isinstance(line,LineString)
        buffer_px=widths[k]*PX_PER_M/2+EXTRA_MARGIN_PX
        line_exclusions.append(line.buffer(buffer_px,quad_segs=2))
    road_mask=unary_union(line_exclusions)
    # Preserve gold. Candidate territories include ONLY portions of old blocks not already covered.
    candidate=source_union.difference(gold_union).difference(road_mask)
    features=[]
    for i,p in enumerate(parts(candidate)):
        if p.area < MIN_POLY_AREA_PX2:continue
        features.append({'type':'Feature','properties':{'review_only':True,'approx_area_atlas_px2':round(p.area,1),'source':'October V6 character blocks outside gold footprint-derived areas'},'geometry':mapping(p.simplify(1,preserve_topology=True))})
    metadata={'status':'UNAPPROVED_CANDIDATE_REVIEW','recovered_old_blocks':len(src['features']), 'gold_regions':len(gold['features']), 'review_territory_area_atlas_px2':round(candidate.area,1), 'do_not_auto_place':True, 'not_checked':['coastline/water','parks','protected open spaces','road cross sections','bridges and elevated grades','foundation elevation','manual district visual review'], 'working_buffer':'stylised local/major road widths with 2px margin; no surveyed kerbs', 'frame':'5175x7966 Atlas image pixels'}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({'type':'FeatureCollection','metadata':metadata,'features':features},separators=(',',':')))
    print('Review-only extra area polygons:',len(features),'total Atlas px²:',round(candidate.area))
if __name__=='__main__':main()