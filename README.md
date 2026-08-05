# Blender Industrial Modeling Kit

A field-tested discipline for building **industrial-product 3D props** (ladders, tables, furniture, fixtures, structural frames) with **Blender Python — parametric, headless, and verifiable**.

This is not a Blender tutorial. It is a set of design rules, canonical dimension tables, verification gates, and reference scripts distilled from real production failures: models that passed every numeric check and still looked wrong, parts that drifted apart when a parameter changed, feet that ignored the rail they were attached to, and "burrs" of geometry poking through neighboring parts. Each rule here exists because its absence produced a concrete, observed defect.

## Core thesis

> **Generic modeling skill does not produce industrial-looking products. Discipline does.**
> Industrial products look right because they obey manufacturing grammar (a process can only produce certain shapes), ergonomic standards (humans have fixed sizes), and engineering verification culture (drawings are checked from multiple views, assemblies are checked for interference). Import those systems instead of reinventing them by trial and error.

The kit deliberately mixes two eras of that culture: the century-old foundations (drawing conventions, anthropometry, weldment practice) and their modern successors — **Model-Based Definition** (the script is the master, everything else is derived), **DfAM and injection-molding grammar** (why current products look organic or shell-ribbed), and **CI-style verification** (gates on every change, golden-image regression). The old layer explains what "correct" looks like; the modern layer makes checking it automatic.

## What's inside

| Path | Content |
|---|---|
| [docs/01-core-principles.md](docs/01-core-principles.md) | BOM-first, parameter dictionary, datum placement, part/assembly separation, derivation rules |
| [docs/02-cad-discipline.md](docs/02-cad-discipline.md) | Design intent, topological-naming trap, chain vs. baseline dimensioning, linked duplicates, scale-apply rules, MBD & code-CAD |
| [docs/03-ergonomics.md](docs/03-ergonomics.md) | Anthropometry and canonical dimension tables (ladders, tables, chairs, stairs, handrails, grips); ANSUR II and digital human modeling |
| [docs/04-manufacturing-grammar.md](docs/04-manufacturing-grammar.md) | Process→shape mapping: sheet metal, extrusion, casting, CNC, injection molding, additive/topology-optimized; joint vocabulary; grammar by era |
| [docs/05-edges-curves-fillets.md](docs/05-edges-curves-fillets.md) | Polygon counts for circles, bevel/fillet/chamfer semantics, curve continuity (G0/G1/G2), catenary vs. parabola, geometry vs. normal-map split |
| [docs/06-terminal-conditions.md](docs/06-terminal-conditions.md) | End treatment of members: trim/miter/cope, burrs and flash, interference, fits as named clearances, coordinate frames for mating parts |
| [docs/07-verification.md](docs/07-verification.md) | Two-layer verification: mechanical gates (BOM audit, interference volume, dimension asserts) + mandatory multi-view visual review; CI and golden-image regression |
| [docs/08-never-list.md](docs/08-never-list.md) | Absolute-never mistakes — the failures that must not reach human review |
| [docs/09-checklists.md](docs/09-checklists.md) | Condensed checklists: before / during / verify / hand-off |
| [docs/10-architectural-structure.md](docs/10-architectural-structure.md) | Building scale: member hierarchy, load path, lateral systems, span/depth tables, long-span arena roofs, seating-bowl C-value, AESS connections and coatings |
| [docs/11-arena-production-infrastructure.md](docs/11-arena-production-infrastructure.md) | The layer hung from the roof: truss standards and duty by size, chain hoists and trim height, centre-hung composition and hoist zoning, pixel pitch tiering, ribbon/fascia |
| [scripts/](scripts/) | Working headless reference scripts (interference gate, BOM audit, review renders — 3 orthos + iso + human scale, parametric ladder example) |
| [reference/bibliography.md](reference/bibliography.md) | Books and standards this kit borrows from (primary sources) |
| [skills/blender-engineering/SKILL.md](skills/blender-engineering/SKILL.md) | Claude Code skill — 4-stage pipeline wiring, engineering-sheet template, gate commands, and docs-to-role index |
| [agents/blender-dossier.md](agents/blender-dossier.md) | Claude Code agent — Stage 0: researches real-world product knowledge and produces a sourced dossier |
| [agents/blender-designer.md](agents/blender-designer.md) | Claude Code agent — Stage 1: generates 3–5 design counter-proposals with tradeoffs; never converges |
| [agents/blender-modeler.md](agents/blender-modeler.md) | Claude Code agent — Stage 3: implements the engineering sheet as a Blender Python script and runs all verification gates |

## Quick start

Read [docs/09-checklists.md](docs/09-checklists.md) first — it is the operational condensation of everything else. Then run the example:

```bash
blender --background --python scripts/example_parametric_ladder.py
blender --background --python scripts/verify_interference.py -- --blend output/ladder_example.blend
```

Scripts target Blender 4.x and use only bundled modules (`bpy`, `bmesh`, `mathutils`) — no add-ons required. The interference and trim techniques were specifically validated headless: `BVHTree.overlap`, boolean `EXACT` intersect volume, and `bmesh.ops.bisect_plane` replace the interference-detection / weldment-trim features of commercial CAD without any add-on.

## Claude Code integration

The kit ships a skill definition and three agent definitions that wire the docs into a role-separated pipeline for Claude Code. The four roles — dossier researcher, design divergence generator, engineering-sheet author (main session), and Blender modeler — each read only the docs relevant to their stage, preventing context overload and keeping dimensional decisions in the judgment layer.

**Install:** copy `skills/blender-engineering/` to `~/.claude/skills/` and `agents/*.md` to `~/.claude/agents/`. Then open each agent file and replace every occurrence of `{{KIT_PATH}}` with the absolute path of your kit clone.

| Stage | Role | Deliverable |
|---|---|---|
| 0 — Dossier | `blender-dossier` agent | `dossier-<product>.md` with sourced dimensions, part census, manufacturing grammar, and modeling risks |
| 1 — Design divergence | `blender-designer` agent | 3–5 counter-proposals with tradeoffs; never converges |
| 2 — Engineering sheet | Main session (judgment layer) | Filled template: PARAMS, datums, BOM, terminal conditions, verification plan |
| 3 — Build & verify | `blender-modeler` agent | Generator script + `.blend` + all three gate commands at exit 0 + PNG renders |

## The five failure classes this kit exists to prevent

1. **No BOM** — modeling "what you can see" and silently omitting rear braces, hinges, cross-members.
2. **No part reuse** — regenerating "the same bar" as a new primitive with slightly different numbers instead of instancing one definition.
3. **Chain placement** — positioning each member relative to the previous one; errors accumulate and parameter changes scatter parts.
4. **Numeric-only verification** — all asserts pass while the render is visibly broken; no multi-view visual check.
5. **No terminal conditions** — member ends left as raw extrusions: burr-like protrusions, coplanar z-fighting, world-axis-aligned feet on inclined rails.

## License

MIT — see [LICENSE](LICENSE).
