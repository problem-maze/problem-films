# G0A — Dual Baseline Comparison Report

Status: **PASS**
Device evidence: Android 15, SM-A057F, Adreno 610, Chrome 151, 384×731 CSS px, DPR 2.8125.

## Measured result

### V3 — Visual Reality Baseline
- Render path: `v3-full`
- Quality tier: `low`
- Post-processing: OFF
- Internal scale: 0.88
- Internal canvas: 338×644
- Rendered frames: 898 / 30.006 s ≈ 29.93 fps
- Mean frame interval: 33.414 ms
- p95 / p99: 33.5 / 33.5 ms
- >50 ms frames: 0
- Max interval: 33.6 ms
- Context loss: 0

### V6 — Runtime/Mobile Baseline
- Render path: `webgl-safe`
- Quality tier: `balanced`
- Post-processing: ON
- Internal scale: 1.20 → 1.30
- Internal canvas: 461×878 → 499×951
- Rendered frames: 893 / 30.024 s ≈ 29.74 fps
- Mean frame interval: 33.563 ms
- p95 / p99: 33.5 / 33.5 ms
- >50 ms frames: 2
- Max interval: 89.1 ms
- Context loss: 0

## Interpretation

The key result is not that V6 has a lower CPU wall-time around `render()`; it does not. V3 averages ~0.343 ms and V6 ~0.431 ms. Those values are CPU wall time around command submission, not GPU timing, so they must not be used as raw GPU performance.

The stronger result is that V6 sustains essentially the same ~30 fps presentation while running at a much higher internal pixel count, with balanced quality and post-processing enabled. At the end of the run V6 renders ~474k pixels/frame versus ~218k for V3, about 2.18× the internal pixel count.

V3 is extremely stable, but its old device-classification logic locks this phone to `low`, scale 0.88, and no post-processing. That protects cadence but suppresses visual quality before measured evidence justifies the downgrade.

V6 demonstrates the more useful mobile runtime policy: it can enter a safe 3D WebGL path, hold ~30 fps, and raise scale to 1.30 on this Adreno 610 device. Its two >50 ms frames and one 89.1 ms maximum interval are small but real stability regressions to investigate during G0B/G7.

## G0A decisions

### Preserve from V3
Use V3 as the visual-reality reference for:
- ocean depth and atmospheric composition;
- scale cues and scene density;
- environmental layering and spatial read;
- camera feel and broad scene composition;
- the principle that the animal is integrated into a larger ocean rather than presented as an isolated demo model.

### Transplant from V6
First runtime candidates:
1. mobile-safe WebGL initialization / safe 3D path;
2. measured render-cost driven quality scaling;
3. dynamic internal render scale;
4. explicit GPU resource cleanup during render-target rebuilds;
5. context/lifecycle recovery;
6. quality-tier logic that does not classify a phone as low only because its CSS width is below 700 px.

### Do not inherit blindly
From V3:
- width-based forced-low policy;
- static 0.88 mobile scale;
- duplicated expensive animal draw without measured value;
- old auto-quality logic tied to presentation cadence.

From V6:
- current shark anatomy as the final visual target;
- any visual downgrade whose benefit is not measured;
- the occasional long-frame regression without investigation.

## First G0B candidate

Create **V7 Hybrid Runtime Foundation** with V3-led visual composition and V6-led runtime control.

The first transplant is deliberately narrow:
- replace V3's device-width forced-low policy with measured tier selection;
- bring over V6's safe WebGL initialization and dynamic render scale;
- preserve V3 scene/camera/material values unchanged at first;
- keep one animation clock;
- add no new visual effect.

## Gate

G0A = **PASS**.

Proceed to G0B only. G1 anatomy/material/lighting work remains blocked until the hybrid runtime proves that V3's visual foundation can survive on the phone without the old forced-low policy.
