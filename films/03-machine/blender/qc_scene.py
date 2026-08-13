#!/usr/bin/env python3
"""Measured scene-level QC for the Film 03 Blender source.

This report verifies source/animation facts that Blender can measure before a
render. It intentionally does not claim rendered collision success; that still
requires baked simulation close-ups and frame inspection.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / "shot_spec.json").read_text())


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--report", default="build/machine-12s-scene-qc.json")
    return p.parse_args(argv)


def max_drift(obj, frames):
    scene = bpy.context.scene
    points = []
    for frame in frames:
        scene.frame_set(frame)
        points.append(obj.matrix_world.translation.copy())
    origin = points[0]
    return max((p - origin).length for p in points)


def scale_at(obj, frame):
    bpy.context.scene.frame_set(frame)
    return tuple(float(v) for v in obj.scale)


def main(report_path):
    scene = bpy.context.scene
    failures = []
    checks = {}
    checks["fps"] = scene.render.fps
    checks["frame_start"] = scene.frame_start
    checks["frame_end"] = scene.frame_end
    checks["resolution"] = [scene.render.resolution_x, scene.render.resolution_y]
    if scene.render.fps != 30: failures.append("fps != 30")
    if scene.frame_start != 1 or scene.frame_end != 360: failures.append("timeline is not 1..360")
    if checks["resolution"] != [1920, 1080]: failures.append("review scene is not native 1920x1080")

    arm = bpy.data.objects.get("ProblemCharacter")
    if arm is None or arm.type != "ARMATURE":
        failures.append("ProblemCharacter armature missing")
        bone_names = []
    else:
        bone_names = sorted(b.name for b in arm.data.bones)
        missing = sorted(set(SPEC["required_bones"]) - set(bone_names))
        checks["missing_required_bones"] = missing
        if missing: failures.append("required rig bones missing")

    ribbons = [o for o in bpy.data.objects if o.get("physical_ribbon")]
    checks["physical_ribbon_count"] = len(ribbons)
    ribbon_results = []
    for obj in ribbons:
        has_cloth = any(m.type == "CLOTH" for m in obj.modifiers)
        width = float(obj.get("ribbon_width", 0.0))
        release_frame = int(obj.get("release_frame", -1))
        ribbon_results.append({"name": obj.name, "cloth": has_cloth, "width": width, "release_frame": release_frame})
        if not has_cloth: failures.append(f"{obj.name}: Cloth modifier missing")
        if width < float(SPEC["ribbon_width_min"]): failures.append(f"{obj.name}: ribbon width below minimum")
        if release_frame < 300 or release_frame > 308: failures.append(f"{obj.name}: release outside approved 10s window")
    checks["ribbons"] = ribbon_results

    colliders = [o.name for o in bpy.data.objects if o.get("problem_collider")]
    checks["collider_count"] = len(colliders)
    if len(colliders) < 10: failures.append("insufficient explicit body/floor colliders")

    left = bpy.data.objects.get("IK_Foot.L")
    right = bpy.data.objects.get("IK_Foot.R")
    if left:
        checks["left_planted_drift_6_to_11s_m"] = max_drift(left, range(180, 331, 5))
        if checks["left_planted_drift_6_to_11s_m"] > SPEC["planted_foot_tolerance"]:
            failures.append("left planted-foot target drifts beyond tolerance")
    else:
        failures.append("IK_Foot.L missing")
    if right:
        checks["right_planted_drift_3_to_7_5s_m"] = max_drift(right, range(90, 226, 5))
        if checks["right_planted_drift_3_to_7_5s_m"] > SPEC["planted_foot_tolerance"]:
            failures.append("right planted-foot target drifts beyond tolerance")
    else:
        failures.append("IK_Foot.R missing")

    tile1 = bpy.data.objects.get("ChoiceTile_1")
    tile2 = bpy.data.objects.get("ChoiceTile_2")
    if tile1:
        checks["tile1_scale_pre_contact"] = scale_at(tile1, 269)
        checks["tile1_scale_after_weight"] = scale_at(tile1, 282)
        if max(checks["tile1_scale_pre_contact"]) > 0.25:
            failures.append("tile 1 is substantially visible before contact")
    else:
        failures.append("ChoiceTile_1 missing")
    if tile2:
        checks["tile2_scale_before_second_step"] = scale_at(tile2, 329)
        checks["tile2_scale_after_second_step"] = scale_at(tile2, 352)
    else:
        failures.append("ChoiceTile_2 missing")

    blank = bpy.data.objects.get("BlankFutureOutput")
    checks["blank_future_output_present"] = bool(blank)
    if not blank: failures.append("BlankFutureOutput missing")

    result = {
        "film": "THE MACHINE THAT DREW EVERY FUTURE",
        "scene_qc_passed": not failures,
        "checks": checks,
        "failures": failures,
        "unverified_until_baked_render": [
            "visible cloth/body penetration",
            "floor penetration after release",
            "quality of tension-wave propagation",
            "natural disorder of ribbon fall",
            "rendered motion continuity",
            "audio synchronization"
        ]
    }
    report = Path(report_path).resolve()
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main(parse_args().report)
