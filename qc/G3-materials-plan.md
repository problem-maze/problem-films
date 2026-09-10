# G3 — Skin / Eye / Mouth Materials

Status: **STARTED**

## Goal
Turn the accepted authored C1 shark from a coherent 3D animal into a convincing close-range wet marine surface without changing the proven large-form anatomy.

## Material priorities
1. Countershading: replace the synthetic/jagged white-gray boundary with a broad anatomical transition driven by local position plus restrained low-frequency variation.
2. Skin: add restrained directional dermal micro-response, mottling, wet-film Fresnel and distance attenuation.
3. Eye: add corneal response, iris/pupil depth cues, controlled catchlight and wet edge Fresnel while preserving C1 placement.
4. Mouth: use geometry-local masking for a dark wet oral cavity and softer lip transition; avoid a graphic black slot.
5. Gills: replace flat black-bar read with recessed wet charcoal/maroon shading and edge falloff integrated into shoulder lighting.

## Locks
- C1 authored geometry and large-form calibration.
- G0B mobile runtime.
- V3 ocean/environment.
- 12-second proof shot and camera.
- no generated images.
- no Canvas2D fallback.
- no additional requestAnimationFrame.
- no G4 locomotion rewrite yet.
- no G5 water/volumetric expansion yet.

## Mobile budget rule
The final C1 run ended at internal scale 1.04 on balanced quality. G3 must remain incremental and measured. Prefer cheap analytic/local-coordinate material functions before extra texture samples or multi-octave noise.

## Acceptance
G3 passes only when the 6–9 second close pass no longer fails primarily because of flat eye, graphic gills, synthetic countershading, plastic skin or dry mouth response, while the target phone still completes the 12-second proof cleanly.
