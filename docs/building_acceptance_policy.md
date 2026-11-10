# Spaciel building acceptance: closed-shell minimum

**Confirmed user choice — 10 November 2026.**

The goal is to place as much original SketchUp architecture as possible, generally retaining its proportions and approximate source position. Detailed facade geometry is **not required**.

## Minimum visible standard

A building is acceptable as a basic representation when it looks like an enclosed building: standing sides/walls and a top (flat, sloped or otherwise), a believable volume, and no obvious missing face, open top, exposed interior, or thin staple-shaped wire frame. A simple box or plain roof is completely acceptable.

A low triangle count, absence of windows, textures or ornament, and a plain massing shape **must not disqualify** a model by themselves. Different polygon counts imply different detail, not necessarily different usability. Keep source geometry at its real proportions wherever possible.

## Automatic screening versus actual acceptance

- **Automated minimum:** connected, watertight positive-volume shell, nonzero width/depth/height. For the current 137-instance in-place shortlist, all 137 pass the first two tests, all have positive dimensions and at least two vertical levels. The 77 with fewer than 36 triangular faces are **not rejected or marked incomplete** for that reason.
- **Visual check remains:** does the recovered shape read as a building with walls and a top, rather than a staple or other malformed form? Is it clearly a freestanding building or a constituent component that needs grouping?
- **Independent siting check remains:** collision with roads/other buildings, coastline, ground/foundation, source-versus-site fit, landmark handling and whether a small move is useful. Passing the minimum geometry requirement never auto-approves a placement.
- **Source identity:** preserve source model and placement IDs, no reshaping merely to fit a target footprint, and no claim of verified historical site identity based solely on overlap.

The new register `data/review/in_place_137_minimum_closed_shell_screen.csv` flags 137 automatic geometry passes with **visual review pending** and **no placement approval**. Detailedness is advisory metadata, not a gate.
