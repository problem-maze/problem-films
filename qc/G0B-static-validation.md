# G0B — Static Validation

Status: **CANDIDATE BUILT / PHONE EVIDENCE PENDING**

Source visual baseline:
- `Problem-OCEAN-WHALE-V3.html`
- SHA-256: `129639b286d263edf2c4c9151fcac07d010d08fa36491dcc4495cef6d1c62825`

Generated hybrid candidate:
- `Problem-OCEAN-V7-HYBRID-RUNTIME-FOUNDATION.html`
- SHA-256: `0eb4506050f624393e8e585eeaa77978f5e4c2f43acdebdd391135e739ec1138`
- Bytes: `1092668`

Generated phone probe:
- `Problem-OCEAN-V7-HYBRID-G0B-PROBE.html`
- SHA-256: `5414b1aaff2796cb1bb63ed000b4e871d3179950e41ed272a6e2c94d83fa74d3`
- Bytes: `1098786`

## Implemented runtime transplant
- Removed CSS-width <700 forced-low classification.
- New initial low-device rule is based on explicit constrained memory/CPU only: <=3 GB reported memory or <=4 reported logical cores.
- Balanced devices begin at internal scale 1.20; constrained devices begin at 0.92.
- Full V3 WebGL shaders remain the first-choice render path.
- Added a WebGL-only 3D-safe shader profile used only if full shader program creation fails.
- Removed the legacy illustrated SVG fallback from the candidate: no Canvas2D and no 2D scene substitute.
- Post target is explicitly deleted before framebuffer rebuild.
- Auto-quality uses both existing frame cadence and CPU render submission wall-time, rather than treating CPU submission time as a raw GPU timer.
- One owned animation clock preserved; no additional requestAnimationFrame was added.

## Visual-preservation static evidence
The following V3 blocks are byte-for-byte unchanged in the G0B hybrid candidate:
- Procedural ocean/animal geometry block: SHA-256 `757e339f5cdc7797515ff7edc9c9c1b769fcf593a4f6fcbe3afd5a8b3755fcf0`
- Full V3 shader set: SHA-256 `1b3b98cd4403aa2606bc9888c8ca838844984303590cd6053a54f28a2620654d`
- Ocean camera math / shot path: SHA-256 `1b4d62b1d19bf310610c3b7fbe242ec4477baecfdc8bcceba995ee7a49e4e85c`
- Main render() scene order/content: SHA-256 `82de54b91a3eaefdbe803fbce01e6cbcff8411895374afc2cbc719e074479169`

## Static checks
- JavaScript syntax: PASS for hybrid and phone probe.
- requestAnimationFrame occurrences: V3=2, hybrid=2, probe=2.
- Canvas2D context calls in hybrid: 0.
- Legacy fallback ocean SVG in hybrid: 0.
- Old width-based forced-low predicate in hybrid: 0.
- 3D-safe shader profile present: 1.
- Geometry execution: PASS; no NaN/Infinity in whale, floor, fish, kelp, dust, or bubbles.

## Geometry lengths (float entries)
- whale: 1,431,840
- floor: 1,003,200
- fish: 160,050
- kelp: 142,560
- dust: 1,840
- bubbles: 600

## Gate
Static G0B engineering work is complete enough for a real-phone candidate test, but **G0B is not PASS yet**.

Required next evidence:
- 5 s warm-up + 30 s phone run from the G0B probe;
- actual render path, scale/tier, frame intervals, long frames, and context stability;
- visual confirmation that the V3 scene look is not materially degraded.

Only after that evidence may G1 begin.