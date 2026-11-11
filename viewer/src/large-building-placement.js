/**
 * Generic Spaciel large-building placement geometry helpers.
 * Source-independent; consumers supply their own licensed model polygons.
 * All calculations use the 5175 × 7966 working atlas pixel frame.
 */
export function sourceHullAtAtlas(centredHull, centre, angleDegrees, sourceToAtlas2x2) {
  const theta = angleDegrees * Math.PI / 180;
  const c = Math.cos(theta), s = Math.sin(theta);
  return centredHull.map(([x, y]) => {
    const u = c*x - s*y, v = s*x + c*y;
    return [
      centre[0] + sourceToAtlas2x2[0][0]*u + sourceToAtlas2x2[0][1]*v,
      centre[1] + sourceToAtlas2x2[1][0]*u + sourceToAtlas2x2[1][1]*v,
    ];
  });
}
export function polygonBounds(polygon) {
  return [
    Math.min(...polygon.map(p => p[0])),
    Math.min(...polygon.map(p => p[1])),
    Math.max(...polygon.map(p => p[0])),
    Math.max(...polygon.map(p => p[1])),
  ];
}
export function boundsOverlap(a, b) {
  return a[0] <= b[2] && b[0] <= a[2] && a[1] <= b[3] && b[1] <= a[3];
}
export function makeUnapprovedPlacement(sourceModelId, atlasX, atlasY, angleDegrees) {
  return {
    source_native_id: String(sourceModelId),
    atlas_x: atlasX,
    atlas_y: atlasY,
    rotation_degrees: angleDegrees,
    review_status: 'PROPOSAL_ONLY_NOT_APPLIED',
  };
}
