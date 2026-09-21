# V8 Reconstruction Roadmap

## V8-R0 — Reference Decomposition & Shot Reconstruction
Lock one canonical 12-second shot from the four reference directions.

Acceptance:
- frontal emergence readable;
- three-quarter hero window is the strongest frame;
- close face remains inside useful framing;
- full body/tail retained long enough to read propulsion;
- departure returns to haze.

## V8-R1 — Hero Light Architecture
Re-time and reshape cinematic light:
- earlier key peak;
- head/shoulder local shaping;
- dorsal-to-cheek gradient;
- controlled far-side falloff;
- cornea/mouth/gill response tied to same light window.

Acceptance:
- no spotlight look;
- no global overbrightening;
- face reads on phone.

## V8-R2 — Water Occupancy
Make shark feel physically embedded:
- silhouette-local haze;
- wake/contact darkening;
- controlled backscatter;
- body-adjacent density variation;
- no visible shell halo.

Acceptance:
- body no longer reads pasted over background;
- water remains subtle enough for phone GPU.

## V8-R3 — Surface Readability
Refine only phone-visible cues:
- eye wet globe;
- recessed gills;
- mouth cavity;
- roughness breakup;
- pectoral-root shading.

Acceptance:
- every change remains visible at actual phone framing.

## V8-R4 — Cinematic Integration
Bring camera, light, water and surface into one master pass.

Acceptance:
- strongest frame language matches the generated references without depending on impossible offline-render features.

## V8-R5 — Performance Recovery
Only after visual lock:
- profile full vs safe path;
- reduce shader cost where invisible;
- recover phone frame pacing while protecting the hero pass.
