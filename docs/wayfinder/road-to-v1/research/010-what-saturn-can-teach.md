---
ticket: "010"
title: What Saturn can teach, deep
status: done
---

# Research 010: what Saturn can teach, deep

The `astronomy-consultant` agent produced this on 2026-09-26 as a deep pass on Saturn, roster page 5 (open, 0.7, conditional under ticket 009 Q17). The main session wrote it here because the agent has no write tools. It follows the format of research 007.

**These are candidates, not design facts.** A claim enters `docs/sources.md` only when ticket 011 adopts it, and only after `astronomy-accuracy-checker` has VERIFIED it.

**What "VERIFIED" means here.** A context-mode hook blocked `WebFetch` in this session, so **no external page was fetched**. Every VERIFIED below rests on one of two things:

- a search-engine excerpt attributed to the named URL, which may be lightly paraphrased;
- a row already in `docs/sources.md`, which carries its own provenance.

Read it as "the source states it, per the excerpt". The checker must fetch each page.

**Walls applied:**

- Rule 2 (hide the math).
- No folklore beats.
- No new pipeline.
- Five kept types only (`zoom-split-star` and `gravity-drop` are deleted).
- Saturn is absent from any drop or pull comparison (`docs/sources.md:248-253`).
- There is no `rotation` drive (`schemas/level-data.schema.json:71-74`).
- No exaggerated ellipse.
- Rings only in a telescope frame (`docs/sources.md:424-431`).
- No repeat of `fact.telescope-saturn` (`content/bg/facts.json:21`).
- Titan gets no page of its own.

## Saturn (deep)

### What is actually happening

- **A gas giant with no surface.** Saturn is mostly hydrogen and helium. Its surface-gravity figures depend on which column you read, and there is no ground to fall to (`docs/sources.md:245-253`).
- **Its axis is tilted about 26.7° and keeps pointing the same way in space as Saturn goes round the Sun.**
  - One orbit takes about 29.5 years.
  - The rings lie in Saturn's equatorial plane, so they share that fixed tilt.
  - As Saturn goes round, the Sun (and Earth, which is almost at the Sun at this scale) sees the rings:
    - first from the north side;
    - then edge-on;
    - then from the south side;
    - then edge-on again.
  - **That is the same geometry that gives Saturn its seasons.** When the rings are edge-on to the Sun, it is equinox on Saturn. NASA/JPL _PIA03156_ says the tilt causes seasons "just as Earth's changing orientation causes seasons on our planet", with a 27° tilt against Earth's 23°. Each season lasts more than seven years (NASA _Saturn Facts_ excerpt).
- **The rings do not tip. Our viewpoint moves.** This is the core physical fact, and the easiest to get wrong. NASA's own caption ("the ring system changes angle majestically") is loose phrasing that invites the wrong model.
- **The edge-on events are uneven.**
  - Recent crossings were in 1995–96, 2009 and 2025. The next is a triple crossing: 2038-10-15, 2039-04-01 and 2039-07-09 (In-The-Sky; obliquity.com).
  - Saturn's orbit is slightly eccentric, so the gaps alternate at about 13.7 and 15.7 years. "Every 15 years" is only an average.
- **The 2025 crossing, precisely.**
  - Earth crossed the ring plane on **2025-03-23**. The Sun crossed it (Saturn's equinox) on **2025-05-06** (In-The-Sky).
  - Since then Earth sees the **south face** of the rings. The long-term trend is **opening**, toward the widest view around **2032**, when Saturn's south pole is tipped most toward us.
  - `docs/sources.md:344-348` records a one-off de440s + IAU-pole computation: **−8.3° (2026-09)** and **−14.1° (2027-09)**, validated at +0.04° on 2025-03-23.
- **The opening does not grow steadily inside the window.** Earth's own orbit adds a yearly wobble of a few degrees.
  - After the March 2025 crossing, the rings closed again to about 0.37° (south face) on 2025-11-23 (AAQ excerpt).
  - A smaller dip is likely around and after the 2026-10-04 opposition. One excerpt gives about 7.5° at opposition, against −8.3° in September; that source is low-grade.
  - **So "the rings open a little more every month" is not established for the window.** Over the whole window they end wider than they start, and the long-term direction is opening.
- **The rings are very thin compared with their width.** That is why they nearly vanish edge-on.
  - Sources disagree on the thickness: "about 10 m" (NASA PIA03156 excerpt) against "10 m to 1 km" in other excerpts. **Quote no number.**
  - Edge-on, the rings shrink to a thin line (ESA/Hubble opo9525c). They are hard to see in a small telescope, but they do not literally cease to exist.
- **The rings are a swarm, not a disc.**
  - Each piece orbits Saturn on its own, and inner pieces go round faster than outer ones.
  - Keeler showed this in 1895 by spectroscopy, confirming Maxwell's theory (RASC; EARTH Magazine; Keeler 1895, ApJ 1, 416).
  - It is the same rule as J2's moons: the closer, the faster.
- **Slow in the sky.** Saturn is the slowest naked-eye planet and spends about 2.5–3 years in each zodiac constellation (EarthSky excerpt).
  - Saturn's opposition is 2026-10-04/05 (`docs/sources.md:115`).
  - The window starts inside Saturn's retrograde stretch. The stationary dates are NEEDS SOURCE.
  - Saturn is within 15° of the Sun from 2027-03-22 to 2027-04-25 (`docs/sources.md:417`).
  - Its ecliptic latitude is −2.72° to −2.23° across the window (`docs/sources.md:476-477`).
- **Naked eye.**
  - Saturn is a steady, modest point that is always fainter than Sirius (peak +0.43; `docs/sources.md:365-368`).
  - The rings and Titan need optics.
- **Titan.**
  - It is 5,150 km across, "slightly larger than Mercury" but about half Mercury's mass. It is second in size to Ganymede, by about 2%.
  - It is "the only moon with a thick atmosphere", mostly nitrogen, with surface pressure about 60% above Earth's (NASA _Titan Facts_ excerpt).
  - Its haze hides the surface in visible light. Cassini saw through it in infrared and by radar.
  - "A 60-mm scope will usually reveal the giant moon Titan" (S&T excerpt). This closes research 002's "Saturn with Titan beside it: NEEDS SOURCE" (`research/002…:206`) for a schematic use, once the checker fetches the page.
- **Shape.** Saturn is the most oblate planet: its polar diameter is about 10% shorter than its equatorial one (excerpts; NASA/NSSDC to confirm). "Noticeable in a small telescope" appears only in amateur-guide excerpts, so it is **NEEDS SOURCE**, the same status as Jupiter's J8.
- **The hexagon** sits at the **north** pole. While Earth sees the south face (the whole window), the north pole is tipped away from us. It is never a small-telescope sight.

### Candidate beats

The "Status" column covers the claim. "Types" gives the type, then → the fallback type.

| # | Beat (the child's noticing moment) | Types / config | Req? | Misconception fought | Source | Status | Data |
|---|---|---|---|---|---|---|---|
| S1 | **The rings "come and go" (spine).** Top-down: Saturn on a **circular** orbit, its axis and ring plane drawn as a fixed arrow. A "what we see" inset shows the ring view. The child drags Saturn round the Sun to match three target views: open from above, a thin line, open from below. Payoff: "the rings never moved; you did". Then the link: "the same tilt gives Saturn seasons, like Earth" | `rotate-match`, **`drives: orbitAngle`**, new renderer (e.g. `ring-tilt`), pinned to `orbitAngle` like `moon-phase` (`schema:88-96`) → `trajectory-match` (drag time; top-down plus view strip) | **Required** | "The rings tip up and down"; "the rings disappear / break"; seasons from distance | NASA/JPL _PIA03156_; In-The-Sky crossing and equinox pages; APOD 2025-04-29 and 2025-11-16 (research 002:175); `docs/sources.md:344-348` | VERIFIED (excerpt) for the geometry, tilt and seasons link. The window's ring state is VERIFIED by a one-off computation | **Not in `data/generated/`.** A cited `data/reference/` row: obliquity 26.73° (NSSDC Saturn sheet, Wayback-dated) and the IAU pole (Archinal et al. 2018, WGCCRE), with the 2025-03-23 crossing as an anchor. Saturn's "you are here" marker comes from the existing `bodies.saturn.helioLonDegrees`. The inset opening for the window is the **monthly** one-off computation, recorded in `sources.md` |
| S2 | **The slowest wanderer.** Connect Saturn's dots over the window on the real star map, beside Mars's trail from the same months. Saturn's is a short creep, with a gap where it hides near the Sun. Fact: it is far away and takes a very long time to go round | `connect-the-dots` (reuses R1a) → `trajectory-match` (outer slow circle against Earth's) | **Required** | "All planets move across the sky alike"; "planets move fast like the Moon" | NASA _Saturn Facts_ (year length); EarthSky (slowest naked-eye planet) | VERIFIED (excerpt). Stationary dates: NEEDS SOURCE, but none is shown | **Exists:** Saturn and Mars `raHours`/`decDegrees`; stars from `stars.json`. Declare the frame (apparent RA/Dec against catalogue-epoch stars; the J4 note applies) |
| S3 | **The moon wrapped in fog.** Two discs at one true scale: our Moon, showing its face, and Titan, a smooth orange ball. The child "looks closer" on each. The Moon shows craters; Titan shows only haze. Reveal: an infrared view through the haze. Fact: Titan is Saturn's big moon, and its air is so thick we cannot see the ground | `parallax-compare` (two visuals, judge) → fact string | **Required** | "Moons have no air"; "a bigger telescope shows everything" | NASA _Titan Facts_ | VERIFIED (excerpt) | A radii row (Moon, Titan). Imagery: Cassini ISS visible-light and VIMS infrared Titan (public domain, PIA numbers to pick), degraded honestly |
| S4 | **The rings are a swarm.** Watch pieces of ring go round. Choose the motion that matches, "all turn together like a record" or "the inner pieces overtake the outer". Ties back to J2 | `trajectory-match` → fact string on S1 | Optional; required only if the owner wants choice at 0.7 (see Verdict) | "The rings are a solid disc" | Keeler 1895 (ApJ 1, 416); RASC; EARTH Magazine | **NEEDS SOURCE**: a NASA or primary page stating that the inner rings orbit faster. The history is VERIFIED by excerpt only | A schematic, relative speeds only. Needs an orbit-speed rule row |
| S5 | **Saturn's own ladder.** Eye: a modest point. Small telescope: a narrowly open ring, a flattened ball and a dot (Titan) | `telescope-focus` → `parallax-compare` | Optional | "Saturn looks like the poster" | `docs/sources.md:330-334`; S&T (Titan) | Rings VERIFIED. Titan VERIFIED (excerpt). Flattened disc NEEDS SOURCE | Real imagery. **Overlaps Earth's beat**, so it is not required |
| S6 | Fainter than Sirius and Jupiter | `parallax-compare` → fact string | **Out** | Risk of "faint means far" | `docs/sources.md:365-368` | VERIFIED as a fact; unsafe as a lesson | Keep only as the back-cover line |
| S7 | Density ("would float") | none | **Out** | — | see false claim 1 | NOT ATTESTED as a scene | Needs mass over volume, which is math |
| S8 | Hexagon | fact string at most | **Out** | "A telescope shows the hexagon" | Cassini imagery | Unsourced as a sight | — |
| S9 | Fast spin, and seasons by tilt as a standalone `seasons-tilt` beat | — | **Out** | — | — | Repeats J7 and Earth; S1 carries the seasons link as extend-not-repeat | — |
| S10 | Enceladus | — | **Out** | — | — | About 500 km, not a "major" moon under a conservative rule 6 reading | — |

### Misconception risks

- **S1 is the one that can go badly wrong.**
  - If the drag changes the _tilt_ (`drives: tilt`, Earth's seasons-tilt config at `src/scenes/earth/earth-data.json:65-66`), the child learns that the rings tip up and down. **It must drive `orbitAngle`, with the axis arrow visibly parallel all the way round.** This also reinforces Earth's lesson that the axis keeps pointing the same way.
  - The orbit must be a circle. Saturn's eccentricity (about 0.056) is invisible at this scale, and an oval invites "the rings close when Saturn is far".
  - The thin-line view is "almost vanishes, a thin line", never an empty Saturn.
- **Distance and seasons.** Say "Saturn has seasons because it is tilted, like Earth". Do not say "only because": Saturn's eccentricity does shade its seasons, and "Distance plays no part anywhere" is already NOT ATTESTED (`docs/sources.md:1701-1703`).
- **The window's ring art must match the real sky.** It shows the south face, narrowly open, not the poster view. **Cross-level check:** Earth's `fact.telescope-saturn` art should also show a narrowly open ring for 2026–27 (`docs/sources.md:344-348` already allows "an open ring"; it should be modest).
- **S2 near opposition** shows a small backward drift. The R1a/R1b lesson covers it; do not re-explain it as new. The gap near the Sun must read as "hidden in the Sun's glare", never as "Saturn stopped".
- **S3 risks.**
  - Size: Titan is drawn at true scale against the Moon (about 1.5×). No Mercury comparison, which would repeat J3.
  - Mass: never "heavier".
  - Colour: the orange is a spacecraft view, never promised in a small telescope.
  - The infrared reveal must be labelled as a spacecraft camera view, not "what your eyes would see".
- **S4.** Never "the rings spin".

### Do not claim

- that the rings tilt, tip, wobble or flip, or that Saturn's tilt changes;
- that the rings disappear or vanish completely. Say they turn into a thin line and are hard to see;
- that edge-on happens "every 15 years", or on one fixed day. Say "twice each trip around the Sun";
- that the rings open a little more every month or night in 2026–27;
- that the rings (or Titan) can be seen with the naked eye, or that Saturn is bright or brighter than stars;
- that Saturn would float in water;
- any ring thickness figure;
- that Titan is the largest moon, is heavier than Mercury, or is the only moon with any atmosphere. "Thick" is required;
- that Titan's orange colour, the hexagon or the flattened disc can be seen in a small telescope (the last until sourced);
- that Saturn's seasons are caused by distance, or "only" by tilt;
- that a stone falls or lands on Saturn, or anything about Saturn's pull compared with other bodies;
- any number, date, period, angle or count on screen, including "about 30 years" and "7 years".

### Data and imagery needs

- **Ring geometry (S1).** A hand-authored `data/reference/saturn-ring-geometry.json`, like `surface-gravity.json`. It holds:
  - obliquity, from the NSSDC Saturn fact sheet (Wayback-dated);
  - the IAU pole RA/Dec, from Archinal et al. 2018;
  - the two anchor events, crossing 2025-03-23 and equinox 2025-05-06 (In-The-Sky).

  This is not a pipeline; the renderer draws geometry from constants. The `dataRef` seam needs the same `data/reference/` extension ticket 006 already requires (`tickets/006…:122-124`).
- **The window's inset (S1).** Re-run the one-off computation behind `docs/sources.md:344-348` at **monthly** sampling across 2026-09-08 → 2027-09-07, and record the table in `sources.md`. It settles whether the window has a dip. Cross-check two dates against an independent almanac (for example the IMCCE or JPL Horizons ring-tilt output).
- **S2:** the existing RA/Dec only. **S3:** a radii row for the Moon and Titan (NASA/NSSDC), plus two Cassini images.
- **Schema:** one new `rotate-match` renderer value, pinned to `orbitAngle` with a validator test (RED/GREEN). Ticket 006 already opens this enum for J7.

### Claims found false or unsupported

For `docs/sources.md` NOT ATTESTED or DISPUTED:

1. **"Saturn would float in a bathtub."** It is on NASA _Saturn Facts_. The average density is below water's, but Saturn is not a rigid body and its dense core would sink (IFLScience, _Is NASA's Claim That Saturn Could Float On Water Really True?_; BBC Sky at Night). **NOT ATTESTED.**
2. **"The rings vanish every 15 years."** The gaps alternate at about 13.7 and 15.7 years, and some crossings are triple (obliquity.com, _Ring Plane Crossings of Saturn_; In-The-Sky 2038/39). **NOT ATTESTED as worded.**
3. **"The rings disappear completely."** They become a thin line (ESA/Hubble opo9525c; NASA _Hubble Views Saturn Ring-Plane Crossing_). **NOT ATTESTED.**
4. **"The rings open steadily through 2026–27."** There is a yearly wobble: about 0.37° on 2025-11-23, after the March crossing (AAQ). **NEEDS SOURCE** until the monthly computation exists.
5. **"The rings are 10 m thick."** Sources range from about 10 m to about 1 km. **DISPUTED: quote no figure.**
6. **"Titan is bigger, so heavier, than Mercury."** It has about half Mercury's mass (NASA _Titan Facts_). **NOT ATTESTED.**
7. **"Titan is the largest moon."** Ganymede is about 2% larger (NASA _Titan Facts_). **FALSE.**
8. **"Titan is the only moon with an atmosphere."** NASA says "thick". **NOT ATTESTED without "thick".**
9. **"The hexagon is visible in a telescope / from Earth now."** The north pole is turned away during the window. This is geometry only, so it needs a source before anything is stated either way. **NOT ATTESTED.**
10. **"The rings change angle"** (NASA PIA03156 phrasing). This is a viewpoint effect. **Do not quote it.**

## Verdict

**Three honest required beats survive: S1 (rings come and go), S2 (the slowest wanderer) and S3 (the moon wrapped in fog). Saturn stays in v1.**

- **The margin is thin, and it is stated plainly:**
  - S1 carries the level. It needs a schema change (one renderer value) and the monthly ring computation.
  - S2 is the weakest of the three. It is a new lesson (slowest), but on a reused interaction (R1a).
  - If ticket 011 judges S2 a repeat of Mars, **the count falls to two and Saturn returns to post-v1**, unless S4 gets its NEEDS SOURCE closed by a NASA or primary page.
- **The gate.** With exactly three required markers at 0.7, the child needs all three, which is not really "open". Adding S4 (once sourced) as a fourth required marker restores choice: 3 of 4.
- **Recommended spine:** S1 first, then S2, S3 and S4 (if sourced) in any order. S5 is an optional extra only.
- **Types Saturn would use** (for ADR 0006's reverse-dependency line):
  - `rotate-match` (S1, new renderer);
  - `connect-the-dots` (S2);
  - `parallax-compare` (S3);
  - `trajectory-match` (S4, and S1's fallback);
  - `telescope-focus` (S5, optional only).

  Saturn's uses change no reopen set. If a set is cut, ticket 011 reopens: R1a → S2; M5/R2/R6/J3/J4 → S3; R1b/J2 → S4.

## Bulgarian terms

Confidence is moderate. Check against bg.wikipedia.

- **пръстени**
- **Титан**
- **спътник**
- **равноденствие** (metadata)
- **„виждаме ги откъм ръба"** for edge-on. Avoid „изчезват".
- **мъгла / плътна атмосфера** for Titan's haze.

## Sources

External sources are all search excerpts, not fetched.

- NASA/JPL, _A Change of Seasons on Saturn_ (PIA03156): <https://science.nasa.gov/resource/a-change-of-seasons-on-saturn/>
- NASA, _Saturn Facts_: <https://science.nasa.gov/saturn/facts/>
- NASA, _Titan Facts_: <https://science.nasa.gov/saturn/moons/titan/facts/>
- NASA, _Hubble Views Saturn Ring-Plane Crossing_: <https://science.nasa.gov/missions/hubble/hubble-views-saturn-ring-plane-crossing/>
- ESA/Hubble, _Saturn ring-plane crossing_: <https://esahubble.org/images/opo9525c/>
- In-The-Sky, _Equinox on Saturn_ (2025-05-06): <https://in-the-sky.org/news.php?id=20250506_12_100>
- In-The-Sky, _Saturn ring plane crossing_ (2038): <https://in-the-sky.org/news.php?id=20381015_12_100>
- Obliquity SkyEye, _Ring Plane Crossings of Saturn_: <https://www.obliquity.com/skyeye/misc/ringcrossing.html>
- AAQ, _Saturn in 2024/2025 – the rings edge-on_: <https://www.aaq.org.au/saturn-in-2024-2025-and-the-next-edge-on-appearance-of-its-rings/>
- Space.com, _Saturn's rings will 'disappear' this weekend_: <https://www.space.com/stargazing/saturns-iconic-rings-will-disappear-this-weekend-heres-why>
- Sky & Telescope, _Viewing Saturn: The Planet, Rings and Moons_: <https://skyandtelescope.org/stargazing-and-observing/celestial-objects-to-watch/viewing-saturn-the-planet-rings-and-moons/>
- Sky & Telescope, _Ultimate Guide on How to See Saturn at Its Best_ (the "60-mm … Titan" excerpt): <https://skyandtelescope.org/astronomy-news/observing-news/see-saturn-best-in-2014/>
- EarthSky, _Give me 5 minutes and I'll give you Saturn_: <https://earthsky.org/astronomy-essentials/give-me-five-minutes-ill-give-you-saturn/>
- IFLScience, _Is NASA's Claim That Saturn Could Float On Water Really True?_: <https://www.iflscience.com/is-nasas-claim-that-saturn-could-float-on-water-really-true-80053>
- BBC Sky at Night, _Saturn could float on water_: <https://www.skyatnightmagazine.com/space-science/saturn-could-float-on-water>
- Keeler 1895, ApJ 1, 416: <https://articles.adsabs.harvard.edu/pdf/1895ApJ.....1..416K>
- RASC, _James Edward Keeler_: <https://www.rasc.ca/honorary-member-james-edward-keeler>
- EARTH Magazine, _Keeler confirms Saturn's rings not solid_: <https://www.earthmagazine.org/article/benchmarks-april-9-1895-james-edward-keeler-confirms-saturns-rings-not-solid/>
- Repo:
  - `docs/sources.md:115`, `:245-253`, `:324-354`, `:365-368`, `:401-434`, `:476-477`, `:1677-1705`
  - `research/002-what-each-world-can-teach.md:175-181,206,249,261`
  - `tickets/006-jupiter-level-design.md:66-127`
  - `schemas/level-data.schema.json:61-99`
  - `src/scenes/earth/earth-data.json:65-66,112-113`
  - `content/bg/facts.json:21`
  - `data/generated/orbital-positions.json:5-8,9947`
