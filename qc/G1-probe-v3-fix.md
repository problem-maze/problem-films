# G1 Phone Attempt 02 — Probe v2 defect and v3 correction

Decision: **REWORK PROBE ONLY**

Attempt 02 returned zero rendered measurement frames and shot remained at 0. This is not a scene/GPU failure.

## Root cause
Probe v2 inserted this condition into the page render loop:

`if(window.__G1_LOCK_SHOT__&&phase==='measuring'&&state.shot<12)state.auto=true;`

But `phase` is declared inside the private `__G1` closure. The main render loop is outside that closure, so `phase` is undefined there. When the probe lock becomes active, the animation tick throws before render/shot advancement. This exactly matches the phone evidence: renderPath initializes as `g1-full`, but shot remains 0 and renderedFrames remains 0.

## v3 fix
The render loop now queries the already-exposed probe accessor instead of referencing closure-private state:

`window.G1Probe.getPhase()==='measuring'`

No visual scene code was changed.

Probe v3:
- `Problem-OCEAN-SHARK-V7-G1-REALITY-PROOF-PROBE-v3.html`
- SHA-256: `4d66953b1d4a99089d0d8e8cb457d6b790a7aa40c7609aa900feee9c59a58326`
- Bytes: `1118313`

Static validation:
- JavaScript syntax PASS.
- no stale private `phase` reference in tick.
- requestAnimationFrame occurrences remain 2.
- Canvas2D calls remain 0.
- G1 scene/build itself remains unchanged.

G1 remains PHONE EVIDENCE PENDING. Repeat only the probe.
