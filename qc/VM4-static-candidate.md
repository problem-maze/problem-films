# VM-4 — Cinematic Master

Status: **CANDIDATE BUILT / PHONE CINEMATIC CHECK PENDING**

## Build
- File: `Problem-OCEAN-SHARK-V7-VM4-CINEMATIC-MASTER.html`
- SHA-256: `ad35eb8645da646d06f315a5b18c595fe74c2ceb49f472fccfaf9cf1c5ce0bce`
- Bytes: `1,461,351`

## Probe
- File: `Problem-OCEAN-SHARK-V7-VM4-CINEMATIC-MASTER-PROBE.html`
- SHA-256: `f5515103a3d36104e8672771bebaa1138f4c7ec481d4cf8da5e8174f7688c97b`
- Schema: `problem-ocean-vm4-v1`
- Probe META locked to the exact build SHA/size above.

## Locked foundations
VM-4 starts from the VM-3R1 motion-pass baseline. It intentionally does not reopen:
- shark authored geometry / large-form anatomy;
- VM-3R1 propulsion deformation;
- pectoral stabilization / body bank;
- VM-2R.2 local gill / cornea / mouth geometry;
- Dark Moonlight material master;
- contact-water system.

## Cinematic camera

### Approach
The early camera remains restrained and slightly elevated so the shark can emerge out of depth without giving away the close-pass composition too early.

### Side / close pass
The previous 5-key camera path is replaced by an 8-key Catmull-Rom path with extra control around 8.0–11.35 s.

Goals:
- stay lateral longer during the strongest propulsion read;
- track the head/shoulder through the pass instead of letting the shark leave the useful framing too quickly;
- retain more of the posterior body / tail while the animal crosses camera;
- remove the rushed feeling in the transition into departure.

### Dynamic FOV
A restrained close-pass FOV pulse is added:
- base FOV remains 0.67 rad;
- maximum close-pass FOV is 0.705 rad;
- the widening is smoothly gated into and out of the 7.15–11.85 s cinematic window.

This is intentionally small: enough to preserve body/tail framing on portrait phone without creating wide-angle distortion.

### Exit
The final camera keys pull back later and more progressively:
- lateral position relaxes instead of snapping away;
- eye height rises gradually;
- target continues to follow the passing mass;
- depth increases to 0.55 at the final frame so the departure falls back into haze.

## Shot-timed light sculpt
A `uCine` envelope is shared across render passes and peaks only during the close-pass window.

Full path:
- adds a restrained cool-neutral key on the anterior body;
- focuses the extra key on head + shoulder local coordinates;
- adds a small upper rim term;
- deepens far-side separation slightly at peak;
- does not change the Dark Moonlight palette.

Safe path:
- receives a lower-cost equivalent anterior key.

Cornea:
- receives only a small specular response increase during the same cinematic window;
- no eye glow or color shift.

## Validation

### Static / exact
- build SHA/bytes: PASS;
- probe SHA/bytes/META: PASS;
- JavaScript parse: PASS;
- geometry: **22,920 triangles / 68,760 expanded vertices**;
- non-finite geometry values: **0**;
- Canvas2D calls: **0**;
- textual requestAnimationFrame occurrences: **2**;
- paths: `vm4-full` / `vm4-webgl-safe`.

### Browser smoke
Headless Chromium / SwiftShader at 390×844:
- WebGL context: PASS;
- fallback shown: NO;
- context lost: NO;
- auto shot advanced normally: PASS;
- visual-run state: PASS;
- page errors: 0;
- relevant console errors: 0.

### Camera sampling
Portrait 390×844:
- cinematic cue = 0 before close pass;
- cue rises to 0.439 at 8.0 s;
- cue = 1.0 at 9.45 s;
- cue = 0.996 at 10.55 s;
- cue falls to 0.310 at 11.35 s;
- cue = 0 at 12 s.
- FOV tan changes from 0.3481 base to 0.3679 at peak, then returns smoothly.

## Phone visual gate
One 12-second recording.

Judge:
1. approach has enough anticipation and does not expose the close-pass angle too early;
2. head + shoulder remain readable during the strongest pass;
3. body and tail stay in a useful frame longer than VM-3R1;
4. timed key light shapes the head/shoulder without looking like a spotlight;
5. no wide-angle distortion;
6. departure feels deliberate and falls back into haze cleanly;
7. VM-3R1 propulsion still reads correctly;
8. no crash, context loss or stopped shot.

If these pass, VM-4 can become the **Visual Lock candidate** before performance recovery.
