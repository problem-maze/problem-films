# OCEAN SHARK V8 — Cinematic Reconstruction Lab

Purpose: build a new isolated visual-development track from the VM-4 baseline and use the four generated cinematic reference frames as target direction, while staying inside what the existing WebGL/runtime architecture can realistically execute on phone.

This is NOT a restart of anatomy from zero and does NOT touch main.

## Baseline
- Source branch: `ocean/v7-vm4-cinematic-master`
- Motion baseline: VM-3R1 PASS
- Current camera/light baseline: VM-4 cinematic candidate
- Geometry remains authored Great White: 22,920 triangles
- Target device class: Android / Adreno 610 / 4 GB
- Safety floor: no crash, no WebGL context loss, no stopped shot, no catastrophic slowdown

## Project idea
The generated images are treated as **cinematic reference frames**, not literal promises of offline-render photorealism.

We will reconstruct their useful traits with the existing real-time system:
- stronger silhouette and body mass;
- readable wet eye / mouth / gills;
- directional top light and controlled backscatter;
- darker canyon framing;
- clearer hero close-pass;
- more believable water contact;
- camera staging that preserves the shark's body and tail;
- controlled detail instead of noisy texture.

## Rule
Every visual change must answer two questions:
1. Does it make the phone recording closer to the target frame language?
2. Can the current WebGL architecture execute it reliably enough to continue?

If not, it does not enter the master build.

## First active stage
`V8-R0 — Reference Decomposition & Shot Reconstruction`

Output:
- map the 4 visual references into practical WebGL traits;
- define one canonical 12-second shot;
- identify what can be achieved by camera/light/material/water changes versus what would require new geometry or a different renderer;
- build only the highest-value achievable changes first.

## Protected foundations
Do not reopen unless evidence forces it:
- authored body mesh;
- VM-3R1 propulsion;
- large-form anatomy;
- contact-water dual-shell system;
- reduced-motion support;
- phone safety floor.

## Main remains untouched
All V8 experimentation stays on `ocean/v8-cinematic-reconstruction-lab` or its descendants until a separate acceptance decision.
