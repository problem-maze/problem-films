# G2-MESH-C1 — Great White Species Calibration Candidate

Status: **CANDIDATE BUILT / PHONE + VISUAL EVIDENCE PENDING**

## Candidate
- File: `Problem-OCEAN-SHARK-V7-G2-MESH-C1-GREAT-WHITE-CALIBRATION.html`
- SHA-256: `efaf0ddf0489d44a3698f38dcbd195da566e3449d0da3c4decdeb51a2825893c`
- Bytes: `1,445,792`

## Probe
- File: `Problem-OCEAN-SHARK-V7-G2-MESH-C1-GREAT-WHITE-CALIBRATION-PROBE.html`
- SHA-256: `5bce374f08a1f6e7aa77c109cdc31ca1f3d163c31250cac139cdd4f1c54329ca`
- Bytes: `1,453,188`

## Controlled species-calibration changes
- Retains the Optic_idealist authored topology as the hero source.
- Blunts and widens the anterior rostrum using smooth large-form deformation rather than rebuilding procedural anatomy.
- Strengthens the cheek/shoulder wedge while preserving the authored body continuity.
- Slightly flattens the anterior vertical profile to reduce the generic pointed-shark read.
- Repositions/widens the eye globes to follow the calibrated skull.
- Adds five curved geometric gill-slit ribbons per side so the gills can be judged in the close pass without relying on a painted texture.
- Adds a mild swept-back adjustment to pectoral geometry tagged from the authored rig regions.
- Adds a small caudal-thickness correction at the far tail.

## Geometry
- Authored base: 22,128 triangles.
- C1: **22,228 triangles**.
- Added geometry: 100 triangles, all from the ten five-segment gill ribbons.
- Expanded runtime vertex layout: 66,684 vertices / 666,840 float entries.
- Geometry validation: zero NaN/Infinity.

## Locked
- G0B mobile runtime.
- V3 ocean/environment.
- 12-second diagnostic shot/camera.
- WebGL-only path.
- No Canvas2D fallback.
- No additional requestAnimationFrame clock.
- No generated images.

## Static validation
- JavaScript parse: PASS for candidate and probe.
- requestAnimationFrame textual occurrences: 2, unchanged.
- Canvas2D context calls: 0.
- Active paths: `g2mesh-c1-full` / `g2mesh-c1-webgl-safe`.

## Scope boundary
C1 does not attempt G3 material realism. Countershading, skin microstructure, eye optical response, mouth wetness and gill shading remain G3 work.

## Gate
Run the C1 probe on the same target phone and review the 6–9 s close pass.

If species silhouette is clearly stronger and runtime remains stable, mark G2-MESH-C1 PASS and begin G3.
