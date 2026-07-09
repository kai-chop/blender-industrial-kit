# 02 — CAD Discipline, Translated to Blender Python

Parametric CAD spent decades learning how models break under change. Borrow the conclusions — both the classic ones and the modern ones (MBD, code-CAD, CI).

## Design intent

*Design intent* = encoding "how should this model react to change" into the model's structure (Onshape's parametric modeling guidance is a good primary source). Practices that transfer directly to script modeling:

- One layout source (the parameter dictionary) drives all parts.
- Driving dimensions declared first, at the top.
- Never reference geometry that a downstream operation created (e.g., don't dimension to an edge a fillet made — in Blender terms: don't place parts relative to vertices that a boolean/bevel produced).
- Record intent in comments: *"changing `LEAN_DEG` re-derives the footprint and foot-cap cut plane."*

## The topological naming trap

FreeCAD's classic failure mode: referencing an internal face/edge name that changes when upstream operations change, breaking everything downstream. The fix in CAD is *datum planes* — attach sketches to origin-based datums, not to generated faces.

The identical Blender trap: **reading coordinates out of an already-generated mesh to place the next part.** Generation order changes, a boolean shifts vertex indices, and the chain collapses. Fix: all placement comes from declared datums + parameters in closed form. Generated geometry is *output only*, never *input* for placement.

## Chain vs. baseline dimensioning

- **Chain** (each feature measured from the previous): errors accumulate. `z_i = z_{i-1} * k` in script form. Forbidden.
- **Baseline/datum** (every feature measured from one reference): errors independent. `z_i = z0 + i * pitch`. Required.

Float error plus a parameter tweak turned chain-placed rungs into visibly scattered geometry in practice. This is not theoretical.

## Linked duplicates = instance references

| CAD concept | Blender equivalent |
|---|---|
| Part definition | mesh datablock (created once) |
| Part instance | `bpy.data.objects.new(name, shared_mesh)` |
| Sub-assembly reference | collection instance |
| Breaking the link deliberately | explicit datablock copy (`mesh.copy()`) |

## Scale apply rules

1. Build the part at real-world size; `transform_apply(scale=True)` **once, at part definition**.
2. Never apply transforms on objects sharing a datablock — it deforms all instances.
3. Never leave non-1.0 scale on export-bound objects: bevel widths, modifier distances, physics, and FBX/OBJ export all read it differently than the viewport suggests.

## Model-Based Definition: the script is the single source of truth

Modern engineering has retired the drawing as master document. **MBD** (ASME Y14.41 / ISO 16792, exchanged as STEP AP242 with embedded PMI) makes the annotated 3D model the *only* authoritative artifact — drawings, if any, are generated views. The script-modeling translation is direct:

- **The generator script + parameter dictionary is the master.** The `.blend`, the FBX, the renders are *derived artifacts* — never hand-edit them; regenerate. A hand-tweaked vertex in a derived file is the modern equivalent of red-penning a print and not updating the model.
- This is the **code-CAD** stance (OpenSCAD / CadQuery / Build123d lineage): geometry as code means the model is **diffable, reviewable, and version-controlled**. Two lines of git diff on `PARAMS` tells a reviewer more than two screenshots.
- Since the model is code, it gets code's quality machinery: the verification gates (doc 07) run headless in **CI on every change**, not "when someone remembers."

## Comments carry the drawing's job

An engineering drawing tells the manufacturer *why* dimensions are what they are (datum symbols, tolerance callouts). In script modeling, comments do this job. Minimum bar:

- Each parameter: unit + what depends on it.
- Each non-obvious constant: which standard or measurement it came from (e.g., `RUNG_PITCH = 0.280  # ISO 14122-4: 225–300 mm, OSHA: 254–356 mm`).
- Each member function: which datum(s) it places from.

A model whose numbers have no recorded origin cannot be reviewed — a reviewer can only shrug at `0.2861`.
