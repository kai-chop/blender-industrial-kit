# Bibliography — Primary Sources

This kit deliberately borrows century-old engineering systems instead of reinventing rules. These are the originals; cite them, don't paraphrase from memory.

## Books

- **Henry Dreyfuss Associates / Alvin R. Tilley — *The Measure of Man and Woman*** (Wiley). Percentile-band anthropometry; the origin of "design for 2.5–97.5%, not the average."
- **Ernst Neufert — *Architects' Data*.** The dimension dictionary for the built environment: doors, ceilings, corridors, furniture. First stop for any human-inhabited prop.
- **Francis D.K. Ching — *Architecture: Form, Space, and Order*.** Column-grid / post-and-beam spatial grammar; proportion and scale.
- **Boothroyd, Dewhurst & Knight — *Product Design for Manufacture and Assembly*.** The DFM canon: process → shape consequences (doc 04's foundation).
- **Gerald Farin — *Curves and Surfaces for CAGD: A Practical Guide*.** Bézier/NURBS mathematics, discretization error, continuity (docs 05's foundation).
- **Pottmann, Asperl, Hofer & Kilian — *Architectural Geometry*.** Freeform discretization and paneling theory.
- **Henry Petroski — *To Engineer Is Human*.** Failure-driven design intuition: stress concentration, safety factors.

## Standards & regulations

- **ISO 14122-3 / 14122-4** — industrial guardrails; fixed ladders (rung pitch 225–300 mm, toe clearance ≥ 200 mm).
- **OSHA 29 CFR 1910.23** — ladder rungs 254–356 mm uniform spacing, ≥ 292 mm clear width; 75.5° (4:1) setup angle.
- **ANSI-ASC A14.2** — portable metal ladders (slip-resistant feet requirement; stepladder geometry).
- **ISO 128** — technical drawing / orthographic multi-view convention (the origin of the multi-view visual gate).
- **ISO 13715** — edge condition callouts (burr permitted/not-permitted; the engineering basis of the burr census).
- **ASME Y14.5** — GD&T; chain vs. baseline dimensioning and tolerance stack-up.
- **JIS S 1010 / S 1011** — desk (700 mm) and chair (seat 400–450 mm) standard heights.
- Building codes (e.g., Japan's Building Standards Act enforcement order art. 23/126) — stair riser/tread limits; 1100 mm fall-protection rails. Substitute your jurisdiction's equivalents; the ergonomic bands are near-universal.
- **Blondel's rule** — 2R + T = 600–660 mm for stair comfort (classical, embedded in most codes).

## CAD-culture references (online, stable)

- Onshape tech tips — *Dos and Don'ts of Parametric Modeling* (design intent, layout sketches).
- FreeCAD wiki — *Topological naming problem* (why generated-geometry references break).
- SolidWorks help — *Interference Detection*; *Weldments Trim and Extend* (through/trimmed member order).
- Blender Manual — *Linked Duplicates*, *Collection Instancing*; Blender Python API — `mathutils.bvhtree`, `bmesh.ops.bisect_plane`, `BMesh.calc_volume`.

## Rule of thumb collections

- ASCE structures-congress rules of thumb for steel (beam depth ≈ span/20 family).
- Sheet-metal DFM guides (bend radius ≥ 1 t, flange ≥ 4 t, holes 2–3 t from bends) — Fiveflute, Xometry, and similar engineering-service guides are consistent with each other.
