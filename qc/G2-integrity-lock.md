# G2 — Integrity Lock

Purpose: prove that G2 changes anatomy while preserving the established environment/camera/runtime foundation.

Compared:
- G1 source: `Problem-OCEAN-SHARK-V7-G1-REALITY-PROOF.html`
- G2 candidate: `Problem-OCEAN-SHARK-V7-G2-ANATOMY-REBUILD.html`

Byte-identical blocks:
- `makeOceanGeometry()`: `af1e07c6221e9a7ee78bbfbc49c4a1cc9202a163104541fc68d4e636602d248d`
- V3 `OCEAN_SHADERS`: `e43cc809603a7c3d0a529ee4d49b9d20802a85a10018cab602147e49c1157135`
- G1/G2 hero material+motion shader body: `db3b7d7614b1c5edc645ff42d1a094efaab2cbb5e895060a6e77513d09e7ee46`
- `OceanMath` / 12-second camera math: `1f183c1f5cd4e2f17523621fc314d0c6b13b48f93705d694719419b8f73df30d`

Runtime invariants:
- requestAnimationFrame textual occurrences: G1=2, G2=2
- Canvas2D context calls in G2: 0
- old CSS-width forced-low predicate: 0
- constrained-device rule unchanged: reported memory <=3 GB or reported logical cores <=4

Geometry budget:
- G1 hero: 33,612 triangles
- G2 LOD0 hero: 43,724 triangles (+10,112 / +30.1% hero)
- G1 major rendered scene: ~77,139 triangles
- G2 major rendered scene: ~87,251 triangles (+13.1% total major scene)
- G2 LOD1: 23,784 hero triangles
- G2 LOD2: 15,708 hero triangles

The geometry increase is intentionally isolated to the close-anatomy proof and is now subject to the target-phone probe. No performance claim is made until that run returns.
