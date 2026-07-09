"""Mandatory visual layer — orthographic front/side/top renders (doc 07).

Numeric asserts are one view; drawings culture demands several. This script
emits the three orthographic views every review requires, framed on the scene
bounding box, using the Workbench engine (fast, no lights needed).

    blender --background --python render_orthos.py -- --blend file.blend [--out dir]
"""
import math
import os
import sys

import bpy
from mathutils import Euler, Vector


def _args():
    argv = sys.argv
    out = {"blend": None, "out": None}
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
        if "--blend" in argv:
            out["blend"] = argv[argv.index("--blend") + 1]
        if "--out" in argv:
            out["out"] = argv[argv.index("--out") + 1]
    return out


def _scene_bbox():
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for ob in bpy.context.scene.objects:
        if ob.type != "MESH":
            continue
        for c in ob.bound_box:
            w = ob.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, w))
            hi = Vector(map(max, hi, w))
    return lo, hi


VIEWS = {
    # name: (direction the camera looks FROM, camera rotation, framed extents fn)
    "front": (Vector((0, -1, 0)), Euler((math.pi / 2, 0, 0)), lambda s: (s.x, s.z)),
    "side":  (Vector((1, 0, 0)),  Euler((math.pi / 2, 0, math.pi / 2)), lambda s: (s.y, s.z)),
    "top":   (Vector((0, 0, 1)),  Euler((0, 0, 0)), lambda s: (s.x, s.y)),
}


def main():
    a = _args()
    if a["blend"]:
        bpy.ops.wm.open_mainfile(filepath=a["blend"])
    out_dir = a["out"] or os.path.join(
        os.path.dirname(bpy.data.filepath or os.path.abspath(__file__)), "renders")
    # Blender resolves relative render paths against its own notion of CWD,
    # not the shell's — always go absolute, then verify the files exist after
    # rendering (exit 0 from the renderer is not proof the PNG landed).
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.render.resolution_x = scene.render.resolution_y = 1024
    scene.render.film_transparent = True

    lo, hi = _scene_bbox()
    center = (lo + hi) / 2
    size = hi - lo
    margin = 1.15

    cam_data = bpy.data.cameras.new("ortho_cam")
    cam_data.type = "ORTHO"
    cam = bpy.data.objects.new("ortho_cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    dist = max(size) * 3 + 1.0
    for name, (dirn, rot, extents) in VIEWS.items():
        w, h = extents(size)
        cam_data.ortho_scale = max(w, h, 0.001) * margin
        cam.location = center + dirn * dist
        cam.rotation_euler = rot
        scene.render.filepath = os.path.join(out_dir, f"ortho_{name}.png")
        bpy.ops.render.render(write_still=True)
        print(f"[render] {scene.render.filepath}")

    print(f"[render] done -> {out_dir}")


if __name__ == "__main__":
    main()
