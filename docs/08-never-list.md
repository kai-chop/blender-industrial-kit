# 08 — The Never List

Defects that must **never reach human review**. Each entry is phrased as the reviewer experiences it, because that is the standard the work is judged by. A human looking at an industrial product applies a lifetime of calibration on real (deburred, ergonomic, process-correct) objects — they will spot these in seconds, and each one burns trust and a review round-trip.

## Geometry

1. **Burr-like protrusions** — any unnamed sliver of one part poking 0–1 mm through another's surface. Reads as manufacturing garbage. (Gate: burr census, doc 06.)
2. **Coplanar face z-fighting** — two parts sharing a face without being unioned. Flickers in every engine. (Gate: interference + declared-union whitelist.)
3. **World-axis-aligned parts on inclined parents** — feet, caps, brackets that ignore the member they attach to. Instantly visible. (Gate: mating-axis check.)
4. **Wobble** — ground contacts not coplanar. A ladder or table that would rock. (Gate: multi-foot coplanarity < 0.5 mm.)
5. **Missing parts the reference clearly has** — rear braces, hinges, cross-members. Only visible parts got modeled. (Gate: BOM audit.)
6. **Razor-sharp edges everywhere** — mathematically sharp edges catch no highlight; the whole object reads as cheap CG. (Gate: bevel pass, doc 05.)

## Proportion & scale

7. **Uniformly scaled variants** — the tall version with thick rails and stretched rung spacing. Reads as a toy blow-up. (Rule: regenerate with fixed sections and fixed pitch, doc 01.)
8. **Ergonomic impossibilities** — rungs a leg can't span, handles a hand can't close on, guardrails at knee height, tables at chest height. (Gate: canonical tables, doc 03; render next to reference figure.)
9. **Process-impossible shapes** — "sheet metal" with varying wall thickness, an "extrusion" with bumps along its length, parts touching with no visible joint. (Rule: process tags, doc 04.)

## Physics & curves

10. **Hand-drawn hanging ropes/chains** — Bézier guesses instead of catenary. Physically false at a glance. (Rule: evaluate `cosh`, doc 05.)

## Process (how work is reported)

11. **"Done" without evidence** — completion claims with no executed check attached. Every claim ships with the command that proves it and its result.
12. **Single-view confidence** — declaring the model correct from one render (or zero renders, from asserts alone). Three orthos + joint close-up + human-scale shot, every time.
13. **Generator self-verification** — the build script grading its own output. Independent script, fresh read of the artifact, expected-value comparison.
14. **Exit-0-as-proof** — treating "the tool ran without error" as "the content is right."
15. **Silent substitution of the requested verification** — if the reviewer asked to check X in a specific way, do exactly that; substituting an "equivalent" easier check is how defects ship. If a check was skipped, say "unverified (reason)" and state when it will be verified — never let it float.
16. **Unlabeled assumptions** — writing an expectation ("this should bind texture A") as if it were a verified fact. If it can be checked with one command, check it; otherwise label it *assumption*.

## Why the process items are on a geometry list

Every geometry defect above shipped, at least once, *because* of a process defect below it: the missing brace passed because nobody diffed a BOM; the broken render passed because asserts were the only gate; the wrong texture shipped because "file exists" stood in for "content matches." The never-list is one list.
