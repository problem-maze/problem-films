# V8-R1 — Cinematic Reality Reconstruction

Status: **STATIC CANDIDATE BUILT / V8-R1 REAL ANDROID VISUAL GATE PENDING**

## Scope and baseline

- Working branch: `ocean/v8-r1-cinematic-reality`.
- Engineering baseline: committed V8-R0 candidate `8011731b40ab568f3c19c97c87c890e29a383e10` on `ocean/v8-r0-shot-reconstruction`.
- Source build SHA-256: `47642578e701aa9e837134f4c017d47928f7a64179f0d1e6bf4b0bd55b4c803a`.
- Source probe SHA-256: `1e4b78f521c7c88316cde1aafb3c56f535846abe9398f02e2413a66951e82aec`.
- The deterministic builder rejects any source that does not match those exact hashes.
- Visual North Stars inspected directly: `reference-A-frontal.jpg` and `reference-B-three-quarter.jpg`.
- The previously supplied R0 phone evidence is the engineering budget only. No R1 phone or performance result is claimed in this report.

R1 reconstructs camera, framing, timing, light, water occupancy, surface response, canyon/background composition, and departure as one shot. It does not add raymarched volumetrics, new libraries, network assets, or another animation clock.

## Deliverables and exact identity

### Build

- File: `Problem-OCEAN-SHARK-V8-R1-CINEMATIC-REALITY.html`
- SHA-256: `52c23e4674fd439fe9befe4f3a02983dd2f8a2464dae3cbf953c35cf78beec65`
- Bytes: `1,464,888`

### Phone probe

- File: `Problem-OCEAN-SHARK-V8-R1-CINEMATIC-REALITY-PROBE.html`
- SHA-256: `485fb9b05c9880072ace3d2d1722ef244893efb9676a5dc45668468463e411ae`
- Bytes: `1,471,756`
- Schema: `problem-ocean-v8-r1-v1`.
- Probe `META` identifies `V8-R1` and embeds the exact build filename, SHA-256, and byte count above.
- Export filename: `V8-R1-phone-probe.json`.
- Probe timing remains CPU wall time around the existing render call. It is not GPU timing and is not screen-recording FPS.

### Deterministic tools

- Builder: `tools/build_v8_r1_cinematic_reality.py`
  - SHA-256: `b51f45b9cd093b4c9727dd3eb1068a3b7f2ab21f2581b74d4b442241dc51940a`
  - Bytes: `34,381`
- Validator: `tools/validate_v8_r1_cinematic_reality.js`
  - SHA-256: `28e81b96b89fa9473fd437bed3534867966b06e2946b690781aeafc6d91c0430`
  - Bytes: `10,555`
- A second build from the verified R0 inputs matched both checked-in R1 artifacts byte-for-byte.

## Integrated visual reconstruction

### Camera, framing, and shot timing

- Replaced the R0 11-key path with an 18-key trajectory designed around the requested phases: 0–2.5 s emergence, 2.5–5.5 s approach, 5.5–9.0 s hero development, 9.0–10.7 s close pass, and 10.7–12.0 s departure.
- The portrait camera continues to be designed at 390×844 first. The lateral and depth axes use the same portrait compensation so body context does not collapse during the three-quarter move.
- Frontal lateral displacement remains near zero through 2.5 s. R1 starts substantially closer: projected full-shark width at 0 s grows from R0 NDC width `0.460` to R1 `0.682`, approximately a **48% increase**, while all authored regions remain inside frame.
- The controlled FOV is 36.669° outside the hero pulse and peaks at only 37.701°. R0 reached approximately 39.65°; R1 does not use widening as the primary framing fix.
- The hero light rises from 5.45–6.8 s, holds through approximately 8.7 s, and clears by 9.35 s. This overlaps the intentional 7–9 s hero composition.
- At 7.0 s, head, shoulder, torso, and posterior authored vertices are all 100% in frame.
- At 8.0 s, head/shoulder/torso are 100% in frame and 82.3% of posterior vertices remain visible.
- At 9.0 s, head is 93.8%, shoulder 100%, torso 99.4%, and posterior 39.4% in frame. The head/shoulder/torso composition therefore survives the full requested hero window.
- The camera then hands the frame to the body: at 10.7 s the torso is 100% and posterior is 83.9% in frame.
- During departure, tracking release and pullback restore the complete silhouette while depth rises from `0.60` at 10.7 s to `0.88` at 12 s. At 12 s, 99.9% of the authored shark is in frame; the image is designed to end through contrast/haze loss rather than by emptying sideways.

The Catmull-Rom camera and target remain continuous. Across 2,881 samples at 240 Hz: zero non-finite samples, maximum sampled eye speed `25.822366` scene units/s during the deliberate departure pullback, maximum target speed `6.030242`, and maximum FOV-tangent rate `0.02732184/s`.

### Lighting architecture

- Replaced the single mild cinematic contribution with a coordinated top/back source and a separate angled hero key.
- The top source remains active as surface motivation; the hero source is spatially gated to head and shoulder and temporally gated to the 5.45–9.35 s envelope.
- Far-side falloff and shoulder occlusion are increased during the hero envelope, preserving skull and shoulder thickness instead of globally brightening the body.
- Upper rim energy is reduced and desaturated. Light-beam alpha is lower, hero-timed, and suppressed during departure.
- The same top source, hero key, far-side falloff, and departure attenuation exist in the WebGL-safe shark shader.

### Eye, mouth, gills, and surface

- The existing eye and cornea geometry is unchanged. The globe remains near-black; corneal response uses a narrow top/hero glint, restrained Fresnel film, lower alpha, and departure attenuation. No emissive/glowing-eye term was added.
- Existing mouth geometry remains unchanged. The cavity stays near-black, lip response is localized, and the cavity loses additional light instead of becoming a bright feature.
- Existing gill and inner-core geometry remains unchanged. Safe and full shaders deepen the slot core, preserve edge falloff, and suppress light through local occlusion.
- Dorsal/ventral separation remains irregular. Wet response now combines lower broad sheen with broken micro-specular highlights, darker ambient water light, and stronger shoulder curvature/far-side shaping to reduce plastic appearance.

### Water occupancy and departure

- Reworked the existing two shell passes without adding geometry or draw calls.
- The dark contact pass remains behind the opaque animal and uses broken silhouette/body/shoulder/wake density.
- The second existing pass is now composited after the opaque shark as subtle, non-luminous body-adjacent water occupancy with lower shell offset and density. Its color is fog-derived rather than cyan-white.
- Departure is phase-driven: fog/extinction rises, local contrast and key response fall, the posterior body receives earlier haze, and a restrained tail-hold mask keeps the caudal silhouette readable briefly before final dissolve.
- No raymarching, volume texture, or visible glowing outline was introduced.

### Canyon and surface opening

- Both full and safe backgrounds now contain a localized upper opening, restrained fan-shaped rays, dark irregular side-wall masks, graphite rock response, depth dimming, and departure haze.
- Canyon walls narrow subtly toward the lower frame to support the frontal mass and scale hierarchy.
- The surface opening remains brighter than the shark; global exposure was not raised.
- Full and safe canyon masks use defined ordered `smoothstep` edges; no reversed-edge behavior remains.

### Full path and real-phone safe path

- Full path marker: `v8r1-full` — retained.
- Safe path marker: `v8r1-webgl-safe` — retained.
- The safe path includes the R1 camera, hero envelope, local head/shoulder key, eye response, gill/mouth depth, water occupancy, canyon opening/walls, and departure treatment.
- Two R0 full-path GLSL defects were repaired: the full shark fragment shader now declares `uCine`, and the full environment fragment shader declares `mouthMask` before assignment. This is a static correction; local GPU compilation could not be run because no supported browser or GLSL validator is installed.

## Locked foundation confirmation

Authored large-form anatomy and VM-3R1 propulsion remain locked.

The following exact source spans are byte-identical between committed R0 and R1:

| Protected span | SHA-256 | Bytes | Result |
|---|---|---:|---|
| authored shark geometry payload/generator | `e3fdcc7866721add98ce1ad265d5e445359d91943d3c746a451fe2899f3bb73a` | 342,322 | PASS |
| full VM-3R1 propulsion vertex shader | `e830cdfe75de98184fac65f190027eb5a5afa7fbdb512000b70c32427ba501f8` | 2,843 | PASS |
| safe VM-3R1 propulsion vertex shader | `a086992a060c66206ff4693c8900f484ed09a4305326f6b492eee6be9532c035` | 1,978 | PASS |
| shark pose/trajectory function | `7000a59284f11dd968c72998620cb6d17f74af7c9df538a895aadbbbc2c9d31e` | 586 | PASS |
| inertial bank function | `d332815e432d1b6c6ec76efb7d0b1c9b6af2dcc5a6eecf9f08741e87110e2e1f` | 397 | PASS |

This explicitly preserves authored anatomy, the full and safe VM-3R1 waveforms, peduncle/caudal timing, pectoral stabilization, shark trajectory, and bank behavior.

## Static validation

- JavaScript parse, build: PASS (one inline script).
- JavaScript parse, probe: PASS (one inline script).
- Authored shark geometry: **22,920 triangles / 68,760 expanded vertices / 687,600 interleaved floats**.
- Generated scene geometry values checked, including the source procedural set and authored payload: **3,427,690**.
- Non-finite geometry values: **0**.
- Shader static integrity: every full/safe environment, shark, cornea, and water-shell source has balanced delimiters and a `main()` entry point.
- Probe-to-build identity: PASS for authored geometry, camera math, full environment shaders, safe environment shaders, full shark shaders, safe shark shaders, and the common/render integration span.
- Canvas2D context calls: **0** in build and probe.
- Textual `requestAnimationFrame` occurrences: **2** in build and **2** in probe; the existing single owned clock is unchanged and no second animation clock was added.
- Full path marker: PASS.
- WebGL-safe path marker: PASS.
- Reduced-motion media query and runtime branch: PASS.
- Deterministic byte-for-byte rebuild: PASS for build and probe.
- Current branch is not `main`; no push or force-push was performed.

## V8-R0 comparison

R0 proved the runtime and basic shot. R1 changes the visible system rather than applying a small correction:

| System | V8-R0 | V8-R1 candidate |
|---|---|---|
| camera | 11 keys, R0 framing correction | 18-key phase path, 48% larger frontal projected width, deliberate 7–9 s hold, tracking release |
| FOV | up to ~39.65° | 36.67–37.70°, composition solved by position/target/timing |
| light | retimed existing envelope | top/back motivation + spatial head/shoulder key + far-side falloff + timed rim/beam reduction |
| eye | existing globe/cornea response | darker integrated globe, narrow physical catchlight, restrained limbal film |
| mouth/gills | existing local materials | deeper cavity/slot occlusion, lower bright response, controlled wet edges |
| skin | VM-4/R0 surface | darker water ambient, broken wet micro-specular, stronger roughness/form separation |
| water | two shells before opaque shark | contact pass behind + low-density occupancy pass over body, departure density envelope |
| canyon | general underwater background | localized opening, dark irregular walls, graphite palette, portrait framing |
| departure | camera pullback + depth key | tracking release + posterior-first haze + tail hold + contrast/key/beam attenuation |
| safe path | R0 framing with simplified material | complete R1 composition, lighting, eye/gill/mouth, water, canyon, and departure treatment |
| full path | retained but static GLSL defects present | both undeclared-symbol defects repaired; runtime compile still awaits a capable browser/device |

These are analytical and code-level differences. Whether they produce the intended photographic quality on Adreno 610 is deliberately left to the real-phone visual gate.

## Browser/WebGL smoke

Status: **NOT RUN — LOCAL ENVIRONMENT UNSUPPORTED**.

- No Chromium, Chromium Browser, Google Chrome, or Firefox executable is installed.
- No Playwright, Puppeteer, `headless-gl`, `glslangValidator`, `eglinfo`, or `glxinfo` runtime is available.
- `adb devices` reported no attached Android device.
- Therefore no page-error count, GPU shader compile result, WebGL context result, context-loss result, screenshot, synthetic FPS, or phone visual result is claimed.
- Headless smoke, if later available, remains smoke evidence only and must not be treated as the visual acceptance gate.

## Real Android phone test

From the repository root:

```sh
python3 -m http.server 8765 --bind 0.0.0.0
```

On the target Android phone, open:

```text
http://127.0.0.1:8765/Problem-OCEAN-SHARK-V8-R1-CINEMATIC-REALITY-PROBE.html
```

Then:

1. Confirm the renderer reported by the probe. On the prior target this is expected to be `v8r1-webgl-safe`, but do not assume it; retain the actual exported value.
2. Tap **Start V8-R1** and record one complete automatic 12-second run with a few seconds before and after.
3. Do not touch the viewport, change orientation, switch apps, or open settings during the measured run; those events invalidate telemetry.
4. After completion, tap **JSON** and retain `V8-R1-phone-probe.json` separately from the screen recording.
5. Do not report the MP4 stream frame rate as engine FPS.
6. Record device/GPU/RAM, browser/version, selected renderer, context-loss state, shot completion, average frame interval, p95/p99, and any sustained freeze or severe slowdown exactly as observed.

## V8-R1 real-phone visual gate

Judge the actual phone recording for:

- 0–2.5 s: larger centered frontal mass, readable pectoral span, partial depth concealment, dark canyon frame, localized upper opening.
- 2.5–5.5 s: inertial approach with progressive face/eye/gill/shoulder separation and no global over-brightening.
- 5.5–9.0 s: unmistakable frontal-to-three-quarter development.
- 7–9 s: sustained head + eye + mouth + gills + cheek + shoulder + pectoral root + torso composition at the visual peak.
- 9–10.7 s: heavy body with readable peduncle/caudal propulsion and no aggressive camera shake or immediate posterior crop.
- 10.7–12 s: tracking release, falling key/contrast, rising haze/scattering, brief tail readability, and a completed silhouette dissolve rather than an empty sideways exit.
- Eye remains wet and dark, not glowing.
- Mouth remains a natural dark cavity; teeth do not become the brightest feature.
- Gills read as recessed slots, not graphic lines.
- Skin reads wet/organic rather than polished plastic.
- Water occupancy reads as local haze/contact density, not a shell halo.
- No crash, WebGL context loss, fallback, frozen shot, or catastrophic sustained slowdown.

No Visual Lock or R1 performance PASS is claimed. Work stops at **V8-R1 — REAL ANDROID VISUAL GATE**.
