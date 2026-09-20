# VM-1 — Creature & Color Master / Static Candidate

Status: **CANDIDATE BUILT / PHONE VISUAL REVIEW PENDING**

## Build
- File: `Problem-OCEAN-SHARK-V7-VM1-CREATURE-COLOR-MASTER.html`
- SHA-256: `a613a1563234de317931129df549015d53c1423aec6eab91e6fdbecf11de2a76`
- Bytes: `1,448,489`

## Probe
- File: `Problem-OCEAN-SHARK-V7-VM1-CREATURE-COLOR-MASTER-PROBE-FINAL-v2.html`
- SHA-256: `f167d2869a93ab57e8e4c7dc9bd3f8cd4eeb4b4708759dd2c873a3077fb2b483`
- Probe metadata is locked to the VM-1 build SHA above.

## Visual-first policy
VM-1 intentionally prioritizes final close-pass appearance before performance recovery.

Safety floor retained:
- no Canvas2D fallback;
- no extra animation clock;
- WebGL-only;
- context/lifecycle recovery preserved;
- truly constrained devices (reported <=2 GB or <=2 logical cores) may still enter the low profile;
- the 4 GB / 4-core target now starts with the balanced/post path so the visual master can actually be judged.

## Creature changes
- countershading no longer depends on the authored UV seam; it is derived from local body geometry;
- dark graphite dorsal colour, restrained neutral flank and moonlit off-white ventral colour;
- macro variation is based on local body coordinates, reducing synthetic tiled texture read;
- skin roughness uses a narrower, more organic range;
- plastic micro-specular response is reduced;
- grazing wet-film response is retained but made more neutral;
- a real shader mouth region is now active on the authored head, with darker wet tissue and lower roughness;
- eye globe remains near-black but receives a stronger corneal film and restrained secondary catch;
- gill ribbons move away from black graphic bars toward muted recessed tissue;
- scars/mottling are weaker and less procedural-looking.

## Colour master changes
- Dark Moonlight palette is less cyan and more graphite/steel/lunar-white;
- underwater fog colour is darker and less saturated;
- beam, dust and bubble colour is more neutral;
- post grade reduces saturation, reduces chromatic-aberration strength, normalizes blur energy and applies a mild filmic shoulder;
- no new volumetric/water system was added; that remains VM-2.

## Integrity
Remote validation:
- JS parse: PASS
- authored shark: 22,228 triangles
- geometry finite: PASS
- requestAnimationFrame textual occurrences: 2
- Canvas2D context calls: 0
- active path: `vm1-full` / `vm1-webgl-safe`
- anatomy remains the accepted G2-MESH-C1 authored geometry
- no generated images

## Gate
Phone test is now a **visual-first gate**, not a final performance gate.

Required:
1. run the final VM-1 probe on the same phone;
2. send JSON only to ensure the safety floor is healthy;
3. send a 6–9 s close-pass recording;
4. judge: countershading, plasticity, eye, mouth, gills, colour balance and whether the shark reads less like a WebGL object.

Performance recovery is deferred until after the visual master sequence.
