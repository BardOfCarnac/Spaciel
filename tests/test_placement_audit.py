#!/usr/bin/env python3
import unittest,sys,json,tempfile
from pathlib import Path
from shapely.geometry import Polygon,mapping
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT/'scripts'))
from audit_skp_original_placements import transform_poly, audit, matrix_to_shapely, run
from shapely.affinity import affine_transform
CONF=json.loads((ROOT/'data/registration/atlas_skp_roads_v2.json').read_text())
class RegistrationAuditTests(unittest.TestCase):
    def test_inverse_registration(self):
        skp=Polygon([(3450,1300),(3460,1300),(3460,1310),(3450,1310)])
        atlas=transform_poly(skp,'skp_map_px',CONF)
        back=affine_transform(atlas,matrix_to_shapely(CONF['atlas_to_skp_plan_matrix_3x3']))
        self.assertLess(skp.hausdorff_distance(back),1e-7)
    def test_world_plan_mapping(self):
        square=Polygon([(0,0),(10,0),(10,10),(0,10)])
        atlas=transform_poly(square,'skp_world_inches',CONF)
        self.assertGreater(atlas.area,0)
        self.assertAlmostEqual(atlas.centroid.x, transform_poly(square,'skp_world_inches',CONF).centroid.x,places=8)
    def test_road_and_slot_review_never_moves_geometry(self):
        p=Polygon([(90,90),(110,90),(110,110),(90,110)])
        f=[{'type':'Feature','geometry':mapping(p),'properties':{'instance_id':'A','native_id':'1'}}]
        sites=[{'type':'Feature','geometry':mapping(p),'properties':{'id':'original-1'}}]
        road=Polygon([(99,80),(101,80),(101,120),(99,120)]).boundary
        roads=[{'type':'Feature','geometry':mapping(road),'properties':{}}]
        rows,geom=audit(f,sites,roads,'atlas_px',CONF)
        self.assertEqual(rows[0]['audit_flag'],'ROAD_CENTRELINE_CONFLICT')
        self.assertEqual(rows[0]['best_candidate_v10_id'],'original-1')
        self.assertEqual(geom[0]['geometry'],mapping(p))
        self.assertEqual(rows[0]['verification_status'],'UNVERIFIED')
if __name__=='__main__':unittest.main()