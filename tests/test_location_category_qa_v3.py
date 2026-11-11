"""Regression tests: Spaciel's seven categories and 28 reused roles stay stable."""
import json
import unittest
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
V2 = json.loads((ROOT / "data/locations/spaciel_locations_556_tag_qa_v2_2026-11-10.json").read_text())
V3 = json.loads((ROOT / "data/locations/spaciel_locations_556_category_qa_v3_2026-11-11.json").read_text())
PATCH = json.loads((ROOT / "data/locations/spaciel_locations_v19_patch_v3_2026-11-11.json").read_text())

EXPECTED = {
    "NC2045-LOC-WATSON-DEVELOPMENT-194-SNACK-SHACK": ("shopping", "shopping:general", "General retailer"),
    "NC2045-LOC-UPPER-MARINA-074-MIDNIGHT-ARMS-REGIONAL-OFFICE": ("shopping", "shopping:specialist", "Specialist retailer"),
    "NC2045-LOC-PORT-OF-NIGHT-CITY-153-HARBOR-PATROL-HQ": ("municipal", "municipal:security", "Security / faction facility"),
}

class LocationCategoryQATests(unittest.TestCase):
    def test_fixed_556_records_unique_ids_and_existing_vocabulary(self):
        rows = V3["records"]
        self.assertEqual(len(rows), 556)
        self.assertEqual(len({r["id"] for r in rows}), 556)
        self.assertEqual(len({r["role"] for r in rows}), 28)
        self.assertEqual(
            {r["role"] for r in rows},
            {r["role"] for r in V2["records"]},
        )
        self.assertEqual(
            {r["category"] for r in rows},
            {"work", "leisure", "food", "living", "shopping", "municipal", "civic"},
        )
        for r in rows:
            self.assertTrue(r["display_tag"])
            self.assertEqual(r["role"].split(":")[0], r["category"])

    def test_only_three_new_corrections_and_no_geometry_or_provenance_changes(self):
        old, new = V2["records"], V3["records"]
        changed = {}
        for a, b in zip(old, new):
            self.assertEqual(a["record_index"], b["record_index"])
            for field in ("id", "name", "district", "x", "z", "height", "source", "sourcebook_basis"):
                self.assertEqual(a[field], b[field], (a["name"], field))
            if (a["category"], a["role"], a["display_tag"]) != (b["category"], b["role"], b["display_tag"]):
                changed[b["id"]] = (b["category"], b["role"], b["display_tag"])
            else:
                self.assertEqual(a, b)
        self.assertEqual(changed, EXPECTED)

    def test_v19_patch_matches_current_classification_for_all_locations(self):
        self.assertEqual(len(PATCH["by_record_index"]), 556)
        for row, patch in zip(V3["records"], PATCH["by_record_index"]):
            for left, right in (("record_index", "record_index"), ("id", "location_id"), ("name", "match_name"), ("category", "category"), ("role", "role"), ("subtype", "subtype"), ("display_tag", "display_tag")):
                self.assertEqual(row[left], patch[right], (row["name"], left, right))

if __name__ == "__main__":
    unittest.main()
