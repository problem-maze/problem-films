# G2 — Shark Anatomy Rebuild / Static Candidate

Status: **CANDIDATE BUILT / PHONE + VISUAL EVIDENCE PENDING**

## Candidate
- File: `Problem-OCEAN-SHARK-V7-G2-ANATOMY-REBUILD.html`
- SHA-256: `570fd16788be4aa459f3f4ad6bb40d0e00fa7f342a0c277c5490ec35e6e7c75a`
- Bytes: `1115326`

## Phone probe
- File: `Problem-OCEAN-SHARK-V7-G2-ANATOMY-REBUILD-PROBE.html`
- SHA-256: `0b710981f2ca54a662f284553042c2cb33c373cfbae694bc5469b09232358137`
- Bytes: `1122423`

## G1 defects addressed geometrically
1. **Head / snout**
   - widened the snout and removed the needle-like front collapse;
   - rebuilt cranial profile into a broader wedge with cheek/shoulder mass;
   - added a rounded nose cap so the mesh closes without a pin-point.

2. **Jaw / mouth**
   - cut a real geometric mouth opening in the body shell;
   - added a separate mandibular capsule for lower-jaw mass;
   - added recessed cavity roof, floor and side walls;
   - added jaw-edge lip geometry;
   - replaced the straight graphic tooth row with irregular volumetric teeth following a curved jaw arc.

3. **Eye**
   - added socket fairing;
   - larger recessed eye globe;
   - separate corneal dome.

4. **Gills**
   - five curved, staggered slit surfaces per side;
   - each slit has a forward lip edge to create depth instead of a flat drawn line.

5. **Pectoral root**
   - added shoulder/root fairing;
   - rebuilt hydrofoil rows with a thicker root and smoother lateral extension.

6. **Torso / peduncle**
   - rebuilt the full longitudinal profile with more muscular shoulder/trunk;
   - widened the pre-caudal region to remove the pinched tail-root read;
   - added lateral lamnid keels and a caudal root hub.

7. **Tail**
   - rebuilt a clearly heterocercal silhouette;
   - stronger/longer upper lobe, shorter lower lobe;
   - true lateral thickness instead of an almost graphic planar tail.

## LOD-ready anatomy generator
The G2 generator supports three deterministic detail levels even though the current G2 proof renders LOD0 only:
- LOD0: **43,724 triangles**
- LOD1: **23,784 triangles**
- LOD2: **15,708 triangles**

All three produce finite geometry with the same overall bounding volume.

## Static validation
- JavaScript syntax: PASS.
- LOD0/1/2 geometry: PASS, zero NaN/Infinity.
- LOD0 bbox: x -6.84..7.36, y -2.42..3.50, z -4.33..4.33.
- No Canvas2D fallback introduced.
- G0B mobile runtime architecture preserved.
- G1 12-second shot/camera structure preserved for direct before/after anatomy judgment.
- G2 active render paths are `g2-full` / `g2-webgl-safe`.

## Important scope boundary
This is **anatomy work**, not the final realism pass.
Skin microstructure, eye optical behavior, mouth wetness, tooth material, muscular force propagation and advanced water/lighting remain intentionally reserved for G3–G5.

## Gate
G2 is not PASS yet.

Required next evidence:
1. one 12-second target-phone probe JSON;
2. one screen recording or close-pass screenshot from seconds 6–9;
3. comparison against G1 for head/jaw/eye/gills/pectoral-root/peduncle/tail;
4. decision PASS / REWORK before G3.
