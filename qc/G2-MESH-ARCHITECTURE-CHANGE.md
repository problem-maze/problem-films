# G2-MESH — Authored Base Mesh Architecture Change

Status: **ARCHITECTURE PASS / C1 COMPLETE**

The procedural shark path was retired after repeated close-pass anatomy failures. The authored-mesh architecture is now accepted and G2-MESH-C1 species calibration has passed its final phone + visual gate.

## Locked authored source
- Shark by Optic_idealist
- CC BY 4.0
- source attribution retained under `third_party/optic-idealist-shark/NOTICE.md`
- authored hero base: 22,128 triangles

## C1 final build
- `Problem-OCEAN-SHARK-V7-G2-MESH-C1-GREAT-WHITE-CALIBRATION.html`
- SHA-256 `efaf0ddf0489d44a3698f38dcbd195da566e3449d0da3c4decdeb51a2825893c`
- 1,445,792 bytes
- 22,228 triangles after the controlled species-calibration pass

## Final phone result
- `g2mesh-c1-full`
- balanced by end of run
- post-processing ON by end of run
- 357 frames / 11.980 s ≈ 29.80 fps
- p95 33.5 ms
- p99 38.34 ms
- 0 frames >50 ms
- max 44.5 ms
- context loss 0
- internal scale 0.84 → 1.04

## Final visual result
Large-form anatomy is good enough to stop topology iteration and proceed to materials. Remaining visible defects are primarily shading/material defects: gill darkness, flat eye optics, synthetic countershading edge, smooth CG skin and dry mouth response.

## Decision
**G2-MESH-C1 PASS. Proceed to G3 — Skin / Eye / Mouth Materials.**
