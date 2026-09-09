# OCEAN SHARK — AAA Mobile Realism Master Plan

Status: ACTIVE
Branch: `ocean/v7-aaa-mobile-foundation`
Repository: `problem-maze/problem-films`
Baseline artifact: `Problem-OCEAN-SHARK-V6-CINEMATIC-REALISM.html`
Baseline SHA-256: `520fed835611502889cf372c67dc701bf3cd88d106c3665db1f666c9d039e0e3`
Baseline size: 1,155,760 bytes
Target: a highly realistic real-time shark/ocean experience that remains usable on phones, with no generated still images used as a shortcut.

## 0. Non-negotiable rules

1. Do not modify `main` directly. Work only on review branches and merge by PR after evidence.
2. Do not use generated still images, fake video backgrounds, image zoom/pan, or AI-morph shortcuts.
3. Realism must come from geometry, materials, lighting, animation, camera, water, and physically coherent secondary motion.
4. Never replace a failed 3D path with a cartoon/2D fallback. A fallback may reduce cost, but must stay 3D.
5. Every phase must preserve a known-good previous build.
6. A phase is not complete because the code exists. It is complete only after its acceptance evidence is collected.
7. Mobile quality reductions must remove invisible cost first: distant geometry, samples, particles, shadow/volumetric work, and internal resolution. They must not intentionally turn the visible shark into a flat/cartoon representation.
8. No claims about FPS, visual fidelity, thermal stability, memory stability, or browser compatibility without measured evidence.
9. Keep the Problem visual identity: deep `#040608`, lunar white `#E1EBF8`, restrained functional cyan only.
10. Prefer one controlled cinematic encounter over an unnecessarily large world. Spend the rendering budget near the camera.

## 1. Definition of success

The goal is not “GTA in a browser.” The achievable target is a compact, controlled scene that can produce the same *per-shot impression* of a high-end game cinematic while remaining real-time on a phone.

A successful build must satisfy all of these:

- The shark reads as an animal rather than procedural CG at normal phone viewing distance.
- Near-pass shots do not expose obviously broken anatomy, plastic materials, rigid-body swimming, flat eyes, or pasted-on lighting.
- The shark visually belongs inside the water: depth attenuation, backscatter, haze, caustics/light breakup, and contact darkening respond coherently.
- Motion shows body mass, inertia, delayed tail response, fin stabilization, and camera buoyancy.
- No cartoon fallback is used.
- Touch interaction, resize/orientation, background/foreground resume, and WebGL context recovery remain functional.
- Mobile acceptance is performed on real target-class devices, not inferred from desktop rendering.
- The build can hold a stable usable frame cadence on the target phone profile without long freezes.

## 2. Target hardware and operating envelope

Primary mobile acceptance profile:
- 390×844 and 360×800 portrait
- 4 GB RAM class Android phone
- 30 fps presentation target
- quality system allowed to reduce internal resolution and scene cost
- no requirement for 60 fps

Secondary profile:
- stronger Android device / desktop browser
- higher LOD and richer volumetrics may activate automatically

The project will use a frame-budget model rather than a single polygon-count target. Polygon count, overdraw, fragment shader cost, post-processing, particles, texture bandwidth, and CPU work all count.

## 3. Working architecture

During development, the scene should be separated conceptually even if the final release is rebundled into one HTML file:

- `engine/` — render loop, lifecycle, WebGL capability, timing
- `shark/` — anatomy, mesh construction/import path, LODs, deformation
- `materials/` — skin, eye, mouth, teeth, roughness/normal logic
- `ocean/` — water color, attenuation, haze, particles, caustics, light shafts
- `camera/` — shot path, inertia, buoyancy, near-pass framing
- `quality/` — device tier, dynamic scale, LOD, feature switches
- `qc/` — measurements and acceptance reports
- `builds/` — immutable review HTML builds

Final delivery may return to a single self-contained HTML after the system is stable.

---

# PHASE G0 — Baseline lock and measurable truth

## Work
- Import V6 unchanged as the reference build.
- Record exact SHA-256, byte size, rendering paths, shader programs, draw calls, triangle estimates, particle counts, and lifecycle hooks.
- Add measurement-only instrumentation without changing the visual result.
- Record actual render time separately from the intentional 30 fps presentation cadence.
- Record WebGL renderer/version if exposed, viewport, DPR, internal render scale, quality tier, context loss, and recovery.

## Acceptance gate
G0 is complete only when:
- the imported V6 hash matches the source artifact;
- one desktop run and one real-phone run produce stored measurement reports;
- we know which path actually runs on the phone;
- no visual change has been introduced.

## Output
- `qc/G0-baseline-report.md`
- immutable V6 baseline build
- phone JSON measurement evidence

---

# PHASE G1 — 12-second realism proof

Before building a long journey, create one controlled 12-second proof. This follows the repository’s existing philosophy of proving physics/cinematic quality before expansion, but this is a new Ocean gate rather than a change to Film 03.

## Shot
0–3 s: distant emergence through haze
3–6 s: approach toward camera
6–9 s: close side pass where skin, eye, gills, mass, and water interaction are visible
9–12 s: tail exits into blue haze

## Why
If the shark cannot survive a close 12-second shot, adding more environment or story will hide—not solve—the realism problem.

## Acceptance gate
- no obvious anatomy collapse in head, jaw, gill, pectoral-root, peduncle, or caudal-fin silhouette;
- no rigid “whole model swings” motion;
- no plastic eye/skin read;
- no camera movement used to hide defects;
- mobile path still renders the same scene in 3D.

---

# PHASE G2 — Shark anatomy rebuild

## Work
Rebuild the visible animal in priority order:
1. cranial silhouette and snout volume;
2. jaw/mouth cavity and lip seam;
3. five gill slits per side with correct placement;
4. shoulder/pectoral-root transition;
5. dorsal profile;
6. belly and countershading boundary;
7. caudal peduncle and keels;
8. heterocercal caudal-fin proportions;
9. eye socket/cornea geometry;
10. fin thickness and leading/trailing edges.

Mesh density is concentrated where silhouette curvature and close-up lighting need it. Do not increase tessellation uniformly.

## LOD deliverables
- LOD0: close cinematic
- LOD1: normal interaction
- LOD2: distant/mobile economy

## Acceptance gate
Compare the three camera distances in silhouette, shaded view, and motion. LOD transitions must not visibly pop during the 12-second proof.

---

# PHASE G3 — Skin, eye, mouth, and material realism

## Work
- directional micro-surface aligned with the body rather than screen/world axes;
- nonuniform roughness;
- wet specular layer constrained by angle and light;
- soft irregular countershading boundary;
- sparse scars/abrasions with no decorative repetition;
- gill tissue variation;
- dark mouth cavity with controlled moisture response;
- tooth material separate from skin;
- corneal layer/highlight over a dark eye;
- distance-based detail attenuation to avoid shimmering on mobile.

No generated image textures are required for this phase. Procedural maps and code-driven material variation remain acceptable.

## Acceptance gate
Close side pass must no longer read as smooth plastic, chrome, or painted clay. Micro-detail must remain stable at phone resolution without aliasing noise.

---

# PHASE G4 — Muscular locomotion

## Work
Replace simple sinusoidal deformation with a segmented locomotion model:
- head: near-stable;
- shoulder: low amplitude;
- trunk: controlled lateral flex;
- posterior body: stronger flex;
- peduncle: delayed, high-energy transfer;
- tail: highest amplitude with phase lag;
- pectorals: stabilization/turn response;
- dorsal/pelvic fins: subtle secondary response;
- roll and vertical corrections tied to steering, not random looping.

Add acceleration/deceleration envelopes so movement has inertia. Camera-relative speed must not create an artificial “model on rails” impression.

## Acceptance gate
Slow-motion inspection of the 12-second proof must show force traveling down the body rather than every segment changing direction simultaneously.

---

# PHASE G5 — Water and lighting integration

## Work
- depth- and distance-dependent spectral absorption;
- forward/back scattering approximation;
- layered suspended particles with depth-dependent density;
- soft volumetric shafts tied to light direction;
- caustic breakup without repetitive geometric stripes;
- local light attenuation around the shark;
- subtle contact darkening/occlusion cues;
- fog color linked to depth;
- underwater exposure and tone response that preserve lunar-white highlights without cyan/neon wash.

## Acceptance gate
A neutral-material shark inserted into the scene must still read as submerged due to lighting and atmosphere alone. The final material then adds, rather than creates, the underwater illusion.

---

# PHASE G6 — Cinematic camera and encounter staging

## Work
- strong shot composition before motion;
- slight buoyancy and operator inertia;
- predictive framing through the near pass;
- delayed camera catch-up after the shark crosses;
- no excessive handheld shake;
- no fast cuts used to conceal defects;
- touch orbit/zoom disabled or constrained during critical auto-shot moments only when needed for composition, then returned to the user.

## Acceptance gate
The 12-second shot remains readable with UI hidden and without explanatory text.

---

# PHASE G7 — Mobile rendering architecture

## Work
Build real cost scaling, not a visual-style fallback:
- dynamic internal resolution;
- LOD selection by projected size;
- distance culling;
- lower volumetric samples;
- lower particle counts;
- reduced post-processing passes;
- lower-cost material branch for distant objects;
- post-processing disabled before close-shark material fidelity is sacrificed;
- texture/memory budget checks;
- resize and orientation-safe framebuffer reuse;
- explicit GPU resource deletion;
- context-loss/restore verification;
- one owned animation clock.

## Performance gate
Target a stable usable ~30 fps presentation on the primary phone class. If the device cannot hold that, the system must identify the dominant cost before any visual downgrade is approved.

Frame stability matters more than a high average with freezes.

---

# PHASE G8 — Interaction and phone usability

## Work
- touch drag/orbit;
- pinch zoom;
- journey/play/pause;
- readable controls with safe areas;
- portrait first;
- no accidental page scroll during scene interaction;
- resume after app switching;
- reduced-motion behavior that preserves a valid static/low-motion 3D scene;
- browser capability message only if no viable 3D WebGL path exists.

## Acceptance gate
Full user journey is completed on a real phone without desktop devtools intervention.

---

# PHASE G9 — Full scene expansion

Only after G1–G8 pass.

Expand from the 12-second proof to the longer encounter:
- emergence
- approach
- inspection
- near pass
- descent
- distant silhouette
- return toward light

Do not add new wildlife/effects merely to increase spectacle. Every added element must improve scale, depth, realism, or story.

---

# PHASE G10 — Golden mobile lock

## Required evidence
- source SHA-256
- build SHA-256
- browser/device/viewport/DPR
- quality tier selected
- average and percentile render/frame times
- long-frame count
- context-loss result
- memory/resource lifecycle notes
- screenshots/video captured from the actual real-time phone build for review (evidence only, never used as the scene itself)
- list of unresolved visual compromises

## Final acceptance
The project is complete only when:
1. the realism gate is visually approved;
2. the target phone can run the approved 3D path;
3. no cartoon/2D substitute is present;
4. performance evidence is stored;
5. the final build is frozen and tagged/merged through review.

---

# Stop conditions and decision rules

At the end of every phase choose one:
- PASS — evidence meets the gate; proceed.
- REWORK — same phase continues.
- REVERT — restore previous immutable build.
- ARCHITECTURE CHANGE — only if measurement proves the current path cannot meet the mobile target.

Never proceed merely because a version number was produced.

# Immediate next action

Start G0. Import V6 unchanged, preserve its SHA-256, create measurement-only instrumentation, and obtain the first real-phone baseline before changing anatomy, materials, water, or camera.
