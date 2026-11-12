# Spaciel — positional integrity audit, 12 November 2026

**Scope:** 661 pin positions in the current Modular 07 / 661-geography V2 review baseline. **Read-only audit**: no locations, IDs, heights, categories, tags or bubble behaviour changed.

## Results

| Test | Result |
|---|---|
| Total pins | 661 = 536 main city + 103 city outlet + 20 main Outskirts + 2 Outskirts outlet |
| Earlier 525 calibrated source-map markers recovered | 525/525 (479 direct ID, 43 unique renamed ID, three individually ordered “The Cells”) |
| Maximum displacement from prior source-master registration | 0.042 atlas pixels |
| Outlets coinciding exactly with parent site | 105/105, by design |
| City main pins with no QA flags | 425/536 |
| City main pins with one or more non-definitive flags | 111/536 |
| Independent city main pin pairs closer than 15 source atlas px | 0 |
| Independent city main pin pairs closer than 25 source atlas px | 8 |
| Main city pins classified as water in registered Modular 07 shoreline mask | 19 |
| Additional outlet pins on water because parent is on water | 5 |
| City main pins deeper than 60m into masked water | 3 |
| City main pins more than 100 atlas pixels from V23 road centreline | 7 |
| Tentative 2045 district polygon comparison | 458 agree; 40 in another polygon; 38 outside the traced polygons |
| Added Hot Zone city sites not represented in earlier 525-source-marker calibration | 11 |

The existing source-master-to-world placement remains numerically consistent (derived world transform RMSE 0.032m east-west and 0.041m north-south in the audit fit). **This only verifies consistency with our earlier recorded source-map points, not fresh independent confirmation of every printed book icon.**

## High-value exceptions

The three main pins more than ~60m offshore by the actual 20m-resolution registered water mask are Flotsam (~738m), The Ascension (~144m) and Morro Strand Yacht Club (~63m). The first two are **intentionally waterborne in the sourcebook** (artificial island settlement and converted cruise ship), not proven placement errors. Waterfront classes can also include dock buildings, floats, boat berths and coast-resolution edge pixels.

The seven most distant pins from the incomplete Roadcraft V23 centreline network are Pacifica Arcology Ruins, Flotsam, Ashcroft Hotel, Dark Zone One, Safe Child, Ebunike Docks and The Crater. These are structures/areas whose access networks or physical extent differ from ordinary urban businesses. Do not move pins based on graph distance alone.

The 78 provisional district-polygon conflicts largely reflect **known uncertain registration of the 1396×1536 morphology atlas**. Districts assigned directly from the location register remain authoritative until the two atlases and coastal/road control points agree independently. These are not 78 confirmed bad placements.

The 11 additional Hot Zone primary pins absent from the older 525-point source calibration merit separate review of printed official markers: Ashcroft Hotel, The Crater, Crisis Center, Dark Zone One, The Dump, Eurasiabank Plaza, Graceland Medical, The N54, Safe Child, Toggle’s Temple and Totentanz.

## QA method and outputs

- 525 historical source-map point coordinates compared to current 661 location records after matching repaired canonical IDs (479 stable IDs, 43 unique same-district names and three uniquely ordered cells).
- Current source-master atlas / V23 road frame = 5175 × 7966; 1,436 graph nodes, 1,992 road paths. Distances from all 536 main city pins to nearest polyline measured exactly, in source-map pixels.
- Actual coast classification sampled from **Modular 07 V4.1** embedded shoreline texture (1112×1392, 20m grid) using the same world-coordinate formula as the shader. Wet classes 1, 2 and 3; class 255 is treated as unresolved. Outskirts aren't judged against the Night City road or district geometry.
- Provisional district polygon intersections independently recomputed for each of 536 main city pins from the stored draft morphology areas; this is an investigative comparison only.
- No automatic relocation, snapped-to-road adjustment or category changes.

The full private audit package was delivered in conversation artifacts:
`Spaciel_661_Pin_Position_Inspector.html`, `Spaciel_661_Pin_Position_Audit.csv`, `Spaciel_661_Pin_Position_Audit.json`, `Spaciel_661_Pin_Position_Findings.md`, `Spaciel_661_Pin_Position_Audit_Package.zip`.

## Recommended follow-up

Check the 11 added Hot Zone positions on the actual official marker map, then inspect the remaining coastal edge and per-district polygon discrepancies with independent control points. Recalculate provenance flags after correction. **Do not conflate parent-site placeholders with independently measured merchant positions.**

The interactive inspector passed Chromium filter, location-selection, search and rendering smoke tests with no JavaScript page errors. The main 3D viewer's WebGL2 route was not retested; this audit uses its saved data and shoreline texture.
