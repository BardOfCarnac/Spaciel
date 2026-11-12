/** Spaciel approved Ocean Optics 02 — reusable source-independent parameters.
 * Mechanics approved 12 Nov 2026; stop RGB and strength are adjustable trial settings.
 * The ocean body clock is separate from sunglint/sun and wave animation clocks.
 */
export const OCEAN_OPTICS_V1 = Object.freeze({
  id: "approved-ocean-optics-02",
  direction: "viewer-centred-earlier-left-later-right",
  defaultHour: 11.5,
  defaultStrength: .7,
  maxPhaseFraction: .15,
  paletteStops: Object.freeze([
    [0,[2,5,8]], [.105,[30,8,16]], [.205,[61,19,19]],
    [.285,[76,43,21]], [.385,[33,65,36]], [.485,[24,82,59]],
    [.575,[19,76,95]], [.67,[24,53,78]], [.75,[71,43,25]],
    [.86,[51,18,23]], [1,[2,5,8]]
  ])
});
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const smooth=x=>x*x*(3-2*x);
/** Screen (0,0) is lower left; (0.5,0.5) is exact phase. */
export function viewerPhaseOffset(x,y,strength=OCEAN_OPTICS_V1.defaultStrength) {
  const nx=2*x-1,ny=2*y-1;
  const rim=clamp(Math.hypot(nx*.88,ny*.92),0,1);
  return OCEAN_OPTICS_V1.maxPhaseFraction*nx*(.35+.65*rim)*clamp(strength,0,1);
}
export function sampleOceanBodyRgb(hour,x=.5,y=.5,strength=OCEAN_OPTICS_V1.defaultStrength) {
  const phase=((hour/24+viewerPhaseOffset(x,y,strength))%1+1)%1;
  const stops=OCEAN_OPTICS_V1.paletteStops;
  for(let i=1;i<stops.length;i++) {
    if(phase<=stops[i][0]) {
      const a=stops[i-1],b=stops[i],t=smooth((phase-a[0])/(b[0]-a[0]));
      return a[1].map((value,channel)=>Math.round(value*(1-t)+b[1][channel]*t));
    }
  }
  return [...stops.at(-1)[1]];
}