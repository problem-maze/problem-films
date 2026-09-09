# G0A Probe Builds

The measurement-only probe builds were produced from the locked source artifacts without changing scene anatomy, materials, water, camera, animation intent, or render order.

## V3 probe
- Source: `Problem-OCEAN-WHALE-V3.html`
- Source SHA-256: `129639b286d263edf2c4c9151fcac07d010d08fa36491dcc4495cef6d1c62825`
- Probe: `Problem-OCEAN-WHALE-V3-G0A-PROBE.html`
- Probe SHA-256: `8bde07d334366c796cbb9a93ff18d474b34fca5d8dc798c0792e9f669c333337`

## V6 probe
- Source: `Problem-OCEAN-SHARK-V6-CINEMATIC-REALISM.html`
- Source SHA-256: `520fed835611502889cf372c67dc701bf3cd88d106c3665db1f666c9d039e0e3`
- Probe: `Problem-OCEAN-SHARK-V6-G0A-PROBE.html`
- Probe SHA-256: `48175d6090fcd14c2b498dbc80de34d5373bc5300fe7b67b109afc4754d20ecd`

## Probe behavior
- no additional `requestAnimationFrame`;
- no added geometry reads;
- existing `render()` call is timed with `performance.now()`;
- existing rendered-frame interval is recorded;
- 5 s warm-up + 30 s measurement;
- records viewport, DPR, internal canvas size/scale, quality tier, render path, WebGL info, context loss/restore, visibility changes and resize events;
- exports one JSON result;
- the small control panel does not animate during the run.

## Phone procedure
1. Serve both files from the same localhost server.
2. Use the same browser and portrait orientation.
3. Do not switch apps during a run.
4. Open V3 probe, tap **Start G0A**, wait until it says ready, then tap **JSON**.
5. Repeat with V6 probe under the same conditions.
6. Submit both JSON files for G0A comparison.

Do not begin G0B until both comparable phone JSON files exist.
