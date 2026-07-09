# 03 — Ergonomics: Canonical Dimensions

Humans are the fixed reference every prop is judged against. Replace "eyeballed" numbers with canonical values from standards and the classic anthropometry literature (Dreyfuss *The Measure of Man and Woman*, Neufert *Architects' Data*, ISO/OSHA/JIS standards — see bibliography).

## Anthropometric quick rules (from stature H)

| Landmark | Ratio | Example (H = 1.70 m) |
|---|---|---|
| Eye height | 0.93 H | 1.58 m |
| Shoulder height | 0.81 H | 1.38 m |
| Overhead fingertip reach | 1.25 H | 2.13 m |
| Forward reach | 0.44 H | 0.75 m |
| Hip (waist) height | ≈0.55 H | 0.94 m |

Design principle (Dreyfuss): design for the **2.5th–97.5th percentile band**, not the average — "must reach it" sizes to the small end, "must fit through it" sizes to the large end.

**Modern data note**: anthropometry drifts (the *secular trend* — populations have grown several cm since the mid-century surveys behind Dreyfuss/Neufert). The current reference dataset is **ANSUR II (2012, publicly available)**; use it when a dimension is percentile-critical. The *ratios* above are stable; the absolute stature you plug in should match your target population/era.

**Practice**: keep a 1.7 m reference figure (even a simple capsule) permanently in the scene and render every prop next to it. Most scale errors are invisible on an isolated model and obvious next to a human. This is the manual form of **Digital Human Modeling** (RAMSIS / Jack / Santos — industry now validates reach, sightlines, and clearance against posed digital manikins *before* any prototype exists). Upgrade path when a prop is interaction-critical: pose a rigged figure actually grasping the handle / standing on the rung, instead of just standing beside it.

## Ladders (climbing equipment)

| Dimension | Canonical value | Source |
|---|---|---|
| Rung pitch | **250–300 mm, uniform** | ISO 14122-4: 225–300; OSHA 1910.23: 254–356 |
| Rung diameter/section | 20–35 mm | ISO 14122-4 |
| Rung clear length | ≥ 292 mm (rail inner width 300–400 mm typical) | OSHA |
| Toe clearance behind rung | ≥ 200 mm | ISO 14122-4 |
| Leaning-ladder setup angle | 75.5° (4:1 rule) | OSHA |
| Stepladder front-rail angle | ~66–75° | ANSI A14.2 practice |

**The single most important rule**: rung pitch does **not** scale with ladder length. It is bounded by leg articulation. A tall ladder = same pitch, more rungs.

## Tables & chairs

| Dimension | Canonical value |
|---|---|
| Desk/table top height | 700 mm (±20) |
| Tabletop thickness | 25–40 mm (over ~100 mm reads as a stone slab) |
| Folding event table | 1800 × 450–600 mm, H 700 mm |
| Chair seat height | 400–450 mm |
| Top-to-seat differential | 270–300 mm |
| Leg sections | wood 40–70 mm square / steel tube 25–40 mm dia. |
| Counter height | 850–1000 mm |

Sanity check: next to the 1.7 m figure, a table top must sit clearly **below the hip line (~0.94 m)**. A "breakable" prop table should use thin (15–20 mm) top stock — thick tops don't look breakable.

## Stairs & handrails

| Dimension | Canonical value |
|---|---|
| Comfortable stair | riser 180–200 mm, tread 210–240 mm |
| Blondel's rule | 2 × riser + tread = 600–660 mm (ideal ≈ 630) — assert this in script |
| Assembly-hall stairs | riser ≤ 180, tread ≥ 260 |
| Fall-protection guard (balcony, platform) | ≥ 1100 mm |
| Graspable stair handrail | 750–850 mm |
| Crowd barrier / guardrail | ~1000–1100 mm (waist to solar plexus) |
| Door | ~2000 × 750–900 mm |
| Ceiling | 2400 mm+ |

## Grip & foothold (the "can be grabbed / stepped on" test)

| Dimension | Canonical value |
|---|---|
| Power-grip handle diameter | 30–50 mm (optimum ≈ 38) |
| Handrail circular section | 32–51 mm (comfort 34–38) |
| Hand clearance behind a handle | ≥ 45 mm (fist pass-through ≥ 110 mm) |
| Foothold depth | ≥ 150 mm |

Anything a character grabs should be a 25–40 mm cylinder; above ~50 mm it reads as structure, not grip. Handles need real modeled clearance behind them — a flat plate with a normal-mapped "handle" breaks the moment a character lifts it.

## Failure classes this table prevents

- Correct in isolation, giant/miniature next to a character (implicit scale drift via texture density or UV convenience).
- Long ladders with proportionally stretched rungs — "unclimbable at a glance."
- Guardrails at knee height; tables at chest height; handles that a hand cannot close around or reach behind.
