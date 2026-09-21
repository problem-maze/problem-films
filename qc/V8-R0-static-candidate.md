# V8-R0 — Reference Decomposition & Shot Reconstruction

Status: **STATIC CANDIDATE BUILT / REAL-PHONE VISUAL GATE PENDING**

## Scope and baseline

- Branch: `ocean/v8-r0-shot-reconstruction`
- Source build: exact VM-4 baseline, SHA-256 `ad35eb8645da646d06f315a5b18c595fe74c2ceb49f472fccfaf9cf1c5ce0bce`, 1,461,351 bytes.
- Source probe: exact VM-4 probe, SHA-256 `f5515103a3d36104e8672771bebaa1138f4c7ec481d4cf8da5e8174f7688c97b`, 1,468,421 bytes.
- Reference A verified: SHA-256 `8a50ed17cff7175b9401797af3c7818bd9f492c4de3e441f12107f9cf85c758c`, 691×1536.
- Reference B verified: SHA-256 `54406fd3864d82e900b483467a6e263a5e696364b3f1dc451a212f1a39762edd`, 691×1536.
- Source hashes were enforced by the deterministic builder; a mismatched VM-4 input aborts.

R0 changes only camera/framing/chapter timing, target tracking, a restrained FOV pulse, and timing of the existing VM-4 cinematic-light envelope. It does not change authored anatomy, VM-3R1 deformation, the shark material shaders, cornea shader, water-shell shader, shark trajectory/bank, particles, or post stack.

## Deliverables and exact identity

### Build

- File: `Problem-OCEAN-SHARK-V8-R0-SHOT-RECONSTRUCTION.html`
- SHA-256: `47642578e701aa9e837134f4c017d47928f7a64179f0d1e6bf4b0bd55b4c803a`
- Bytes: `1,461,775`

### Phone probe

- File: `Problem-OCEAN-SHARK-V8-R0-SHOT-RECONSTRUCTION-PROBE.html`
- SHA-256: `1e4b78f521c7c88316cde1aafb3c56f535846abe9398f02e2413a66951e82aec`
- Bytes: `1,468,781`
- Schema: `problem-ocean-v8-r0-v1`
- Probe `META`: `V8-R0`, with the exact build filename, SHA-256, and byte count above.
- Export filename: `V8-R0-phone-probe.json`.
- Probe timing is CPU wall time around the existing `render()` call; it is not raw GPU timing and is not screen-recording FPS.

### Deterministic builder

- File: `tools/build_v8_r0_shot_reconstruction.py`
- SHA-256: `d838f714af9debcefd7dc72b37d5aaaf08f165b96de5e89a83926453db8ecdc2`
- Bytes: `10,338`
- A second build from the verified VM-4 inputs matched both checked-in candidate artifacts byte-for-byte.

## Reference-derived reconstruction

### 0.0–2.6 s — frontal emergence

- Near-symmetric camera position retains the centered, heavy frontal mass.
- Full authored shark, pectoral span, canyon scale, and tail context remain in frame analytically at the 390×844 phone aspect.
- FOV remains at the VM-4 base value, 0.67 rad / 38.39°.

### 2.6–5.2 s — controlled approach

- Lateral camera displacement grows gradually.
- No hero-light contribution is added before 5.4 s.
- Target remains stable in depth during the frontal-to-three-quarter transition.

### 5.2–8.6 s — primary hero window

- Dense keys at 5.2, 6.3, 7.2, 8.0, and 8.6 s hold the three-quarter composition instead of depending on a single wide-FOV correction.
- The target leads from center mass toward head/shoulder, then begins tracking in Z as the shark passes.
- The existing cinematic-light envelope rises from 5.4–6.6 s, stays at peak from 6.6–8.35 s, and remains 0.768 at 8.6 s before clearing at 9.15 s.
- FOV reaches only 0.692 rad / 39.65° at maximum. VM-4 reached 0.705 rad / about 40.39°.

### 8.6–10.4 s — close pass / propulsion handoff

- Target X/Z follows the lateral and depth movement rather than remaining fixed at world Z=0.
- Head and shoulder remain visible briefly after the hero window; framing then hands off to shoulder/body/tail.
- At 10.4 s the tail is 78% inside the analytical phone frame, followed by 97% at 10.8 s and 100% from 11.2 s onward.

### 10.4–12.0 s — controlled haze departure

- Camera pullback is progressive and target tracking continues with the animal.
- Depth/haze rises from 0.55 at 10.4 s to 0.70 at 12.0 s.
- The authored shark returns fully inside frame by 11.6 s.
- At 12.0 s the full projected bounds are approximately X `[-0.87, 0.66]`, Y `[-0.03, 0.24]` in NDC: visible mass remains, but it is receding rather than leaving a long empty frame.

## VM-4 comparison at 390×844

Percentages below count projected authored vertices inside the NDC viewport. This is deterministic framing evidence, not visual approval.

| Shot time | Region | VM-4 in frame | V8-R0 in frame |
|---:|---|---:|---:|
| 8.6 s | head | 28% | 97% |
| 8.6 s | shoulder | 100% | 100% |
| 9.2 s | head | 0% | 88% |
| 9.2 s | shoulder | 63% | 100% |
| 10.4 s | tail | 44% | 78% |
| 11.6 s | full shark | 0% | 95% |
| 12.0 s | full shark | 0% | 100% |

The comparison directly addresses the documented VM-4 failure: the light peak is no longer delayed until after the head/shoulder exit, and the final section is no longer analytically empty.

## Protected-foundation lock checks

The following source spans are byte-identical between verified VM-4 and V8-R0:

| Protected span | SHA-256 | Bytes | Result |
|---|---|---:|---|
| authored shark geometry generator | `ba03feb97e44e21dfa81239d7b685136b0ff8ad29748c0382fce8b0bb41c1d29` | 353,675 | PASS |
| full VM-3R1 motion + material shader object | `ef4f7dfc5a6dd9f5814334b1e6e93b33bcf4f7789e6c8aada4c14aa5cfc26488` | 13,430 | PASS |
| safe VM-3R1 motion + material shader object | `a419d0e4924019988619a68b772b04a07ffcea50f5bcb0f2d7f0b835adbdb3c4` | 4,563 | PASS |
| cornea shader | `d7b100e2dca96774381272490f9069b4de1e4b3c26f16cc337682b768c179890` | 793 | PASS |
| dual contact-water shell shader | `14997371d3addf6cdf275686c2a38f67cb8386192bb172c515047fa64c56d227` | 1,193 | PASS |
| shark pose/trajectory and bank functions | `9209d441090140af49bb6a767ed9107ec6c7ed640a8282878bca0376e6c3b608` | 983 | PASS |

This locks VM-3R1 propulsion, pectoral stabilization, authored anatomy, local gill/cornea/mouth geometry, material response, water architecture, and the animal's trajectory/bank.

## Static validation

- JavaScript parse, build: PASS (one inline script).
- JavaScript parse, probe: PASS (one inline script).
- Authored shark geometry: **22,920 triangles / 68,760 expanded vertices / 687,600 interleaved floats**.
- All generated scene geometry values checked: 3,427,690.
- Non-finite geometry values: **0**.
- Canvas2D context calls: **0** in build and probe.
- Textual `requestAnimationFrame` occurrences: **2** in build and **2** in probe; no second animation clock added.
- Full render path: `v8r0-full` present.
- WebGL-safe render path: `v8r0-webgl-safe` present.
- Reduced-motion media query and runtime branch: present.
- Camera sample count: 2,881 across 0–12 s at 240 Hz.
- Non-finite camera/target/FOV/depth samples: **0**.
- Maximum sampled eye speed: 24.363 scene units/s during deliberate departure pullback.
- Maximum sampled target speed: 5.292 scene units/s.
- Maximum sampled FOV-tangent rate: 0.01548/s.
- Catmull-Rom camera/target positions are continuous through all chapter keys; no target assignment snap was introduced.
- Deterministic rebuild: PASS for build and probe.

## Browser smoke

Status: **NOT RUN — ENVIRONMENT UNSUPPORTED**.

Checked executables: Chromium, Chromium Browser, Google Chrome, and Firefox; none is installed. Checked Node browser drivers: Playwright and Puppeteer; neither is installed. No fallback browser result, page-error count, WebGL context result, or synthetic phone FPS is claimed.

Headless smoke, if later available, must use 390×844 and confirm WebGL context, no fallback, no context loss, automatic shot advancement, visual-run state, and zero relevant page/console errors. It remains smoke evidence only.

## Real-phone probe procedure

From the repository root:

```sh
python3 -m http.server 8765 --bind 0.0.0.0
```

On the target Android phone, open:

```text
http://127.0.0.1:8765/Problem-OCEAN-SHARK-V8-R0-SHOT-RECONSTRUCTION-PROBE.html
```

Then:

1. Tap **Start V8-R0** and record one complete automatic run, including a few seconds before and after if convenient.
2. Do not touch the viewport or switch apps during the measured run; those events invalidate probe telemetry.
3. After completion, tap **JSON** and retain `V8-R0-phone-probe.json` separately from the screen recording.
4. Do not report the MP4 stream frame rate as engine FPS.

## Real-phone visual acceptance gate

Pending human review of the actual Android recording:

- A) frontal emergence reads centered and heavy;
- B) the three-quarter hero frame is unmistakable;
- C) head + shoulder remain framed during the 6.6–8.6 s hero-light window;
- D) body/peduncle/caudal propulsion remains readable during close pass and departure;
- E) there is no abrupt head crop;
- F) the final 1.6 s returns the shark into haze without a long empty section;
- G) there is no context loss, fallback, frozen/stopped shot, or catastrophic slowdown.

No phone performance or visual PASS is claimed. V8-R0 stops here until the real-phone recording and probe JSON are reviewed.
