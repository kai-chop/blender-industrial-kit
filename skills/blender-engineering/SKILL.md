---
name: blender-engineering
description: Four-stage pipeline for industrial-product modeling in Blender — dossier research → design divergence → engineering sheet → build & verify.
---

# blender-engineering — Role-separated pipeline for industrial 3D modeling

**This skill carries only process and role wiring.** All content knowledge (dimensions, manufacturing grammar, the never-list) lives in the kit's `docs/` directory. Nothing is duplicated here — `docs/` is the single authoritative source.

If the kit is not installed on the current machine, skip the `docs/` references and run the pipeline with general knowledge, noting the gap in the dossier output.

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
- Visual review of renders is the human's and main session's responsibility — an agent's "PASS" report covers only mechanical gate exit codes, not visual correctness.

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
- Renders: front / side / top ortho + human-scale figure
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

After all three exit 0, the session's judgment layer and the user review the PNG renders. Approved renders are saved as a golden baseline; subsequent changes are regression-checked against them.

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
