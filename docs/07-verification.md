# 07 — Verification: Two Layers, Independently Executed

The costliest lesson in this kit: **a model passed every numeric assert and the render was destroyed.** Numeric checks and visual checks catch disjoint defect classes; you need both, and neither may be run by the code that generated the model.

## Principle 1: The generator must not verify itself

A generation script that checks its own output re-executes its own misunderstanding. If the generator computed a wrong UV mapping, its built-in "check" applies the same wrong formula and passes. Observed instances:

- A UV remap script with a broken formula reported its own output as correct.
- A dump tool that only checked *texture exists* (not *which* texture, at what size) passed a build where the wrong texture was bound — "false PASS."

Rules:

- Verification lives in a **separate script** that reads the artifact fresh (open the `.blend`/export and inspect actual vertices, materials, image sizes, hashes).
- Verify **content against expected values**, not existence: packed texture pixel dimensions, byte size, checksum — "the file is there" and "hasTex=True" prove nothing.
- Exit code 0 from a pipeline tool is evidence the tool *ran*, not that the output is *right*.

## Principle 2: Mechanical layer (what scripts assert)

| Gate | Method |
|---|---|
| BOM match | scene scan: object count per part name vs. declared BOM; diff must be zero (`scripts/verify_bom.py`) |
| Dimensions | `obj.dimensions` / bounding box / direct vertex reads asserted against the parameter dictionary |
| Interference | BVH overlap + boolean intersect volume per pair (`scripts/verify_interference.py`) |
| Terminal conditions | the 7-row table in doc 06 |
| Mesh health (final) | self-intersection & manifold check on the joined export mesh (3D Print Toolbox add-on, or equivalent bmesh checks) |
| Determinism | build twice, byte-compare (or hash) the outputs — a nondeterministic generator hides drift |
| Deployment | hash-compare the built artifact at **every** location it's consumed from; "copy succeeded" ≠ "the right content arrived" |

No add-ons are needed for the core gates: `BVHTree.FromBMesh` + `overlap`, boolean `EXACT` modifier + `calc_volume(signed=True)`, and `bmesh.ops.bisect_plane` cover interference, containment, and trim verification headless (validated on Blender 4.x).

## Principle 3: Visual layer (mandatory, not optional)

Engineering drawing culture (ISO 128 / orthographic projection) exists because **one view is never enough** — a front view can look perfect while the top view exposes the contradiction. All-asserts-green is exactly "one view."

Before declaring any model complete, render and *look at*:

1. **Three orthographic views** — front, side, top (`camera.data.type = 'ORTHO'`) for overall consistency;
2. **At least one close-up** of each joint class (rung × rail, leg × top, brace × frame) — the drawing culture's *detail view*;
3. **One perspective shot next to the 1.7 m reference figure** — the scale gate;
4. A **Matcap/reflective pass** if curved surfaces matter (highlight breaks reveal G1 seams, doc 05).

Make the renders a fixed pipeline step emitted by a script (`scripts/render_orthos.py`) so "did we look at it?" is never a memory question. Wireframe overlay helps expose penetrations and floating parts.

## Principle 4: Verify the derivation, not just the endpoints

When deriving variant B from canonical A (e.g., a taller ladder), cross-check the derivation math itself two independent ways — closed-form recomputation vs. interpolation between anchors. Sub-millimeter agreement between two derivations is strong evidence; one derivation checked against itself is none.

## Principle 5: Import the verification culture with the knowledge

Every engineering domain ships its own inspection practice (drawings → multi-view checks; manufacturing → BOM audits and interference detection). When you import a domain's modeling knowledge but not its verification culture, you get confident-looking work with false PASSes. Import both, always.
