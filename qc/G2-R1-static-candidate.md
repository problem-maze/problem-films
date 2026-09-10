# G2-R1 — Anatomy Continuity Pass / Static Candidate

Status: **CANDIDATE BUILT / PHONE + VISUAL EVIDENCE PENDING**

## Candidate
- File: `Problem-OCEAN-SHARK-V7-G2-R1-ANATOMY-CONTINUITY.html`
- SHA-256: `3d70903044f2dbce3549116e69fb2a4cc59578018077e59974befe493b5b9330`
- Bytes: `1116799`

## Probe
- File: `Problem-OCEAN-SHARK-V7-G2-R1-ANATOMY-CONTINUITY-PROBE.html`
- SHA-256: `da0353d50b2c9b722904462ae48a556e73974c666a4a915964d08cee31fee6ad`
- Bytes: `1123983`

## R1 anatomy continuity work
- Rebuilt the front profile with a flatter, broader blunt rostrum.
- Increased lateral head width while reducing the balloon/dome read.
- Removed the independent cheek and pectoral-root body-colour ellipsoids that were exposing assembled-part seams.
- Integrated lower-jaw mass into the main body cross-section.
- Rebuilt the lower mandible as a curved shell sharing one mouth envelope with the cavity and lip ribbons.
- Replaced rectangular-looking mouth walls with curved cheek-to-jaw corner surfaces.
- Rebuilt tooth spacing/height/lean variation along a curved jaw arc.
- Enlarged/repositioned socket/globe/cornea anatomy while leaving final optical material work for G3.
- Rebuilt five gills per side on the actual flank curvature with recessed dark grooves and paired skin lips.
- Shortened and swept the pectorals; first root stations are buried into the shoulder to hide blade-like root seams.
- Lowered/widened the dorsal fin and softened its trunk transition.
- Thickened the pre-caudal profile and keel transition.
- Removed the floating caudal root-hub ellipsoid.
- Rebuilt upper/lower tail lobes with thicker roots and a less graphic heterocercal silhouette.
- Added a short caudal web to unify the posterior root.
- Added a continuity-only shader correction for jaw/lip body-colour pieces so broad countershading is derived from local geometry instead of their independent patch UVs. No G3 micro-material work was added.

## LOD geometry
- LOD0: **50,948 triangles**
- LOD1: **27,930 triangles**
- LOD2: **17,892 triangles**
- All LODs: zero NaN/Infinity.

## Integrity lock
Byte-identical G2 → G2-R1:
- V3 ocean geometry
- V3 ocean shaders
- 12-second OceanMath camera
- 12-second hero pose/staging

Runtime invariants:
- requestAnimationFrame textual occurrences: 2 → 2
- Canvas2D context calls: 0
- old CSS-width forced-low predicate: 0
- no 2D fallback introduced

## Static validation
- JavaScript syntax: PASS for candidate and probe.
- Active render paths: `g2r1-full` / `g2r1-webgl-safe`.
- Probe lock uses the existing render loop; no second animation clock.

## Scope boundary
G2-R1 is still anatomy continuity, not final skin/eye/mouth realism. G3 remains blocked until a real-phone close pass shows the body reads as one continuous animal.

## Gate
Need:
1. one target-phone 12 s probe JSON;
2. close-pass video/screenshot from seconds 6–9;
3. direct judgment of head wedge, jaw continuity, gills, pectoral roots, dorsal root and peduncle/tail.

Decision after evidence: PASS / REWORK.
