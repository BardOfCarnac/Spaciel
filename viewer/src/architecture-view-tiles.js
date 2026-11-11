/**
 * Spaciel camera-aware native architecture tile selection.
 * Pure source-independent helper; this file contains NO SketchUp/model data.
 *
 * Camera position is atlas-centred; width/height in CSS pixels, scale in
 * CSS pixels per atlas pixel. The approximate 2D projected bounds intentionally
 * include margin for tall buildings and tilt; this is not exact 3D frustum culling.
 *
 * Returns nearby tile IDs sorted by camera proximity, capped to maxTiles.
 */
export function selectNativeArchitectureTiles({
  manifest,
  centerX,
  centerY,
  viewportWidth,
  viewportHeight,
  scale,
  yawRadians = 0,
  pitchRadians = 0,
  minNativeScale = 0.20,
  maxTiles = 16,
  marginX = 200,
  marginY = 260,
}) {
  if (!manifest?.tiles || !(scale >= minNativeScale)) return [];
  const cw = viewportWidth / (2 * scale) + marginX;
  const ch = viewportHeight /
      (2 * scale * Math.max(0.26, Math.cos(pitchRadians))) + marginY;
  const c = Math.cos(yawRadians);
  const s = Math.sin(yawRadians);
  const rx = Math.abs(cw * c) + Math.abs(ch * s);
  const ry = Math.abs(cw * s) + Math.abs(ch * c);
  return Object.entries(manifest.tiles)
    .filter(([, tile]) => {
      const [minx, miny, maxx, maxy] = tile.bounds;
      return maxx >= centerX - rx && minx <= centerX + rx &&
          maxy >= centerY - ry && miny <= centerY + ry;
    })
    .sort(([, a], [, b]) => {
      const [ax, ay, ax2, ay2] = a.bounds;
      const [bx, by, bx2, by2] = b.bounds;
      return Math.hypot((ax + ax2) / 2 - centerX, (ay + ay2) / 2 - centerY) -
          Math.hypot((bx + bx2) / 2 - centerX, (by + by2) / 2 - centerY);
    })
    .slice(0, Math.max(0, Math.floor(maxTiles)))
    .map(([id]) => id);
}
