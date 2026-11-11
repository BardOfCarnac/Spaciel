# Roadcraft V23 — parallel traces absorbed within the painted road width

11 November 2026 · **Private, reversible, experimental graph cleanup**. Roadcraft V21, V22 and the current Spaciel mainline have **not** been overwritten.

## Why another pass?

V22 removed very small diamonds, close double junctions and short dead-end hairs. It still left long, narrow loops and two near-parallel links between the same pair of routing junctions, even though both traces are clearly inside the width of one originally painted street.

V23 starts with the **underlying V22 width-18 routing candidate**, and adds three distinct geometric edits:
1. **Parallel alternatives:** collapse duplicate paths with matching endpoint junctions and small symmetric corridor separation, preserving the preferred geometric route.
2. **Long, thin cycles:** if the fully rendered path geometry occupies a narrow elongated corridor, replace multiple traces with a single longitudinal centreline through their real branch-access junctions. Reattach existing external branches rather than treating close painted lines as new junctions.
3. **Parallel dead ends:** remove leaf paths when they follow another existing route nearby and in the same direction for substantially their whole length.

The condition is **road-width containment**, not simply a maximum loop perimeter. Wide real blocks, roundabouts and roads separated by more than the stroke remain.

## Default trial (22 atlas-pixel local width, approximately 34 for major roads)

| V22 width-18 graph | V23 default graph |
|---|---|
| 630 cycle-rank | **557** |
| 2,112 routing chains | **1,992** |
| one connected component | **one connected component** |

V23 made **60** duplicate parallel-path removals, **12** long-narrow loop centreline collapses and **41** close parallel-hair removals in this preset. These are edit-category counts; the **73** removed cycles are a separate graph-topology result.

Five trial widths are available: 14, 18, 22, 26, 30 atlas px. Each passed an independent Python network check for one connected component, finite coordinates, matching true path endpoints and consistent cycle rank. Browser-level desktop and mobile interaction smoke tests passed with no JavaScript page exceptions. Real map positioning and route correctness have **not** been certified against the official atlas.

## Next review

Use the **private standalone viewer** to compare V22 versus V23 and inspect each collapsed corridor. Check the official painted map and road names before accepting individual changes; local graph connectedness alone does not establish every turning restriction, pedestrian connection or route length. Avoid merging distinct carriageways or true side streets.

The portable viewer, all five complete routing graphs, local reconstruction scripts, screenshots and QA report are stored privately in the user's ChatGPT Library under `/Spaciel/working-data/`, beginning with `Spaciel_Roadcraft_V23_`. Original source maps, derived private geometry, complete viewer HTML, routing candidate files and screenshots were deliberately **not committed** to this public repository.
