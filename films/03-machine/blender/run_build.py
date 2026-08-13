#!/usr/bin/env python3
from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path
import bpy
import build_scene as scene_source

def add_collision_compat(obj, thickness=0.012):
    mod = obj.modifiers.new("Collision", "COLLISION")
    settings = getattr(obj, "collision", None)
    if settings is not None and hasattr(settings, "thickness_outer"):
        settings.thickness_outer = thickness
    obj["problem_collider"] = True
    return mod

def configure_render_compat(output_blend):
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = scene_source.FRAME_END
    scene.render.fps = scene_source.FPS
    scene.render.resolution_x = scene_source.SPEC["review_resolution"][0]
    scene.render.resolution_y = scene_source.SPEC["review_resolution"][1]
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.use_file_extension = True
    if hasattr(scene.render, "use_motion_blur"):
        scene.render.use_motion_blur = True
    requested = os.environ.get("PROBLEM_RENDER_ENGINE", "BLENDER_EEVEE_NEXT")
    try:
        engines = {item.identifier for item in scene.render.bl_rna.properties["engine"].enum_items}
    except Exception:
        engines = {"CYCLES", "BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"}
    if requested in engines:
        scene.render.engine = requested
    elif "CYCLES" in engines:
        scene.render.engine = "CYCLES"
    elif "BLENDER_EEVEE_NEXT" in engines:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    else:
        scene.render.engine = "BLENDER_EEVEE"
    if scene.render.engine == "CYCLES":
        scene.cycles.samples = int(os.environ.get("PROBLEM_CYCLES_SAMPLES", "128"))
        scene.cycles.use_denoising = True
    try:
        scene.view_settings.view_transform = "AgX"
    except Exception:
        pass
    scene.world.color = scene_source.hex_rgb(scene_source.SPEC["colors"]["background"])
    scene["film"] = "THE MACHINE THAT DREW EVERY FUTURE"
    scene["duration_seconds"] = 12.0
    scene["native_review_resolution"] = "1920x1080"
    scene["output_blend"] = str(output_blend)

def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="build/machine-12s.blend")
    return p.parse_args(argv)

def main():
    args = parse_args()
    scene_source.add_collision = add_collision_compat
    scene_source.configure_render = configure_render_compat
    scene_source.build(Path(args.output).resolve())

if __name__ == "__main__":
    main()
