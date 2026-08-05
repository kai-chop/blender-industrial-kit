---
name: blender-engineering
description: Four-stage pipeline for industrial-product modeling in Blender — dossier research → design divergence → engineering sheet → build & verify.
---

# blender-engineering — Role-separated pipeline for industrial 3D modeling

**This skill carries only process and role wiring.** All content knowledge (dimensions, manufacturing grammar, the never-list) lives in the kit's `docs/` directory. Nothing is duplicated here — `docs/` is the single authoritative source.

If the kit is not installed on the current machine, skip the `docs/` references and run the pipeline with general knowledge, noting the gap in the dossier output.

> **Rules carry IDs; `RULES.md` next to this file says where each came from and whether it may be enforced.** `[U*]` = the user confirmed it. `[C*]` = an inference — a working default, advisory, **never a pass/fail gate** until the user promotes it. Retiring a rule = flip its status in `RULES.md` and delete its line here; no incident narrative is left behind in this file.

## Stage −1: fix the requirement source before anything else

**Two questions, two different authorities. Confusing them is how this pipeline fails.**

| Question | Ground truth | Who wins |
|---|---|---|
| (a) What *is* — behaviour, dimension, cause | measurement | measurement beats anyone's words, including the user's guesses |
| (b) What is *wanted* — the shape to build | **the user's words and drawings** | the user, axiomatically. No measurement exists in this space `[U1]` |

Before Stage 0, write the **requirement register** `[C1]`: every artefact carrying (b) — image paths, verbatim user sentences — one line each on what it governs.

- `[U2]` When new requirement material arrives mid-build, its authority covers **everything it depicts**, not just the part under discussion. Re-derive that whole extent; demote your earlier readings to hypotheses.
- `[U3]` If two artefacts conflict, **ask** — do not invent a compromise reading.
- `[U4]` Criticism and counter-proposals about the requested shape are input to the user's decision, never licence to build a different "correct" shape.
- `[U5]` **Never turn something the user has not confirmed into a pass/fail condition.** Your reading of a drawing is a hypothesis: write it down as a question, not a spec line, and do not invent numbers to fill it (angles, margins, tolerances). An invented value that reaches a gate or a handoff document is the same failure as an invented shape.

Every sheet row carries its source, and sources are of exactly two kinds: `src: <image/quote>` from the requirement register (**binding**), or `src: <catalogue/standard/measurement>` from (a) (binding only where the user has not spoken — photographic appearance outranks catalogue dimensions when the user says so). A row you cannot cite is **not specified yet** — go ask. An uncited row is exactly the thing that later passes every gate and fails the user.

## Trigger conditions

Apply this skill when:
- Building a **new industrial prop** (ladder, table, fixture, structural frame, tool, or similar).
- Doing a **major shape rework** (geometry changes beyond one parameter).

Do NOT apply for single-dimension tweaks, material swaps, or UV-only edits — go directly to the modeler.

## The four-stage pipeline

| Stage | Owner | Input → Output |
|---|---|---|
| **0. Dossier** | `blender-dossier` agent (delegated) | Product name + intended use → `dossier-<product>.md` (part census, sourced canonical dimensions, manufacturing grammar + era, ergonomic constraints, modeling risks) |
| **1. Design divergence** | `blender-designer` agent (delegated) | Dossier + user intent → 3–5 counter-proposals (one deliberately off-canon) + two-line tradeoffs per proposal. **Never converges — convergence is the session's job.** |
| **2. Engineering sheet** | **Session's judgment layer — never delegated** | Chosen proposal → filled engineering-sheet template (see below) + user sign-off. Rationale: delegated design was the verified root cause of repeated modeling failures; the sheet is the commitment point and must be owned by the decision maker. |
| **3. Build & verify** | `blender-modeler` agent (delegated) | Signed engineering sheet → generator script + `.blend` + all three gate commands at exit 0 + PNG renders |

**Skipping rules:**
- Stages 0 and 1 may be skipped with explicit written justification (e.g., "product geometry is well-established, dossier not needed" or "user has specified the form").
- Stages 2 and 3 are **never skippable**.
- **Judgement of the shape** — is this what was asked for — is the human's and main session's responsibility; an agent's "PASS" covers mechanical gate exit codes, not requirement conformance. But `[U8]` the agent that produced the renders **opens them first**, and `[C5]` sweeps them for objective defects only (never-list 1–6). That look is a pre-flight, not a verdict: it reports a defect list or "none of the listed defects found", never "looks good".

## Engineering-sheet template (Stage 2 deliverable — never omit)

```markdown
# Engineering Sheet — <product>

## PARAMS (driving dimensions — every value includes unit + source comment)
{ "H_TOTAL":    2.440,  # m, OSHA 1926.1053 minimum working height
  "RUNG_PITCH": 0.280,  # m, ISO 14122-4: 225–300 mm — ergonomic constant, does NOT scale with height
  "RAIL_GAP":   0.400,  # m, clear width between rails; OSHA minimum 292 mm — fixed human-reach constant
  ... }

## Datums (named reference planes; all placement in closed form: z_i = z0 + i*pitch)
FLOOR_Z = 0
CENTER_X = 0
<inclined surface or other datum>

## BOM (part × qty × parent × process-tag × build-method)
| Part  | Qty | Parent | Process tag | Build method |
|-------|-----|--------|-------------|--------------|
| rail  |  2  | frame  | extrusion   | linked       |
| rung  |  N  | rail   | extrusion   | linked       |
| foot  |  2  | rail   | casting     | new          |

## Terminal conditions (every member end: flush-trim / miter / named clearance)
- Rail bottom: bisect at FLOOR_Z, foot socket clearance = 1 mm
- Rung ends: stop short of rail inner face by named clearance (RUNG_CLEAR)

## Through / trimmed hierarchy (which members are continuous; which are trimmed to them)
- Through: rails (continuous, floor to top)
- Trimmed to rails: rungs (bisected at rail inner face)

## Verification plan
- BOM audit: declared BOM in scene["bom_json"] matches script PARAMS
- Interference: zero undeclared overlap volume (declared unions whitelisted); rung–rail gap = RUNG_CLEAR exactly — floating is caught by the side-view render, not this gate (see note below)
- Dimension asserts: RUNG_PITCH between rungs within tolerance
- Renders: front / side / top ortho + iso (form) + human-scale figure — all five opened and swept
- Requirement conformance (axis B below): each expectation transcribed from the requirement register with its citation
```

**Rule:** If any field cannot be filled, design is not settled — return to Stage 0 or 1. Do not hand an incomplete sheet to the modeler.

## Stage 3 gate commands

Run these in order. All three must exit 0 before renders are requested. Replace `{{KIT_PATH}}` with your clone directory and resolve the Blender executable for your machine.

```bash
blender --background --python <generator>.py

blender --background --python {{KIT_PATH}}/scripts/verify_bom.py \
        -- --blend <output>.blend

blender --background --python {{KIT_PATH}}/scripts/verify_interference.py \
        -- --blend <output>.blend

blender --background --python {{KIT_PATH}}/scripts/render_orthos.py \
        -- --blend <output>.blend --out <renders_dir>
```

`render_orthos.py` emits the set never-list #14 requires — `ortho_front/side/top`, `view_iso` (perspective 3/4: orthos give dimensions, only this gives form), `view_scale` (1.7 m reference figure, doc 03). **Then `[U8]` open them.** Sweep for never-list 1–6 and for framing sanity — an empty or clipped frame means the render proved nothing. Doc 09's checklist D also wants a close-up per joint class; that cannot be framed generically, so it comes from a feature-framing operator where the feature names are known.

After all three gates exit 0 **and the renders have been looked at**, the session's judgment layer and the user review them. Approved renders are saved as a golden baseline; subsequent changes are regression-checked against them.

## Stage 3, axis B — requirement conformance (the axis gates miss)

Exit 0 proves the tool *ran*, not that the output is *right*, and axis A ("is the model self-coherent") cannot answer "is this the thing that was asked for". Independence from the generator is not enough either — a gate written from your own sheet is self-verification one level up.

- `[U6]` Expectations are transcribed **from the requirement register**, each assert carrying its citation. An expectation transcribed from your own sheet certifies only that you built what you decided to build.
- `[U7]` **If a green gate disagrees with the user's words, the gate is stale by definition.** Fix the gate. Never shelve the user's words because "the checks pass".
- `[C2]` Conditions want to be **shapes, not booleans** — "is the hook open?" is satisfiable by a 28° slit that reads as a snap ring. But the shape values themselves are `[U5]`: ask, do not supply them.
- `[C3]` A feature judged at a few pixels has not been looked at. Render each judged feature large enough to decide before claiming visual confirmation, and check the target is actually in frame — an off-frame target produces the "nothing changed" render.
- `[C4]` Run the part census against the **source image** as well as the sheet: count what the drawing shows between each pair of named parts.

## Live MCP sessions, where available

Where an interactive Blender MCP bridge is configured (viewport screenshots, scene queries, arbitrary `bpy` execution), use it to **look and diagnose, not to author**. Doc 02's MBD rule stands: the generator script is the master, so anything found in a live session goes back into the script and is re-run headless — a model poked into shape interactively is unreproducible. Note that such bridges need a GUI Blender with the add-on running; they do not work under `--background`.

## Real-world note: why numeric gates and visual review are complementary

An interference gate once passed a ladder whose rungs floated clear of the rails. The gate was correct — no overlap means no interference volume — but the geometry was wrong: the rungs had no contact with the rails at all. The side-view ortho caught the floating gap in one glance. Numeric gates and visual review answer different questions and neither replaces the other (see `docs/07-verification.md` for the full two-layer model).

## Kit docs index — required reading by role

| Doc | Content | Must-read for |
|---|---|---|
| `docs/01-core-principles.md` | BOM-first, parameter dictionary, datum placement, part/assembly separation, derivation rules | modeler, main session |
| `docs/02-cad-discipline.md` | Design intent, topological-naming trap, chain vs. baseline dimensioning, MBD (script = master) | main session |
| `docs/03-ergonomics.md` | Anthropometry and canonical dimension tables; ANSUR II and digital human modeling | dossier, designer |
| `docs/04-manufacturing-grammar.md` | Process → shape mapping: sheet metal, extrusion, casting, CNC, injection molding, AM; grammar by era | dossier, designer |
| `docs/05-edges-curves-fillets.md` | Polygon counts, bevel/fillet/chamfer semantics, curve continuity, catenary, silhouette/normal-map split | modeler |
| `docs/06-terminal-conditions.md` | End treatment of members: trim/miter/cope, burrs, fits as named clearances, coordinate frames for mating parts | main session, modeler |
| `docs/07-verification.md` | Two-layer verification: mechanical gates + mandatory multi-view visual review; CI and golden-image regression | everyone |
| `docs/08-never-list.md` | Absolute-never mistakes — the failures that must not reach human review | everyone (read before starting) |
| `docs/09-checklists.md` | Condensed checklists: before / during / verify / hand-off | modeler, main session |
