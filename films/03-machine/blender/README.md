# Film 03 Blender source v1

This directory builds the approved 12-second Machine proof as a real 3D scene source rather than a 2D frame generator.

## Production intent

- articulated full-body armature with pelvis, spine, chest, clavicles, arms, legs and feet
- external IK targets for planted-foot and wrist control
- ribbon meshes with visible width
- Cloth simulation with body/floor collision and self-collision enabled
- constrained ribbon ends before frame 300, gravity-driven release after frame 300
- restrained Problem palette and perspective camera
- no new story beats beyond the approved 12-second sequence

## Build

Use the compatibility bootstrap on a machine with Blender available:

```bash
blender --background --python films/03-machine/blender/run_build.py -- --output build/machine-12s.blend
```

`run_build.py` normalizes Collision settings and render-engine discovery across Blender API variants, then invokes the authored scene in `build_scene.py`.

Then run scene QC:

```bash
blender --background build/machine-12s.blend --python films/03-machine/blender/qc_scene.py -- --report build/machine-12s-scene-qc.json
```

The repository does not claim a rendered MP4 until a render-capable runner actually executes the scene, bakes simulation, renders frames, encodes the result, and stores measured QC evidence.
