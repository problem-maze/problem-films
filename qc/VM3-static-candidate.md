# VM-3 — Life & Weight

Status: **CANDIDATE BUILT / PHONE MOTION CHECK PENDING**

## Build
- File: `Problem-OCEAN-SHARK-V7-VM3-LIFE-WEIGHT.html`
- SHA-256: `0714b274d514f424c3db508b4c2c88201aa0f10561aacf1fba34fa3c785bfde7`
- Bytes: `1,459,365`

## Probe
- File: `Problem-OCEAN-SHARK-V7-VM3-LIFE-WEIGHT-PROBE.html`
- SHA-256: `0f8f3a489464b6004d5341542540b1017891915586cad492101a29177b1ecb67`
- Schema: `problem-ocean-vm3-v1`
- META locked to the build SHA/size above.

## Motion changes

### 1. Head stability
- anterior head is nearly excluded from the swim-wave envelope;
- lateral amplitude grows progressively toward trunk/peduncle instead of moving the full body as a single sine wave;
- global heave was reduced to a very small low-frequency component.

### 2. Propulsion chain
- primary wave travels from trunk toward peduncle with explicit phase delay along local X;
- a smaller second harmonic breaks the mechanical single-sine appearance;
- amplitude grows strongly only near the posterior body;
- caudal rotation uses its own delayed phase at the tail pivot, so the tail reads as the final driver in the chain.

### 3. Pectoral stabilization
- removed visible fin flapping as a propulsion cue;
- pectorals now hold a small swept setpoint and apply only low-amplitude stabilization corrections;
- stabilization counters the path bank.

### 4. Inertial bank
- added a small path-dependent bank curve, peaking during the strongest turn;
- the same bank is applied to shell, hero, cornea and all local head features;
- magnitude remains subtle to avoid “airplane banking.”

### 5. Trajectory continuity
- replaced per-segment smoothstep interpolation with Catmull-Rom continuity;
- this removes artificial stop/start velocity at 3s / 6s / 9s path knots;
- camera path itself remains unchanged for VM-4.

### 6. Cross-pass continuity
- shark model transform and bank are computed once per frame and reused by contact shell, opaque hero and cornea;
- full hero vertex path now explicitly supports `uShell` / `uWake`, matching the safe path so contact-water offsets are not silently lost on full rendering.

## Preserved
- VM-2R.2 local feature geometry/material work;
- Dark Moonlight color master;
- local gill cores, cornea shell, mouth insert;
- dual contact-water system;
- large-form G2-MESH-C1 anatomy remains locked;
- no generated images.

## Integrity
Remote/static checks:
- build SHA/bytes: PASS;
- probe SHA/bytes/META: PASS;
- JavaScript parse: PASS;
- geometry: 22,920 triangles / 68,760 expanded vertices;
- non-finite geometry values: 0;
- Canvas2D calls: 0;
- textual requestAnimationFrame occurrences: 2;
- path: `vm3-full` / `vm3-webgl-safe`;
- cached shark pose: present once per frame;
- bank function: present;
- full path shell/wake uniforms: present.

## Phone gate
Use one short 12-second probe run.

Judge:
1. head stays comparatively quiet;
2. lateral energy visibly travels rearward rather than rocking the entire shark;
3. tail feels like the final propulsive driver;
4. pectorals stabilize instead of flap;
5. trajectory passes through 3/6/9s without visible easing stops;
6. bank is subtle and adds weight rather than wobble;
7. no context loss / stopped shot / catastrophic slowdown.

If motion reads physically heavier and the safety floor holds, proceed to **VM-4 — Cinematic Master**.
