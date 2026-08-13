# Problem Ribbon Physics

Film 03 requires ribbons to behave as physical surfaces rather than decorative lines.

## Required simulation behavior

- Visible width and surface twist
- Collision-aware wrapping at wrist and ankle contact zones
- Tension propagation from reel toward the body
- Believable sag between constrained points
- Rebound after a change in force
- Gravity-driven release and fall
- Floor collision and body collision
- Irregular secondary motion after release

## Contact rule

A ribbon may visually compress around a wrist or ankle, but it must not pass through the character mesh. Contact zones need explicit collision margins and review close-ups.

## Release rule

When the character exits the predicted paths, tension is removed from the future ribbons. They must lose support, overshoot, fold, collide, and settle under gravity. A clean geometric collapse is rejected.

## Validation targets

- zero visible body penetration in approved close-ups
- zero floor penetration after release
- measurable sag before release
- visible secondary motion after release
- no synchronized ribbon fall unless physically justified
