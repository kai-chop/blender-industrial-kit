"""Minimal parametric ladder — a working demonstration of the kit's core rules.

Demonstrates:
  * parameter dictionary (single layout source, doc 01)
  * named datums + closed-form placement, no chain references (docs 01/02)
  * part/assembly separation: one rung mesh, N instances (doc 01)
  * mating part in the parent's frame: feet inherit the rail lean,
    only the sole is cut by the world-horizontal floor plane (doc 06)
  * explicit terminal conditions: rungs end short of rail inner faces
    with a declared clearance (doc 06)

Run headless:
    blender --background --python example_parametric_ladder.py
Output:
    output/ladder_example.blend
"""
import math
import os

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters
# All driving dimensions in ONE dict. Units: meters.
PARAMS = {
    "H_TOP": 3.000,        # overall vertical height; changing it re-derives rail length & rung count usage
    "LEAN_DEG": 13.8,      # rail lean from vertical; feet cut plane and rung Y positions follow
    "RAIL_GAP": 0.400,     # clear inner width between rails (OSHA >= 0.292)
    "RAIL_W": 0.076,       # rail section width  (X)
    "RAIL_D": 0.030,       # rail section depth  (along climb normal)
    "RUNG_PITCH": 0.280,   # ISO 14122-4: 225-300 mm — ergonomic constant, never scaled with H_TOP
    "RUNG_R": 0.015,       # rung radius (ISO: 20-35 mm dia)
    "RUNG_SEGS": 12,       # by camera distance, not default 32 (doc 05)
    "Z0": 0.300,           # first rung height above floor (datum-based, closed form)
    "RUNG_CLEAR": 0.0005,  # declared clearance per rung end vs rail inner face (terminal condition)
    "FOOT_LEN": 0.090,     # foot cap length along the rail axis
    "FOOT_CLEAR": 0.0005,  # declared clearance between foot top and rail end
}

# ---------------------------------------------------------------- datums
FLOOR_Z = 0.0                      # world floor plane
CENTER_X = 0.0                     # ladder centerline
THETA = math.radians(PARAMS["LEAN_DEG"])
RAIL_AXIS = Vector((0.0, math.sin(THETA), math.cos(THETA)))  # unit vector along rails
RAIL_X = PARAMS["RAIL_GAP"] / 2 + PARAMS["RAIL_W"] / 2       # rail centerline |X|


def rail_matrix(sign):
    """World matrix of a rail: leaned THETA about X, based at the floor datum."""
    # NOTE the sign: Blender's Rotation(+X) sends +Z toward -Y. We lean toward
    # +Y (where the rung math y_i = z*tan(theta) lives), so rotate by -THETA.
    # The side-view ortho render is what catches this class of sign error —
    # the interference gate cannot (parts that miss each other overlap nothing).
    rot = Matrix.Rotation(-THETA, 4, "X")
    loc = Matrix.Translation((sign * RAIL_X, 0.0, FLOOR_Z))
    return loc @ rot


def _box_mesh(name, w, d, h, z0=0.0):
    """Axis-aligned box mesh: X width, Y depth, Z from z0 to z0+h. Origin at section center."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(w, d, h), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(0, 0, z0 + h / 2), verts=bm.verts)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


def build():
    scene = bpy.context.scene
    # remove ALL pre-existing objects (the default cube lives in a child
    # collection — unlinking from scene.collection alone misses it, and the
    # BOM/interference gates will rightly fail on the stowaway)
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)

    col = bpy.data.collections.get("Ladder") or bpy.data.collections.new("Ladder")
    if col.name not in {c.name for c in scene.collection.children}:
        scene.collection.children.link(col)

    p = PARAMS
    rail_len = p["H_TOP"] / math.cos(THETA)  # closed form from the height parameter

    # ---- rails: ONE mesh definition, two instances (part/assembly separation)
    rail_mesh = _box_mesh("rail", p["RAIL_W"], p["RAIL_D"], rail_len)
    for sign, tag in ((-1, "L"), (1, "R")):
        ob = bpy.data.objects.new(f"rail_{tag}", rail_mesh)
        ob.matrix_world = rail_matrix(sign)
        col.objects.link(ob)

    # ---- rungs: ONE mesh definition, N instances, closed-form placement
    rung_len = p["RAIL_GAP"] - 2 * p["RUNG_CLEAR"]  # declared terminal clearance
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=p["RUNG_SEGS"],
        radius1=p["RUNG_R"], radius2=p["RUNG_R"], depth=rung_len,
    )
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"), verts=bm.verts)
    rung_mesh = bpy.data.meshes.new("rung")
    bm.to_mesh(rung_mesh)
    bm.free()

    n_rungs = int((p["H_TOP"] - p["Z0"]) // p["RUNG_PITCH"]) + 1
    for i in range(n_rungs):
        z_i = p["Z0"] + i * p["RUNG_PITCH"]      # z_i = z0 + i*pitch — never a recurrence
        y_i = z_i * math.tan(THETA)              # rail centerline Y at that height (datum math)
        ob = bpy.data.objects.new(f"rung_{i:02d}", rung_mesh)
        ob.matrix_world = Matrix.Translation((CENTER_X, y_i, z_i))
        col.objects.link(ob)

    # ---- feet: built IN THE RAIL'S FRAME, sole cut by the world floor plane.
    # The cap runs along the rail axis (inherits the lean); only the ground
    # face is horizontal — the two-constraint composition of doc 06.
    foot_w = p["RAIL_W"] + 0.008   # cap wraps the rail section slightly
    foot_d = p["RAIL_D"] + 0.008
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # local frame = rail frame; run from below the floor up to just under the rail end
    bmesh.ops.scale(bm, vec=(foot_w, foot_d, p["FOOT_LEN"]), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(0, 0, -p["FOOT_LEN"] / 2 - p["FOOT_CLEAR"]), verts=bm.verts)
    foot_mesh_local = bpy.data.meshes.new("foot_uncut")
    bm.to_mesh(foot_mesh_local)
    bm.free()

    for sign, tag in ((-1, "L"), (1, "R")):
        m = rail_matrix(sign)
        bm = bmesh.new()
        bm.from_mesh(foot_mesh_local)
        bm.transform(m)  # world space, leaned like the rail
        # cut the sole with the WORLD horizontal floor offset (wedge sole)
        sole_z = FLOOR_Z - 0.5 * p["FOOT_LEN"] * math.cos(THETA)
        res = bmesh.ops.bisect_plane(
            bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
            plane_co=(0, 0, sole_z), plane_no=(0, 0, -1.0),
            clear_outer=True, use_snap_center=False,
        )
        bmesh.ops.holes_fill(bm, edges=[e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)])
        mesh = bpy.data.meshes.new(f"foot_{tag}")
        bm.to_mesh(mesh)
        bm.free()
        ob = bpy.data.objects.new(f"foot_{tag}", mesh)  # matrix already baked (world)
        col.objects.link(ob)

    bpy.data.meshes.remove(foot_mesh_local)

    # ---- declared BOM (the mechanical audit target, doc 07)
    bom = {"rail": 2, "rung": n_rungs, "foot": 2}
    scene["bom_json"] = repr(bom)
    return bom


if __name__ == "__main__":
    bom = build()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.abspath(os.path.join(out_dir, "ladder_example.blend"))
    bpy.ops.wm.save_as_mainfile(filepath=path)
    print(f"[ladder] BOM: {bom}")
    print(f"[ladder] saved: {path}")
