"""Regression checks for Spaciel reviewed primary/secondary classifications."""
import copy
import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "location_facets", ROOT / "scripts" / "apply_location_primary_secondary.py"
)
facets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(facets)
OVERLAY = json.loads((ROOT / "data/decisions/location_primary_secondary_v1.json").read_text())


def sample():
    locations, audit = [], []
    for decision in OVERLAY["records"]:
        row = {
            "id": decision["location_id"], "name": decision["location_name"],
            "category": decision["original_primary"]["category"],
            "role": decision["original_primary"]["role"],
            "subtype": "original subtype",
            "x": "123.450", "z": "-76.250", "height": "11.125",
            "short_description": "Original source description",
        }
        locations.append(row)
        audit.append({"id": row["id"], "name": row["name"], "proposed_display_tag": "Generic"})
    locations.append({
        "id": "", "name": "Unmatched location", "category": "work",
        "role": "work:industry", "subtype": "Industry & utilities",
        "x": "21", "z": "-3", "height": "0", "short_description": "Keep me"
    })
    audit.append({"id": "", "name": "Unmatched location", "proposed_display_tag": "Industrial site"})
    return locations, audit


class ClassificationTests(unittest.TestCase):
    def test_applies_all_reviewed_and_preserves_geometry_and_descriptions(self):
        locations, audit = sample()
        before = copy.deepcopy(locations)
        converted, issues, count = facets.build(locations, audit, OVERLAY)
        self.assertEqual(count, 38)
        self.assertEqual(len(converted), 39)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["issue"], "missing_canonical_id")
        for old, new in zip(before, converted):
            for field in ("id", "name", "x", "z", "height", "short_description"):
                self.assertEqual(old[field], new[field])
        self.assertEqual(before, locations)
        keyed = {r["name"]: r for r in converted}
        self.assertEqual(keyed["The Night City Animal Shelter"]["role"], "civic:medical")
        self.assertEqual(keyed["University Cargo Bay"]["role"], "living:homes")
        self.assertEqual(keyed["GraffitiX"]["role"], "leisure:culture")
        self.assertIn("Maelstrom", keyed["Totentanz"]["affiliations"])
        self.assertEqual(keyed["Unmatched location"]["role"], "work:industry")
        self.assertFalse(keyed["Unmatched location"]["review_overlay_applied"])

    def test_name_mismatch_blocks_import(self):
        rows, audit = sample()
        rows[0]["name"] = "Unexpected Name"
        with self.assertRaises(ValueError):
            facets.build(rows, None, OVERLAY)

    def test_stale_classification_blocks_import(self):
        rows, audit = sample()
        rows[0]["role"] = "work:warehouses"
        with self.assertRaises(ValueError):
            facets.build(rows, None, OVERLAY)

    def test_tag_audit_identity_mismatch_blocks_import(self):
        rows, audit = sample()
        audit[0]["name"] = "Wrong"
        with self.assertRaises(ValueError):
            facets.build(rows, audit, OVERLAY)

    def test_duplicate_reviewed_id_blocks_import(self):
        rows, audit = sample()
        rows.append(copy.deepcopy(rows[0]))
        with self.assertRaises(ValueError):
            facets.build(rows, None, OVERLAY)


if __name__ == "__main__":
    unittest.main()
