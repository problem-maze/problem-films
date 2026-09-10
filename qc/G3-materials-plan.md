# G3 — Skin / Eye / Mouth Materials

Status: **STARTED**

## Goal
Turn the now-accepted authored C1 shark from a coherent 3D animal into a convincing close-range wet marine surface without changing the proven large-form anatomy.

## Material priorities
1. **Countershading** — replace the synthetic/jagged white-gray boundary with a broad, anatomically plausible dorsal-to-ventral transition derived from local position and low-frequency surface variation.
2. **Skin** — add restrained directional dermal micro-response, low-frequency mottling, wet-film Fresnel and distance attenuation. Avoid noisy procedural texture that reads as fake detail.
3. **Eye** — preserve anatomical placement but add corneal dome response, dark iris/pupil depth cue, small controlled catchlight and wet edge Fresnel.
4. **Mouth** — use geometry-local masking for a dark wet oral cavity, softer lip transition and non-black crushed shading; avoid a graphic smile slot.
5. **Gills** — stop rendering the C1 gill ribbons as flat black bars; give them recessed maroon/charcoal wet shading with edge falloff and integrate them into shoulder lighting.

## Locks
- C1 authored geometry and large-form calibration.
- G0B mobile runtime.
- V3 ocean/environment.
- 12-second proof shot and camera.
- no generated images;
- no Canvas2D fallback;
- no additional requestAnimationFrame;
- no locomotion rewrite yet (G4);
- no expanded water/volumetric budget yet (G5).

## Mobile budget rule
The final C1 phone run ended at internal scale 1.04 on the balanced path. G3 shader work must therefore be incremental and measured. Prefer cheap analytic/local-coordinate material functions before additional texture samples or multi-octave noise.

## Acceptance
G3 passes only when the 6–9 second close pass no longer fails primarily because of flat eye, graphic gills, synthetic countershading, plastic skin or dry mouth response, while the target phone still completes the 12-second proof cleanly.
