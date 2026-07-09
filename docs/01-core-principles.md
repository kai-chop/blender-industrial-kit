# 01 — Core Principles

Four rules that must be in place **before** any geometry is created. Every one of them was learned by violating it.

## 1. BOM first (Bill of Materials)

Before modeling or modifying anything, write the complete parts table:

| Part | Qty | Parent assembly | Build method |
|---|---|---|---|
| Side rail | 4 | frame | new (one definition) |
| Front step | 8 | front frame | linked duplicate of step |
| Rear brace | 3 | rear frame | linked duplicate of brace |
| Hinge | 2 | top | new |
| Top plate | 1 | top | new |
| Foot cap | 4 | rails | new (one definition, 4 instances) |

Why: modeling from what you can *see* in a reference image reliably omits parts — rear braces, hinges, the far side of symmetric assemblies. A BOM makes "process only the visible parts" structurally impossible. Manufacturing culture does exactly this: no factory starts assembly without a parts list.

**When modifying an existing model**: first *measure* the actual BOM by scanning the scene (enumerate objects, count instances), then write the target BOM, then diff the two mechanically after the change. See `scripts/verify_bom.py`.

## 2. Parameter dictionary (single layout sketch)

All driving dimensions live in **one dictionary at the top of the script**. Member-builder functions receive the dictionary; they never contain coordinate literals.

```python
PARAMS = {
    "H_TOP": 3.000,        # overall height (m)
    "RUNG_PITCH": 0.280,   # rung spacing — ergonomic constant, never scaled
    "N_STEPS": 10,
    "LEAN_DEG": 13.8,      # rail lean from vertical
    "RAIL_W": 0.076,       # rail cross-section width
    "RAIL_D": 0.030,
}
```

This is the Blender equivalent of parametric CAD's *layout sketch*: one sketch drives all parts. Scattered literals are chained references — they drift, and nobody can tell which number drives what. Add a one-line comment stating what follows when each parameter changes (this records *design intent*).

## 3. Datum placement (no chain dimensioning)

Declare named reference geometry at the top of the script — floor plane `z = 0`, centerline `x = 0`, the inclined climbing plane — and compute **every** member position in closed form from datums plus parameters:

```python
z_i = Z0 + i * PITCH          # correct: closed form from datum
z_i = z_prev * k              # forbidden: recurrence / chain reference
```

Chain dimensioning accumulates error (this is textbook tolerance stack-up, ASME Y14.5) and a single parameter change scatters every downstream member. Also forbidden: reading vertex coordinates of already-generated meshes to place the next part — that is the *topological naming problem* in Blender form (see doc 02).

## 4. Derivation = regenerate, never scale

To make a longer/taller variant of an industrial product:

- **Keep cross-sections fixed.** A 10 m ladder's rail is not twice as thick as a 5 m ladder's — extrusion dies don't scale with product length. (If the design genuinely calls for a heavier section, change the section *parameter* deliberately; a uniform ×2 on everything is never the answer.)
- **Keep ergonomic constants fixed.** Rung pitch (0.25–0.30 m) is set by human leg articulation, not by ladder length. Scaling it up produces a ladder that visibly "cannot be climbed."
- **Change the repeat count** (`N_STEPS`) and regenerate from the parameter dictionary.

Uniform scaling of an industrial product is a category error: it thickens sections, stretches ergonomic spacings, and enlarges joint details simultaneously. The result reads instantly as a toy.

## 5. Part / Assembly separation (instance, don't re-create)

"I need another one of the same part" has exactly one answer: **share the mesh datablock**.

```python
mesh = build_rung_mesh(PARAMS)              # define ONCE
for i in range(PARAMS["N_STEPS"]):
    ob = bpy.data.objects.new(f"rung_{i}", mesh)   # instance N times
    ob.matrix_world = rung_matrix(i, PARAMS)
    col.objects.link(ob)
```

Generating a "new box of the same size" instead is how two nominally identical parts end up subtly different — and how edits to one silently miss the others. This is CAD's Part/Assembly separation. Editing one instance edits all; that is a feature. Unlink the datablock only when divergence is explicitly intended.

Corollary — **apply scale on the part definition, never on instances**: a non-1.0 object scale distorts bevel widths, physics, and exports; but applying transform on a shared datablock deforms every instance. Bake scale into the mesh once, at definition time.
