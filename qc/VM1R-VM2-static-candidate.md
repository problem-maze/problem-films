# VM-1R + VM-2 — Surface Correction + Water Integration

Status: **CANDIDATE BUILT / PHONE VISUAL REVIEW PENDING**

## Build
- File: `Problem-OCEAN-SHARK-V7-VM1R-VM2-VISUAL-INTEGRATION.html`
- SHA-256: `9154eae2b736d829a554dea73defc1491f4acea1181bffec92bf99bcce0b4f90`
- Bytes: `1,450,878`

## Probe
- File: `Problem-OCEAN-SHARK-V7-VM1R-VM2-VISUAL-INTEGRATION-PROBE.html`
- SHA-256: `8108aba07d670be0831b1281ce00c827eee1adee5a9570ba36c4318c9ee49555`
- Probe metadata points to the build SHA/size above.

## Locked
- G2-MESH-C1 authored anatomy remains unchanged.
- 22,228 authored triangles.
- 12-second proof path retained.
- No generated images.
- No Canvas2D fallback.
- No additional animation clock.

## VM-1R surface correction
- removed the regular/stamped dermal pattern in favor of low-amplitude directional local-coordinate microstructure;
- corrected normal response to avoid biased normal-map contribution;
- layered roughness is less uniform and less plastic;
- mouth now has distinct geometry-driven cavity + lip-band shading instead of one broad painted band;
- eye is darker with a smaller hard corneal catch, soft film and restrained secondary reflection;
- gill material uses softer tissue edges and a recessed center rather than uniform dark bars;
- teeth are warmer, dimmer and rougher to avoid graphic white enamel.

## VM-2 water integration
- added silhouette water-wrap in the creature shader so grazing edges inherit local fog colour;
- added one animated expanded authored-mesh contact shell (`uShell = 0.22`) around the shark;
- shell is transparent, depth-tested, does not write depth, and uses low-density breakup to create local contact haze / volumetric separation from the background;
- shell uses the same authored animation path as the shark, so it follows the body instead of being a screen-space fake;
- automatic 12-second visual run hides UI copy/console without forcing fullscreen, improving phone visual judgment.

## Static validation
- remote build SHA/bytes: verified;
- remote probe SHA/bytes: verified;
- JS parse: PASS;
- geometry: 22,228 triangles;
- NaN/Infinity in authored geometry: 0;
- textual requestAnimationFrame occurrences: 2;
- Canvas2D context calls: 0;
- paths: `vm12-full` / `vm12-webgl-safe`;
- water-contact shell shader present and connected to the render path.

A desktop GPU smoke check was not used as phone authority; the real Android/Adreno run remains the gate.

## Gate
This remains **visual-first**. The phone run should answer:
1. does skin still read plastic or stamped?
2. does the eye stop reading as a flat black button?
3. does the mouth read as wet recessed tissue rather than paint?
4. do gills read recessed rather than five graphic stripes?
5. does the shark now sit inside a local water volume instead of on top of the background?
6. does the contact shell stay subtle (no visible halo)?

Performance numbers are recorded only as a safety floor; full recovery remains deferred until the visual master sequence is locked.
