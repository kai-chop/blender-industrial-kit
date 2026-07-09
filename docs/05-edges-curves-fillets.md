# 05 — Edges, Curves, and Fillets

## Circle discretization: choose segment counts by on-screen size

An n-gon approximating a circle sags below the true radius by `r · (1 − cos(π/n))` at each chord midpoint. The visible error scales with apparent (on-screen) size — so segment count is a function of **camera distance**, not habit.

| Segments | Use for |
|---|---|
| 8 | distant objects, thin pipes |
| 12–16 | standard props (workhorse; ladder rungs 8–12, table legs 12–16 suffice) |
| 32 | close-up / hero assets |
| >32 | almost always waste — indistinguishable in screenshots |

Don't blindly accept the default 32. Typical LOD chain: 32 → 16 → 8 → 6.

## Every real edge is beveled

**Perfectly sharp edges do not exist on manufactured products** — and they catch no highlight, which is a large part of why unbeveled CG looks cheap. Standard treatment:

- Bevel modifier on all visible edges, width ~1–3 mm equivalent, 2 segments.
- Shade Auto Smooth.
- The edge highlight this produces is the single cheapest "industrial-ness" upgrade available.

## Fillet vs. chamfer carry meaning

They are not interchangeable decorations:

- **Fillet (round, R)**: relieves stress concentration. Load-bearing junctions, cast parts, places where cracks would start. (Documented effect: optimized fillets can raise effective strength double-digit percentages.)
- **Chamfer (cut, C)**: guides assembly (lead-in for insertion) and protects hands/parts from sharp corners. Hole entries, plate edges, insertion ends.

Applying one uniform radius everywhere flattens the product grammar. Use R at load junctions, C at insertion/handling edges.

## Curve vocabulary: which curve, and why

| Curve | Physical origin | Use |
|---|---|---|
| Circular arc | lathes, compasses, bent tube | machine parts, pipe bends |
| Ellipse | circle viewed obliquely; angled pipe section | intersections, projections |
| Parabola | uniformly distributed load | suspension bridge main cables (loaded), projectile paths |
| **Catenary** (`cosh`) | self-weight only | **hanging ropes, chains, slack cables**; inverted = zero-bending arch |
| Clothoid | curvature ∝ arc length | road/rail transition from straight to arc |

The common defect: drawing a hanging rope/chain as a hand-placed Bézier or a circular arc. It reads as physically false. Evaluate `cosh` in Python (two endpoints + sag fix the parameters) and bake it into the curve.

## Continuity: why some curves look cheap

- **G0** — positions touch (a corner).
- **G1** — tangents match. Highlights still **break** at the seam.
- **G2** — curvature matches. Highlights flow through in one stroke. (Automotive Class-A surfacing requires G2 as a floor.)

"Cheap-looking curve" usually = arc-to-line joints stuck at G1, or uneven Bézier control points. Inspection method: apply Subdivision, view with a reflective Matcap, and look for highlight breaks — a broken highlight is a G1 seam. For Bézier work: `Aligned` handles give G1; approximating G2 requires tuning relative handle lengths.
