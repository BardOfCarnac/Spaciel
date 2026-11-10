#!/usr/bin/env python3
"""Prepare Spaciel's reviewed POI classifications without touching live V19."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def build(register, audit, overlay):
    decisions = {r["location_id"]: r for r in overlay["records"]}
    assert len(decisions) == len(overlay["records"]), "Duplicate review IDs"
    counts = Counter(r.get("id", "") for r in register if r.get("id"))
    found, applied, issues, enriched = set(), 0, [], []
    if audit is not None:
        if len(audit) != len(register):
            raise ValueError("Tag-audit row count differs from source register")
        for i, (loc, tag) in enumerate(zip(register, audit)):
            if (loc.get("id"), loc.get("name")) != (tag.get("id"), tag.get("name")):
                raise ValueError(f"Tag-audit identity/order mismatch at row {i}")

    for index, raw in enumerate(register):
        row = dict(raw)  # source coordinates and descriptive fields stay unchanged
        loc_id = row.get("id", "")
        review = decisions.get(loc_id)
        source_category = row.get("category")
        source_role = row.get("role")
        if not loc_id:
            issues.append({"index": index, "issue": "missing_canonical_id", "name": row.get("name")})
        elif counts[loc_id] > 1:
            issues.append({"index": index, "issue": "duplicate_canonical_id", "id": loc_id})
            if review:
                raise ValueError(f"Reviewed ID is ambiguous: {loc_id}")

        row["original_category"] = source_category
        row["original_role"] = source_role
        if review:
            old, new = review["original_primary"], review["primary"]
            if row.get("name") != review["location_name"]:
                raise ValueError(f"Reviewed ID name mismatch: {loc_id}")
            if (source_category, source_role) not in (
                (old["category"], old["role"]), (new["category"], new["role"])
            ):
                raise ValueError(f"Stale/unexpected classification for {loc_id}")
            row["category"], row["role"] = new["category"], new["role"]
            row["subtype"] = overlay["role_subtypes"][new["role"]]
            found.add(loc_id)
            applied += 1

        tag_text = (audit[index].get("proposed_display_tag", "") if audit else "")
        if review:
            tag_text = review["display_tag"]
        row["display_tag"] = tag_text
        row["secondary_functions"] = review.get("secondary_functions", []) if review else []
        row["affiliations"] = review.get("affiliations", []) if review else []
        row["context_tags"] = review.get("context_tags", []) if review else []
        row["needs_function_validation"] = bool(review and review.get("needs_function_validation"))
        row["review_overlay_applied"] = bool(review)
        # For map integration, colour derives from row['category'],
        # pictogram from row['role']; secondary metadata never changes either.
        enriched.append(row)

    if found != set(decisions):
        raise ValueError("Reviewed POI IDs absent from source: " + str(sorted(set(decisions) - found)))
    return enriched, issues, applied


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--register", required=True, help="Original 556-location category CSV")
    ap.add_argument("--overlay", default="data/decisions/location_primary_secondary_v1.json")
    ap.add_argument("--display-audit", help="Optional 556-row display-tag CSV")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    register = read_csv(args.register)
    audit = read_csv(args.display_audit) if args.display_audit else None
    with Path(args.overlay).open(encoding="utf-8") as handle:
        overlay = json.load(handle)
    locations, issues, applied = build(register, audit, overlay)
    output = Path(args.out_dir)
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "Spaciel_Locations_Primary_Secondary_556.csv"
    json_path = output / "Spaciel_Locations_Primary_Secondary_556.json"
    issue_path = output / "Spaciel_Location_ID_QA.json"
    columns = list(locations[0])
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for loc in locations:
            writer.writerow({
                key: json.dumps(value, ensure_ascii=False) if isinstance(value, list) else value
                for key, value in loc.items()
            })
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({
            "schema": "spaciel.location_export.v1",
            "source_register_count": len(register),
            "reviewed_count": applied,
            "live_viewer_modified": False,
            "locations": locations
        }, handle, indent=2, ensure_ascii=False)
    with issue_path.open("w", encoding="utf-8") as handle:
        json.dump({"source_id_issues": issues, "total": len(issues)}, handle, indent=2)
    print(json.dumps({"locations": len(locations), "reviewed": applied,
                      "id_issues": len(issues), "outputs": [str(csv_path), str(json_path), str(issue_path)]}))


if __name__ == "__main__":
    main()
