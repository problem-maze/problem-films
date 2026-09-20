# VM-2R — Contact & Light Integration

Status: **CANDIDATE BUILT / PHONE VISUAL REVIEW PENDING**

## Build
- File: `Problem-OCEAN-SHARK-V7-VM2R-CONTACT-LIGHT-INTEGRATION.html`
- SHA-256: `059f2af8994ad570fec9810e04ea6d6e2b2f0a7a4630d3a3c0dab6cd4f5a166f`
- Bytes: `1,452,797`

## Probe
- File: `Problem-OCEAN-SHARK-V7-VM2R-CONTACT-LIGHT-INTEGRATION-PROBE.html`
- SHA-256: `2222b9c61c073418a316516f8f54bef1b789fe8bb1bcedcf8420ec93fa6a5d3d`
- Probe META is locked to the build SHA and size above.
- Schema: `problem-ocean-vm2r-v1`

## Scope
VM-2R is a visual-first correction pass. Large-form G2-MESH-C1 anatomy remains locked.

### Gill integration
- retained five authored surface-detail gill ribbons, but made them narrower, slightly staggered, shorter and closer to the body;
- center is darker than the edges;
- edges blend back toward skin tone instead of reading as five uniform black bars;
- specular response is reduced and concentrated toward the recessed center.

### Eye / cornea
- strengthened phone-visible corneal depth with:
  - broader low-energy film;
  - smaller hard primary catch;
  - restrained secondary catch;
  - tiny directional glint;
- globe remains near-black, avoiding a bright cartoon eye.

### Mouth
- strengthened cavity occlusion without changing jaw topology;
- wet response is concentrated toward the lip/cavity mask instead of broad glossy paint;
- cavity receives additional local attenuation so it reads deeper under the same lighting.

### Contact + light integration
- added far-side attenuation and shoulder self-shadowing to the creature shader;
- added restrained forward local scattering on grazing/backlit areas;
- replaced the single VM-2 contact shell with two low-density passes:
  1. a darker near-body / trailing soft-shadow volume;
  2. a wider fog-coloured scattering volume;
- both passes use the same animated authored mesh and move with the shark;
- added a small local-space wake offset so the volume trails the body instead of reading as a symmetric halo.

### UI cleanup
- removed the literal backslash-n artifacts that were visible above the scene in the previous phone recording;
- visual-run UI hiding remains active during the 12-second proof.

## Integrity
Remote validation:
- build SHA/bytes: PASS;
- probe SHA/bytes/META: PASS;
- JavaScript parse: PASS;
- authored geometry: 22,228 triangles / 66,684 expanded vertices;
- non-finite geometry values: 0;
- Canvas2D context calls: 0;
- textual `requestAnimationFrame` occurrences: 2;
- render paths: `vm2r-full` / `vm2r-webgl-safe`;
- no generated images.

## Phone gate
Run the VM-2R probe on the same target phone and capture the close pass.

Primary visual criteria:
1. gills must stop reading as five black graphic bars;
2. eye must read as a wet globe/cornea, not a flat black dot;
3. mouth cavity must read deeper without becoming a black smile;
4. water integration must be stronger than VM-2 but must not create a visible outline/halo;
5. far-side body shading should add mass without crushing detail;
6. no reappearance of the top-page newline artifact.

Performance is recorded only as a safety floor. Final performance recovery remains deferred until the visual master is locked.
