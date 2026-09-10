# G1 Phone Attempt 01 — Invalid Probe Run

Decision: **REWORK PROBE, NOT SCENE**

The phone itself did not show a performance failure.

Measured:
- active path: `g1-full`
- balanced tier
- scale 1.30
- 499×951 internal canvas
- 448 frames / 15.01 s
- mean interval 33.414 ms
- p95/p99 33.5 ms
- >50 ms frames: 0
- context loss: 0

The run timed out because the shot stopped at 4.511 s instead of reaching 12 s. With 448 rendered frames at ~33.4 ms intervals, the animation loop was healthy enough to advance ~15 seconds of wall time. Therefore this is not evidence that the phone could not render the shot.

Root cause in probe design:
the G1 page intentionally supports interactive/manual control. A touch/pointer/manual-control path can set `state.auto=false` while the measurement phase continues. The first probe did not lock those controls during the measurement window. Once auto was cancelled, the benchmark kept collecting frames until its timeout, leaving `shot` frozen around 4.511 s.

Fix:
- probe v2 locks scene interaction while measurement is active;
- manual, journey, pause, timeline, chapter, pointer, wheel and keyboard paths cannot cancel the measured shot;
- the measurement tick also reasserts auto-play until 12 s;
- no new requestAnimationFrame is added;
- visual scene/render code is not changed;
- timeout tolerance raised only to distinguish a true completion failure from the old interaction cancellation.

Probe v2 SHA-256:
`db1fa23cc925515766d48991e7f121f6e37c8f0c0d51079ff095930c69362967`

G1 remains open. Repeat only the probe run; do not rebuild the G1 scene yet.
