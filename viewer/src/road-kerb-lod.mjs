/** Zoom-level road presentation for Spaciel V33.
 * One corridor, one centreline, one width: visual kerbs and pavements emerge with zoom.
 * Widths are atlas-pixel graphic estimates, not surveyed real-world dimensions.
 * This is a purely cartographic effect; it never edits routing geometry.
 */
export function clamp01(n) { return Math.max(0, Math.min(1, n)); }
export function smoothstep(a, b, x) {
  const t = clamp01((x - a) / (b - a));
  return t * t * (3 - 2 * t);
}
/** Returns widths in atlas pixels for drawing in the existing atlas coordinate frame. */
export function roadDetailAtZoom(path, zoomPxPerAtlasPx, mode = 'adaptive') {
  if (!Number.isFinite(zoomPxPerAtlasPx) || zoomPxPerAtlasPx <= 0) throw new Error('Positive zoom required');
  if (!Number.isFinite(path?.width) || path.width <= 0) throw new Error('V33 road width required');
  const projectedWidth = path.width * zoomPxPerAtlasPx;
  const reveal = mode === 'edges' ? 0 : mode === 'kerbs' ? 1 : smoothstep(9, 27, projectedWidth);
  const potentialPavement = { local: 2.8, medium: 3.7, arterial: 5.6 }[path.roadClass] ?? 2.8;
  return {
    projectedWidthPx: projectedWidth,
    reveal,
    roadwayWidthAtlasPx: path.width,
    kerbLipAtlasPx: .78 * reveal + .64 * (1 - reveal) / Math.max(zoomPxPerAtlasPx, .2),
    pavementAtlasPx: potentialPavement * reveal,
    status: reveal < .2 ? 'edges' : reveal < .83 ? 'emerging-kerbs' : 'kerbs-and-pavement',
  };
}
function stroke(ctx, points, width, colour, opacity = 1) {
  if (!Array.isArray(points) || points.length < 2 || width <= 0) return;
  ctx.globalAlpha = opacity;
  ctx.strokeStyle = colour;
  ctx.lineWidth = width;
  ctx.beginPath();
  ctx.moveTo(points[0][0], points[0][1]);
  for (let i = 1; i < points.length; i++) ctx.lineTo(points[i][0], points[i][1]);
  ctx.stroke();
}
/** Draw all roads in separate passes so connecting intersections share one road surface.
 * Expects ctx already transformed into the atlas coordinate frame; use visiblePaths to cull offscreen streets.
 * Optional `mode` is adaptive (default), edges, or kerbs (inspection override).
 */
export function drawRoadsAtZoom(ctx, visiblePaths, zoom, {mode = 'adaptive'} = {}) {
  const paths = visiblePaths;
  if (!Array.isArray(paths)) throw new Error('Road paths array required');
  const oldAlpha = ctx.globalAlpha, oldJoin = ctx.lineJoin, oldCap = ctx.lineCap;
  ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  const info = paths.map(p => roadDetailAtZoom(p, zoom, mode));
  // Outside band: the thin distant outline resolves into a pavement strip.
  paths.forEach((p, i) => {
    const d = info[i];
    if (d.pavementAtlasPx > .025) {
      stroke(ctx, p.points, p.width + 2 * d.pavementAtlasPx + 1.5 / zoom, '#172731', .72 * d.reveal);
      stroke(ctx, p.points, p.width + 2 * d.pavementAtlasPx, '#586e73', .71 * d.reveal);
    }
  });
  // Kerb lip wraps the single corridor; never create a second navigable road.
  paths.forEach((p, i) => {
    const d = info[i];
    stroke(ctx, p.points, p.width + 2 * d.kerbLipAtlasPx, '#a3c2c2', .58 + .33 * d.reveal);
  });
  // All roadway strokes together remove interior kerb lines across junction openings.
  paths.forEach(p => stroke(ctx, p.points, p.width, p.roadClass === 'arterial' ? '#33444a' : '#27363f', 1));
  ctx.globalAlpha = oldAlpha; ctx.lineJoin = oldJoin; ctx.lineCap = oldCap;
}
