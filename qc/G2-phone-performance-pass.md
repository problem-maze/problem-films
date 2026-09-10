# G2 Phone Run — Performance Gate

Status: **PERFORMANCE PASS / VISUAL GATE PENDING**

## Verified target phone
- Android 15 / SM-A057F
- Adreno 610
- 384×731 CSS px, DPR 2.8125
- 4 GB reported memory / 8 logical cores
- active path: `g2-full`
- quality: `balanced`
- post-processing: ON

## 12-second result
- shot completed successfully
- 357 rendered frames in 11.969 s ≈ **29.83 fps**
- internal scale: **1.17 → 1.30**
- internal canvas: 449×856 → 499×951
- average frame interval: **33.507 ms**
- p95: **33.5 ms**
- p99: **33.5 ms**
- >50 ms: **1 frame**
- max: **55.7 ms**
- context loss: **0**

## Comparison to G1
G1 valid phone run:
- 357 frames / 11.980 s ≈ 29.80 fps
- avg interval 33.538 ms
- p95 33.5 ms
- >50 ms: 1
- max 55.7 ms
- scale 1.20 → 1.30

G2:
- 357 frames / 11.969 s ≈ 29.83 fps
- avg interval 33.507 ms
- p95 33.5 ms
- >50 ms: 1
- max 55.7 ms
- scale 1.17 → 1.30

Interpretation:
The anatomy rebuild increased the hero from 33,612 to 43,724 triangles, yet the target-phone presentation cadence is effectively unchanged. The phone still reaches scale 1.30 on the full 3D path with post-processing enabled.

This does **not** prove the new anatomy is visually good. It proves that the G2 geometry increase is affordable enough on this phone at the current 30 fps operating point.

## Decision
- G2 performance: **PASS**
- G2 visual anatomy: **PENDING**

Required next evidence:
one close-pass video or screenshot from seconds 6–9 for direct anatomy review. G3 remains blocked until that visual gate is decided.
