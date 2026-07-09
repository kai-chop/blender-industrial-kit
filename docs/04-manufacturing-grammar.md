# 04 — Manufacturing Grammar: Process Determines Shape

The source of "industrial-looking": **a manufacturing process can only produce certain shapes.** Model the shape the process would have made (DFM literature — Boothroyd/Dewhurst/Knight — is the primary source). Before modeling any part, assign it a **process tag**; then only build shapes that tag allows.

## Process → shape vocabulary

### Sheet metal (tag: `sheet`)
- Uniform thickness everywhere — a "sheet metal" part whose wall thickness varies is impossible.
- Formed by bends only; inner bend radius ≥ 1 × thickness (2–3 t for hard alloys).
- Flanges ≥ 4 t; holes stay 2–3 t away from bend lines.
- Vocabulary: constant thickness, identical bend radii throughout, cutouts and hems, spot-weld marks.
- Blender: Solidify modifier for constant thickness; all bends share one radius.

### Extrusion (tag: `extrusion`)
- Constant cross-section along the full length. **No bumps or features along the length** — only the ends may be machined/punched.
- Cross-section can be elaborate: hollow, ribs, screw bosses, C-channels — all encoded in the profile.
- Vocabulary: long uniform members (ladder rails, window frames, heat sinks).
- Blender: build the profile curve once, extrude along the axis. One extrusion per part, uniform section — this also makes trims and miters clean.

### Casting (tag: `casting`)
- Draft angles (sand 1–3°, die-cast 0.5–2°), uniform wall thickness, generous fillets everywhere, a parting line.
- Vocabulary: organic-ish blended shapes with visible parting lines (tool bodies, brackets, machine bases).

### Machining (tag: `machined`)
- Prismatic/rotational features, sharp-ish internal corners limited by tool radius, chamfered entries.
- Modern CNC specifics: **internal corners always carry a radius = tool radius** (a sharp internal pocket corner is unmanufacturable on a mill — model the radius or the corner reads as fake). Pocket depth ≲ 4 × tool diameter; undercuts imply 5-axis or a second setup, so most parts show only 3-axis-reachable features.

### Injection molding (tag: `molded`)
The dominant grammar of modern consumer products (tool housings, ladder feet, chair shells, casings):
- **Uniform wall thickness 1–3 mm** — thick solid regions sink and warp, so "solid-looking" plastic parts are actually shells with **ribs** underneath (rib thickness ≈ 50–60 % of wall, to hide sink marks).
- Draft 0.5–2° on faces along the pull direction; **bosses** around screw holes; visible **parting line**, ejector-pin circles, and a gate scar on hidden faces.
- Joint vocabulary of its own: **snap-fits and living hinges** instead of fasteners — two molded parts clip together with no visible screws on the A-side.
- Blender: model the outer shell at wall thickness (Solidify), add rib lattices on the inside only where a close-up shows them; parting line as a faint edge loop.

### Additive / 3D printing (tag: `printed`)
The one modern process whose grammar is *organic*, and the reason many current parts look nothing like century-old ones:
- Legal shapes: internal lattices, conformal channels, **topology-optimized "bone-like" forms** — material only along load paths (Bendsøe & Sigmund; generative-design tools automate this). No draft, no uniform-wall constraint.
- Its own constraints instead: **~45° overhang rule** (steeper needs support, leaving witness marks), minimum feature ≈ 0.8 mm (FDM), visible **layer stratification** along one build axis (a texture/normal-map detail, oriented consistently).
- The discipline still applies: an organic printed bracket is *not* an arbitrary blob — its ribs follow force flow between mounting points. Organic shape without load-path logic is the modern version of box-modeling grammar.

## Choose the grammar by era and price point

A prop's process mix dates it: mid-century industrial = sheet + casting + rivets; current consumer = molded shells + snap-fits + a few printed or machined accents; structural/heavy = extrusion + weld, unchanged for a century. Mixing eras on one product (a cast-iron body with living hinges) reads as wrong even to viewers who can't say why.

## Joints are parts too

Parts touching with no visible joining method is toy grammar. Real assemblies show **how** parts attach:

- **Rivet / swage**: circular boss and flare where a ladder rung passes through the rail — model the boss.
- **Bolt/nut**: hex heads at brackets and hinges (a low-poly hex cylinder is enough; normal-map fine detail).
- **Weld**: fillet bead at structural steel junctions (a small bevel/rounding along the seam reads as a weld).
- Fine surface detail (grip serrations, knurling) goes to textures/normal maps, not geometry.

## Worked example: an aluminum stepladder

| Part | Process tag | Shape consequence |
|---|---|---|
| Side rails | extrusion | C-channel profile, flanges inward, constant along length |
| Rungs/steps | extrusion | D-shaped or rectangular profile, serrated top face (texture) |
| Rung-to-rail joint | swage/rivet | circular flare boss on the rail face at each rung |
| Top plate | casting or sheet | uniform thickness + fillets, or folded sheet with hems |
| Feet | molded caps | fitted to the rail profile, **oriented along the rail axis**, only the tread face meets the floor |
| Rung spacing | (standard) | ~300 mm uniform (ANSI A14.2 / OSHA) |

The anti-pattern this table kills: assembling a ladder from unrelated boxes ("box-modeling grammar"). Four consecutive failed ladder builds traced back to exactly that — parts generated ad hoc, without a process tag, without a BOM, positioned by chained ratios.

## Structural proportion (frames, trusses, venues)

For architectural-scale members, section size has a canonical relationship to span (steel rules of thumb, e.g. ASCE guidance):

- Beam depth ≈ span / 20 as a first approximation (steel simple beams L/15–L/20; continuous L/20–L/30; RC L/12–L/15).
- Beam width ≈ 0.35–0.67 × depth.
- Lay the column grid first (uniform spacing), size beams from span, then detail.

A member whose thickness has no span-derived justification will look wrong — too thin reads as fragile, too thick reads as toy. Leave a one-line comment deriving each section from its span.
