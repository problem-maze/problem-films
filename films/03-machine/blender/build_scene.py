#!/usr/bin/env python3
"""Build the approved 12-second Film 03 Blender scene.

The script deliberately creates physical 3D source: an articulated armature,
collision proxies, surface ribbons with Cloth, pinned contacts, a physical
release, perspective camera, and restrained Problem lighting. It does not
claim a finished render; a Blender runner must execute, bake, render and QC it.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / "shot_spec.json").read_text())
FPS = SPEC["fps"]
FRAME_END = SPEC["frame_end"]
RELEASE_FRAME = SPEC["release_frame"]


def fr(seconds: float) -> int:
    return max(1, min(FRAME_END, int(round(seconds * FPS))))


def hex_rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials,
                       bpy.data.armatures, bpy.data.cameras, bpy.data.lights):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def set_input(node, names, value):
    for name in names:
        socket = node.inputs.get(name)
        if socket is not None:
            socket.default_value = value
            return


def make_principled(name, color, roughness=0.48, metallic=0.0,
                    emission=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    set_input(bsdf, ["Base Color"], (*color, 1.0))
    set_input(bsdf, ["Roughness"], roughness)
    set_input(bsdf, ["Metallic"], metallic)
    if emission is not None:
        set_input(bsdf, ["Emission Color", "Emission"], (*emission, 1.0))
        set_input(bsdf, ["Emission Strength"], emission_strength)
    return mat


def make_reveal_material(name, color, emission_strength=2.2):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    transparent = nt.nodes.new("ShaderNodeBsdfTransparent")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    set_input(bsdf, ["Base Color"], (*color, 1.0))
    set_input(bsdf, ["Roughness"], 0.38)
    set_input(bsdf, ["Emission Color", "Emission"], (*color, 1.0))
    set_input(bsdf, ["Emission Strength"], emission_strength)
    tex = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    less = nt.nodes.new("ShaderNodeMath")
    less.operation = "LESS_THAN"
    reveal = nt.nodes.new("ShaderNodeValue")
    reveal.name = "Reveal"
    reveal.label = "Reveal"
    reveal.outputs[0].default_value = 1.0
    nt.links.new(tex.outputs["UV"], sep.inputs[0])
    nt.links.new(sep.outputs["Y"], less.inputs[0])
    nt.links.new(reveal.outputs[0], less.inputs[1])
    nt.links.new(less.outputs[0], mix.inputs[0])
    nt.links.new(transparent.outputs[0], mix.inputs[1])
    nt.links.new(bsdf.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    if hasattr(mat, "surface_render_method"):
        try:
            mat.surface_render_method = "DITHERED"
        except Exception:
            pass
    elif hasattr(mat, "blend_method"):
        mat.blend_method = "BLEND"
    return mat


def animate_reveal(mat, start, end):
    value = mat.node_tree.nodes.get("Reveal")
    value.outputs[0].default_value = 0.0
    value.outputs[0].keyframe_insert("default_value", frame=start)
    value.outputs[0].default_value = 1.0
    value.outputs[0].keyframe_insert("default_value", frame=end)


def add_cube(name, location, dimensions, material=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    if material:
        obj.data.materials.append(material)
    return obj


def add_cylinder(name, location, radius, depth, material=None, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=depth,
                                       location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj


def add_uv_sphere(name, location, radius, material=None):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj


def add_collision(obj, thickness=0.012):
    mod = obj.modifiers.new("Collision", "COLLISION")
    if hasattr(mod.settings, "thickness_outer"):
        mod.settings.thickness_outer = thickness
    obj["problem_collider"] = True
    return mod


def build_world(materials):
    floor = add_cube("WorldFloor", (0, 1.0, -0.07), (10.0, 12.0, 0.12), materials["floor"])
    add_collision(floor, 0.02)
    return floor


def create_armature(materials):
    arm_data = bpy.data.armatures.new("ProblemCharacterRig")
    arm = bpy.data.objects.new("ProblemCharacter", arm_data)
    bpy.context.collection.objects.link(arm)
    arm.show_in_front = True
    bpy.context.view_layer.objects.active = arm
    arm.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    bones = {
        "root": ((0, 0, 0.04), (0, 0, 0.45), None),
        "pelvis": ((0, 0, 0.88), (0, 0, 1.12), "root"),
        "spine": ((0, 0, 1.12), (0, 0, 1.54), "pelvis"),
        "chest": ((0, 0, 1.54), (0, 0, 1.88), "spine"),
        "neck": ((0, 0, 1.88), (0, 0, 2.06), "chest"),
        "head": ((0, 0, 2.06), (0, 0, 2.42), "neck"),
        "clavicle.L": ((0, 0, 1.82), (0.28, 0, 1.84), "chest"),
        "upper_arm.L": ((0.28, 0, 1.84), (0.63, 0.02, 1.55), "clavicle.L"),
        "forearm.L": ((0.63, 0.02, 1.55), (0.93, 0.10, 1.30), "upper_arm.L"),
        "hand.L": ((0.93, 0.10, 1.30), (1.08, 0.16, 1.22), "forearm.L"),
        "clavicle.R": ((0, 0, 1.82), (-0.28, 0, 1.84), "chest"),
        "upper_arm.R": ((-0.28, 0, 1.84), (-0.63, 0.02, 1.55), "clavicle.R"),
        "forearm.R": ((-0.63, 0.02, 1.55), (-0.93, 0.10, 1.30), "upper_arm.R"),
        "hand.R": ((-0.93, 0.10, 1.30), (-1.08, 0.16, 1.22), "forearm.R"),
        "thigh.L": ((0.19, 0, 1.00), (0.20, 0.02, 0.57), "pelvis"),
        "shin.L": ((0.20, 0.02, 0.57), (0.20, 0.02, 0.14), "thigh.L"),
        "foot.L": ((0.20, 0.02, 0.14), (0.20, 0.34, 0.09), "shin.L"),
        "thigh.R": ((-0.19, 0, 1.00), (-0.20, 0.02, 0.57), "pelvis"),
        "shin.R": ((-0.20, 0.02, 0.57), (-0.20, 0.02, 0.14), "thigh.R"),
        "foot.R": ((-0.20, 0.02, 0.14), (-0.20, 0.34, 0.09), "shin.R"),
    }
    edit = {}
    for name, (head, tail, parent) in bones.items():
        b = arm_data.edit_bones.new(name)
        b.head = head
        b.tail = tail
        edit[name] = b
        if parent:
            b.parent = edit[parent]
            b.use_connect = False
    bpy.ops.object.mode_set(mode="POSE")
    for p in arm.pose.bones:
        p.rotation_mode = "XYZ"
    bpy.ops.object.mode_set(mode="OBJECT")

    def make_target(name, point):
        e = bpy.data.objects.new(name, None)
        bpy.context.collection.objects.link(e)
        e.empty_display_type = "SPHERE"
        e.empty_display_size = 0.06
        e.location = point
        return e

    targets = {
        "foot.L": make_target("IK_Foot.L", bones["shin.L"][1]),
        "foot.R": make_target("IK_Foot.R", bones["shin.R"][1]),
        "hand.L": make_target("IK_Hand.L", bones["forearm.L"][1]),
        "hand.R": make_target("IK_Hand.R", bones["forearm.R"][1]),
    }
    for side in ("L", "R"):
        leg = arm.pose.bones[f"shin.{side}"]
        c = leg.constraints.new("IK")
        c.target = targets[f"foot.{side}"]
        c.chain_count = 2
        arm_bone = arm.pose.bones[f"forearm.{side}"]
        c = arm_bone.constraints.new("IK")
        c.target = targets[f"hand.{side}"]
        c.chain_count = 2

    body_specs = {
        "pelvis": 0.23, "spine": 0.20, "chest": 0.26, "neck": 0.11,
        "clavicle.L": 0.09, "clavicle.R": 0.09,
        "upper_arm.L": 0.105, "upper_arm.R": 0.105,
        "forearm.L": 0.09, "forearm.R": 0.09,
        "hand.L": 0.105, "hand.R": 0.105,
        "thigh.L": 0.135, "thigh.R": 0.135,
        "shin.L": 0.115, "shin.R": 0.115,
        "foot.L": 0.12, "foot.R": 0.12,
    }
    colliders = []
    for bone_name, radius in body_specs.items():
        length = arm.data.bones[bone_name].length
        obj = add_cylinder(f"Body_{bone_name}", (0, 0, 0), radius, max(0.12, length * 0.92), materials["character"], (math.pi / 2, 0, 0))
        obj.parent = arm
        obj.parent_type = "BONE"
        obj.parent_bone = bone_name
        obj.matrix_parent_inverse = Matrix.Identity(4)
        obj.location = (0, length * 0.46, 0)
        add_collision(obj, 0.015)
        colliders.append(obj)
    head = add_uv_sphere("Body_head", (0, 0, 0), 0.205, materials["character"])
    head.scale = (0.92, 0.86, 1.08)
    head.parent = arm
    head.parent_type = "BONE"
    head.parent_bone = "head"
    head.matrix_parent_inverse = Matrix.Identity(4)
    head.location = (0, arm.data.bones["head"].length * 0.48, 0)
    add_collision(head, 0.018)
    colliders.append(head)
    arm["canonical_problem_rig"] = True
    return arm, targets, colliders


def bone_anchor(name, arm, bone_name):
    bone = arm.pose.bones[bone_name]
    world = arm.matrix_world @ bone.matrix
    e = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(e)
    e.empty_display_type = "PLAIN_AXES"
    e.empty_display_size = 0.08
    e.parent = arm
    e.parent_type = "BONE"
    e.parent_bone = bone_name
    e.matrix_world = world
    return e


def resample_polyline(points, segments_per_span=10):
    out = []
    pts = [Vector(p) for p in points]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        for s in range(segments_per_span):
            t = s / segments_per_span
            out.append(a.lerp(b, t))
    out.append(pts[-1])
    return out


def strip_mesh(name, points, width, material, jitter=0.0):
    rows = resample_polyline(points)
    verts, faces = [], []
    up = Vector((0, 0, 1))
    for i, p in enumerate(rows):
        if i == 0:
            tangent = (rows[1] - p).normalized()
        elif i == len(rows) - 1:
            tangent = (p - rows[i - 1]).normalized()
        else:
            tangent = (rows[i + 1] - rows[i - 1]).normalized()
        side = tangent.cross(up)
        if side.length < 1e-5:
            side = Vector((1, 0, 0))
        side.normalize()
        if jitter:
            p = p + Vector((math.sin(i * 1.73) * jitter, math.cos(i * 1.21) * jitter, math.sin(i * 0.87) * jitter * 0.35))
        verts.extend([p - side * width * 0.5, p + side * width * 0.5])
    for i in range(len(rows) - 1):
        faces.append((i * 2, i * 2 + 1, (i + 1) * 2 + 1, (i + 1) * 2))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    uv = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        for li in poly.loop_indices:
            vi = mesh.loops[li].vertex_index
            row, side_index = divmod(vi, 2)
            uv.data[li].uv = (float(side_index), row / max(1, len(rows) - 1))
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    obj["physical_ribbon"] = True
    obj["ribbon_width"] = float(width)
    obj["release_frame"] = int(RELEASE_FRAME)
    return obj, len(rows)


def add_cloth(obj, pin_indices, release_frame, mass=0.18, self_collision=True):
    pin = obj.vertex_groups.new(name="PIN")
    pin.add(list(pin_indices), 1.0, "REPLACE")
    cloth = obj.modifiers.new("Cloth", "CLOTH")
    s = cloth.settings
    if hasattr(s, "quality"):
        s.quality = 8
    if hasattr(s, "mass"):
        s.mass = mass
    if hasattr(s, "tension_stiffness"):
        s.tension_stiffness = 18.0
    if hasattr(s, "compression_stiffness"):
        s.compression_stiffness = 10.0
    if hasattr(s, "shear_stiffness"):
        s.shear_stiffness = 8.0
    if hasattr(s, "bending_stiffness"):
        s.bending_stiffness = 1.8
    if hasattr(s, "air_damping"):
        s.air_damping = 2.0
    if hasattr(s, "vertex_group_mass"):
        s.vertex_group_mass = pin.name
    if hasattr(s, "pin_stiffness"):
        s.pin_stiffness = 45.0
        s.keyframe_insert("pin_stiffness", frame=max(1, release_frame - 1))
        s.pin_stiffness = 0.0
        s.keyframe_insert("pin_stiffness", frame=release_frame + 2)
    cs = cloth.collision_settings
    if hasattr(cs, "use_collision"):
        cs.use_collision = True
    if hasattr(cs, "distance_min"):
        cs.distance_min = 0.008
    if hasattr(cs, "use_self_collision"):
        cs.use_self_collision = bool(self_collision)
    if hasattr(cs, "self_distance_min"):
        cs.self_distance_min = 0.012
    return cloth


def add_hook(obj, group_name, indices, target, release_frame):
    vg = obj.vertex_groups.new(name=group_name)
    vg.add(list(indices), 1.0, "REPLACE")
    mod = obj.modifiers.new(group_name, "HOOK")
    mod.object = target
    mod.vertex_group = vg.name
    try:
        mod.matrix_inverse = target.matrix_world.inverted() @ obj.matrix_world
    except Exception:
        pass
    mod.strength = 1.0
    mod.keyframe_insert("strength", frame=max(1, release_frame - 1))
    mod.strength = 0.0
    mod.keyframe_insert("strength", frame=release_frame + 2)
    return mod


def make_path_ribbon(name, points, width, material, reveal_start, reveal_end, release_offset=0):
    obj, rows = strip_mesh(name, points, width, material, jitter=0.012)
    add_cloth(obj, range(rows * 2), RELEASE_FRAME + release_offset, mass=0.11, self_collision=True)
    animate_reveal(material, reveal_start, reveal_end)
    return obj


def helix_points(start, center, axis="Z", radius=0.17, turns=0.75, samples=12):
    start = Vector(start)
    center = Vector(center)
    pre = [start, start.lerp(center + Vector((0, -0.45, 0.35)), 0.62)]
    pts = list(pre)
    for i in range(samples):
        a = (i / max(1, samples - 1)) * turns * math.tau
        if axis == "Z":
            p = center + Vector((math.cos(a) * radius, math.sin(a) * radius, (i / samples - 0.5) * 0.10))
        else:
            p = center + Vector(((i / samples - 0.5) * 0.12, math.cos(a) * radius, math.sin(a) * radius))
        pts.append(p)
    return pts


def make_body_ribbon(name, reel_anchor, body_anchor, points, material,
                     reveal_start, reveal_end, release_offset=0, width=0.075, wrap_rows=12):
    obj, rows = strip_mesh(name, points, width, material, jitter=0.004)
    start_rows = 2
    end_rows = min(wrap_rows, rows - 2)
    start_indices = range(0, start_rows * 2)
    end_indices = range((rows - end_rows) * 2, rows * 2)
    pin_indices = list(start_indices) + list(end_indices)
    add_hook(obj, "HOOK_REEL", start_indices, reel_anchor, RELEASE_FRAME + release_offset)
    add_hook(obj, "HOOK_BODY", end_indices, body_anchor, RELEASE_FRAME + release_offset)
    add_cloth(obj, pin_indices, RELEASE_FRAME + release_offset, mass=0.14, self_collision=True)
    animate_reveal(material, reveal_start, reveal_end)
    return obj


def create_machine(materials):
    housing = add_cube("MachineHousing", (0, -2.65, 2.75), (3.6, 0.75, 1.15), materials["machine"], bevel=0.08)
    slot = add_cube("MachinePrintSlot", (0, -2.20, 2.45), (1.15, 0.08, 0.18), materials["cyan"])
    reels = []
    reel_positions = [(-1.15, -2.20, 2.80), (0, -2.20, 3.05), (1.15, -2.20, 2.80)]
    for i, pos in enumerate(reel_positions):
        reel = add_cylinder(f"Reel_{i}", pos, 0.31, 0.25, materials["machine_edge"], (math.pi / 2, 0, 0))
        reels.append(reel)
    return housing, slot, reels, reel_positions


def create_eye(materials):
    curve = bpy.data.curves.new("ProblemEyeCurve", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.018
    curve.bevel_resolution = 3
    spline = curve.splines.new("POLY")
    count = 40
    spline.points.add(count - 1)
    for i in range(count):
        t = i / (count - 1) * math.tau
        x = 0.68 * math.cos(t)
        z = 0.24 * math.sin(t) * (0.72 + 0.28 * abs(math.cos(t)))
        spline.points[i].co = (x, 0, z, 1)
    spline.use_cyclic_u = True
    obj = bpy.data.objects.new("ProblemEye", curve)
    bpy.context.collection.objects.link(obj)
    obj.location = (0, -2.18, 3.55)
    curve.materials.append(materials["moon_emit"])
    pupil = add_uv_sphere("ProblemEyePupil", (0, -2.16, 3.55), 0.105, materials["moon_emit"])
    pupil.scale.y = 0.35
    return obj


def key_loc(obj, frame, location):
    obj.location = location
    obj.keyframe_insert("location", frame=frame)


def key_scale(obj, frame, scale):
    obj.scale = scale
    obj.keyframe_insert("scale", frame=frame)


def animate_character(arm, targets, reels):
    left = targets["foot.L"]
    right = targets["foot.R"]
    hand_l = targets["hand.L"]
    hand_r = targets["hand.R"]
    left0 = left.location.copy(); right0 = right.location.copy()
    hl0 = hand_l.location.copy(); hr0 = hand_r.location.copy()

    key_loc(right, fr(0.0), right0)
    key_loc(right, fr(0.7), right0)
    key_loc(right, fr(1.45), right0 + Vector((0, 0.32, 0.28)))
    key_loc(right, fr(2.15), right0 + Vector((0, 0.32, 0.22)))
    key_loc(right, fr(3.0), right0 + Vector((0, 0.24, 0.0)))

    head = arm.pose.bones["head"]
    head.rotation_mode = "XYZ"
    for frame, z in [(fr(2.0), 0.0), (fr(2.45), 0.42), (fr(2.75), 0.0),
                     (fr(3.05), -0.50), (fr(3.45), 0.0)]:
        head.rotation_euler.z = z
        head.keyframe_insert("rotation_euler", frame=frame)

    key_loc(hand_l, fr(4.0), hl0); key_loc(hand_r, fr(4.0), hr0)
    key_loc(hand_l, fr(6.0), hl0 + Vector((0.22, -0.38, 0.12)))
    key_loc(hand_r, fr(6.0), hr0 + Vector((-0.22, -0.38, 0.12)))

    pelvis = arm.pose.bones["pelvis"]
    chest = arm.pose.bones["chest"]
    pelvis.rotation_mode = chest.rotation_mode = "XYZ"
    arm.location = (0, 0, 0); arm.keyframe_insert("location", frame=fr(4.0))
    arm.location = (0, -0.07, 0); arm.keyframe_insert("location", frame=fr(6.0))
    pelvis.rotation_euler.x = 0.0; pelvis.keyframe_insert("rotation_euler", frame=fr(4.0))
    pelvis.rotation_euler.x = math.radians(4.5); pelvis.keyframe_insert("rotation_euler", frame=fr(6.0))
    chest.rotation_euler.x = 0.0; chest.keyframe_insert("rotation_euler", frame=fr(4.0))
    chest.rotation_euler.x = math.radians(-9.0); chest.keyframe_insert("rotation_euler", frame=fr(6.0))

    for frame, dz, chest_delta in [(184, 0.000, 0.0), (194, 0.008, 0.012),
                                   (204, 0.002, -0.008), (214, 0.010, 0.010),
                                   (225, 0.004, 0.0)]:
        arm.location.z = dz
        arm.keyframe_insert("location", frame=frame)
        chest.rotation_euler.x = math.radians(-9.0) + chest_delta
        chest.keyframe_insert("rotation_euler", frame=frame)

    key_loc(left, 225, left0)
    key_loc(left, 330, left0)
    arm.location.x = 0.0; arm.keyframe_insert("location", frame=225)
    arm.location.x = 0.20; arm.keyframe_insert("location", frame=242)
    key_loc(right, 232, right0 + Vector((0, 0.24, 0.0)))
    key_loc(right, 250, right0 + Vector((0.48, 0.30, 0.20)))
    key_loc(right, 270, right0 + Vector((1.03, 0.30, 0.0)))
    arm.location.x = 0.56; arm.keyframe_insert("location", frame=282)

    key_loc(left, 330, left0)
    key_loc(left, 342, left0 + Vector((0.68, 0.34, 0.18)))
    key_loc(left, 352, left0 + Vector((1.48, 0.36, 0.0)))
    arm.location.x = 0.94; arm.keyframe_insert("location", frame=358)

    for i, reel in enumerate(reels):
        reel.rotation_mode = "XYZ"
        reel.rotation_euler.y = 0.0
        reel.keyframe_insert("rotation_euler", frame=fr(4.0))
        reel.rotation_euler.y = math.tau * (5.0 + i * 0.7)
        reel.keyframe_insert("rotation_euler", frame=fr(6.0))
        reel.rotation_euler.y += 0.18 * (i + 1)
        reel.keyframe_insert("rotation_euler", frame=fr(7.5))


def create_tiles_and_blank(materials):
    tile1 = add_cube("ChoiceTile_1", (0.83, 0.34, 0.025), (0.68, 0.82, 0.035), materials["moon_emit"], bevel=0.04)
    key_scale(tile1, 272, (0.02, 0.02, 0.2))
    key_scale(tile1, 282, (1.0, 1.0, 1.0))
    tile2 = add_cube("ChoiceTile_2", (1.30, 0.68, 0.025), (0.68, 0.82, 0.035), materials["moon_emit"], bevel=0.04)
    key_scale(tile2, 330, (0.02, 0.02, 0.2))
    key_scale(tile2, 352, (1.0, 1.0, 1.0))

    blank = add_cube("BlankFutureOutput", (0, -1.92, 2.43), (0.90, 0.66, 0.025), materials["blank"], bevel=0.02)
    blank.rotation_euler.x = math.radians(16)
    key_scale(blank, 336, (1.0, 0.02, 1.0))
    key_scale(blank, 359, (1.0, 1.0, 1.0))
    blank["meaning"] = "machine attempted future output; surface intentionally contains no predicted path"
    return tile1, tile2, blank


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_camera_and_lights(materials):
    cam_data = bpy.data.cameras.new("ProblemCamera")
    cam = bpy.data.objects.new("ProblemCamera", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = (5.9, -8.2, 3.35)
    cam_data.lens = 48
    look_at(cam, (0.25, 0.55, 1.35))
    bpy.context.scene.camera = cam

    def area(name, loc, energy, color, size, target):
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.color = color
        data.shape = "DISK"
        data.size = size
        obj = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(obj)
        obj.location = loc
        look_at(obj, target)
        return obj

    moon = hex_rgb(SPEC["colors"]["lunar_white"])
    cyan = hex_rgb(SPEC["colors"]["functional_cyan"])
    area("MoonKey", (-3.5, -1.0, 5.2), 950, moon, 3.0, (0, 0.4, 1.2))
    area("CyanRim", (4.0, -1.4, 3.6), 260, cyan, 2.0, (0.2, 0.2, 1.4))
    area("MachineTop", (0, -3.2, 5.3), 420, moon, 2.1, (0, -2.3, 2.8))


def configure_render(output_blend):
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = FRAME_END
    scene.render.fps = FPS
    scene.render.resolution_x = SPEC["review_resolution"][0]
    scene.render.resolution_y = SPEC["review_resolution"][1]
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.use_file_extension = True
    if hasattr(scene.render, "use_motion_blur"):
        scene.render.use_motion_blur = True
    requested = os.environ.get("PROBLEM_RENDER_ENGINE", "BLENDER_EEVEE_NEXT")
    engines = {item.identifier for item in scene.bl_rna.properties["render_engine"].enum_items}
    scene.render.engine = requested if requested in engines else ("CYCLES" if "CYCLES" in engines else next(iter(engines)))
    if scene.render.engine == "CYCLES":
        scene.cycles.samples = int(os.environ.get("PROBLEM_CYCLES_SAMPLES", "128"))
        scene.cycles.use_denoising = True
    try:
        scene.view_settings.view_transform = "AgX"
    except Exception:
        pass
    scene.world.color = (*hex_rgb(SPEC["colors"]["background"]),)
    scene["film"] = "THE MACHINE THAT DREW EVERY FUTURE"
    scene["duration_seconds"] = 12.0
    scene["native_review_resolution"] = "1920x1080"
    scene["output_blend"] = str(output_blend)


def add_timeline_markers(scene):
    markers = {
        "PATH_SPLIT": 45,
        "ANKLE_WRAP": 92,
        "REELS_ACCELERATE": 130,
        "TENSION_HOLD": 180,
        "SILENCE_PEAK": 205,
        "LATERAL_COMMIT": 246,
        "FOOT_CONTACT": 270,
        "TILE_AFTER_WEIGHT": 278,
        "RIBBON_RELEASE": 300,
        "SECOND_STEP": 336,
        "BLANK_PRINT": 352,
    }
    for name, frame in markers.items():
        scene.timeline_markers.new(name, frame=frame)


def build(output_blend: Path):
    clear_scene()
    background = hex_rgb(SPEC["colors"]["background"])
    moon = hex_rgb(SPEC["colors"]["lunar_white"])
    cyan = hex_rgb(SPEC["colors"]["functional_cyan"])
    materials = {
        "floor": make_principled("ProblemFloor", background, roughness=0.62),
        "character": make_principled("ProblemCharacterMat", (0.28, 0.33, 0.39), roughness=0.42, metallic=0.15),
        "machine": make_principled("MachineDark", (0.025, 0.035, 0.045), roughness=0.36, metallic=0.62),
        "machine_edge": make_principled("MachineEdge", (0.09, 0.13, 0.17), roughness=0.28, metallic=0.75),
        "cyan": make_principled("FunctionalCyan", (0.02, 0.08, 0.10), roughness=0.30, emission=cyan, emission_strength=1.8),
        "moon_emit": make_principled("LunarWhite", (0.32, 0.37, 0.43), roughness=0.30, emission=moon, emission_strength=2.3),
        "blank": make_principled("BlankPhysicalOutput", (0.012, 0.017, 0.022), roughness=0.22, metallic=0.28),
    }
    configure_render(output_blend)
    build_world(materials)
    _, _, reels, reel_positions = create_machine(materials)
    create_eye(materials)
    arm, targets, _ = create_armature(materials)
    animate_character(arm, targets, reels)

    path_defs = [
        ("FuturePath_Main", [(0, 0.45, 0.16), (0, 2.0, 0.16), (0, 5.0, 0.16)], 1, 1, 0),
        ("FuturePath_Left", [(0, 0.70, 0.16), (-0.4, 1.55, 0.18), (-1.45, 4.8, 0.17)], 42, 60, 0),
        ("FuturePath_Center", [(0, 0.70, 0.17), (0.1, 2.1, 0.17), (0.45, 5.0, 0.16)], 42, 60, 2),
        ("FuturePath_Right", [(0, 0.70, 0.18), (0.55, 1.55, 0.19), (1.65, 4.7, 0.16)], 42, 60, 4),
        ("FuturePath_HeadTurnA", [(0, 0.9, 0.20), (-0.9, 2.0, 0.21), (-2.25, 4.0, 0.17)], 70, 84, 6),
        ("FuturePath_HeadTurnB", [(0, 0.9, 0.20), (1.0, 2.2, 0.22), (2.45, 3.9, 0.17)], 90, 104, 8),
    ]
    path_ribbons = []
    for name, points, rs, re, release_offset in path_defs:
        mat = make_reveal_material(name + "Mat", moon, emission_strength=2.6)
        path_ribbons.append(make_path_ribbon(name, points, 0.105, mat, rs, re, release_offset))

    wrist_l = bone_anchor("Anchor_Wrist.L", arm, "hand.L")
    wrist_r = bone_anchor("Anchor_Wrist.R", arm, "hand.R")
    ankle_r = bone_anchor("Anchor_Ankle.R", arm, "foot.R")
    reel_anchors = []
    for i, pos in enumerate(reel_positions):
        e = bpy.data.objects.new(f"ReelAnchor_{i}", None)
        bpy.context.collection.objects.link(e)
        e.location = pos
        key_loc(e, 120, Vector(pos))
        key_loc(e, 180, Vector(pos) + Vector((0, -0.24, 0.14 + i * 0.02)))
        key_loc(e, 225, Vector(pos) + Vector((0, -0.25, 0.15 + i * 0.02)))
        reel_anchors.append(e)

    body_data = [
        ("Ribbon_Ankle", reel_anchors[0], ankle_r, helix_points(reel_positions[0], (-0.20, 0.26, 0.14), "Z", 0.18, 0.85, 14), 68, 112, 0, 0.075),
        ("Ribbon_Wrist.L", reel_anchors[1], wrist_l, helix_points(reel_positions[1], (1.02, 0.14, 1.25), "X", 0.145, 0.82, 14), 122, 166, 2, 0.070),
        ("Ribbon_Wrist.R", reel_anchors[2], wrist_r, helix_points(reel_positions[2], (-1.02, 0.14, 1.25), "X", 0.145, 0.82, 14), 128, 172, 4, 0.070),
    ]
    for name, reel_anchor, body_anchor, pts, rs, re, ro, width in body_data:
        mat = make_reveal_material(name + "Mat", (0.12, 0.17, 0.21), emission_strength=0.38)
        make_body_ribbon(name, reel_anchor, body_anchor, pts, mat, rs, re, ro, width=width)

    create_tiles_and_blank(materials)
    setup_camera_and_lights(materials)
    add_timeline_markers(bpy.context.scene)
    bpy.context.scene.frame_set(1)
    output_blend.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output_blend))
    print(f"Saved Film 03 source scene: {output_blend}")


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="build/machine-12s.blend")
    return p.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    build(Path(args.output).resolve())
