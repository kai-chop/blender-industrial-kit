"""BOM audit — scene scan vs. declared parts table (doc 07).

Counts mesh objects per name prefix (``rail_L`` -> ``rail``) and diffs the
result against the expected BOM. The expected BOM comes from, in priority:
  1. --bom "rail=2,rung=10,foot=2" on the command line
  2. the scene custom property ``bom_json`` (written by the generator)

Exit 0 = zero diff, 1 = mismatch. Run as a SEPARATE script from the
generator — the generator grading itself is a false-PASS machine.

    blender --background --python verify_bom.py -- --blend file.blend [--bom rail=2,rung=10,foot=2]
"""
import ast
import sys
from collections import Counter

import bpy


def _args():
    argv = sys.argv
    out = {"blend": None, "bom": None}
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
        if "--blend" in argv:
            out["blend"] = argv[argv.index("--blend") + 1]
        if "--bom" in argv:
            out["bom"] = argv[argv.index("--bom") + 1]
    return out


def _prefix(name):
    return name.rsplit("_", 1)[0] if "_" in name else name


def main():
    a = _args()
    if a["blend"]:
        bpy.ops.wm.open_mainfile(filepath=a["blend"])

    if a["bom"]:
        expected = {k: int(v) for k, v in (kv.split("=") for kv in a["bom"].split(","))}
    else:
        raw = bpy.context.scene.get("bom_json")
        if not raw:
            print("[bom] FAIL: no --bom argument and no scene['bom_json']")
            sys.exit(1)
        expected = ast.literal_eval(raw)

    actual = Counter(_prefix(o.name) for o in bpy.context.scene.objects if o.type == "MESH")

    ok = True
    for part in sorted(set(expected) | set(actual)):
        e, g = expected.get(part, 0), actual.get(part, 0)
        mark = "OK " if e == g else "FAIL"
        if e != g:
            ok = False
        print(f"[bom] {mark} {part}: expected={e} actual={g}")

    if not ok:
        sys.exit(1)
    print("[bom] PASS — scene matches declared BOM")


if __name__ == "__main__":
    main()
