# Spaciel Modular 04 — compact bubbles, sequential closure, aligned magnifier, exact focus colours

**11 November 2026 — private viewer integration.** Built by patching the actual Modular 03 V19 viewer in place, with its V23 candidate roads, irregular V17 terrain topology, V19 20m elevations, 661 pins, source-face buildings and optical water unchanged. Modular 03 remains available for rollback.

## Fixes

1. **Name-only bubble height:** When no genuine description exists, suppress the invented 'Short description to be added' line. Both the WebGL-overlay canvas bubble and accompanying DOM location detail now use compact content; canvas overall height is 206 px for ordinary names, 224 px for long names, versus the 256 px described form. Preserve the v07 hierarchy and geography footer.
2. **Bubble handoff:** On selecting a different pin, queue the new selection and play the old bubble's existing ~862 ms close track (panel → ball → original glyph) before opening the replacement. Further selections update the queued item; clicking away cancels it. This avoids a one-frame disappearance/replacement.
3. **Top-left spyglass:** Hidden search input was consuming padded flex space inside a 42 px closed control, displacing and clipping the lens. Remove the collapsed input from the flex layout, use a centered 21 px vector magnifier within the original 40×40 hit target, preserve rightward expansion and keyboard/search behaviour.
4. **Bottom spectrum focus:** Restored the approved 11 November true-icon-RGB logic from the frozen V19 focused-colour baseline and canonical [shared palette](../data/ui/spaciel_category_colours_v1.json). The gaseous focus uses the same 7 icon RGB tokens, not a separate OKLCH focus palette; remove the 245-channel cap, preserve the softer unfocused lighting and category order. Existing category icon transitions unchanged.

## Verification / limits

- All 17 Node tests pass (13 prior + 4 new); all 20 JavaScript files pass syntax checks; ZIP integrity verified.
- An isolated Playwright mobile layout check at 392 px width measured: collapsed search 42 px, centered button 40 px, hidden input display none; expanded search 376 px wide with the button at the right, and input display block.
- The test browser blocks complete local/file viewer navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`; **full viewer/WebGL2 bubble animation and category-spectrum appearance have not been visually certified on hardware**.
- Private viewer and bundled assets saved to `/Spaciel/working-data/Spaciel_Modular_04_Private.zip` and `Spaciel_Modular_04_Portable.html`. Not published publicly due to sourcebook/art-source licensing boundaries.

The key next inspection is pin-to-pin closing behaviour, short content panel sizing, mobile magnifier visibility, and the focused red/orange/yellow RGB alongside icons.