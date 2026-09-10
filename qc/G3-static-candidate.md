# G3 — Skin / Eye / Mouth Materials / Static Candidate

Status: **CANDIDATE BUILT / PHONE + VISUAL EVIDENCE PENDING**

## Build
- `Problem-OCEAN-SHARK-V7-G3-SKIN-EYE-MOUTH-MATERIALS.html`
- SHA-256: `49fae3f286c9c2d30f13dc7e0a27c51569c515769ea7c91b130e8f94c4c455f0`
- bytes: `1,447,931`

## Final probe
- `Problem-OCEAN-SHARK-V7-G3-SKIN-EYE-MOUTH-MATERIALS-PROBE-FINAL.html`
- SHA-256: `6744e33c99dee0a0fdf16e591fdb2c64430cdc2f3f8c4b2c3e4a86f335669484`
- bytes: `1,455,241`

## Material changes
- countershading now derives from local geometry rather than the authored mesh's synthetic angular UV seam;
- boundary irregularity is low-frequency and continuous rather than a high-frequency jagged edge;
- legacy roughness map is no longer applied to the authored body material;
- skin uses restrained longitudinal dermal response and low-amplitude local mottling;
- wet lip seam uses local head/jaw coordinates and low roughness instead of a black graphic smile;
- eye remains anatomically locked but gains near-black globe shading, restrained iris ring, corneal highlight, side catchlight and edge-film response;
- geometric gill ribbons now use wet charcoal/maroon tissue shading with longitudinal falloff instead of pure-black bars;
- safe WebGL shader receives the same broad countershading/eye/gill direction at lower ALU cost.

## Locks
- C1 authored geometry positions: unchanged;
- 22,228 triangles: unchanged;
- G0B runtime: retained;
- V3 ocean/environment: retained;
- 12-second camera/shot: retained;
- no generated images;
- Canvas2D fallback: 0;
- requestAnimationFrame textual occurrences: 2, unchanged;
- no G4 locomotion rewrite;
- no G5 water/volumetric expansion.

## Static validation
- JavaScript parse: PASS for build and final probe;
- geometry: 22,228 triangles, zero NaN/Infinity;
- remote build re-download SHA: PASS;
- final probe metadata matches the G3 build SHA/bytes;
- remote final probe JavaScript parse: PASS.

## Gate
Need one target-phone final-probe JSON and a 6–9 second close-pass recording. G3 is not PASS until both performance and the material read are reviewed.
