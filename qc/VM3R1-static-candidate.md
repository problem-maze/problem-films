# VM-3R1 — Propulsion Readability

Status: **CANDIDATE BUILT / PHONE MOTION CHECK PENDING**

## Build
- File: `Problem-OCEAN-SHARK-V7-VM3R1-PROPULSION-READABILITY.html`
- SHA-256: `3665c93ebef92a0ca1d270e88e80c42211f930664f6afd7a351c1e19dba75eba`
- Bytes: `1,459,992`

## Probe
- File: `Problem-OCEAN-SHARK-V7-VM3R1-PROPULSION-READABILITY-PROBE.html`
- SHA-256: `7493ed2b1d7487060b7706fdcdf6681aed0bfed80c7fdba1a90cd1f28924f366`
- Schema: `problem-ocean-vm3r1-v1`
- META locked to the exact build SHA/size.

## Purpose
VM-3 phone review showed clear progress in Life & Weight, but the rear drive still read too quietly in the side pass. VM-3R1 changes only propulsion readability. Camera, surface master, water, local feature geometry and large-form anatomy stay locked.

## Motion correction

### Head
- head envelope reduced slightly relative to VM-3;
- anterior head remains effectively outside the propulsion deformation;
- no new head wobble or heave.

### Trunk -> peduncle
- swim phase frequency raised moderately so a full propulsive cycle reads inside the 12-second shot;
- trunk amplitude remains close to VM-3;
- posterior amplitude ramps earlier and more strongly into the peduncle;
- phase gradient along local X increased slightly.

### Counter-bend
- added a narrow pre-tail counter-bend gate between posterior trunk and caudal pivot;
- counter-bend is opposite the caudal drive phase;
- its amplitude is deliberately small: enough to make an S-curve readable without creating rubber-body motion.

### Caudal drive
- caudal phase lag increased;
- sweep raised from the VM-3 range to a restrained ~21.2 degree analytical maximum;
- a low secondary harmonic prevents a metronomic single-sine look.

### Pectorals / bank
- VM-3 pectoral stabilization is preserved;
- no extra fin flap was introduced;
- VM-3 bank curve is preserved unchanged.

## Analytical motion envelope
Approximate maximum lateral body offsets from the full-path deformation over the 12-second window:
- x=-5.0 (head): 0.00000
- x=-2.0 (anterior): 0.00022
- x=0.0 (mid body): 0.00777
- x=2.0 (posterior trunk): 0.01766
- x=3.5: 0.03572
- x=4.5: 0.06595
- x=5.4 (peduncle / tail base): 0.09691
- analytical caudal angular maximum: ~21.2 degrees

This keeps the middle body close to VM-3 while concentrating the increase in the posterior third.

## Preserved
- VM-2R.2 local gill cores / cornea / mouth insert;
- VM-2R.1 / VM-2R water-contact integration;
- Dark Moonlight palette;
- VM-3 Catmull-Rom trajectory continuity;
- VM-3 path bank;
- 22,920 triangles / 68,760 expanded vertices;
- no generated images.

## Validation
Static / remote:
- build SHA/bytes: PASS;
- probe SHA/bytes/META: PASS;
- JavaScript parse: PASS;
- non-finite geometry values: 0;
- Canvas2D calls: 0;
- textual requestAnimationFrame occurrences: 2;
- paths: `vm3r1-full` / `vm3r1-webgl-safe`.

Browser smoke (headless Chromium / SwiftShader, 390x844):
- WebGL context created: PASS;
- fallback shown: NO;
- context lost: NO;
- auto test advanced to 2.7 s: PASS;
- visual-run state active: PASS;
- page errors: 0;
- relevant console errors: 0.

Browser smoke is not a substitute for the Android/Adreno 610 visual gate.

## Phone gate
One 12-second recording.

Judge:
1. head stays calm;
2. rear-body wave becomes visible before the tail;
3. peduncle and caudal fin form a readable S-curve;
4. tail now reads as the final propulsive driver instead of passive drift;
5. pectorals still stabilize rather than flap;
6. no rubber-body exaggeration;
7. no context loss / stopped shot / catastrophic slowdown.

If the propulsion reads naturally, close VM-3 and proceed to **VM-4 — Cinematic Master**.
