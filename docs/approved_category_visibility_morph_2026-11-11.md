# Approved Spaciel category visibility morph — 2026-11-11

Status: **APPROVED — preserve unchanged as reference**.

## Frozen viewer snapshot

The full self-contained V19 HTML is stored in the Spaciel Library project:
`/Spaciel/approved-baselines/Spaciel_Approved_Category_Morph_2026-11-11.html`

A ZIP with the same HTML and manifest is stored at:
`/Spaciel/approved-baselines/Spaciel_Approved_Category_Morph_2026-11-11.zip`

SHA-256 of the HTML: `6cb84d3379e50ca17c4c518d44e2716622c3e61bf86fe39a21159ff5dcfc5d9f`

The original working viewer remains untouched. This is an approved reference snapshot, not a deployment. It includes 661 location pins (556 main plus 105 individual Vend-R outlets), category assignments, display tags, Contour icons and expanding bubbles.

## Accepted behaviour

- All icon hide/disappear actions use **glyph → ball → nothing**.
- All icon show/appear actions use **nothing → ball → glyph**.
- Incoming icons overlap with departing icons: no empty map interval.
- Departing icons last **610 ms**, arriving icons start **85 ms** after departure begins and run **615 ms**; total filter change window **720 ms**.
- When selecting the first category from All, keep relevant icons stable; morph away only icons that no longer qualify.
- The same disappearance applies any time an icon gets hidden in a future UI.
- Returning to All uses emergence for newly visible icons.
- Spectrum bar itself does not morph. Category membership, map positions and tags are not changed by the animation.

## Reference implementation

The frozen HTML contains `window.SPACIEL_VISIBILITY_MORPH`:

```js
window.SPACIEL_VISIBILITY_MORPH = {
  totalMs: 720, outMs: 610, inDelayMs: 85, inMs: 615,
  smooth(a, b, v) {
    const t = Math.max(0, Math.min(1, (v-a)/(b-a)));
    return t*t*(3-2*t);
  },
  sampleOut(v) {
    const p = Math.max(0, Math.min(1, v));
    const smooth = this.smooth.bind(this);
    return {
      contraction: smooth(0, .72, p),
      scale: 1 - .93*smooth(.69, 1, p),
      opacity: 1 - smooth(.70, 1, p)
    };
  },
  state(mode, elapsed) {
    const u = mode === 'out'
      ? Math.max(0, Math.min(1, elapsed/this.outMs))
      : 1 - Math.max(0, Math.min(1, (elapsed-this.inDelayMs)/this.inMs));
    return this.sampleOut(u);
  }
};
```

Do not treat this minimal object alone as a complete integration; the frozen HTML also contains both the 2D and 3D draw paths and their per-icon transition state. The 2D mobile fallback was visually checked; 3D renderer still needs device verification. Make future iterations in a newly versioned build and keep this baseline intact.
