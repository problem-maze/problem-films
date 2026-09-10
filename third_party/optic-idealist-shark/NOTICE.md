# Optic_idealist Shark — authored mesh candidate

G2-MESH uses geometry derived from the following clearly attributed asset:

- Work: **Shark**
- Creator: **Optic_idealist**
- Original source: https://sketchfab.com/3d-models/shark-8bcd4d861bd84e87b2832e83c9cb898b
- Redistribution inspected: `bob6664569/open-water/site/assets/animals/fish/shark.glb`
- License: **Creative Commons Attribution 4.0 International (CC BY 4.0)**
- License URL: https://creativecommons.org/licenses/by/4.0/
- Inspected GLB SHA-256: `1056b1bc09f11e259aca73f7d56e7b614ddff64299c2530990e792878a6a6610`
- Inspected GLB size: `7,072,212 bytes`
- Upstream geometry: 21,616 body triangles + 512 eye triangles = **22,128 triangles**
- Rig metadata: 43 joints, one animation (`Action_Shark Armature`)

## Project handling

The full third-party GLB is **not vendored in this branch**. An earlier transfer attempt created an empty file; that empty artifact was removed.

The G2-MESH HTML candidate embeds a compact geometry-only derivative of the body and eye meshes. The source texture, full GLB container, and upstream runtime are not bundled. The derivative keeps the creator/source/license attribution in the HTML source.

This asset is an **authored shark anatomy candidate**, not yet claimed to be a definitive Carcharodon carcharias / Great White reference. The phone close-pass gate must decide whether its silhouette is good enough for the project before material and motion work proceed.

Changes made by Problem:
- geometry extracted from the GLB;
- positions quantized for embedding and restored at runtime;
- normals compacted;
- indexed geometry expanded into the existing WebGL vertex layout;
- procedural UV coordinates generated for the existing Problem shader;
- existing Problem 12-second shot, ocean and mobile runtime retained.

Attribution and change notice are retained for CC BY 4.0 compliance.
