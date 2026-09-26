---
ticket: "011"
title: Saturn level design: the claims the design adopts, and their sources
status: done
---

# Research 011: Saturn claims and their sources

Drafted by the main session on 2026-09-26 from research 010 (search-excerpt level): one row per player-facing fact,
nudge, completion line and load-bearing visual of the design ticket 011 settled. It is a hand-off to
`astronomy-accuracy-checker`, which reads each page in full and records the status in `docs/sources.md`. **Nothing here
is VERIFIED until that happens.**

| #   | Claim | Where | Source | Wording guard |
| --- | ----- | ----- | ------ | ------------- |
| 1 | Saturn's axis is tilted and keeps pointing the same way in space as Saturn goes round the Sun; the rings lie around its equator, so they share that tilt | S1 model (oblique orbit view): fixed axis arrow, ring plane; S1 fact „не се накланят“ | NASA/JPL _A Change of Seasons on Saturn_ (PIA03156) <https://science.nasa.gov/resource/a-change-of-seasons-on-saturn/>; NASA _Saturn Facts_ <https://science.nasa.gov/saturn/facts/> | The rings never tip, tilt, wobble or flip (NOT ATTESTED). Never "the rings never moved" or "you moved": the rings travel with Saturn. Never `drives: tilt`; the renderer is `ring-view`. Circular orbit. No angle on screen |
| 2 | Over one trip round the Sun we see the rings from above, then edge-on, then from below, then edge-on again, because our viewpoint moves, not the rings | S1 three rounds (the solve compares the view, so both edge-on positions count) | As 1; In-The-Sky _Equinox on Saturn_ <https://in-the-sky.org/news.php?id=20250506_12_100>; Obliquity _Ring Plane Crossings of Saturn_ <https://www.obliquity.com/skyeye/misc/ringcrossing.html> | "Twice each trip round the Sun", never "every 15 years" (NOT ATTESTED). Never quote NASA's "the ring system changes angle". Earth sits almost at the Sun at this scale; the model views from the Sun's side |
| 3 | Edge-on, the rings shrink to a thin line that is hard to see; they do not disappear | S1 thin-line target | ESA/Hubble opo9525c <https://esahubble.org/images/opo9525c/>; NASA _Hubble Views Saturn Ring-Plane Crossing_ <https://science.nasa.gov/missions/hubble/hubble-views-saturn-ring-plane-crossing/> | Never "vanish" or „изчезват" (NOT ATTESTED). The thin line is drawn, never an empty Saturn. No thickness (DISPUTED) |
| 4 | In 2026–27 Earth sees the south face of the rings, narrowly open | S1 start position and inset; cross-level: Earth's `fact.telescope-saturn` art | `docs/sources.md` "Through a small telescope" one-off computation (de440s + IAU pole), to be re-run monthly across 2026-09-08 → 2027-09-07 and recorded | Never "opening a little more every month" (NEEDS SOURCE until the monthly table exists). Undated on screen |
| 5 | Of the five planets we can see without a telescope, Saturn is the slowest: it creeps among the stars far more slowly than Mars | S2: two panels at one angular scale, Nov 2026 – May 2027 | EarthSky _Give me 5 minutes and I'll give you Saturn_ <https://earthsky.org/astronomy-essentials/give-me-five-minutes-ill-give-you-saturn/>; committed RA/Dec in `data/generated/orbital-positions.json` | Anchor to the VERIFIED five-planet row in `docs/sources.md` (Uranus is not in the five). Never „най-бавната планета“ unqualified. Frame: apparent RA/Dec against catalogue-epoch stars, as J4. No constellation-years figure. The small backward bit is not re-explained (R1a covers it) |
| 6 | Saturn is far from the Sun, so one trip round the Sun takes it a very long time | S2 fact | NASA _Saturn Facts_ | No years on screen. "Far, so a long trip", never a speed number |
| 7 | For a few weeks in spring 2027 Saturn is too close to the Sun in our sky to see | S2 gap in the dots | `docs/sources.md` (Saturn within 15° of the Sun, 2027-03-22 → 04-25) | The gap reads as hidden in the Sun's glare, never "Saturn stopped". No dates on screen |
| 8 | Titan is Saturn's largest moon, and it is wider than our Moon | S3 discs at one true scale; S3 fact | NASA _Titan Facts_ <https://science.nasa.gov/saturn/moons/titan/facts/>; NASA _Earth's Moon_ facts (radius) | Never "the largest moon" (FALSE: Ganymede) or "heavier". Drawn true (about 1.5×), never stated |
| 9 | Titan has a thick atmosphere, and its haze hides the ground in ordinary (visible) light | S3 haze disc; S3 fact | NASA _Titan Facts_ | "Thick" (плътна) is required (NOT ATTESTED without it). Never an absolute "we cannot see its ground": infrared shows it. The orange colour is a spacecraft view, never promised in a small telescope |
| 10 | The Cassini spacecraft saw Titan's surface through the haze in infrared light | S3 reveal (a labelled Cassini infrared frame) | NASA _Titan Facts_; the chosen Cassini VIMS PIA page | Labelled a spacecraft camera view, never "what your eyes would see". Imagery public-domain, degraded honestly, never AI |
| 11 | Our Moon shows craters when you look closer | S3 Moon disc | `docs/sources.md` Moon rows (ticket 003, M9) | Telescope-like, not a poster |
| 12 | Saturn's rings are not a solid disc: each piece goes round Saturn on its own | S4 fact ("countless pieces" is recalled from Earth's `fact.telescope-saturn`, not restated) | NASA _Saturn Facts_ (ring composition); Keeler 1895 <https://articles.adsabs.harvard.edu/pdf/1895ApJ.....1..416K> | Never "the rings spin" or "turn like a record". No piece sizes |
| 13 | The inner pieces go round faster than the outer ones | S4 motion and target line-up (speeds computed at build time from row 18); S4 nudge | **NEEDS SOURCE**: Keeler 1895 (ApJ 1, 416) is primary; a NASA page stating it is wanted | Speeds drawn, never stated. The target is generated from the model. **If unverified, S4 drops and the level runs 3 of 3** |
| 14 | Saturn's tilt gives it seasons, just as Earth's tilt gives Earth seasons | Completion line (new key) | NASA/JPL PIA03156 | "Like Earth", never "only because of the tilt" ("distance plays no part anywhere" is NOT ATTESTED). No season length |
| 15 | Seen from Earth, even through a telescope, Titan is only a dot; every Titan close-up (the haze disc and the infrared view) is a spacecraft picture | S3 "look closer" framing | S&T _Viewing Saturn_ <https://skyandtelescope.org/stargazing-and-observing/celestial-objects-to-watch/viewing-saturn-the-planet-rings-and-moons/>; NASA _Titan Facts_ | Label every close-up as a spacecraft view. Fights "a bigger telescope shows everything" |
| 16 | Titan's orange haze colour, as drawn | S3 Titan disc | Cassini ISS natural-colour frame (PIA number to pick) | A spacecraft view, never promised in a small telescope |
| 17 | The Moon's and Titan's radii, as drawn at one true scale | S3 discs | NASA/NSSDC _Moon Fact Sheet_; NASA _Titan Facts_ or the NSSDC _Saturnian Satellite Fact Sheet_ | Cited `data/reference/` rows. The ratio is drawn, never stated |
| 18 | The inner and outer ring radii that set S4's relative speeds (inner C ring, B ring, outer A-ring edge) | S4 schematic | NSSDC _Saturnian Rings Fact Sheet_ <https://nssdc.gsfc.nasa.gov/planetary/factsheet/satringfact.html> | Cited `data/reference/` row. Speeds computed at build time from the orbit rule (row 13). No numbers on screen |
| 19 | The Cassini visible and infrared Titan frames: public domain or licensed, with credit | S3 imagery | The chosen PIA pages (VIMS frames may carry a University of Arizona credit) | Through `process-textures.py`, max 2048px WebP. Degraded honestly. Never AI |

## Verification — astronomy-accuracy-checker, 2026-09-26

**Method: full page.** Each source was downloaded, stripped to text and searched for the supporting sentence. No
status below rests on a search excerpt. Quotes, values and exact URLs are in `docs/sources.md`, "Saturn level — the
claims ticket 011 adopts". Sky & Telescope (403), In-The-Sky (bot wall) and Britannica (403) were read as dated
Wayback snapshots. The NSSDC fact sheets are live. Committed Saturn RA/Dec/distance were spot-checked against JPL
Horizons (agreement within 0.0003 h, 0.003°, 1e-5 AU).

| #   | Verifier status | Page that carries it (read in full) |
| --- | --------------- | ----------------------------------- |
| 1 | VERIFIED | PIA03156 „first one hemisphere, then the other is tilted towards the Sun"; NASA _Saturn Facts_ 26.73°; IAU pole (NAIF `pck00011.tpc`) drifts about 0.001° per Saturn orbit; Obliquity „the rings are in the equatorial plane"; In-The-Sky „closely aligned with its equator" |
| 2 | VERIFIED | In-The-Sky _Equinox on Saturn_ (Wayback 2026-04-21) „arises twice within each orbit"; Obliquity „twice a Saturnian year … single … or triple"; Britannica Kids (Wayback 2026-08-20) north side ~15 years, then south |
| 3 | VERIFIED, **reworded** | In-The-Sky „so thin as to be incredibly hard to see"; NASA _Hubble Views … Ring-Plane Crossing_ „thinner and … more difficult to see", backyard telescope „sometimes invisible"; ESA opo9525c (image only) |
| 4 | VERIFIED (computed) | Monthly table from committed data + IAU pole: −8.3° (2026-09) → −6.1° (2026-12) → −14.4° (2027-08), south face throughout; EarthSky „-7.5-degree tilt around opposition" (computed −7.46°); Obliquity 2025 crossing „North → South" |
| 5 | VERIFIED, **guard added** | EarthSky _Give me 5 minutes_ „moves more slowly than the other bright planets in front of the fixed stars"; committed data Nov 2026 – May 2027: Saturn 17.4° path, Mars 57.8° |
| 6 | VERIFIED | NASA Space Place _How Long is a Year on Other Planets?_ „farther from the Sun … longer years" (two reasons: longer path, weaker pull); NASA _Saturn Facts_ 9.5 AU, 29.4 years |
| 7 | VERIFIED | In-The-Sky _Saturn at solar conjunction_ (Wayback 2026-03-23) „totally unobservable for several weeks while it is lost in the Sun's glare"; Horizons elongation < 15° 2027-03-22 → 04-25, exactly as committed |
| 8 | VERIFIED | NASA _Titan Facts_ „second largest moon … Only … Ganymede is larger, by just 2 percent. Titan is bigger than Earth's moon" |
| 9 | VERIFIED, **reworded** | NASA _Titan Facts_ „the only moon with a thick atmosphere"; „makes the moon's surface difficult to view from space"; PIA21923 „aerosols … strongly scatter visible light" |
| 10 | VERIFIED | PIA20016 „A view at visible wavelengths … would show only Titan's hazy atmosphere … near-infrared wavelengths … penetrate the haze and reveal the moon's surface" |
| 11 | VERIFIED | NASA _Moon Viewing Tips_ „with binoculars … resolve into craters and large mountain ridges" (upgrades the Moon row's search-excerpt status) |
| 12 | VERIFIED | Keeler 1895 „an immense multitude of comparatively small bodies, revolving around Saturn … a solid or fluid ring could not exist"; NASA _Saturn Facts_ „billions of small chunks" |
| 13 | **VERIFIED** (was NEEDS SOURCE) | Keeler 1895, ApJ 1, 416 (ADS PDF): „the velocity of the inner edge of Saturn's ring exceeds the velocity of the outer edge … satisfy Kepler's third law"; NASA _Cassini: Saturn Rings_ „particles nearer Saturn move faster … those farther from Saturn move slower"; NASA _Ripples from Daphnis_ „inner edge … orbits faster … outer edge moves slower" |
| 14 | VERIFIED | PIA03156 „causes seasons on Saturn, just as the changing orientation of Earth's tilt causes seasons on our planet"; NASA _Saturn Facts_ „like Earth, Saturn experiences seasons" |
| 15 | VERIFIED (computed), **reworded** | S&T _Viewing Saturn_ (Wayback 2026-08-13) „A 2-inch scope will show Titan"; BBC Sky at Night „not actually looking at Titan's surface"; Titan 0.68″–0.84″ (NSSDC radius, committed distance) vs 1.9″ Dawes limit at 60 mm |
| 16 | VERIFIED | **PIA06230** (ISS wide-angle, natural colour): „approximately what Titan would look like to the human eye: a hazy orange globe". Credit „NASA/JPL/Space Science Institute". Alternate PIA14602 („NASA/JPL-Caltech/Space Science Institute") |
| 17 | VERIFIED | NSSDC _Saturnian Satellite Fact Sheet_ Titan 2,575 km; NSSDC _Moon Fact Sheet_ 1,737.4 km (mean); ratio 1.482 = _Titan Facts_ „nearly 50 percent wider" |
| 18 | VERIFIED | NSSDC _Saturnian Rings Fact Sheet_: C inner 74,658 km, B 91,975–117,507 km, A outer 136,780 km; Kepler speeds relative to A outer 1.354 / 1.220 / 1.079 / 1.000 |
| 19 | VERIFIED | **PIA20016** (VIMS, T-114): credit „NASA/JPL/University of Arizona/University of Idaho"; PIA06230 as in 16. No copyright mark on either page; JPL _Image Use Policy_ „may be used for any purpose"; NASA media guidelines „generally are not subject to copyright … NASA should be acknowledged" |

**Wording corrections the reads force.**

- **3**: the rings are still there, but a small telescope may not show them at all (NASA: „sometimes invisible").
  „Не изчезват" may only mean "they are still there". Never "you can still see them" or "a telescope always shows
  the line". The line is drawn in the model inset, which is a diagram and not a telescope view. The cited ESA and
  NASA Hubble pages both say „every 15 years" and must not be copied.
- **5 (HIGH, new guard)**: across Nov 2026 – May 2027, **Jupiter moves no more than Saturn** (16.0° path and 4.1° net,
  against Saturn's 17.4° and 14.6°), because it loops round its February opposition. S2 compares Saturn with **Mars
  only**. A Jupiter panel would contradict the lesson on screen.
- **9**: the haze hides the ground **seen from above / from space**. The Huygens probe descended beneath it (_Titan
  Facts_). Never an unqualified "no one has seen the ground in ordinary light".
- **15**: "through a **small** telescope Titan is only a dot", not "even through a telescope". _Titan Facts_ says
  „Spacecraft and telescopes can … see through the haze" in infrared. Never "only spacecraft can see Titan's ground".
  The claim that holds is "the close-ups in this game are spacecraft pictures".
- **19**: PIA20016 is **false colour** (1.3 / 2.0 / 5.0 µm mapped to blue / green / red). Label it as an infrared camera
  picture, so no child takes its colours for Titan's ground.
- **1, 14 (source line)**: PIA03156 is a **Hubble Heritage** image („NASA and The Hubble Heritage Team (STScI/AURA)"),
  not NASA/JPL. Its caption has neither "changes angle" nor a ring thickness. Both misattributions are corrected in
  `docs/sources.md`: the myth row now quotes „nod majestically", and the thickness row now cites _Saturn Facts_ and
  NSSDC. The ring thickness stays DISPUTED.
- **4 (for the owner)**: the monthly table shows the rings **narrowing** from September to early December 2026 before
  they open. The "open a little more every month" myth row was left NEEDS SOURCE, as instructed. The table is the
  evidence against it.

**Verdict on S4: claim 13 is VERIFIED** from Keeler's primary paper and two NASA pages, so S4 stays. No claim in
this file stays NEEDS SOURCE, and none was found false. No new NOT ATTESTED entry was needed: the one false reading
("rings open steadily") was already on the myths list.
