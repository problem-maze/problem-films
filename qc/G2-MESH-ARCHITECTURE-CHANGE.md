# G2-MESH — Authored Base Mesh Architecture Change

Status: **CANDIDATE BUILT / PHONE + VISUAL EVIDENCE PENDING**

## Why the architecture changed

G1, G2 and G2-R1 phone recordings repeatedly exposed a ceiling in the hand-built procedural shark topology: the close pass continued to show a bulbous head, graphic mouth, button-like eyes, weak gills, bar-like pectorals and flat caudal lobes. Additional local procedural patches were no longer the shortest path to a coherent animal.

The proven G0B mobile runtime, V3 ocean foundation and 12-second diagnostic shot remain locked. Only the hero anatomy source changes.

## Selected authored candidate

Work: **Shark** by **Optic_idealist**
- Original source: https://sketchfab.com/3d-models/shark-8bcd4d861bd84e87b2832e83c9cb898b
- Inspected redistribution: `bob6664569/open-water/site/assets/animals/fish/shark.glb`
- License: **CC BY 4.0**
- GLB SHA-256: `1056b1bc09f11e259aca73f7d56e7b614ddff64299c2530990e792878a6a6610`
- GLB bytes: `7,072,212`
- Body: 11,774 vertices / 21,616 triangles
- Eyes: 274 vertices / 512 triangles
- Total: **22,128 triangles**
- Skin: 43 joints
- Animation: one authored armature animation, 123 channels

The source is treated as an **authored shark anatomy candidate**, not yet certified as a definitive Great White reference. The close-pass gate decides whether the silhouette is sufficient.

## Rejected alternative

PyVista's `Data/great_white_shark/greatWhite.stl` was inspected but rejected for project use because its folder-specific license file explicitly states that origin and license are not definitively established (`LicenseRef-unknown`). It is not used or redistributed here.

## Integration

The G2-MESH build:
- extracts body and eye geometry only;
- quantizes positions and normals for compact in-HTML embedding;
- expands indexed triangles at runtime into the existing 10-float Problem vertex layout;
- generates procedural UVs for the existing Problem shark shader;
- preserves the existing G0B mobile runtime;
- preserves the V3 ocean/environment;
- preserves the existing 12-second close-pass camera and staging;
- adds no Canvas2D fallback and no extra animation clock;
- does not embed the 7 MB source texture or require a network request at runtime.

Pectoral and far-tail vertices receive coarse authored-geometry part tags for the existing deformation shader. Full use of the source rig/skin is deferred to the locomotion gate if this anatomy candidate passes.

## Candidate build

- File: `Problem-OCEAN-SHARK-V7-G2-MESH-AUTHORED-BASE.html`
- SHA-256: `c24bbac24dab6a8a1bb776ce42a8fcfd81d3c5fb4b96fcccbe53a56cd5ae2567`
- Bytes: `1,443,781`

Probe:
- File: `Problem-OCEAN-SHARK-V7-G2-MESH-AUTHORED-BASE-PROBE-v2.html`
- SHA-256: `0ac221bfeea365bd7c722867dd4412cebea561a75ba06bfc7d24deaff96e0adb`
- Bytes: `1,451,168`

Static checks:
- JavaScript parse: PASS
- requestAnimationFrame textual occurrences: 2
- Canvas2D context calls: 0

## Geometry-budget result

G2-R1 procedural hero: **50,948 triangles**
G2-MESH authored hero: **22,128 triangles**

The authored base removes **28,820 hero triangles (~56.6%)** while replacing procedural anatomy with an artist-authored topology. This gives the mobile budget more headroom for later G3–G5 work.

## Gate

G2-MESH is not PASS yet.

Required evidence:
1. target-phone 12-second probe JSON;
2. real-phone close-pass video/screenshot from seconds 6–9;
3. visual decision on head wedge, jaw, eye placement, gills, pectoral sweep, trunk continuity and tail;
4. if the authored silhouette is not genuinely better, reject this candidate rather than forcing it through G3.
