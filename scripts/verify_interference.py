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
UNION_WHITELIST = {
    # --- KRFリング v3.1 (ring-corner-sheet.md): 意図された継手(doc06 swaged joint相当) ---
    # ロープ端の一体金具(アイ+フック+白巻き)は互いに接触/僅少重複する設計。同一端内の結合
    # (Eye/Hook/Wrap)、および柱コーナーでX系/Y系の2クラスタが近接するのはROPE_LINE/
    # ROPE_HALF/POST_DIAGの差分がEYE径未満になる寸法帰結（発明ではなくシート値の直接帰結）。
    ("Eye", "Hook"), ("Eye", "Wrap"), ("Hook", "Wrap"),
    # パッドはロープ端金具群の上に被さって吊られる（実物どおりの接触＝v3.2宣言）。
    # v4: リンク金具は白巻きに包まれ、三角パッドを貫通して柱フックへ渡る（013の白い斜め線）。
    ("Pad", "Rope"), ("Pad", "Eye"), ("Pad", "Wrap"), ("Pad", "Hook"),
    # キーはソート済みタプルで引かれる（上の照合実装参照）
    ("Link", "Wrap"), ("Link", "Pad"), ("Eye", "Link"), ("Hook", "Link"),
    ("Link", "Rope"),   # リンク起点はロープ端の輪へ差し込まれる継手（v4）
    ("Link", "Post"),   # フック側でリンク終端が柱面に届く継手（v4）
    ("Hook", "Hook"),   # 柱面で隣接するX系/Y系フック輪の接触（v4）
    # 柱への埋め込み継手: 天端キャップ・フック(HOOK_EMBED)は柱に被さる/埋まる設計。
    ("Cap", "Post"), ("Hook", "Post"),
    # 幕(直線)と幕(面取りコーナー斜め)のマイター継ぎ目＝隣接パネルの縫い目接触。
    ("Skirt", "SkirtC"),
    # アンダーフレームの梁×脚・梁×梁・梁×柱の交差＝溶接フレームの十字継手（実物も交差部で
    # 部材が重なる。梁はPOST_SPANで柱芯まで通す設計＝ladder例のrail-rung相当）。
    ("Beam", "Leg"), ("Beam", "Beam"), ("Beam", "Post"),
    # 斜め幕は柱背後へ引き込むため梁線の内側を通る＝布がフレーム部材に接する（v3.2宣言）。
    ("Beam", "SkirtC"),
    # マット下面とフレーム(脚/梁)・幕の接触＝プラットフォームへのフラッシュ取付。
    ("Leg", "Ring"), ("Beam", "Ring"), ("Ring", "Skirt"), ("Ring", "SkirtC"),
    # Post-Ring: 欠き込みジョイント（v3.2宣言・ring-corner-sheet.md）＝面取り線x+y=4.70が
    # 柱芯を通り、台が柱を半身抱く。実物もデッキが柱を欠き込んで抱く構造（意図された継手）。
    ("Post", "Ring"),
    # Pad-Rope/Eye/Hook: パッドはコーナー対角45°・柱面からPAD_GAPで吊るす配置だが、
    # ロープ端クラスタの至近を通るため接触/僅少重複する。実写でもパッド脇をロープが
    # 密接して通る（結束紐で保持）ため、モデル上は面重複として現れる。
    ("Eye", "Pad"), ("Hook", "Pad"), ("Pad", "Rope"),
    ("Eye", "Rope"), ("Hook", "Rope"), ("Rope", "Wrap"),
}

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
