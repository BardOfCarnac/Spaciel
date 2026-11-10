# Spaciel V19 — direct repaired viewer
This branch contains 40 UTF-8 chunks of the complete standalone Spaciel V19 HTML map, assembled automatically by GitHub Actions. Download the generated viewer from the workflow artifact; there is no need to upload or select a file.

Fixes: declare the previously missing GLSL oceanModel uniform. If the 44-component spectral shader is rejected by the device GPU, switch automatically to the previous working water shader rather than blank the entire map. The map data and all road, terrain, coastline, buildings and locations are unchanged.
