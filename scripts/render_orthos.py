"""Mandatory visual layer — the render set a human review requires (doc 07).

Numeric asserts are one view; drawings culture demands several. Never-list #14
sets the minimum: three orthos + a shot that shows form + a human-scale shot,
every time. This script emits all of them off the Workbench engine (fast, no
lights needed), framed on the scene bounding box.

    blender --background --python render_orthos.py -- --blend file.blend [--out dir]

Outputs: ortho_front / ortho_side / ortho_top / view_iso / view_scale.

Doc 09's checklist D also wants a close-up per joint class. That one cannot be
framed generically — it needs the feature names — so it stays with
`bpy.ops.kit.frame_feature` (kit_inspect). Checklist D is not met by this
script alone.

**These renders exist to be looked at**, so they are set up for a reader, not
for a screenshot: opaque background (a transparent film reads as pure black in
most viewers, and black parts vanish into it), plus cavity + outline + shadow,
without which flat ortho Workbench turns every part into a featureless
silhouette and hides exactly the coplanar/joint defects the review is for.
"""
import math
import os
import sys

import bpy
from mathutils import Euler, Vector

# doc 03 §ergonomics: keep a 1.7 m reference figure in shot — most scale errors
# are invisible on an isolated model and obvious next to a human.
FIGURE_STATURE = 1.70


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


def _setup_shading(scene):
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = scene.render.resolution_y = 1024
    scene.render.film_transparent = False

    sh = scene.display.shading
    sh.light = "STUDIO"
    # Workbench MATERIAL mode reads material.diffuse_color (the viewport display
    # colour), NOT the Principled Base Color. A generator that sets only the node
    # colour renders uniformly grey here and silently hides every material split.
    sh.color_type = "MATERIAL"
    sh.background_type = "VIEWPORT"
    sh.background_color = (0.22, 0.23, 0.25)   # mid grey: dark AND light parts stay readable
    sh.show_object_outline = True
    sh.show_cavity = True
    sh.cavity_type = "BOTH"
    sh.show_shadows = True


def _add_reference_figure(lo, hi):
    """Stand a capsule of FIGURE_STATURE beside the model, on the model's floor."""
    h = FIGURE_STATURE
    # Radius is a drawing convenience, not an anthropometric claim: the figure is
    # a scale rod for the eye and never a source of dimensions or gate values.
    r = h * 0.09
    x = hi.x + r * 3
    y = (lo.y + hi.y) / 2
    z0 = lo.z

    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h - 2 * r,
                                        location=(x, y, z0 + h / 2))
    bpy.context.object.name = "REF_FIGURE"
    # Left unparented on purpose: parenting after placement reinterprets the
    # child location in parent space and throws the caps off the body.
    for cap_z in (z0 + r, z0 + h - r):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, y, cap_z))
        bpy.context.object.name = "REF_FIGURE_cap"


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
    _setup_shading(scene)

    lo, hi = _scene_bbox()
    center = (lo + hi) / 2
    size = hi - lo
    margin = 1.15

    cam_data = bpy.data.cameras.new("review_cam")
    cam_data.type = "ORTHO"
    cam = bpy.data.objects.new("review_cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    def shoot(name):
        scene.render.filepath = os.path.join(out_dir, f"{name}.png")
        bpy.ops.render.render(write_still=True)
        print(f"[render] {scene.render.filepath}")
        return scene.render.filepath

    written = []
    dist = max(size) * 3 + 1.0
    for name, (dirn, rot, extents) in VIEWS.items():
        w, h = extents(size)
        cam_data.ortho_scale = max(w, h, 0.001) * margin
        cam.location = center + dirn * dist
        cam.rotation_euler = rot
        written.append(shoot(f"ortho_{name}"))

    # Three orthos show dimensions but not form: proportion and joint reading
    # need a 3/4 view, and it must be perspective — an ortho 3/4 flattens the
    # depth cue it exists to provide.
    cam_data.type = "PERSP"
    iso_dir = Vector((1, -1, 0.7)).normalized()
    cam.location = center + iso_dir * (size.length / 2 / math.tan(cam_data.angle / 2) * margin)
    cam.rotation_euler = iso_dir.to_track_quat("Z", "Y").to_euler()
    written.append(shoot("view_iso"))

    # Human-scale shot last: the figure enlarges the bbox, so every framing that
    # must show the model alone is already done by this point.
    _add_reference_figure(lo, hi)
    lo, hi = _scene_bbox()
    center = (lo + hi) / 2
    size = hi - lo
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = max(size.x, size.z, 0.001) * margin
    cam.location = center + Vector((0, -1, 0)) * (max(size) * 3 + 1.0)
    cam.rotation_euler = Euler((math.pi / 2, 0, 0))
    written.append(shoot("view_scale"))

    # Exit 0 from the renderer is not proof the PNG landed (never-list #16).
    missing = [p for p in written if not os.path.exists(p) or os.path.getsize(p) == 0]
    if missing:
        raise SystemExit(f"[render] FAIL — no image written: {missing}")

    print(f"[render] done -> {out_dir} ({len(written)} images)")
    print("[render] LOOK AT THESE. An unopened render has verified nothing.")


if __name__ == "__main__":
    main()
