# Spaciel Realisation 11 — complete screened source-definition recovery

11 November 2026 · **Private original SketchUp extraction and tentative landmark review**; no city placement changes.

## Source recovery

The user-supplied source binary SHA256 was independently verified against the previous registration: `17317588df75a4bea8a87ad86d0438ff112c693f6c54e4ca9da4fa4c53842ee0`.

Of the original working catalogue's **4,470** screened building definitions:
- **3,079** definitions already underlie current placed direct-face source models (Realisation 07/08).
- **100** additional previously unused large definitions were recovered in Realisation 09/10.
- **1,291** previously unused definitions have now been extracted from the exact SketchUp source; all 1,291 generated GLBs reopened with valid finite vertices and face indices, representing **59,400** new direct-face triangles.
- Of the 1,291: **533** have catalogue ground area at least 500 m², **758** smaller. Of the 533 large, 528 have usable original-envelope screening, while five are held for repair. In total, eight of the newly extracted models carry existing envelope-repair flags.

Thus direct-face source geometry has been recovered for **all 4,470 definitions in this screened catalogue**. This is **not** a claim that all nested SketchUp components, materials, every SketchUp definition in the file, source architecture details, or every city site is complete/verified.

## Expanded large-building review

- **633** recovered-but-unplaced large definitions in the private viewer: old 100 + new 533.
- **656** approximate original-source instance positions; nine newly recovered large definitions have no top-level instance reference.
- Preliminary status distribution for the 551 newly recovered original-instance anchors: **180** coarse coastline concerns, **155** approximate V17 road contacts, **38** existing-building overlap cases, **178** outside previously recovered 560-block polygons. Masks are indicative and not official lot constraints.
- A narrow **27-model / 28-instance urban review shortlist** avoids the coarse water and V17 road exclusions and falls inside older road-separated block areas, but overlaps existing smaller provisional buildings. These may warrant *selective repacking*—not automatic replacement or reinstatement. A source model and its instance can be part of a larger original assembly, so nearby source instances must be reviewed together.
- Historic SKP anchor coordinates may lie well offshore or far beyond developed areas; they might represent a staging workspace or imperfect registration. They are **rough hints, not trustworthy final positions**.

The private viewer provides source-derived mesh thumbnails, original-size/angle silhouette previews, approximate source-instance navigation, a priority filter, preliminary collision hints and unapproved proposal export. No original building was relocated or deleted. The city remains at **7,993** current placement objects with **7,981** registered original direct-face mesh uses, **556** tagged pins and V17 road fallback / experimental V21 roads.

## QA
- All new 1,291 GLBs reopened and passed finite coordinate/index checks.
- Portable standalone desktop/mobile browser smoke tests passed: **633 models**, **656** original anchors, **27** priority-filtered source models, source preview interactions and **556** locations; no JavaScript errors.
- Modular JavaScript was checked through a browser with script sources inlined because this environment blocks local file and local HTTP navigation; this does **not** substitute for a real served modular test.
- Native on-device WebGL2 rendering for the full city and complete native-source mesh appearance are **still unverified**.
- No newly recovered large building was incorporated into the city's approved geometry.

## Private files and publication boundary
Private ChatGPT Library folder `/Spaciel/working-data/`:
- `Spaciel_Realisation_11_Expanded_Large_Viewer.html` — portable combined-city large-model review
- `Spaciel_Realisation_11_Review_and_Modular.zip` — private modular review build and catalogue
- `Spaciel_Realisation_11_Newly_Recovered_1291_GLBS_PRIVATE.zip` — additional source-derived mesh library
- `priority_urban_anchor_candidates.csv`, `new_large_origins_qa.csv`, `mesh_reopen_qa.json`, preview/contact sheet and README

**Do not publish the private HTML, GLBs, source geometry, thumbnails, source site coordinates or original SketchUp binary** to this public repository until redistribution rights are verified. This report contains only aggregate findings.

## Next restoration pass
Visually review the 27 urban-site candidates against the authoritative atlas and city character, identify related source-model parts, reserve major-building sites, then relocate/repack only the specific smaller provisional objects required. Include the other 633 source models in the private review catalogue, not in the live city until accepted.
