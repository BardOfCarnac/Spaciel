# Spaciel — original SketchUp architectural review, pass 2

**Date:** 9 November 2026  
**Project:** Night City 2045 / Spaciel  
**Status:** inspection candidates, not approved replacements or live map changes.

## Purpose

The original model should guide architectural character and be retained in or near its original source position wherever practical. The V10 footprints are approximate target sites, not templates for stretching original architecture. Keep the approved roads, shoreline and terrain stable. Smaller original buildings can populate genuine infill gaps. No scaling, move, or replacement was applied in this pass.

## Reassessment of the 137 in-place shortlist

The earlier 137 selected source models were prioritised because at least half of each *source* convex hull overlapped a planned V10 target and they did not have a major overlap with another screened source hull. That **does not mean** the source and target occupy similar ground areas. The threshold is asymmetric, especially where the V10 target represents a large development site.

| Geometric review bucket | Count | Meaning |
| --- | ---: | --- |
| Large footprint overlap | 12 | Source/target polygon IoU >= 0.45; strongest direct location/scale visual checks |
| Partially aligned | 23 | Source largely inside target and covers >=25% of target |
| Small original within larger target | 61 | Source largely inside target but covers <25%: potentially useful for infill, not complete one-for-one replacement |
| Partial crossing | 41 | Source projects into part of target; review arrangement and road context |
| **Total** | **137** | Every record remains provisional |

Only **7** have polygon IoU >=0.50. No candidate exceeds 0.70. The **median IoU is 0.152**. Thus calling all 137 well-matched buildings would overstate the evidence.

We extracted the corresponding original source-derived GLBs for all 137 and audited their mesh structure. Seven private contact sheets provide isometric geometry previews for all 137; representative sheets have been inspected, but each item still needs individual architectural review. **All 137 have one connected, watertight mesh shell** in the recovered source-derived GLB, but that is not proof of a complete architectural building. **77 models contain fewer than 36 triangles** (simple massing/roof geometry); 60 have at least 36 triangles. Contact-sheet previews show many simple untextured solids; their source provenance is genuine, but extra modelling may still be necessary to achieve the intended street-level architectural detail.

No confirmed historical SKP-to-V10 building identity has been established. All original positions are under the recovered road-derived V2 Atlas transform, not the old density match. The underlying hull shapes are conservative convex-hull approximations and can overstate complex concave building footprints.

## New, non-destructive small-translation candidates

We screened **552** original source placements that do not cross or approach within five Atlas pixels of a cleaned V17 road centreline, are not already in the earlier in-place shortlist, and have no recorded major original-source hull overlap. For each we evaluated nearby approved sites within 18 Atlas pixels, testing small translations (not scaling or rotation).

This produced **127** geometrically feasible source/target translation proposals. Retaining one candidate per original source and per target site leaves **84 distinct, provisional small-move proposals**. Each is at most **12 Atlas pixels** from the original position, was selected to raise the fraction of source hull inside its proposed target to at least 68%, stays at least 5 Atlas pixels from a V17 road centreline and does not incur a screened source-hull overlap exceeding 25% of the smaller outline. Selection prioritises better source coverage and modest moves; it does not certify safe construction setbacks or terrain foundation fit.

Five candidates meet a stricter first-inspection filter: <=8-pixel translation, >=75% source-hull coverage, >=20% target-site coverage and >=8-pixel road-centreline clearance:

| Source instance | Proposed target | Shift (atlas px) | Source inside target after move | Target covered |
| --- | --- | ---: | ---: | ---: |
| 5061582 | original-937 | 6 | 97.5% | 38.0% |
| 4942979 | original-6672 | 6 | 86.1% | 28.5% |
| 5123852 | original-4923 | 4 | 97.3% | 26.6% |
| 4570095 | gap-8342 | 6 | 77.7% | 23.1% |
| 3540532 | original-670 | 8 | 76.3% | 62.7% |

**Not yet checked:** verified full road widths and junction geometry, coast/water polygon exclusion, foundations/grade/terrain, canonical landmark identities, group/component dependency in the wider original SKP hierarchy, rendering appearance/texture, or visual approval of individual 3D silhouettes. Site-overlap conflicts already flagged in the original V10 plan also remain.

## Private, directly openable review website

`Spaciel_Original_Buildings_Architecture_Review.html` provides 221 visual-review records (137 in place + 84 proposed translations) and includes:

- Local plan showing V10 target polygons, cleaned road centrelines and original SKP hulls, plus a moved outline where relevant;
- Rotatable triangular source-derived 3D geometry, native dimensions and independent source-versus-target coverage metrics;
- Source search, category filters, model geometry ordering, map zoom/pan, review labels and note-taking;
- An exported JSON of the user's manual decisions. Nothing is automatically applied to the city or repository.

It embeds geometry from the original SKP and is therefore **private**, not suitable for publishing to a public repository without checking redistribution rights. The website has been tested by executing its full source in Chromium; the browser reported no JavaScript errors, and filters and map/model rendering worked. `file://` navigation was blocked in the testing environment, so opening the downloaded file on every device/browser remains unverified.

## Public repository outputs

- `data/review/in_place_137_architectural_structure_triage.csv` — per-instance fit, geometric simplicity and connectivity flags.
- `data/review/small_move_candidates_no_scaling.csv` — translation proposals only, with displacement, source and target coverage, and centreline clearance.
- `data/review/small_move_first_five.csv` — practical first inspection priorities.
- `reports/architecture_review_phase2.md` — this report.

The private original SKP, exact 4,902 native hull polygons, full source GLBs and offline review website are deliberately excluded from the public repository.

## Next decision

Review the twelve stronger in-place matches and five best small translations in the private viewer, then decide whether each original source mesh has enough design character for production use, should be grouped with neighbouring SketchUp objects, or should serve only as an existing shell needing detail. Keep any approvals as explicit versioned placement records, never as a silent rewrite of V10 geometry.

## Acceptance-policy update — 10 November 2026

The user has clarified that **simple enclosed building forms are acceptable**: sides/walls plus a top, without a staple-like open appearance. The earlier discussion of 77 models under 36 triangles reflects detail classification **only**, not a defect or a requirement for additional modelling. All 137 are eligible at the initial one-shell watertight stage; manual silhouette inspection, distinction from partial components, and all placement constraints remain to be reviewed. Refer to `docs/building_acceptance_policy.md` and `data/review/in_place_137_minimum_closed_shell_screen.csv`. This update does not approve placement or change any geometry.
