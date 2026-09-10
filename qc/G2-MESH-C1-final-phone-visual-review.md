# G2-MESH-C1 — Final Phone + Visual Gate

Decision: **PASS**

## Integrity
The corrected final probe now identifies the intended C1 build:
- build id: `V7-G2-MESH-C1`
- file: `Problem-OCEAN-SHARK-V7-G2-MESH-C1-GREAT-WHITE-CALIBRATION.html`
- SHA-256: `efaf0ddf0489d44a3698f38dcbd195da566e3449d0da3c4decdeb51a2825893c`
- bytes: `1,445,792`

## Phone performance
- render path: `g2mesh-c1-full`
- shot completed: yes
- 357 frames / 11.980 s ≈ **29.80 fps**
- average interval: 33.538 ms
- p95: 33.5 ms
- p99: 38.34 ms
- >50 ms: **0 frames**
- max interval: 44.5 ms
- context loss: 0
- final quality tier: balanced
- final post processing: on
- internal scale: 0.84 → 1.04

The lower final scale versus the earlier G2-MESH run is retained as a G3/G7 budget warning; it does not invalidate C1 because cadence and stability stayed clean and the full C1 path completed.

## Close-pass visual review
The 6–9 s close pass now provides enough species/anatomy continuity to stop large-form geometry iteration:
- head/rostrum reads broader and less generic than the pre-C1 authored base;
- body silhouette remains one continuous authored animal;
- pectoral root/sweep and caudal continuity remain materially stronger than the retired procedural G2-R1 path;
- five gill slots are now readable at close range;
- eye placement is acceptable as anatomy, although the eye still reads flat/dark;
- overall silhouette is sufficient to proceed to material realism.

Remaining visible problems are now predominantly material/shading problems rather than blockers in large-form anatomy:
- gill slots are too dark/graphic;
- eye is still button-like because corneal/iris optical response is absent;
- countershading boundary remains visibly synthetic/jagged;
- skin reads smooth/CG;
- mouth lacks wet volumetric shading;
- water/lighting and muscular locomotion remain later gates.

## Final decision
**G2-MESH-C1 = PASS.**

Do not return to the procedural shark body. Begin **G3 — Skin / Eye / Mouth Materials** on the authored C1 geometry and keep G0B runtime + V3 ocean + 12-second proof locked.