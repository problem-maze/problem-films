# VM-2R.1 — Depth Cue Correction

Status: **CANDIDATE BUILT / ONE SHORT PHONE VISUAL CHECK PENDING**

## Build
- File: `Problem-OCEAN-SHARK-V7-VM2R1-DEPTH-CUE-CORRECTION.html`
- SHA-256: `f8f71bad1677221da017f1d5117ed8beb79b1909504d8a8eb843e87217378540`
- Bytes: `1,453,315`

## Probe
- File: `Problem-OCEAN-SHARK-V7-VM2R1-DEPTH-CUE-CORRECTION-PROBE.html`
- SHA-256: `2cc2eade737f6a91faec0ec8319c216c0e02ea92c5cfd191decf6ef40a6345d0`
- Schema: `problem-ocean-vm2r1-v1`
- Probe META is locked to the build SHA/size above.

## Scope
This is the small correction pass before VM-3. Large-form G2-MESH-C1 anatomy remains locked.

### Gills
- kept five geometric surface-detail slits, but tapered their width at both ends;
- pulled them closer to the body;
- increased skin-tone blending at slit edges;
- concentrated darkness into the center rather than the whole ribbon.

### Eye / cornea
- deeper near-black globe base;
- stronger limbal falloff;
- wider but low-energy corneal veil;
- small curved corneal band plus tiny directional glint;
- still deliberately avoids a bright/cartoon eye.

### Mouth
- narrowed and deepened the cavity mask;
- separated cavity depth from lip wetness more strongly;
- increased center attenuation;
- kept wet response localized so it does not become a painted black smile.

### Water / depth cue
- stronger grazing local scattering;
- stronger but more silhouette-concentrated water wrap;
- dark contact shell density raised moderately;
- fog shell density/extent raised moderately;
- wake offsets remain asymmetric to avoid a symmetric halo.

### Visual-run cleanup
- status and header controls now hide during the 12-second visual proof;
- the proof should present only the scene while judging the close pass.

## Integrity
Remote validation:
- build SHA/bytes: PASS;
- probe SHA/bytes/META: PASS;
- JavaScript parse: PASS;
- authored geometry: 22,228 triangles;
- non-finite geometry values: 0;
- Canvas2D context calls: 0;
- textual requestAnimationFrame occurrences: 2;
- paths: `vm2r1-full` / `vm2r1-webgl-safe`;
- no generated images.

## Gate
One short phone recording is enough.

Judge only:
1. gills: slits, not five bars;
2. eye: wet globe/cornea, not black dot;
3. mouth: deeper cavity without graphic smile;
4. water: stronger body-volume integration without halo.

If these four cues pass visually, proceed directly to **VM-3 — Life & Weight** without reopening anatomy.
