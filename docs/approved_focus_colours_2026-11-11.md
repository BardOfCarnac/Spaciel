# Approved Spaciel focused category colours — 11 November 2026

**Status: APPROVED DESIGN STANDARD.** The user accepted matching the focused spectrum-bar segment to the corresponding category icon colour. This supersedes the earlier muted focus treatment in future Spaciel viewers. Preserve the previously approved V19 glyph/bubble morph unchanged.

## Canonical category colours

Use [the machine-readable palette](../data/ui/spaciel_category_colours_v1.json) as the authoritative index-to-colour mapping, shared across map icons, category bubbles and the focused bar segment. Do not create a second focused palette.

| Internal index | Category | RGB hex |
| ---: | --- | --- |
| 0 | Work & industry | `#d54ae8` |
| 1 | Leisure & culture | `#08a4f5` |
| 2 | Food & nightlife | `#42d7ff` |
| 3 | Living & lodging | `#00d79d` |
| 4 | Shopping & services | `#ffeb26` |
| 5 | Municipal | `#ff8527` |
| 6 | Civic & care | `#ff4237` |

The spectrum's visible order is index 6 to 0: red, orange, yellow, green, cyan, blue, violet. These are **map category array indices**, not new category IDs. Do not renumber or reclassify any locations.

## Behavioural contract

1. **Focused segment:** take its base colour directly from the selected category's shared icon RGB. Red/orange/yellow must no longer look dull because of dark blending, independent lightened-palette remapping, or capped channels.
2. **Unfocused segments:** retain their prior softer, gently illuminated baseline; never brighten the entire bar to achieve focus parity.
3. **Depth:** preserve the gaseous lighting, smooth flow, restrained glow and subtle shading, but do not let these recolour the selected base hue.
4. **Consistency:** a category colour change updates its map icons, bubbles and selected bar colour as one design token.
5. **No interaction regression:** retain glyph artwork, location tags/positions, filtering, search, camera and the approved visibility morph: outgoing glyph→ball→nothing **610 ms**, incoming nothing→ball→glyph starts **85 ms** later and runs **615 ms**; **720 ms** total. Unchanged icons remain visible. The spectrum bar itself does not morph.

## Implementation references

- **V19 focused-colour derivative:** the gaseous concentration core now blends directly towards the existing shared Contour icon RGB rather than independently remapped OKLCH focus colours; the former upper-channel cap is removed.
- **Integrated Review 02 derivative:** the focused segment base uses `SPACIEL_POI_DATA.colors` directly rather than a 28–48% dark colour mix filtered by brightness/saturation. Unfocused segments retain their ambient treatment.
- **Private snapshots:** `/Spaciel/approved-baselines/Spaciel_V19_True_Focus_Colours_2026-11-11.html` (SHA-256 `1548925739f37be55a38aba3ea53677304fcbe1e58f252cf504921eebedd597c`) and `/Spaciel/approved-baselines/Spaciel_Integrated_Review_02_True_Focus_Colours.html` (SHA-256 `e79f6939b5ac58ec37dbadca74bb8d3dc926046c9ebc79bf5fcc43acf62429e5`). Corresponding ZIPs/manifest are stored privately.
- **Historical morph reference:** `/Spaciel/approved-baselines/Spaciel_Approved_Category_Morph_2026-11-11.html` remains frozen and unmodified. See [the morph standard](approved_category_visibility_morph_2026-11-11.md).

## Verification

The focused-colour derivative JS passed syntax checks on 11 November 2026; the resulting appearance had not been independently inspected via real-device browser or WebGL at the time of archiving. The **design decision is approved**, and the **builds are preserved as implementation references**, not as claims of complete device validation.

**Publication boundary:** do not commit the complete private viewer HTML, licensed atlas or source-derived building/pin payloads to the public GitHub repository.
