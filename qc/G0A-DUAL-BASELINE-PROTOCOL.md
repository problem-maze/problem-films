# G0A — Dual Baseline Phone Measurement Protocol

Status: ACTIVE
Branch: `ocean/v7-aaa-mobile-foundation`
Issue: #6

## Purpose
Produce comparable, real-phone evidence for the V3 visual baseline and V6 runtime/mobile baseline before any V7 optimization or visual rebuild.

## Locked sources

### V3 — Visual Reality Baseline
- File: `Problem-OCEAN-WHALE-V3.html`
- SHA-256: `129639b286d263edf2c4c9151fcac07d010d08fa36491dcc4495cef6d1c62825`
- Bytes: `1142267`

### V6 — Runtime / Mobile Baseline
- File: `Problem-OCEAN-SHARK-V6-CINEMATIC-REALISM.html`
- SHA-256: `520fed835611502889cf372c67dc701bf3cd88d106c3665db1f666c9d039e0e3`
- Bytes: `1155760`

## Test invariants
Both builds must be tested with:
- the same physical phone;
- the same browser build;
- portrait orientation;
- the same viewport;
- the same browser zoom;
- the same local-server method;
- the same quality selection policy;
- the same test duration;
- the same interaction state;
- no DevTools open;
- no concurrent heavy app started intentionally during one run but not the other.

If a condition changes, discard the pair and repeat both runs.

## Test duration
- Warm-up: 5 seconds.
- Measurement window: 30 seconds.
- One clean run per baseline is the minimum.
- If a run suffers a context loss, app switch, orientation change, or accidental interaction, mark it invalid and repeat.

## Required measurement fields

### Environment
- timestamp of run
- build id
- source SHA-256
- browser user agent
- viewport CSS width/height
- devicePixelRatio
- internal canvas width/height
- internal render scale
- WebGL version
- renderer/vendor if exposed
- selected quality mode/tier
- active render path (full/mobile-safe/other 3D)
- post-processing enabled/disabled

### Timing
- measurement duration
- rendered frame count
- presentation frame count if distinct
- average render cost in ms
- p50 render cost
- p95 render cost
- p99 render cost
- average frame interval
- p95 frame interval
- p99 frame interval
- frames >33.3 ms
- frames >50 ms
- longest frame interval
- dropped/skipped render opportunities where measurable

### Stability
- context lost count
- context restored count
- visibility pause/resume count
- resize/rebuild count
- fatal shader/program failure if any
- fallback path if any

## Instrumentation constraints
Instrumentation must:
- reuse the existing animation loop;
- not add another `requestAnimationFrame`;
- not add geometry reads;
- not call `getBoundingClientRect()` per frame;
- not mutate camera, animation, quality, scene content, material values, or timing cadence;
- not add visual effects;
- not change the normal render order;
- collect timing around the existing render work only.

## Measurement implementation guidance
- Measure actual render-call wall time with `performance.now()` immediately before and after the existing `render()` call.
- Keep frame-interval measurement independent from render-cost measurement.
- Use a bounded in-memory sample array for the 30-second run.
- Compute percentiles only after the run ends.
- Export one JSON object.
- Do not continuously repaint a benchmark overlay during the run; a small start/status/export control is acceptable if it does not animate.

## Output filenames
- `qc/G0A-v3-phone.json`
- `qc/G0A-v6-phone.json`
- `qc/G0A-comparison-report.md`

## Comparison questions
The report must answer:
1. Which V3 visual systems are materially stronger and should survive into V7?
2. Which V3 systems are too expensive or structurally unsafe for the target phone?
3. Which V6 runtime systems measurably improve stability or cost?
4. Which V6 changes reduce visual quality without enough performance benefit?
5. Is the dominant bottleneck geometry, fragment shading, post-processing, particles/overdraw, or CPU/runtime overhead?
6. What is the first G0B transplant candidate with the lowest visual risk?

## G0A PASS gate
G0A = PASS only if:
- both SHA-256 values match;
- both reports were captured on the same phone setup;
- both active 3D paths are known;
- the reports are directly comparable;
- no optimization was mixed into the measurement build;
- the first G0B transplant candidate is justified by evidence.

Otherwise: REWORK G0A.
