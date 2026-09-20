# VM-2R.2 — Local Feature Depth

Status: **CANDIDATE BUILT / ONE PHONE VISUAL CHECK PENDING**

## Build
- File: `Problem-OCEAN-SHARK-V7-VM2R2-LOCAL-FEATURE-DEPTH.html`
- SHA-256: `84150c6529f5a068bbd196d41814d6a4567eda7c3737199159cd56c96cb06493`
- Bytes: `1,457,449`

## Probe
- File: `Problem-OCEAN-SHARK-V7-VM2R2-LOCAL-FEATURE-DEPTH-PROBE.html`
- SHA-256: `b65a091b25edfef5986ce980913af2c02d10d4b37e4b89aead8656f7216f24a6`
- Schema: `problem-ocean-vm2r2-v1`
- Probe META is locked to the build SHA/size above.

## Why this pass exists
VM-2R.1 showed that shader-only tuning had mostly reached its useful limit on the phone close pass. VM-2R.2 adds minimal local geometry only where depth still read as graphic/flat. Large-form G2-MESH-C1 anatomy stays locked.

## Local geometry additions
- gill inner cores: +100 triangles;
- authored-eye corneal shell: +512 triangles;
- shallow mouth insert: +80 triangles;
- total authored shark geometry: **22,920 triangles**.

### Gills
- retained the existing five outer slit ribbons;
- added a narrower inner core for each slit, slightly closer to the body;
- center core is darker and lower-energy than the outer tissue;
- outer tissue still tapers into skin, so the target read is “slot + recessed core,” not two parallel stripes.

### Eye / cornea
- retained the near-black authored eye globe;
- duplicated the authored eye topology as a thin shell expanded ~0.03 local units;
- the shell is discarded from the opaque hero pass;
- a dedicated transparent cornea pass renders only material 12 with Fresnel edge, primary specular catch and restrained secondary response.

### Mouth
- added a shallow, tapered local cavity strip on each side of the jaw;
- center vertices sit closer to the body than lip-edge vertices, producing a small geometric depth cue;
- cavity material stays dark/low-roughness with localized wet specular;
- no large jaw topology change.

### Water / contact
- retained the VM-2R.1 dual shell system;
- only the near-body dark pass was strengthened;
- the dark pass is now weighted toward the body mask so fins/edges do not become a uniform halo.

### Motion continuity
- head-local materials above material 8.5 now inherit the same subtle body vertical life in the full path, preventing local eye/gill/cornea/mouth pieces from visually lagging behind the head.

## Integrity
Remote/static validation:
- JavaScript parse: PASS;
- geometry finite values: PASS;
- triangles: **22,920**;
- expanded vertices: **68,760**;
- material vertex counts:
  - body 0: 64,848
  - eye globe 9: 1,536
  - outer gills 10: 300
  - inner gill cores 11: 300
  - cornea shell 12: 1,536
  - mouth insert 13: 240
- Canvas2D calls: 0;
- textual requestAnimationFrame occurrences: 2;
- paths: `vm2r2-full` / `vm2r2-webgl-safe`;
- no generated images.

## Gate
One short phone recording only.

Judge:
1. gills: visible slot depth instead of five bars;
2. eye: globe + separate corneal surface instead of black dot;
3. mouth: real shallow cavity cue instead of a painted line;
4. water: stronger near-body occlusion without a visible halo.

If these pass, close the material/water depth loop and move directly to **VM-3 — Life & Weight**.
