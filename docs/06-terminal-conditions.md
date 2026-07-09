# 06 — Terminal Conditions: How Members End

The naive model of a structural member is "a profile extruded between two points, both ends raw." Weldment culture (SolidWorks Weldments, structural steel practice) defines a member as **profile × path × end treatment** — three things, not two. Leaving out the third produces the most common visible defects in generated assemblies.

## Through-member / trimmed-member hierarchy

Declare, per assembly, which members are *through* (continuous) and which are *trimmed against* them. For a ladder: rails are through-members; rungs, braces, and brackets trim to the rails. Record this as a column in the BOM.

- Trimmed member ends are cut by the through-member's face: `bmesh.ops.bisect_plane` with the mating face's plane, `clear_outer=True`.
- Diagonal members get an angle cut (miter) — same operation, inclined plane. **Share one miter plane between both members and they are guaranteed flush.**
- Result: flush (face-on-face) contact or an explicit clearance (e.g., 0.1 mm fitting gap). Never an overlap, never a protrusion.

## Burrs and flash: the sub-millimeter protrusion is a defect

Engineering definition: a *burr* is unintended material projecting past an edge after processing; *flash* is molding material leaked at the parting line. Real products ship **deburred** (edge condition is even a drawing callout — ISO 13715). Therefore:

> Any unnamed geometry protruding 0–1 mm past a neighboring part's surface is a defect, full stop. If a protrusion is intended (bolt head, rivet boss), it must exist as a *named part* in the BOM.

In renders these show up as z-fighting on coplanar faces and as edge slivers poking through the mate — the reviewer will describe them as "burrs" even if they've never heard the manufacturing term, because human eyes are calibrated on deburred products.

**Every member end must have an explicitly chosen condition**: flush trim / chamfer / radius / declared clearance. "Whatever the extrusion left" is not a condition.

## Interference is a mechanical check, not a visual one

CAD assemblies run *interference detection* as a standard gate: any solid-solid overlap (except declared press fits / threads) fails the build. Overlap in the real world means the parts cannot be assembled. Overlap in a render means z-fighting and shading artifacts.

Blender needs no add-on for this:

1. **`mathutils.bvhtree.BVHTree.overlap`** — enumerate intersecting triangle pairs between two objects. Zero pairs = no surface contact. Fast first gate.
2. **Boolean `INTERSECT` (EXACT) + `bmesh.calc_volume`** — the numeric interference *volume*, equivalent to commercial interference detection. Catches full containment, which pure surface overlap misses.
3. Maintain a **declared-union whitelist**: pairs that intentionally merge (e.g., rung ends swaged into rails) are excluded by name; everything else must measure zero.

See `scripts/verify_interference.py` for a working gate.

## Mating parts inherit the parent's coordinate frame

Case study — ladder feet. Real ladder feet are molded caps that **fit over the rail end**: the cap points along the rail axis (inheriting the rail's 13.8° lean), and only the tread face meets the floor (wedge-shaped sole, or a swivel foot). A foot modeled as a world-axis-aligned box under an inclined rail is instantly, visibly wrong.

The general rule: **a mating part is the composition of two constraints** — it inherits the parent member's frame (build it in the rail's local coordinates: `child.matrix_world = parent.matrix_world @ local_offset`), and only its interface face conforms to the other constraint (cut the sole with a world-horizontal plane: bisect at `z = const`). Building it with only one of the two constraints (all-world or all-parent) breaks it.

## Verification table for terminal conditions

| # | Check | Pass condition |
|---|---|---|
| 1 | Mating part axis | angle between cap local axis and parent member axis ≤ 0.1° |
| 2 | Ground-face flatness | sole face normals within 0.1° of (0,0,−1); sole vertex Z variance < 0.01 mm |
| 3 | Multi-foot coplanarity | max Z spread across all ground contacts < 0.5 mm (no wobble) |
| 4 | Pairwise interference | intersect volume = 0 for all pairs not on the union whitelist |
| 5 | Trimmed-member ends | zero vertices outside the through-member's face plane |
| 6 | Burr census | zero unnamed vertices located 0–1 mm outside any neighbor's surface |
| 7 | Independence | checks 1–6 run from a **separate script**, not the generator (see doc 07) |
