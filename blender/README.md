# Blender Production Layer

Blender is the intended 3D production layer for Problem Films when a render-capable machine is connected.

## Scene responsibilities

- Problem world background and floor
- Canonical character rig
- Machine and eye assets
- Ribbon surfaces and contact zones
- Camera, lighting, color management, and render profiles

## Motion responsibilities

- planted feet and controlled steps
- spine, chest, shoulder, and pelvis articulation
- ribbon surface deformation, sag, release, gravity, and collision
- micro-motion during held tension

## Output rule

Review renders start at native 1920×1080. A file is described as native 4K only when the scene is rendered directly at 3840×2160.

Heavy render frames and simulation caches are outputs, while the reusable scene rules, rig definitions, material definitions, and shot timing remain versioned source assets.
