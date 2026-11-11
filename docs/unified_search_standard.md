# Spaciel unified geographic search — standard

**Canonical geographic coverage, reviewed 10 November 2026; expanding search-bar UI approved for implementation 11 November 2026.** This is the reusable version of the V19 search approved for Spaciel. It applies to full-map viewers and any map search UI. Its repository home is the search module, not another 31 MB standalone viewer.

## Coverage and behaviour

- **24 official districts.** Searching a district name returns the district itself and selecting it frames its area.
- **11 mapped neighbourhoods.** Selection centres the neighbourhood within its parent district.
- **527 named streets.** Selection centres and highlights the mapped street geometry. The V23 original-map street-transfer data remain a working registration: surface the provisional and review flags; never imply uncertain alignment is definitive.
- **Location pins** from the current live map dataset. Selection uses the existing colour/category rules and pin-to-bubble interaction.
- **Vend-R venues** within parent locations. Selection opens the parent location bubble and focuses the linked venue; do not invent a standalone entrance or extra pin.

Results carry distinct DISTRICT, NEIGHBOURHOOD, STREET, PLACE or VENUE tags. Search is case- and accent-insensitive, begins at two characters, returns at most 50 results, and sorts exact-name > prefix > substring > contextual pin match, breaking ties by district > neighbourhood > street > pin > venue.

## Files

- `src/search/spaciel-search.js` — standard index/matching, renderer-neutral destinations and responsive search panel handler.
- `src/search/spaciel-search.css` — expanding top search bar, carried magnifier, the slim result dropdown and responsive rules.
- `data/search/unified_geographic_v1.json` — the exact 24 district / 11 neighbourhood / 527 street dataset extracted from the approved V19 search prototype.
- `tests/test_unified_search.js` — executable search regression tests.

## Integration

Include the CSS and JavaScript files from the repository and place the established V19 search elements in the viewer. The host application supplies its own live location pin array.

```html
<!-- These familiar V19 IDs are moved into a single top search bar by mount(). -->
<button type="button" id="geo-search-button" aria-label="Open Night City search">⌕</button>
<div id="geo-search-panel" aria-label="Search suggestions">
  <input type="search" id="geo-search-input" placeholder="Search places, districts or streets…" autocomplete="off">
  <div id="geo-search-results"></div>
</div>
<link rel="stylesheet" href="src/search/spaciel-search.css">
<script src="src/search/spaciel-search.js"></script>
```

```js
const geography = await fetch('data/search/unified_geographic_v1.json')
  .then(response => {
    if (!response.ok) throw Error('Search data unavailable: ' + response.status);
    return response.json();
  });
const idx = SpacielSearch.createIndex({geography, locations: GEO_POINTS});
SpacielSearch.mount({
  index: idx,
  trigger: document.getElementById('geo-search-button'),
  panel: document.getElementById('geo-search-panel'),
  input: document.getElementById('geo-search-input'),
  results: document.getElementById('geo-search-results'),
  onSelect: (hit, target) => spSearchNavigate(hit)
});
```

The approved unified-search V19 integration has a `spSearchNavigate(hit)` adapter with the expected `{kind, payload}` shape, so this can replace its query/UI event handling while preserving the established camera and bubble behaviour. Remove the older pin-only search handlers when wiring it up; **do not attach two handlers to the same search controls**.

The `target` argument from `SpacielSearch.destination(hit)` is useful for another renderer: districts contain prototype-frame bounds, neighbourhoods prototype-frame points, streets V17 local-road coordinates and the full traced polylines, and pins/venues map-world locations plus stable location/shop IDs.

### Map registration

Do not interpret search coordinates as GPS. V19 uses prototype 900 × 1390 coordinates for districts/ neighbourhoods and V17 local-road coordinates for streets. The known V19 street-to-bitmap adapter is:

```js
const roadToBitmap = ([x,y]) => [
  (x * 0.1538 - 0.54) * 3304 / 792,
  (y * 0.15373 - 0.29) * 5100 / 1224
];
// For 3D: bmpToWorld(...roadToBitmap([x,y]))
// For 2D: use roadToBitmap([x,y]) as pixel coordinates
```

Always revalidate the transform when Roadcraft or the district geometry is revised. The future production viewer should frame full district polygons when available rather than treating prototype bounding rectangles as surveyed boundaries.


## Expanding search-bar behaviour (11 November 2026)

- A single rounded-square magnifier starts at the top-right. On activation, the **same button** depresses briefly and its parent track expands leftward to nearly the screen width; the magnifier stays against the right edge and travels with it.
- The input is part of that expanding track, **not** in a separate modal/window. It becomes editable as the track opens. Press **Enter** or activate the magnifier again to search; both choose the top-ranked current result, using the existing navigation adapter. Tapping a suggestion chooses that specific result.
- A compact results panel appears *below* the expanded bar when there is a nonempty query. The registered labels, geographic index, result ranking and navigation semantics are unchanged.
- **Escape**, or tapping outside, collapses the search bar. On a mobile screen the bar expands to nearly the full viewport width. Users who request reduced motion do not get the expansion/press animation.
- The desktop expansion width is at most 880 px, falling back to the available screen width. Timing: approximately 90 ms before width expansion, 470 ms width animation, 420 ms brief depressed-surface response. It is intentionally low-gloss, not a glass panel.
- Use **only** the current `SpacielSearch.mount()` handler. The legacy on-click popup and input listeners must be removed in the host viewer before it is mounted. Keep the magnifier element itself rather than replacing it with another icon.

## Repository and copyright boundaries

The full V19 HTML and its embedded viewer assets are **not** committed because the public Spaciel repository does not establish redistribution rights for the commercial/sourcebook artwork or original SKP assets. The saved V19 viewer stays in the private Spaciel working files. This repository module plus the working derived search index is the reusable implementation; adding these files alone does not deploy the full viewer or publish a live site.

Run search tests with `node --test tests/test_unified_search.js`.
