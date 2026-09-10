# G0B — Hybrid Runtime Foundation Phone Report

Status: **PASS**

## Device
Android 15 / SM-A057F / Adreno 610 / Chrome 151
Viewport 384×731 CSS px, DPR 2.8125, deviceMemory 4 GB, hardwareConcurrency 8.

## Actual V7 runtime path
- renderPath: `full`
- qualityTier: `balanced`
- postProcessing: ON
- internalRenderScale: 1.30
- internal canvas: 499×951
- context loss/restore: 0 / 0
- resize events during measurement: 0

This is the key G0B result: the phone no longer falls into the V3 forced-low path. It runs the **full V3 visual shader path** at balanced quality and scale 1.30.

## Frame evidence
- 893 rendered frames in 30.061 s ≈ **29.71 fps**
- average interval: 33.651 ms
- p50: 33.4 ms
- p95: 33.5 ms
- p99: 33.5 ms
- >50 ms: 2 frames
- longest interval: 133.6 ms

The 133.6 ms outlier is real and is carried forward as a stability item for G7. It does not invalidate G0B because the cadence distribution is otherwise tightly locked near the 30 fps presentation target and there was no context loss.

## Comparison against G0A
- V3 baseline: ~29.93 fps at scale 0.88, low tier, post OFF, `v3-full`.
- V6 baseline: ~29.74 fps at scale 1.20→1.30, balanced, post ON, `webgl-safe`.
- V7 G0B: ~29.71 fps at scale 1.30, balanced, post ON, **`full`**.

V7 therefore reaches the higher-resolution operating envelope of V6 while retaining the full V3 geometry/shader/camera/render core instead of dropping to V6's safe visual path.

## Visual-preservation evidence
Static G0B validation already verified that V3 geometry, full shader set, camera math, and main render scene order are byte-for-byte preserved. This phone run confirms that the active runtime path is `full`, not the safe fallback. Therefore the phone is executing the preserved V3 visual core.

## Decision
**G0B = PASS.**

Proceed to G1 — 12-second Reality Proof.

G1 must now create the first deliberate visual improvement. It may change the hero animal and shot staging, but must keep the proven G0B runtime foundation and must not reintroduce width-forced-low or any 2D/cartoon fallback.
