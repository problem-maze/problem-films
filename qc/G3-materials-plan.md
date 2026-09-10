# G3 — Skin / Eye / Mouth Materials

Status: **STARTED**

The C1 large-form anatomy gate is now closed as PASS. G3 is responsible for the dominant remaining close-pass failures.

Priorities:
1. Replace the synthetic/jagged countershading edge with a broad anatomical transition.
2. Add restrained dermal micro-response, mottling and wet-film Fresnel without noisy fake detail.
3. Build corneal/iris/pupil depth cues and controlled catchlight for the eye.
4. Give the mouth a wet volumetric cavity/lip response instead of a graphic dark slot.
5. Integrate the five gill slots with recessed wet shading instead of flat black bars.

Locks: C1 authored geometry, G0B runtime, V3 ocean, 12-second proof shot, no generated images, no Canvas2D fallback, no extra rAF, no G4 locomotion rewrite, no G5 water expansion.

Mobile budget: the final C1 run ended at scale 1.04 on balanced quality; G3 changes must stay incremental and measured.
