# 09 — Checklists

The operational condensation of docs 01–08. Run them in order; each item is mechanical (yes/no).

## A. Before geometry (design)

- [ ] **BOM written** — part × qty × parent × build-method (new / linked duplicate). For modifications: measured scene BOM taken first.
- [ ] **Process tag per part** — sheet / extrusion / casting / machined. Only tag-legal shapes will be built.
- [ ] **Parameter dictionary** — every driving dimension in one dict, each with unit + source comment (standard, measurement, or derivation).
- [ ] **Datums declared** — floor, centerlines, inclined planes as named constants.
- [ ] **Through/trimmed hierarchy declared** — which members are continuous, which trim to them (BOM column).
- [ ] **Ergonomic constants pinned** — rung pitch, seat height, rail height etc. from the canonical tables (doc 03), never guessed.
- [ ] **Derivation policy** — variants regenerate (fixed sections, fixed pitch, change N); no uniform scaling.

## B. During modeling

- [ ] Same part twice ⇒ **shared mesh datablock**, never a new primitive.
- [ ] All placement **closed-form from datums** (`z_i = z0 + i·pitch`); no reads from generated geometry; no recurrences.
- [ ] Scale applied **once at part definition**; never on instances; nothing exported with non-1.0 scale.
- [ ] Every member end has an **explicit terminal condition** (flush trim / miter / chamfer / declared clearance).
- [ ] Mating parts built **in the parent's frame** (`parent.matrix_world @ local_offset`), interface faces cut against their own constraint plane.
- [ ] Joints modeled (rivet boss / bolt head / weld bead); micro-detail (serration, knurl) to textures.
- [ ] Visible edges beveled (~1–3 mm, 2 segments) + auto smooth.
- [ ] Circle segments chosen by camera distance (8/16/32), not default.

## C. Verification (mechanical layer — separate script, fresh artifact read)

- [ ] **BOM audit**: scene scan vs. declared BOM, zero diff.
- [ ] **Dimension asserts**: bounding box & key vertices vs. parameter dictionary.
- [ ] **Interference gate**: all part pairs — BVH overlap, then intersect volume = 0 (union whitelist excepted).
- [ ] **Terminal-condition gate**: mating axes ≤ 0.1°, sole flatness, ground coplanarity < 0.5 mm, zero trimmed-end protrusions, burr census = 0.
- [ ] **Mesh health** on the joined export mesh: no self-intersections, manifold.
- [ ] **Determinism**: build twice, hash-compare.
- [ ] Every claim in the report carries its command + result. Unverified items say "unverified (reason) — will verify at (when)."

## D. Verification (visual layer — mandatory)

- [ ] Three **orthographic renders** (front / side / top), reviewed.
- [ ] **Close-up render of each joint class**, reviewed.
- [ ] **Human-scale render** next to a 1.7 m reference figure, reviewed.
- [ ] Curved/reflective surfaces: **Matcap pass** for highlight breaks.
- [ ] No completion claim before all four are actually looked at. Asserts green ≠ done.

## E. Hand-off (export / deployment)

- [ ] Export mesh: transforms applied, correct axes for the target engine, one final mesh-health pass.
- [ ] Artifact **content** verified against expectations (texture pixel size / hash — not just "file exists").
- [ ] Deployed artifact **hash-compared at every consuming location**.
- [ ] Report: what was done, evidence per claim, what remains unverified and when it will be checked.
