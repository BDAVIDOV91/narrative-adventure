---
ticket: "002"
title: What each candidate world can teach through the seven types
status: done
---

# Research 002: what each world can teach through the seven types

Produced by the `astronomy-consultant` agent on 2026-09-25. The main session wrote it here because the agent has no
write tools.

**This is a list of candidates, not design facts** (map Notes, "Sourcing on this map"). A claim enters
`docs/sources.md` when a design ticket adopts it, and that ticket cannot close until `astronomy-accuracy-checker`
has VERIFIED it.

**What "VERIFIED" means below.** The consultant confirmed each source through web-search excerpts of the named page,
not full page fetches. Read VERIFIED as "the source states it, per the excerpt". The checker must fetch each page
before the claim goes into `docs/sources.md`.

**Walls applied:**

- Rule 6: the Sun, planets and major moons only.
- Rule 2: no numbers on screen.
- No folklore beats.
- `gravity-drop` never models mass, and Saturn is excluded from it.
- There is no `rotation` drive.
- No exaggerated orbit ellipse.
- No new data pipeline.

## Two findings every design ticket needs

- **Only `rotate-match` has a config today** (`schemas/level-data.schema.json:61-99`). Its `renderer` enum is
  closed: `sundial`, `day-night`, `seasons-tilt`, `moon-phase`.
  - Every beat below marked "new renderer" is a schema change. That is cheaper than a new type, but not free.
  - The other six types carry `noEngineConfig`.
- **The data window:**
  - `orbital-positions.json` covers 365 days from 2026-09-08.
  - The bodies are Mercury, Venus, Earth, Mars, Jupiter, Saturn and the Moon. The Sun is not a body in the file.
  - There is one sample per day.

## Main-session follow-up

**Earth's seasons wording, checked.** `content/bg/facts.json:4` (`fact.seasons.distance`) says
"Разстоянието почти не се променя" ("the distance barely changes"). That is specific to Earth. It does not claim
distance never matters anywhere, so Mars R8 would *extend* the lesson rather than make the child unlearn it. There is
no defect.

---

## Moon (deep)

### What is actually happening

- **Rotation.** The Moon turns once on its axis per orbit (synchronous rotation). One face always points at us. It
  *does* rotate.
- **Day and night.** Every part of the Moon gets both. The far side is fully lit at new Moon.
- **Phases.** They come from the Sun–Moon–observer angle. Earth's shadow points away from the Sun, so it can reach
  the Moon only at full Moon.
- **Eclipses.** The Moon's orbit is tilted about 5°, so most full Moons miss the shadow. Eclipses cluster in eclipse
  seasons about every six months.
- **Near and far.** The orbit is slightly eccentric. At perigee the Moon looks up to 14% wider than at apogee. The
  repo's data gives perigee 356,779 km and apogee 406,564 km.
- **The horizon Moon.** Its huge look is an illusion; photographs show the same width.
- **Earthshine.** Sunlight bounced off Earth dimly lights the dark part of a crescent.
- **The daytime Moon.** The Moon is in the daytime sky almost as often as the night sky.

### Candidate beats

| #   | Beat | Type | Misconception | Source | Status | Data |
| --- | ---- | ---- | ------------- | ------ | ------ | ---- |
| M1 | **Same face, and it turns.** Drag the Moon around Earth; a marked crater keeps facing Earth, and the renderer turns the Moon to match | `rotate-match` `orbitAngle`; new renderer or a `moon-phase` mode | "The Moon doesn't rotate" | NASA, _Tidal Locking_, <https://science.nasa.gov/moon/tidal-locking/> | VERIFIED | None; pure geometry |
| M2 | **The far side isn't dark.** Same drag, top-down view; the far side is fully lit at new Moon | `rotate-match` `orbitAngle`, `moon-phase` plus a top-down panel | "Dark side of the Moon" | NASA, _Top Moon Questions_, <https://science.nasa.gov/moon/top-moon-questions/>; NASA SVS 14992 | VERIFIED (already `docs/sources.md:64-66`) | None |
| M3 | **Shadow or phase?** Earth's shadow cone drawn; it touches the Moon only at full, never at crescent | `rotate-match` `orbitAngle`, shadow overlay | "Phases are Earth's shadow" (the project's named misconception) | NASA, _Eclipses and the Moon_, <https://science.nasa.gov/moon/eclipses/> | VERIFIED | None |
| M3b | Extension: why there is no eclipse every month | same, side-on tilt view | "Every full Moon is an eclipse" | same, plus NASA SVS 4158 | VERIFIED | Moon ecliptic latitude, derivable from committed RA/Dec (frame note under "Data that does not exist yet") |
| M4 | **Earthshine.** A crescent whose dark part faintly glows | `rotate-match` `orbitAngle` | "The dark part is Earth's shadow" | NASA, _The Da Vinci Glow_ (2005); APOD 2025-04-03 | VERIFIED | None |
| M5 | **Near and far Moon.** Two discs, perigee and apogee; different, but only slightly | `parallax-compare` | "A supermoon is huge" | NASA, _Supermoons_, <https://science.nasa.gov/moon/supermoons/> | VERIFIED | **Exists:** `bodies.moon.distanceAu` |
| M6 | **The horizon Moon is the same size.** Drag a ring over two photos, low and high; it fits both | `parallax-compare` | "The Moon is bigger when it rises" | NASA, _The Moon Illusion_ | VERIFIED; NASA says the cause is unsettled | Real photography only |
| M7 | **The daytime Moon** | `trajectory-match` | "The Moon only comes out at night" | NASA, _Why Can You See the Moon During the Day?_ | VERIFIED | **Partial.** Hourly altitude over Sofia would be new pipeline (barred); a qualitative version needs no data |
| M8 | **Hammer and feather**, the vacuum panel | `gravity-drop` | "Heavy things fall faster" | `docs/sources.md:126-137` (Apollo 15) | VERIFIED | **Exists.** **It repeats Earth's Moon panel:** reuse of the type, but no new lesson |
| M9 | **Seas and craters through the eyepiece.** Maria are lava plains, not water; craters stand out best at the terminator | `telescope-focus` | "The dark patches are seas"; "full Moon is best for viewing" | NASA, _Moon Facts_; the terminator claim needs a Sky & Telescope source | NEEDS SOURCE (both) | Real LRO imagery |

**What the Moon teaches beyond Earth's `moon-phase` beat.** Earth's beat teaches one thing: we see the lit part. The
Moon level adds:

- M1: the Moon turns, locked to its orbit.
- M2: there is no dark side.
- M3 and M4: the shadow is not the phase, which closes the named misconception directly rather than by omission.
- M5 and M6: real versus imagined size change.

M1 to M4 all fit the existing `orbitAngle` drive. M8 repeats Earth and should be optional, if it appears at all.

**Misconception risks:**

- **M1 can backfire.** If the child sees "same face" with no remark, they conclude "it doesn't spin". The fact string
  must say it turns once per trip.
- **M3's shadow** must always point straight away from the Sun. If it sweeps with the drag, it re-teaches the shadow
  model.
- **M5** shows the two discs, never an oval orbit (the eccentricity is about 0.055).

**Do not claim:**

- a "тъмна страна" (dark side);
- that the Moon does not rotate;
- that a supermoon is "huge";
- that the horizon Moon *is* bigger;
- that Earth's shadow causes any phase;
- that the Moon is closer at full Moon;
- any in-window eclipse date. None was verified, and the likely candidates are penumbral.

## Mars (deep)

### What is actually happening

- **Retrograde.** Earth, on its faster inner orbit, overtakes Mars. From Earth, Mars appears to loop backwards against
  the stars. Mars never reverses.
- **The 2027 opposition.**
  - Opposition is 2027-02-19; closest approach is 2027-02-20 at 0.678 AU.
  - It is **aphelic**: a small opposition, with a disc of about 13.8″.
  - Retrograde runs roughly 10 January to 1 April 2027. **NEEDS SOURCE.** Derive the dates from the committed RA
    series, and cross-check against ALPO.
- **Why red.** Iron oxide.
- **Day and year.** A Mars day is about 24.6 h. Its year is nearly two Earth years, so the data window shows about half
  an orbit.
- **Seasons.** The tilt is 25.2°, so Mars has seasons from tilt, but eccentricity also matters: southern summer is
  warmer and shorter.
- **Air.** The atmosphere is thin, mostly CO₂.
- **Phobos** rises in the west.

### Candidate beats

| #   | Beat | Type | Misconception | Source | Status | Data |
| --- | ---- | ---- | ------------- | ------ | ------ | ---- |
| R1 | **Retrograde, two views.** A top-down panel where Earth overtakes Mars, beside a sky-track loop; the child drags time | `trajectory-match` | "Mars really goes backwards" | NASA, _Mars Retrograde_, <https://mars.nasa.gov/all-about-mars/night-sky/retrograde/>; APOD 2014-10-28 | VERIFIED (`docs/sources.md:74-79`) | **Exists:** `helioLonDegrees` for Earth and Mars, plus Mars RA/Dec. The window covers the retrograde |
| R2 | **Mars never looks as big as the Moon.** A Mars disc near and far, beside the Moon for scale | `parallax-compare` | The "Mars as big as the full Moon" hoax | NASA, _Mars Hoax_; JPL Night Sky Network | VERIFIED | **Exists:** `distanceAu`. Radii need a cited reference row |
| R3 | **A real telescope view.** A small orange disc, perhaps a hint of markings | `telescope-focus` | "A telescope shows Mars like the photos" | Sky & Telescope, _An Observer's Guide to Mars_; ALPO, _2026-2027 Aphelic Apparition_ | VERIFIED for the disc and markings. **Polar cap at small aperture is not supported** | Real imagery; disc size from `distanceAu` |
| R4 | **Why red: rust.** Fact string on R3 | none of its own | "Mars is red because it's hot" | NASA, _Mars Facts_ | VERIFIED | None |
| R5 | **A Mars day is almost an Earth day.** Two daylight arcs (reuses day-length-compare) | `parallax-compare` | Surprise | NASA, _Mars Facts_ | VERIFIED | A cited `data/reference/` row |
| R6 | **Blue sunset.** Earth's sunset beside Curiosity's Gale Crater sunset | `parallax-compare` | "Mars sunsets are red" | JPL, _PIA19400_ | VERIFIED. The image is white-balanced, so say "a camera on Mars saw" | Real image, public domain |
| R7 | **Falling on Mars** | `gravity-drop` | "Heavy falls faster" | `docs/sources.md:143-156` | VERIFIED | **Repeats Earth's Mars rung.** **Air-flag trap:** Mars has thin real air, so neither `air: false` nor `air: true` is honest. Show no feather panel on Mars, or cut R7 |
| R8 | **Mars has seasons too, from its tilt** | `rotate-match` `tilt`, `seasons-tilt` reskin | Extends Earth's lesson | NASA, _Helio and You: Seasons on Earth, Mars, and Beyond_ | VERIFIED | None. **High risk:** see below |
| R9 | **Phobos rises in the west**, three times a sol | `trajectory-match`, qualitative | "Every moon rises in the east" | NASA, _Phobos in Orbit around Mars_ | VERIFIED for the west rising. **The page's "only such moon" is DISPUTED** (claim 2 in the false-claims list) | A cited period row. **Is Phobos a major moon under rule 6?** |

**Misconception risks:**

- **R8 is the one to watch.** The honest Mars picture is "tilt, and here distance matters too". Earth's wording
  permits that (see "Main-session follow-up"). Still:
  - Do not draw an oval to make the point.
  - If R8 cannot be done without the eccentricity story, cut it.
- **R1.** The top-down panel must show that Mars keeps moving forward the whole time.
- **R2 and R3.** 2027 is a *small* opposition. Do not dramatise it.

**Do not claim:**

- that Mars reverses or stops;
- that Mars ever looks Moon-sized;
- that a small telescope shows the polar cap;
- that a feather and hammer land together on Mars, or that Mars has no air;
- any Mercury "which pulls harder" comparison;
- retrograde dates, until they are sourced;
- that distance plays no part in Mars's seasons;
- that Phobos is the only fast-orbiting moon.

## Breadth (at most two beats per world)

| World | Candidate beat | Type | Source | Status / data |
| ----- | -------------- | ---- | ------ | ------------- |
| **Sun** | Sun and Moon look almost the same size (the Sun is about 400× bigger and about 400× farther). Hook: a **partial** solar eclipse from Bulgaria on 2027-08-02 | `parallax-compare` | NASA, _Why Do Eclipses Happen?_; timeanddate, Sofia 2027-08-02 | VERIFIED. Earth `helioDistanceAu` exists; radii need a row. **A never-look-at-the-Sun safety string is mandatory**; its source is NEEDS SOURCE |
| Sun | No honest second beat without a solar-safety design | — | — | Never model looking at the Sun through `telescope-focus` |
| **Mercury** | Always near the Sun, only low in twilight | `trajectory-match` | NASA, _Skywatching FAQ_ | VERIFIED. Mercury RA/Dec exists; the Sun's position must be derived (frame trap) |
| Mercury | Closest is not hottest: Venus is hotter | `parallax-compare` | NASA, _Venus Facts_ | VERIFIED. Supports Earth's "distance isn't the whole story" |
| **Venus** | Phases and size: crescent Venus looks bigger (near), full Venus smaller (far). Galileo's evidence | `telescope-focus`, or `rotate-match` with a new `venus-phase` renderer | NASA, _Galileo's Phases of Venus_; APOD 2024-01-08 | VERIFIED. **Exists:** `distanceAu` and `helioLonDegrees`. The inferior-conjunction date is NEEDS SOURCE. Pairs with Зорница as astronomy, not folklore |
| Venus | Venus spins backwards; the Sun rises in the west | `rotate-match`, new renderer | NASA, _Venus Facts_ | VERIFIED. **Not** "a day is longer than a year" (claim 3 in the false-claims list) |
| **Jupiter** | Moons beside a "star": naked eye one point, binoculars up to four dots in a line | `zoom-split-star` | NASA Night Sky Network, _From Galileo to Clipper_ | VERIFIED. See Q1 |
| Jupiter | The moons move night to night | `trajectory-match` | NASA, _Galileo's Observations_ | Periods are NEEDS SOURCE (#20). Nightly positions would need new pipeline, so they are barred; only a schematic version is honest |
| **Saturn** | The rings vanish edge-on about every 15 years, because of Saturn's tilt | `rotate-match` `tilt`, new renderer | APOD 2025-04-29; APOD 2025-11-16 | VERIFIED. Ring opening is not in `data/generated/`; the window shows open rings (−8° to −14°) |
| Saturn | Rings are ice and rock | `telescope-focus` | `docs/sources.md:247-252` | **Already Earth's beat.** Nothing for `gravity-drop` |
| **Uranus** | Tipped on its side: about 21 years of sunlight per pole, then about 21 of dark | `rotate-match` `tilt`, `seasons-tilt` reskin | NASA, _Uranus Facts_ | VERIFIED. No ephemeris needed. **The collision cause is "may be"; never state it as fact** |
| **Neptune** | — | — | — | **No honest beat** |
| **Ganymede** | A moon bigger than the planet Mercury | `parallax-compare` | NASA, _Ganymede Facts_ | VERIFIED. Radii need a row |
| **Titan** | Also bigger than Mercury | fact string on the Ganymede beat | NASA, _Titan Facts_ | VERIFIED. **No `gravity-drop`:** its thick air makes the binary flag dishonest |
| Io, Europa, Callisto, Triton, Enceladus | — | — | — | **No honest beat through the seven types.** Fact strings only, each with its own source |

## Q1. Does `zoom-split-star` have an honest solar-system use?

**Yes, on Jupiter.** The case is moderately strong on the physics, and strong on what a child can actually do.

The ladder mirrors Mizar:

1. Naked eye: one bright point, brighter than any star (`docs/sources.md:265-296`).
2. Binoculars: up to four points in a line.
3. Small telescope: a disc with belts. This rung is already Earth's `telescope-focus` beat.

A Bulgarian child can do rungs 1 and 2 on the evening they play, February to June 2027 (`docs/sources.md:283-285`).
It is also Galileo's 1610 discovery.

**Weaknesses:**

- **The type's name lies.** The dots are moons, not stars. Content must never call them stars.
- **The count varies nightly.** Say "up to four" and show one undated arrangement.
- **No real positions without a pipeline.**
- **It overlaps `telescope-focus` on Jupiter.** For ADR 0006, `zoom-split-star` survives **only if Jupiter is on the
  roster**, and the two may merge there.

**Other solar-system uses are weaker:**

- Saturn with Titan beside it: NEEDS SOURCE.
- The Mars moons are not small-telescope objects.
- The Moon and Venus do not fit.

## Q2. Claims found false or unsupported

Items 1, 4–11 and 13 are recorded in `docs/sources.md` under "Claims ruled out during v1 roster research". Items 2
and 3 are recorded there as DISPUTED. Items 12 and 14 stay here as NEEDS SOURCE.

1. "Mars will look as big as the full Moon": FALSE (NASA _Mars Hoax_).
2. "Phobos is the only moon that orbits faster than its planet spins": the NASA Phobos page says so. Jupiter's
   Metis and Adrastea, Uranus's Cordelia and Neptune's Naiad contradict it. This is from general knowledge, not yet
   sourced; verify against the JPL satellite tables.
3. "A day on Venus is longer than its year": true only for rotation relative to the stars. A sunrise-to-sunrise day is
   about 117 Earth days, *shorter* than the year. The ~117 figure is NEEDS SOURCE.
4. "The Moon doesn't rotate": FALSE (NASA _Tidal Locking_).
5. "The Moon is bigger at the horizon": FALSE; it is an illusion (NASA).
6. "A supermoon is huge": unsupported. It is up to 14% bigger than the smallest Moon, which is hard to notice.
7. "Mercury is the hottest planet": FALSE; Venus is (NASA).
8. "The Sun and Moon are exactly the same size in the sky": FALSE as worded. NASA says "almost exactly", and annular
   eclipses exist because they differ.
9. "A total solar eclipse will be seen from Bulgaria on 2027-08-02": FALSE; it is partial from Bulgaria
   (timeanddate).
10. "A small telescope shows Mars's polar cap": unsupported. It wants a 4–6 inch telescope in excellent seeing
    (Sky & Telescope).
11. "Distance plays no part in seasons, anywhere": FALSE for Mars (NASA _Helio and You_).
12. "Uranus was knocked over by a collision": a hypothesis only ("may be", NASA).
13. "The Galilean moons are visible to the naked eye": unsupported for a child; say binoculars.
14. "Mars's atmosphere is 100× thinner than Earth's": not found on the NASA page checked. NEEDS SOURCE.

## Q3. Data that does not exist yet

- **Uranus and Neptune** are not in `orbital-positions.json`. Uranus's tilt beat needs no ephemeris, and Neptune has
  no beat.
- **The Sun's geocentric position** is not a body in the file. It can be derived as Earth's heliocentric vector plus
  180°.
  - **Frame trap:** `helioLonDegrees` is J2000-ecliptic (`docs/sources.md:183-200`), while `raHours`/`decDegrees`
    are Skyfield `.apparent().radec()`. Declare the frame before mixing the two.
  - This matters for Mercury, the Venus phases, M3b and the Moon's phase angle.
- **Moon phase fraction, Moon ecliptic latitude and Venus phase angle** are not stored. Each is derivable from the
  committed series: a computation, not a pipeline, but still an owner build-time decision.
- **Galilean periods:** NEEDS SOURCE (#20). A cited `data/reference/` row would not be a pipeline. Nightly positions
  would need a satellite ephemeris, which is barred.
- **Saturn's ring opening** was computed once for `docs/sources.md` and never committed.
- **Hourly altitudes for Sofia** (daytime Moon, Mercury in twilight) are absent. The daily samples are too coarse for
  the Moon.
- **Physical constants** are not in the repo, and each would be a cited `data/reference/` row:
  - radii (Sun/Moon, Mars/Moon, Ganymede/Mercury);
  - Mars sol length;
  - Phobos period;
  - Venus rotation;
  - Uranus tilt.
- **Mars 2027 stationary dates** are not sourced. Derive them from the committed RA series and cross-check against
  ALPO.
- **The window limit.** 365 days shows only about half of Mars's orbit, about 30° of Jupiter's and about 12° of
  Saturn's. No beat can show a full orbit of an outer planet from the committed data.

## Forks routed to later tickets

These are open questions for later tickets, not decisions:

- **Is Phobos a "major moon" under rule 6?** It decides R9. Goes to ticket 001.
- **M8 and R7 only repeat Earth's `gravity-drop` rungs.** Does a reuse with no new lesson count for ADR 0006? The
  consultant recommends no. Goes to ticket 005, and it also shapes 003 and 004.
- **`zoom-split-star` survives only if Jupiter is on the roster.** Goes to tickets 001 and 005.
