# 10 — Architectural Structure: What Makes a Building Read as Built

Doc 04 governs objects you can pick up: process determines shape. At building scale a different
logic takes over — **a structure is a chain of members carrying load to the ground, and every
visible thing is either part of that chain or hangs off it.** A venue modelled without that chain
reads as a stage set even when every surface is beautiful, and viewers who cannot name the fault
still feel it.

Everything below is sized for *visual plausibility*, not for engineering. Rules of thumb tell you
what a real member looks like; they do not make a building stand up. Sources are listed per
section, and anything the sources themselves flagged as unverified is marked here too.

## The hierarchy — three levels, and members never skip one

Real framing is strictly ranked, and each level spans between the level above it:

| Level | Members | Spans between |
|---|---|---|
| Primary | columns, main trusses, girders, arches | foundations |
| Secondary | beams, joists, purlins, rafters | primary members |
| Tertiary | decking, cladding rails, sag rods, diagonal wire braces | secondary members |

A purlin is supported by the primary member; tertiary elements then *stabilise* the secondary ones.
The commonest fake tell is a member that skips a level — deck landing straight on a main truss, or
cladding spanning 20 m with nothing behind it. Roof sheeting normally sits on **no more than two
layers** of structure.

Model the hierarchy explicitly: it is also your LOD hierarchy, because primary members are what a
distant silhouette is made of.

## Load path — every load reaches the ground

A building splits into a **load-bearing structure** and a **non-load-bearing structure** (curtains,
ceilings, partitions: they cover the frame and subdivide space, they carry nothing). The load-bearing
part splits again into the gravity system and the lateral system.

Failures that read instantly as fake:

- A column that stops in mid-air with nothing transferring its load sideways.
- A truss whose end lands on cladding, glazing or a partition.
- A cantilever with no back-span or counterweight behind its support.

## Lateral stability — the most-missed system

Gravity framing alone is not a building. Every real structure carries a **lateral load resisting
system** for wind and seismic force, and it is usually visible:

- **Braced frames** — X, K or chevron diagonals in specific bays (this is what you see in arenas,
  warehouses and stair cores).
- **Moment frames** — no diagonals, but haunches and stiffeners bulk out the beam-column joints.
- **Shear walls / cores** — solid concrete around lifts and stairs.

Horizontally, floor and roof **diaphragms act like large simply supported beams spanning between
the vertical systems**. Where bracing resists only lateral force and carries no gravity load beyond
its own weight, it is classed as secondary structure.

One nuance worth modelling: bracing is direction-specific. Under gravity the upper flange between
primary members goes into compression; an outward wind load puts the *lower* flange in compression,
so a brace arranged for one case does not brace the other. That is why real roof bracing runs
diagonally through the webs of the secondary members rather than sitting neatly on top.

**If a venue model has columns and beams but no braced bays, no core and no diaphragm, it is a
diagram of a building, not a building.**

## Preliminary sizing — span-to-depth

Choose `d = L / (target L/d)`. Continuous members take roughly **0.85 ×** the simple-span depth.

| Element | Span / depth | Practical max span |
|---|---|---|
| Primary beams | 10–15 | 12 m |
| Secondary beams | 15–25 | 10 m |
| Steel floor joist | 17 | 6–9 m |
| Plate girder | 10–12 | 25 m |
| Castellated UB | 14–17 | 12–20 m |
| Roof truss (pitch > 20°) | 14–15 | 17 m |
| Simple-span roof beam | 15 | 25 m |
| Simple-span rafter | 24 | 30 m |
| Space frame | 15–30 | 100 m |
| Portal frame leg | 35–40 | 60 m |
| RC beam | 12–15 (width 0.35–0.67 × depth) | — |
| RC one-way slab | 30 (roof 36) | — |
| RC flat plate | 36 | 12–24 ft |
| Waffle slab | 24 | 24–54 ft |

Steel I-sections tolerate far higher L/h than concrete — 18–30 and up — because of steel's
stiffness; the American shorthand is about ½ inch of depth per foot of span (L/d ≈ 24).

A member whose section has no span-derived justification looks wrong: too thin reads fragile, too
thick reads toy. Leave a one-line comment deriving each section from its span.

## Long-span roofs — the arena case

Trusses run **span/10 to span/15** for efficiency; across load intensities the band widens to
10–25. A shallower truss means lower shear-member volume but higher chord forces — that trade-off
is why arena trusses are deep.

Primary trusses are spaced at roughly **¼ to ⅕ of their span**.

Worked real example (AISC *Modern Steel Construction*): four primary arena roof trusses spanning
**406 ft**, Warren configuration with W14 chords and webs, depth varying **21 ft 6 in → 44 ft** —
that is span/19 at the shallow end and **span/9** at the deep end.

At arena scale the truss depth is often set by what has to live *inside* the truss envelope —
catwalks, rigging beams, MEP, fall-protection — as much as by structural efficiency. Model the roof
as an inhabited zone, not a lid. Rigging grids inside the trusses are often assembled at trim
height rather than on the floor, and where a catwalk shares space with non-parallel trusses the
result is full of corners, stairs and turns; that awkwardness is what makes it look real.

Catwalk runs of 20–100 ft, 20–50 ft above the floor, with grid capacities around 100–120 kip, are
reported in the trade press — **treat these figures as unverified** (the sources were a wiki-style
page and a vendor blog); check ANSI E1.2 / E1.21 before relying on them.

## The seating bowl

The bowl is the primary design generator: everything else aligns to it.

**C-value** is the vertical distance between a spectator's sight line to the focal point and the eye
level of the person one row in front — measured at the *front* person's eye, on the *rear* person's
sight line.

| C-value | Quality |
|---|---|
| 60 mm | bare minimum; works only if the row in front sits still |
| 90 mm | comfortable standard |
| 120 mm+ | clear view even when the row in front stands (premium / safe standing) |

UK Green Guide §12.3: `C = (D(N + R) / (D + T)) − R`, where D is horizontal distance to the focal
point, R the eye height above the focal plane, N the riser, T the tread. In practice C is fixed and
you solve for N per row — which is why **holding a constant C-value bends the seating profile into
a curve**, typically from about a 300 mm riser at the front to over 450 mm at the back. A bowl
modelled with one constant riser is the giveaway that no sightline was ever considered.

Working dimensions: seat width 460–500 mm general, 500–600 mm premium; tread 750–800 mm standard,
850–950 mm with gangway comfort; rake steeper than **34°** is considered uncomfortable and induces
vertigo (Pickard 2002); UEFA optimum C is 90–120 mm, minimum 60 mm.

## Junctions and finishes — the "処理" layer

Up close, a building is its connections. AISC classifies **architecturally exposed structural steel
(AESS)** by viewing distance, and the category decides how much detail is worth modelling:

| Category | Meaning |
|---|---|
| AESS 1 | basic elements |
| AESS 2 | feature elements viewed **beyond 6 m / 20 ft** |
| AESS 3 | feature elements viewed **within 6 m / 20 ft** — weld seams less visible and consistently located |
| AESS 4 | showcase elements |
| AESS C | custom |

Two design intents: **tectonic** (shows the assembly, favours bolted connections) and **plastic**
(the assembly is smoothed away). Pick one per venue and hold it — mixing them looks like an accident.

What to actually model at close range: base plates with anchor bolts, gusset plates at brace ends,
splice plates along long members, haunches and stiffeners at moment joints. Members meeting with no
connection detail is the close-range equivalent of a column that stops in mid-air.

Coatings change the silhouette, so they are geometry, not just material:

- **Intumescent** fire protection keeps the slender profile but needs precise thickness; too thick
  gives a heavy orange-peel texture. A thick coat also *hides* imperfections — real projects have
  relaxed connection grinding because of it. There is no agreed appearance standard for intumescent
  finish on AESS.
- **Sprayed cementitious** fireproofing is lumpy and obscures the section entirely — a completely
  different read.
- Corrosion: galvanizing, metallization, stainless, weathering steel. Blast cleaning removes mill
  scale first; a high-gloss finish shows every flaw.

Mill marks and butt/plug welds leave raised or depressed surfaces and are removed from view in
AESS 3 by grinding or filling. AESS carries a real cost premium — roughly 25 % over standard steel
for simple work, 50 % for an office atrium, over 100 % for high-end airport structures — which is
why it appears only where people stand close.

## Movement, services and the things that hang off structure

- Long buildings need **movement joints**; a continuous facade running hundreds of metres with no
  joint is wrong.
- Cladding hangs off the frame and its panel joints align to the structural grid; mullions do not
  wander independently of columns.
- In arenas the underside of the roof is **visibly serviced** — ducts, conduit, sprinkler mains,
  house lighting and projectors mounted to catwalks. Where lighting mounts directly to a catwalk,
  rigid stability governs, which is why those catwalks are stiffer and more braced than a walkway
  needs to be.

## Never-list (building scale)

1. Columns and beams with no lateral system anywhere.
2. A member that skips a hierarchy level.
3. A load that never reaches the ground.
4. Uniform riser height through a seating bowl.
5. A roof modelled as a lid with nothing inside it.
6. Members meeting with no connection detail inside 6 m of the camera.
7. Sections whose depth has no relationship to their span.
8. A facade hundreds of metres long with no movement joint.
9. Cladding spanning further than any member behind it.
10. Tectonic and plastic AESS intent mixed in one venue.

## Checklist

- [ ] Column grid laid out first, uniform, before any member is sized.
- [ ] Each member's depth derived from its span, with the derivation in a comment.
- [ ] A lateral system identified and modelled (braced bays / moment joints / core).
- [ ] Every column and truss traced to a foundation.
- [ ] Roof truss depth from span/10–15, and the catwalk / rigging zone modelled inside it.
- [ ] Bowl risers varying to hold a constant C-value, with the C target recorded.
- [ ] AESS category chosen from actual camera distance; connections modelled to match.
- [ ] Coating type chosen, and its effect on silhouette applied.

## Sources

- [Span-to-depth rules of thumb — Eng-Tips FAQ](https://www.eng-tips.com/forums/507/faqs/1574)
- [Span to depth ratio of slabs and beams — Sheer Force Engineering](https://sheerforceeng.com/2021/11/26/span-to-depth-ratio-of-slabs-and-beams/)
- [Span-Depth Ratios for preliminary structural design of steel beams — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0141029625018954)
- [Thumb rules for RC beam design — theconstructor.org](https://theconstructor.org/practical-guide/assumptions-specifications-design-reinforced-concrete-beam/233721/)
- [Lateral stability of building structures](https://www.slideshare.net/slideshow/lateral-stability-of-building-structures-58620763/58620763)
- [Steel construction with trusses — New Steel Construction](https://www.newsteelconstruction.com/wp/steel-construction-with-trusses/)
- [Large trusses provide a wide-open venue — AISC Modern Steel Construction](https://www.aisc.org/globalassets/modern-steel/archives/2010/03/2010v03_rave_review.pdf)
- [Stadium seating layout and sightlines — JMR InfraSolutions](https://jmrinfrasolutions.com/blog/stadium-seating-layout-and-sightlines/)
- [Stadium seating bowl with Dynamo — Parametric Monkey](https://parametricmonkey.com/2017/10/23/seating-bowl/)
- [How to design a stadium — Archgyan](https://archgyan.com/how-to-design-a-stadium/)
- [Categorized by Design: Architecturally Exposed Structural Steel — AISC / BNP Media](https://continuingeducation.bnpmedia.com/architect/courses/american-institute-of-steel-construction/categorized-by-design-architecturally-exposed-structural-steel/4/)
- [Architecturally Exposed Structural Steel: Specifications, Connections, Details](https://dokumen.pub/architecturally-exposed-structural-steel-specifications-connections-details-9783038214830-9783038215745.html)
- [Finish standard for intumescent coatings on AESS — Sherwin-Williams](https://industrial.sherwin-williams.com/na/us/en/protective-marine/media-center/articles/finish-standard-intumescent-cellulosic-fire-protection-aess.html)
- [Intumescent steel protection — Hilti](https://www.hilti.com/content/hilti/W1/US/en/business/business/engineering/fire-protection/intumescent-steel-protection.html)

Primary canon this doc only summarises: UK Green Guide §12.3, UEFA Guide to Quality Stadiums (2011),
Pickard (2002), AISC Steel Construction Manual, ASCE 7, ANSI E1.2 / E1.21, Schodek *Structures*.
