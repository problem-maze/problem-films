# G1 — 12-Second Reality Proof / Static Candidate Report

Status: **CANDIDATE BUILT / PHONE + VISUAL EVIDENCE PENDING**

## Candidate
- File: `Problem-OCEAN-SHARK-V7-G1-REALITY-PROOF.html`
- SHA-256: `997b663148ff029c41aa3d1c3b978681a8ccb78eb0a1a1e922bf6d1885c5c727`
- Bytes: `1111217`

## Phone probe
- File: `Problem-OCEAN-SHARK-V7-G1-REALITY-PROOF-PROBE.html`
- SHA-256: `0634cb9ef0d7b946ef50eff76f93a2d8d542b16926076a322c0e8f6830d23656`
- Bytes: `1117722`

## What changed in G1
- Replaced the G0B whale hero with the V6 great-white prototype geometry while preserving the V3 ocean/environment geometry.
- Kept V3 background/water, canyon/floor, fish, kelp, particles, beams and post-processing path as the scene foundation.
- Added a dedicated shark material/motion shader program so the environment continues to use the V3 mesh shader while the shark uses the V6 shark shader.
- Changed the journey from 96 seconds to one controlled 12-second proof.
- Added a staged hero transform for emergence → approach → close pass → departure.
- Reframed the camera for the 12-second test.
- Removed the distant duplicate hero draw for this proof so the rendering budget is concentrated on the close animal.
- Preserved the G0B runtime rules: no CSS-width forced-low, dynamic render scale, WebGL-only 3D fallback, no Canvas/2D fallback, one owned animation clock.

## Static validation
- JavaScript syntax: PASS.
- Existing V3 ocean geometry generation: finite values only.
- G1 shark geometry: 1,008,360 float entries / 33,612 triangles / zero NaN or Infinity.
- requestAnimationFrame occurrences: 2 (unchanged from G0B source structure; no probe animation clock added).
- Canvas2D context calls: 0.
- 12-second timeline: present.
- Legacy 96-second clamp/end logic: removed.
- Render paths: `g1-full` and `g1-webgl-safe`.

## G1 phone probe behavior
The probe performs a 3-second warm-up, then resets the proof to 0 seconds and measures exactly one 12-second run using the existing render loop. It records render path, scale/tier, WebGL renderer, frame intervals, render-call CPU wall time, context stability and whether the 12-second shot completed.

## Acceptance still required
G1 is **not PASS yet**. Required:
1. Real-phone probe JSON showing the complete 12-second shot on the target phone.
2. Human visual review of the 6–9 second close pass.
3. Explicit defect list for head/jaw/gills/pectoral root/skin/eye/peduncle/tail.
4. Decision: PASS / REWORK / proceed to G2 anatomy scope based on observed close-pass defects.

No G2 code should begin before this evidence is returned.
