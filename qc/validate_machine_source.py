#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "films/03-machine/blender/shot_spec.json"
BUILD = ROOT / "films/03-machine/blender/build_scene.py"
SCENE_QC = ROOT / "films/03-machine/blender/qc_scene.py"

errors = []
spec = json.loads(SPEC.read_text())
if spec["duration_seconds"] != 12.0: errors.append("duration must be 12.0")
if spec["fps"] != 30: errors.append("fps must be 30")
if spec["frame_end"] != 360: errors.append("frame_end must be 360")
if spec["review_resolution"] != [1920, 1080]: errors.append("review resolution must be native 1920x1080")
if spec["release_frame"] != 300: errors.append("release frame must be 300")
for path in (BUILD, SCENE_QC):
    if not path.exists(): errors.append(f"missing source: {path.relative_to(ROOT)}")
if errors:
    raise SystemExit("Film 03 source QC failed:\n- " + "\n- ".join(errors))
print("Film 03 source QC passed")
