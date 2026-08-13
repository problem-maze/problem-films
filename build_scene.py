#!/usr/bin/env python3
"""Compatibility shim for Blender CI.

Blender's --python execution may not add the executed script directory to
sys.path. The Film 03 runner imports ``build_scene`` by module name, so this
root-level shim loads the canonical source file and forwards its API while
preserving runtime monkey-patches applied by run_build.py.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_IMPL_PATH = Path(__file__).resolve().parent / "films/03-machine/blender/build_scene.py"
_SPEC = importlib.util.spec_from_file_location("_problem_film03_build_scene", _IMPL_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(f"Unable to load Film 03 scene source: {_IMPL_PATH}")
_IMPL = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _IMPL
_SPEC.loader.exec_module(_IMPL)

for _name, _value in vars(_IMPL).items():
    if not _name.startswith("__") and _name != "build":
        globals()[_name] = _value


def build(*args, **kwargs):
    # run_build.py patches these compatibility hooks on this shim.
    if "add_collision" in globals():
        _IMPL.add_collision = globals()["add_collision"]
    if "configure_render" in globals():
        _IMPL.configure_render = globals()["configure_render"]
    return _IMPL.build(*args, **kwargs)
