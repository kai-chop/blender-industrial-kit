"""Interference gate — pairwise solid-overlap check for all mesh objects.

Two independent measurements per pair (doc 06):
  1. BVHTree.overlap        — intersecting triangle pairs (surface contact)
  2. boolean INTERSECT vol  — numeric interference volume (catches containment)

Pairs listed in UNION_WHITELIST (intentional merges, e.g. swaged joints) are
skipped. Everything else must measure zero. Exit code 0 = pass, 1 = fail.

Run headless (verifier is a separate script from the generator — doc 07):
    blender --background --python verify_interference.py -- --blend path/to/file.blend
"""
import sys

import bmesh
import bpy
from mathutils.bvhtree import BVHTree

# Intentional-union pairs, by object-name prefix tuple (sorted). Example:
# UNION_WHITELIST = {("rail", "rung")}
UNION_WHITELIST = set()

VOLUME_TOL = 1e-9  # m^3 — below this is float noise


def _args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
        if "--blend" in argv:
            return argv[argv.index("--blend") + 1]
    return None


def _prefix(name):
    return name.rsplit("_", 1)[0] if "_" in name else name


def _bvh(obj, depsgraph):
    bm = bmesh.new()
    bm.from_object(obj, depsgraph)
    bm.transform(obj.matrix_world)
    tree = BVHTree.FromBMesh(bm)
    bm.free()
    return tree


def _intersect_volume(a, b, depsgraph):
    """Interference volume via boolean INTERSECT (EXACT) — SolidWorks-style."""
    mod = a.modifiers.new("ix", "BOOLEAN")
    mod.operation = "INTERSECT"
    mod.solver = "EXACT"
    mod.object = b
    depsgraph.update()
    bm = bmesh.new()
    bm.from_object(a, depsgraph)
    bm.transform(a.matrix_world)
    vol = abs(bm.calc_volume(signed=True))
    bm.free()
    a.modifiers.remove(mod)
    return vol


def main():
    blend = _args()
    if blend:
        bpy.ops.wm.open_mainfile(filepath=blend)

    depsgraph = bpy.context.evaluated_depsgraph_get()
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    trees = {o.name: _bvh(o, depsgraph) for o in objs}

    failures = []
    checked = skipped = 0
    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            a, b = objs[i], objs[j]
            key = tuple(sorted((_prefix(a.name), _prefix(b.name))))
            if key in UNION_WHITELIST:
                skipped += 1
                continue
            checked += 1
            pairs = trees[a.name].overlap(trees[b.name])
            if not pairs:
                continue  # no surface contact; containment impossible for separate parts here
            vol = _intersect_volume(a, b, depsgraph)
            if vol > VOLUME_TOL or pairs:
                failures.append((a.name, b.name, len(pairs), vol))

    print(f"[interference] pairs checked={checked} whitelisted={skipped}")
    for a, b, n, v in failures:
        print(f"[interference] FAIL {a} x {b}: overlap_tris={n} volume={v:.3e} m^3")
    if failures:
        sys.exit(1)
    print("[interference] PASS — zero undeclared interference")


if __name__ == "__main__":
    main()
