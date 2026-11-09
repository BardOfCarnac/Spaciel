# Spaciel V19 — 556 location icon categories (review)

This branch reconciles the original sourcebook location research with the current V19 Vend-R-integrated 3D map. It preserves the 556 map points, the original `GEO_ROWS` and `GEO_SHOP_ROWS`, building models, roads, terrain, heights, and existing linked Vend-R venues. No changes are made to Supabase or the working `main` branch.

## Recover the working seven families

The 2026-11-01 icon-role exploration defined **seven families and 35 roles**. The older 3D viewer still rendered the earlier seven categories. The new mapping restores the later grouping, using the existing spectrum colours:

| Visual spectrum / family | Proposed primary pins |
|---|---:|
| Civic & Care (red) | 89 |
| Municipal (orange) | 74 |
| Shopping & Services (yellow) | 72 |
| Living & Lodging (green) | 86 |
| Food & Nightlife (cyan) | 62 |
| Leisure & Culture (blue) | 62 |
| Work & Industry (magenta) | 111 |
| **Total** | **556** |

**Review status:** 473 are matched by exact workbook ID. The other 83 are reconciled using existing local names, sourcebook sublocations, the old viewer classifications, or explicit provisional inference (65 named/sub-location rules; 6 legacy category fallbacks; 12 Executive Zone person-labelled residential locations). **175 classifications have a review flag**, including broad name-based inferences from the original worksheet. These are proposed categorical assignments; they are not 556 independently verified business descriptions.

## Use it

**Phone / browser:** Save [Spaciel_V19_Icon_Taxonomy_Installer.html](../review/Spaciel_V19_Icon_Taxonomy_Installer.html) and open it in a browser. Choose your existing `Spaciel_V19_VendR_Icon_Integration_Review.html`, tap **Build updated viewer**, then download the resulting self-contained `Spaciel_V19_556_Seven_Family_Taxonomy_Review.html`. The conversion occurs locally in the browser; no upload occurs.

**Node 18+:**
```sh
node tools/build-v19-taxonomy-viewer.mjs \
  /path/to/Spaciel_V19_VendR_Icon_Integration_Review.html \
  /path/to/Spaciel_V19_556_Seven_Family_Taxonomy_Review.html
```

The converter refuses an incorrect or already-patched source viewer. It validates each map record's name, index, coordinates, height and original category against the supplied manifest. The original `GEO_ROWS` and Vend-R occupants remain untouched; only presentation-level roles and family filtering change.

## Data files

- `data/locations/v19_location_icon_taxonomy_review.json`: 556 reconciled rows, source type, evidence tier, 35-role assignment, review flag, original geometry and legacy icon assignments
- `tools/build-v19-taxonomy-viewer.mjs`: checked HTML conversion
- `review/Spaciel_V19_Icon_Taxonomy_Installer.html`: self-contained local browser converter

**Art limitation:** where the existing 56-icon artwork lacks a suitable role (such as faith, schools, and parks), the updated viewer uses a family-coloured marker instead of misleading icon artwork. The custom final icons can be assigned later without changing the POI classification.

**Limitations:** A source-data replacement test and JavaScript syntax check have passed. The full 3D rendering has **not** been browser-tested in this environment; open the converted viewer and spot-check it before merging or replacing anything. This is a review branch, not a deployment.
