# V8 Acceptance Gates

## Visual gate
A phone recording must show:
- one unmistakable hero frame with head + shoulder + eye + gills readable;
- body mass remains convincing before and after that frame;
- tail propulsion remains visible;
- no premature head crop;
- no long empty departure;
- water contact without halo;
- no obvious plastic/glowing material response.

## Runtime safety gate
Required during visual development:
- no crash;
- no WebGL context loss;
- no fallback;
- no frozen shot;
- no severe sustained slowdown.

## Performance gate
Deferred until visual lock.

Final recovery target remains:
- stable phone runtime near the project's 30 FPS acceptance class;
- preserve the close-pass master quality;
- safe path remains available for weaker devices.

## Change discipline
Before editing a subsystem, state whether the problem is:
- framing,
- light,
- material,
- local geometry,
- water/contact,
- motion,
- performance.

Do not solve a camera problem with geometry or a lighting problem with texture complexity.
