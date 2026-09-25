---
ticket: "006"
title: Jupiter level design: the claims the design adopts, and their sources
status: done
---

# Research 006: Jupiter claims and their sources

Drafted by the main session on 2026-09-25 from research 007 (search-excerpt level): one row per player-facing fact,
nudge, completion line and load-bearing visual, widened after two `challenger` reviews. It is a hand-off to `astronomy-accuracy-checker`, which reads each page
in full and records the status in `docs/sources.md`. **Nothing here is VERIFIED until that happens.**

| #   | Claim | Where | Source | Wording guard |
| --- | ----- | ----- | ------ | ------------- |
| 1 | Through binoculars, Jupiter shows up to four of its moons as small dots in a line beside it | J1 rung 2; J2 | NASA Night Sky Network, _From Galileo to Clipper_ <https://science.nasa.gov/solar-system/skywatching/night-sky-network/octobers-night-sky-notes-from-galileo-to-clipper-exploring-jupiters-moons> | "Up to four", never "four". Binoculars, never the naked eye (NOT ATTESTED). Never "stars". Undated, schematic |
| 2 | Jupiter is a huge ball of gas; a small telescope shows it as a small disc with dark cloud belts, when the air is steady (the whole of `fact.telescope-jupiter`) | J1 rung 3 + fact | `docs/sources.md` "Through a small telescope — what a child will actually see" (S&T, _Jupiter Is Outstanding at Opposition_; NASA _Jupiter Facts_). The "ball of gas" and "steady air" clauses need their own quote | Small and shimmering, not a Hubble poster. No aperture. Rung 2 (binoculars) shows no belts |
| 3 | The Great Red Spot is faint and pale in a small telescope, and is on view only while Jupiter's spin turns it toward us | J1 nudge; J1 and J7 art | S&T, _Jupiter's Not-So-Great Red Spot_ <https://skyandtelescope.org/astronomy-news/observing-news/jupiters-great-red-spot/>; S&T, _Transit Times of Jupiter's Great Red Spot_ <https://skyandtelescope.org/observing/interactive-sky-watching-tools/transit-times-of-jupiters-great-red-spot/> | Pale, never poster-red. **No size** ("twice Earth" is DISPUTED) |
| 4 | Io, Europa, Ganymede and Callisto circle Jupiter, each at its own pace: the closer ones faster. Their orbit sizes and Jupiter's radius set the drawing at true relative scale | J2 motion and layout | NASA _Io Facts_, _Europa Facts_, _Ganymede Facts_, _Callisto Facts_ (URLs in research 007); Jupiter radius from NASA _Jupiter Facts_. Re-statuses `docs/sources.md` "Jupiter's Galilean moons" (#20) for a schematic, undated use, stored as cited `data/reference/` rows | No periods, radii or dates on screen. Target line-up generated from the model. Callisto not drawn locked to the others' rhythm |
| 5 | We see the moons' orbits almost edge-on, so the moons appear strung along a line through Jupiter | J2 fact; the edge-on strip | **NEEDS SOURCE** (standard geometry; research 007 found no page stating it) | If unsourced: show the geometry, never state it in words |
| 6 | Galileo saw these four moons move around Jupiter, which showed that not everything circles Earth | J2 fact | **To source** (NSN _From Galileo to Clipper_ is a candidate) | "Showed", never "first proof" unless the page says it. No year on screen. If unsourced: drop the Galileo clause |
| 7 | Sometimes fewer than four show, because a moon can pass behind Jupiter or in front of it | J2 nudge; J2 strip shows one passing behind | **NEEDS SOURCE** (`docs/sources.md` "Jupiter myths" marks the mechanism so). Candidates: NSN (as 1), S&T | If unsourced: the nudge says only "up to four" and the strip shows no hiding. A moon in front is never drawn as a bright dot over the disc |
| 8 | Ganymede is the largest moon in the Solar System, and it is wider than the planet Mercury | J3 fact + nudge; J3 discs | NASA _Ganymede Facts_ <https://science.nasa.gov/jupiter/jupiter-moons/ganymede/facts/>; NASA _Mercury Facts_ <https://science.nasa.gov/mercury/facts/> (radii for the drawing) | „по-широк" or „по-голям на ръст", never heavier (NOT ATTESTED). The ~8% margin is drawn true |
| 9 | Planets shine only by reflected sunlight and look bright because they are far closer (`fact.brightest-why`) | J4 fact | `docs/sources.md` "The brightest "star" in the evening sky is usually a planet" | Carry "reflected" and "near" |
| 9a | The brightest "star" in the evening can be a planet: Jupiter outshines Sirius, the brightest true star (trimmed from `fact.brightest-is-a-planet`, without Venus) | J4 nudge (new key) | Same entry: the ordering is unconditional | No Venus. No magnitudes |
| 10 | Jupiter and Sirius are both in the Bulgarian evening sky, February to April 2027, about 50° apart | J4 scene | Same entry (computed for Sofia; not committed); separation from `orbital-positions.json#/bodies/jupiter` and `stars.json` | Never "beside" or „до Сириус". A wide view at the true separation. No date on screen. Declare the frames: apparent RA/Dec for Jupiter, catalogue epoch for Sirius. The binocular peek on Jupiter reuses claim 1 |
| 11 | Jupiter spins faster than any other planet: it has the shortest day | J7 fact | NASA _Jupiter Facts_ <https://science.nasa.gov/jupiter/jupiter-facts/> | No hours on screen |
| 12 | While Earth turns once, Jupiter turns more than twice, and both turn the same way | J7 coupled globes; a round = one Earth turn | NASA _Jupiter Facts_ (about 10 h) and an Earth rotation source; ratio about 2.4 | No hour marks. The ratio is drawn, never stated. Earth at true relative size, or in a separate inset. The J7 close-up is real imagery framed as seen up close; never bleached |
| 13 | Jupiter's fast spin helps stretch its clouds into long bands | J7 nudge | **NEEDS SOURCE**: no `docs/sources.md` line has ever stated it. Candidate: NASA _Jupiter Facts_, fetched in full | If unsourced: the nudge says only "Jupiter's clouds lie in long stripes" (VERIFIED). Never "the spin paints the stripes" |
| 14 | Jupiter pulls much harder than Earth | Completion line: a new key (e.g. `fact.jupiter.complete`), shown when the gate is met; `fact.gravity-drop.bodies` is deleted | `docs/sources.md` "Surface gravity per body" (NSSDC via Wayback; 1-bar row) | Only „дърпа" or „притегля". Never falls, lands, stands or weighs, and no surface |
| 15 | Ganymede and Mercury as J3 draws them (radii, and real imagery) | J3 discs | NASA _Ganymede Facts_, NASA _Mercury Facts_ | Discs from cited radius rows; imagery public-domain, never AI |

## Verification — `astronomy-accuracy-checker`, 2026-09-25

**Method: full page.** Each source was downloaded, stripped to text and searched for the supporting sentence. No
status below rests on a search excerpt. Quotes, values and exact URLs are in `docs/sources.md`, "Jupiter level — the
claims ticket 006 adopts". Sky & Telescope returns 403 to scripts, so every S&T page was read as a dated Wayback
snapshot. The NSSDC fact sheets are live again (HTTP 200) and are cited live.

| #   | Verifier status | Page that carries it (read in full) |
| --- | --------------- | ----------------------------------- |
| 1 | VERIFIED | NSN _From Galileo to Clipper_: „with a pair of binoculars … a line of smaller dots on one or both sides"; S&T _How to See Jupiter: Big, Bright, and Beautiful_ (Wayback 2024-07-16): „a line of three or four tiny stars" at ≥7× |
| 2 | VERIFIED, all clauses | Ball of gas: S&T _Big, Bright_ „a gas giant planet — … almost entirely of hydrogen and helium, nearly all the way down"; NASA _Jupiter Facts_ „doesn't have a true surface". Steady air: S&T _Jupiter Is Outstanding at Opposition_ (Wayback 2025-12-07) „nights of calm and steady seeing when the planet sits rock-steady and sharp". Belts: S&T _Not-So-Great Red Spot_ „two main cloud belts appear in most any backyard setup" |
| 3 | VERIFIED, **reworded** | S&T _Transit Times of the GRS_ (Wayback 2026-01-06): „generally … a much less conspicuous pale tan", „surprisingly difficult to see", well placed „for 50 minutes before and after" transit; S&T _Big, Bright_: „a challenge in a small telescope". Say „often pale", not „faint and pale": S&T 2019 found it „orange-red" and easy at 100× |
| 4 | VERIFIED | NASA _Europa Facts_ (1:2:4 resonance), _Ganymede Facts_ (7.155 d), _Callisto Facts_ (16.689 d; 1.8/2.8/4.5× farther), _Io Facts_ (422,000 km, no period); values from NSSDC _Jovian Satellite Fact Sheet_; Jupiter radius NASA _Jupiter Facts_ 69,911 km (mean) / NSSDC 71,492 km (equatorial — draw with this) |
| 5 | VERIFIED (was NEEDS SOURCE) | S&T _Big, Bright_: „We see their orbits almost exactly edge on", same passage as the „line"; NASA _Europa Facts_: „the orbital plane of its moons" |
| 6 | VERIFIED, **reworded** | NASA _Io Facts_ and _Ganymede Facts_: „the first time a moon was discovered orbiting a planet other than Earth" … „eventually led to the understanding that planets … orbit the Sun"; NSN: Galileo „chronicled the four moving dots … and surmised that they were orbiting" |
| 7 | VERIFIED (was NEEDS SOURCE) | S&T _Big, Bright_: „possibly only three … they sometimes glide in front of the planet, behind it, or through its shadow"; S&T _Outstanding at Opposition_: „one or other often pass in front or behind the planet" |
| 8 | VERIFIED | NASA _Ganymede Facts_: „the largest moon in our solar system, bigger than the planet Mercury"; „5,260 kilometers"; NASA _Mercury Facts_: radius „2,440 kilometers". Ratio 1.079 (NSSDC 5,262 / 4,879 km) |
| 9 | VERIFIED | Univ. of Illinois Physics Van, _Light From Planets and Stars_: „They do not produce their own light … reflected from the sun"; „look as bright or brighter than most stars because they are much closer to us" |
| 9a | VERIFIED | Existing `docs/sources.md` entry; NSSDC _Jupiter Fact Sheet_ re-read (max −2.94, mean −2.7); Sirius −1.44 in `stars.json` |
| 10 | VERIFIED (computed), **guard corrected** | Separation 54.0° (Feb 1) → 50.4° (Apr 15) from committed data. Both well up at dusk from late Feb to mid-Apr (Jupiter 2.7° at dusk on Feb 1). Committed Jupiter RA/Dec match JPL Horizons **astrometric ICRF** to 0.0004 h / 0.002° — so both bodies are already ICRS; not "apparent vs catalogue epoch" |
| 11 | VERIFIED | NASA _Jupiter Facts_: „Jupiter has the shortest day in the solar system"; S&T _Big, Bright_: „Among the planets, Jupiter has the fastest spin" |
| 12 | VERIFIED | NSSDC _Jupiter Fact Sheet_: sidereal rotation 9.9250 h vs Earth 23.9345 h (ratio 2.41); NASA _Earth Facts_ 23.9 h. Same direction: NSSDC _Planetary Fact Sheet_ both positive + _Notes_: „Negative numbers indicate retrograde … rotation" |
| 13 | VERIFIED (was NEEDS SOURCE) | NASA _Jupiter Facts_: „Jupiter's fast rotation … creates strong jet streams, separating its clouds into dark belts and bright zones across long stretches" (same page: how the jets form is still „a mystery") |
| 14 | VERIFIED | NSSDC _Jupiter Fact Sheet_ (live): gravity 25.92 vs 9.82 m/s² (2.64×); NASA _Jupiter Facts_: no true surface |
| 15 | VERIFIED | NSSDC _Jovian Satellite Fact Sheet_ (Ganymede radius 2631.2 km); NSSDC _Planetary Fact Sheet_ (Mercury diameter 4,879 km) |

**Wording corrections the reads force.**

- **3**: „often pale and hard to see in a small telescope". Its colour varies by season, and S&T found it orange-red
  in 2019, so never an unconditional „faint and pale". The two S&T pages give different sizes („twice the size of
  Earth" and „about 1.3 Earths"), which confirms the existing DISPUTED size entry.
- **6**: Galileo *saw the dots move and worked out* that they circle Jupiter (NSN „surmised"), not „saw them move
  around Jupiter". Never „proved Earth goes round the Sun": NASA says only „eventually led to".
- **7**: the source names a third cause, Jupiter's shadow. "Behind or in front" is true, but never say those are the
  only reasons.
- **10**: the frame guard is wrong as written. The committed positions and Sirius are both ICRS, so do not convert
  one of them to of-date coordinates.
- **4**: cite NSSDC for the periods, not the JPL SSD mean-element „P" column. That column gives Io and Europa periods
  0.4% and 0.7% off. Draw the planet with the 71,492 km equatorial radius, because NSSDC's R_J column uses it.
- **2**: „кълбо от газ" may ship, but never "gas all the way to the centre". NASA says the interior is gases *and*
  liquids.

No claim in this file stays NEEDS SOURCE, and none was found false.
