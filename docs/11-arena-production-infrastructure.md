# 11 — Arena Production Infrastructure: the Part Hung From the Roof

Doc 10 governs the building. But photograph the inside of a modern arena and **most of the frame is
not building** — it is a centre-hung display, a lighting truss rig, ribbon boards and the steelwork
they hang from. Model an arena shell correctly and leave this out, and it reads as an empty hall,
not a venue.

Everything below is sized for *visual plausibility*. Load ratings, hoist capacities and rigging
practice here are descriptive, never a basis for real rigging design.

## The three layers overhead, top to bottom

1. **Roof structure / mother grid** — the building's own steel, plus a rigging grid where the venue
   has one. Fixed.
2. **Centre-hung display** — suspended on cables or hoists from that steel. Semi-fixed: raised and
   lowered between events.
3. **Show rig** — lighting truss on chain motors, hung *below* the centre-hung, at a trim height
   chosen per show. This is the layer that differs between two photos of the same arena.

Getting the stacking order and the gaps right matters more than any single member's section: a
model that puts the lighting truss above the scoreboard reads wrong instantly.

## Truss

Truss is built from **2 in round aluminium chords**, and the chord count names it:

| Chords | Name | Read |
|---|---|---|
| 2 | ladder truss | flat, light, single plane of diagonals |
| 3 | triangle truss | triangular section |
| 4 | box truss | horizontal cross members on top and bottom chords, diagonals on the *sides* |

Standard box sizes are **8″, 10″, 12″, 20.5″ and 30″** square (roughly 200–600 mm), plus
rectangular **20.5″ × 12″** and **30″ × 20.5″**. Typical stock lengths are **5, 8 and 10 ft** with
1 ft filler sections. Diagonals are 1″ OD; sections join with ¾″ steel clevis pins at fork ends.

Duty by size — this is what makes a rig read as the right scale:

- **8″** — small mobile rigs, trade-show accents, short spans. Reaches its limit as soon as moving
  heads or video are added.
- **12″** — stage lighting, small-to-medium platforms, overhead flyswatters.
- **20.5″** — heavier fixture packages and longer spans.
- **30″** — heavy loads, long spans, and vertical towers.

**Sizes mix in one rig, and the mix is legible**: 20.5″ dead-hung from the building steel up top,
12″ hung from motors below it; self-climbing towers of 12″ with 20.5″ spanning between them. A rig
modelled in one uniform size looks like a kit of parts rather than a rig.

## Hoists, points and trim

Chain motors lift and position truss. In arenas, motors attach to the grid by heavy steel rope and
shackles; riggers haul the hook and hardware from the floor up to the beams by rope. Where motors
live permanently, a hard safety takes the load once trim is reached.

**Trim height** — the finished height of a truss above the floor — is per-show data, and venues
require the trim height and the maximum load per point (motor and chain included) on every
submitted plot. Levelling is imperfect in practice: an 8-hoist truss levelled 4 ft off the ground
rarely arrives at 40 ft still level. A rig modelled with millimetre-perfect level is subtly wrong;
a slight variation reads true.

Scale anchor: the Tacoma Dome's flown mother grid — the largest — is **400 ft × 160 ft at 80 ft
trim** above the floor.

## The centre-hung display

Two mounting schemes, and they look different:

- **Static suspension** — cables from the board to the building's structural framework. Nothing
  moves.
- **Electric hoists** — the board is raised and lowered for different event configurations and for
  service, and can be assembled on the floor. Complex boards **split hoisting into zones**: at one
  NBA arena the flame ball, the ring displays, and the main plus underbelly displays sit on three
  separate hoists.

Composition, from the photographs and the vendor literature, is consistent:

- a **crown / top ring** carrying branding,
- the **main four (or more) faces**, often a continuous wrap rather than flat panels,
- an **underbelly** facing straight down at the closest seats,
- an optional **bottom ring**.

Cabinets are die-cast aluminium; against traditional iron cabinets this cuts roof-structure load by
roughly **25 %**, which is why modern boards can be so large. Corners are the giveaway detail:
stock boards show **black bezels at the corners**, and the expensive ones use right-angle modules
for a seamless, bezel-free cube.

Sizes to anchor against:

| Example | Size |
|---|---|
| Crypto.com Arena main wrap | 27 ft high × 170.5 ft circumference |
| United Center | 8,600 sq ft of display |
| Capital One Arena | 7,000 sq ft wrapping all surfaces |
| Kaseya Center underbelly | four displays, 10 ft × 21 ft each |
| Prefabricated centre-hungs | five standard sizes, 8–16 ft wide, self-climbing hoist, adjustable tilt |
| Entry-level four-sided | ~6 ft 2 in × 10 ft 10 in × 10 ft 10 in overall |

## Pixel pitch — why it matters to a modeller

Pitch is **tiered by viewing distance, not uniform across one structure**:

| Surface | Typical pitch |
|---|---|
| Main wrap | 3.9–4 mm |
| Underbelly (closest seats) | 2.5 mm, down to P1.86 |

The modelling consequence is texture budget, not geometry: the underbelly is the surface a close
camera sees, so it is the one that needs real resolution. Everything else can be coarser than
instinct suggests, because in life it *is* coarser.

## Ribbon and fascia

Ribbon boards wrap the balcony fascia as a continuous horizontal band and are normally a **separate
procurement** from the centre-hung — the two are often installed years apart, so they need not match
in pitch, brightness or content. Ring/fascia elements on the centre-hung itself are catalogue
options: top ring, bottom ring, or both.

## Never-list (production infrastructure)

1. Lighting truss modelled above the centre-hung instead of below it.
2. One uniform truss size through a whole rig.
3. Truss with no visible motors, shackles or steel rope reaching the building steel.
4. A centre-hung with no crown, no underbelly and no suspension hardware — a floating box.
5. Perfectly level, perfectly spaced truss everywhere.
6. Ribbon board and centre-hung rendered at the same apparent pixel density.
7. A rigging grid drawn as a flat plane rather than as steel with depth and catwalks.
8. Fixtures modelled as boxes with no yoke or clamp attaching them to the chord.

## Sources

- [What size truss for lighting works best — ProX](https://www.proxdirect.com/blog/2026/06/What-Size-Truss-for-Lighting-Works-Best/)
- [Truss sizes for stage & events — Soundkraft](https://www.soundkraft-me.com/how-wide-is-a-truss-for-lighting/)
- [Box trusses — XSF Truss](https://www.xsftruss.com/box-truss/)
- [Arena installations — XSF Truss](https://www.xsftruss.com/arena-installations/)
- [The grip's ultimate guide to box truss — Legacy Grip](https://www.legacygrip.com/blog/ultimate-grip-guide-to-box-truss)
- [30-inch truss inventory — Gallagher Staging](https://gallagherstaging.com/home-gallagher-staging-and-manufacturing/truss-inventory/30in/)
- [Hanging truss / chain hoist information (PDF) — Freeman](https://www.nacsshow.com/Exhibit/Exhibit-Preparation-and-Booth-Setup/ExhibitorServiceKit/Tab-2_Freeman-Services/Hanging-Truss-Chain-Hoist.pdf)
- [Rigging guidelines and regulations (PDF) — Pennsylvania Convention Center](https://www.paconvention.com/assets/doc/PCC-Rigging-Guidelines-and-Regulations-Updated-December-2020-1a404bc292.pdf)
- [Entertainment rigging — Wikipedia](https://en.wikipedia.org/wiki/Entertainment_rigging)
- [Centerhung scoreboards catalogue — Daktronics](https://pdf.aeroexpo.online/pdf/daktronics-inc/centerhung-scoreboards/177505-4175.html)
- [Centerhung & halo displays — Watchfire](https://www.watchfiresigns.com/led-signs/centerhungs/)
- [Capital One Arena center-hung scoreboard — ALSD](https://alsd.com/content/capital-one-arena-center-hung-scoreboard)
- [Miami Heat LED torch centre-hung — Sixteen:Nine](https://www.sixteen-nine.net/2024/09/23/nbas-miami-heat-incorporates-giant-led-torch-inside-its-new-center-hung-scoreboard-at-home-arena/)
- [Crypto.com Arena centre-hung upgrade — Daktronics via StockTitan](https://stocktitan.net/news/DAKT/crypto-com-arena-brings-big-center-hung-scoreboard-upgrade-to-games-lhheiolmvmcw.html)

**Not established by these sources** — cabinet/module granularity (whether a given board is built
from 500 × 500 mm or 320 × 160 mm modules), truss depths for the centre-hung's own internal frame,
and hoist capacity ratings. Manufacturer cut sheets are needed for those; do not infer them.
