# G2-MESH — Real-phone Performance + Visual Review

## Decision
**AUTHORED-MESH ARCHITECTURE: PASS**
**GREAT-WHITE SPECIES CALIBRATION: ONE CONTROLLED PASS REQUIRED**
**DO NOT RETURN TO PROCEDURAL SHARK.**

## Performance
Target-phone run completed:
- active path: `g2mesh-full`
- quality: balanced
- post-processing: ON
- scale: 1.11 → 1.30
- 357 frames / 11.982 s ≈ **29.79 fps**
- mean frame interval: 33.538 ms
- p95/p99: 33.5 / 33.5 ms
- >50 ms: 1 frame
- max: 55.7 ms
- context loss: 0

The authored hero is 22,128 triangles versus 50,948 triangles for G2-R1, so the new topology gives substantial geometry headroom while preserving the same ~30 fps presentation envelope.

## Visual review of close pass
Material improvement over the procedural G2-R1 is clear:
- silhouette reads as one authored animal rather than assembled procedural pieces;
- torso continuity is much stronger;
- pectoral sweep/root integration is substantially better;
- caudal silhouette and root continuity are more coherent;
- frontal and three-quarter reads are recognizably shark-like at close range.

Remaining blockers are now narrower and more specific:
1. **Species calibration:** snout/head is still somewhat pointed/generic relative to a great-white's broader, blunter cranial wedge.
2. **Eye:** placement is better, but it still reads as a dark dot because current optics/material are primitive.
3. **Gills:** insufficiently readable in the close pass; current geometry/material combination does not expose the five slots strongly enough.
4. **Countershading:** the white/gray boundary is visibly jagged/polygonal because the old procedural UV/material mapping is being applied to a new authored mesh.
5. **Mouth:** the authored model gives a cleaner facial silhouette, but the mouth lacks the wet volumetric read required later.
6. **Skin:** still flat/CG due to inherited G2 shader; not an anatomy failure.
7. **Motion:** current coarse part-tag deformation is only a compatibility bridge. The source model has a 43-joint rig and one authored animation; locomotion should eventually use a more anatomical chain rather than rely on the legacy procedural deformation.

## Correct next step
Create **G2-MESH-C1 — Great White Species Calibration**. Keep the authored topology and perform only controlled large-form deformation:
- blunt/widen rostrum;
- strengthen cheek/shoulder wedge;
- calibrate eye socket position;
- make five gill slots legible without painting fake lines;
- verify pectoral and caudal proportions.

Then enter **G3** to solve the now-dominant material problems:
countershading, skin, eye optics, mouth wetness, gill shading.

The architecture change itself is accepted. Returning to the old procedural body is rejected unless new evidence shows a regression.
