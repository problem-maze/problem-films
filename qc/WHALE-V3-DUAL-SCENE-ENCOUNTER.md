# Whale V3 — Dual Scene / Encounter Switch

Branch: `ocean/whale-v3-dual-scene-switch`

Purpose: preserve the original 96-second Whale V3 journey and add a second, stronger 24-second cinematic encounter that can be entered/exited with one top-bar icon.

## New mode
**THE ENCOUNTER — 24s**

Shot design:
- 0–6s: frontal approach from the head axis
- 6–12s: three-quarter reveal
- 12–18s: close mass pass beneath/alongside camera
- 18–24s: departure into haze

The encounter uses its own Catmull-Rom camera keys and a small model-yaw/scale envelope. The original journey camera is preserved.

## Toggle
New `#sceneMode` control in the existing top actions:
- normal state label: `لقاء`
- encounter state label: `رحلة`
- updates ARIA state/label
- resets scene time/orbit/zoom safely on switch
- keeps the control faintly accessible in Cinema mode

## Encounter-specific rendering
Without reopening whale geometry:
- localized head/shoulder key light
- restrained wet-response cue on dark facial materials
- slightly denser body-local fog
- stronger localized surface aperture
- darker canyon-side framing
- distant second whale hidden in Encounter mode

## Preserved
- original procedural humpback geometry
- original 96-second journey
- one owned animation clock
- no Canvas2D path
- reduced-motion behavior
- existing quality governor and post-processing ownership
- G0A instrumentation remains present

## Local candidate
File:
`Problem-OCEAN-WHALE-V3-DUAL-SCENE-ENCOUNTER.html`

Local deterministic build result:
- bytes: **1,155,813**
- SHA-256: **18b01767a5a9c3e97f9725dbe0ecdf7bbf303f0a76b30378a5f3cdad7904b775**
- JavaScript parse: PASS
- scene button count: 1
- `encounterShot`: present
- `uEncounter` integration: present
- Canvas2D calls: 0
- textual `requestAnimationFrame` occurrences remain 2

A container Chromium WebGL smoke was attempted, but that environment could not initialize the requested GL implementation, so no browser/GPU success claim is made. Real phone remains the visual gate.

## Build
Run:

```bash
python3 tools/build_whale_v3_dual_scene.py \
  Problem-OCEAN-WHALE-V3-G0A-CONTINUATION-BASELINE.html \
  Problem-OCEAN-WHALE-V3-DUAL-SCENE-ENCOUNTER.html
```
