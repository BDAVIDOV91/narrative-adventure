# Sources

Every astronomy and folklore claim the game makes, with its source and its
verification status. The `astronomy-report` skill checks content against this
file before a commit that touches `content/` or `data/generated/`.

## Why this file is mandatory

This is an education game for children. A claim that ships without a source is a
claim nobody checked. Wrong astronomy taught to an 11-year-old is the most
severe defect this project can produce — it is this project's equivalent of a
security hole, and it gets the same treatment.

## What this game is about

**The astronomy and astrophysics are the point.** Bulgarian folklore is a bonus
layer that makes the sky feel like it belongs to the player — it is never the
lesson. A folk name earns its place only when learning the folklore and learning
the astronomy are the same act. See
`docs/adr/0005-folklore-beats-must-carry-astronomy.md`.

## Status vocabulary

| Status           | Meaning                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| **VERIFIED**     | Checked against a named authoritative source, cited below.                                      |
| **NEEDS SOURCE** | Believed true, no source recorded yet. Must not ship in player-facing content until it has one. |
| **DISPUTED**     | A specific problem has been identified. Must be resolved before it ships.                       |
| **NOT ATTESTED** | Investigated and found unsupported. Recorded so nobody re-adds it.                              |

---

## Solar system

### Day and night — Earth's rotation

- **Claim** (`fact.day-night`): Earth turns on its axis, so the Sun rises and sets.
- **Status**: VERIFIED — uncontroversial, standard reference astronomy.

### Seasons — axial tilt, not distance

- **Claim** (`fact.seasons`): Earth's axis is tilted; that causes seasons, _not_
  our distance from the Sun.
- **Status**: **VERIFIED, and now backed by our own generated data.**
- **Evidence in the repo**: `data/generated/orbital-positions.json`,
  `bodies.earth.helioDistanceAu`. Perihelion **2027-01-03 at 0.983 AU**,
  aphelion **2027-07-05 at 1.017 AU** — a **3.4%** variation whose near point
  falls in the middle of northern winter. Asserted by
  `tests/test_orbital_positions.py::test_perihelion_falls_in_northern_winter`.
- **Why it is called out explicitly**: "we are closer to the Sun in summer" is
  one of the most persistent misconceptions in science education. The level must
  actively contradict it, and it now has the real numbers to do so.
- **Design constraint**: do not draw Earth's orbit as a pronounced ellipse. At
  3.4% it is visually indistinguishable from a circle, and an exaggerated oval
  teaches the misconception the level exists to remove.

### Moon phases — illumination, not Earth's shadow

- **Claim** (`fact.moon-phases`): We see the part of the Moon the Sun lights.
- **Status**: VERIFIED. Citation added 2026-09-25 (search excerpt; the full-page
  fetch was blocked in that session). NASA Science, _Moon Phases_
  <https://science.nasa.gov/moon/moon-phases/>: „The Moon is always half-lit by
  the Sun" … „we see different portions of the lit side of the Moon." NASA
  Science, _Top Moon Questions_ <https://science.nasa.gov/moon/top-moon-questions/>:
  „The Moon does not make its own light. 'Moonlight' is really sunlight that has
  reflected off of the Moon's surface."
- **Why it is called out**: children commonly believe phases are Earth's shadow
  on the Moon. That is a lunar eclipse, a different and much rarer event. The
  rotate-match puzzle must not accidentally reinforce the shadow model.
- **Related trap** (`fact.moon-far-side`): "the dark side of the Moon". The far
  side is not dark — it receives as much sunlight as the near side. Say
  **далечната страна**, never тъмната. Source: _Top Moon Questions_, above —
  „The far side of the Moon gets as much sunlight as the near side"; see also
  "The far side is fully lit at new Moon" below.

### Parallax

- **Claim** (`fact.parallax`): Viewing one object from two positions makes it
  appear to shift; astronomers use this to measure distance.
- **Status**: VERIFIED.

### Mars retrograde motion

- **Claim**: Mars sometimes appears to move backwards across the sky.
- **Status**: VERIFIED, and derivable from the repo's own data —
  `helioLonDegrees` for Earth and Mars drive the walk-the-orbits puzzle, so the
  apparent reversal comes out of real geometry rather than being asserted.
- **External sources — full pages read 2026-09-25 by `astronomy-accuracy-checker`.**
  - NASA Mars Exploration, _Mars Retrograde_. **The live URL
    <https://mars.nasa.gov/all-about-mars/night-sky/retrograde/> no longer carries
    the page: it redirects to `science.nasa.gov/mars/facts/`, which has no
    retrograde text.** Cite the Wayback snapshot
    <https://web.archive.org/web/20221205212053/https://mars.nasa.gov/all-about-mars/night-sky/retrograde/>:
    „Every two years or so, there are a couple of months when Mars' position from
    night to night seems to change direction and move east to west." · „It's an
    illusion, caused by the ways that Earth and Mars orbit the sun." · „Earth has
    the inside lane and moves faster than Mars" · „About every 26 months, Earth
    comes up from behind and overtakes Mars." · „Connect the dots, and you'll draw
    either a loop or an open zigzag."
  - APOD 2014-10-28, _Retrograde Mars_ <https://apod.nasa.gov/apod/ap141028.html>
    (live): „About every two years, however, the Earth passes Mars as they orbit
    around the Sun." · „Mars appeared to move backwards in the sky, a phenomenon
    called retrograde motion."
- **Cross-check of the dates.** ALPO, _The 2026-2027 Aphelic Apparition of Mars_
  <https://www.alpo-astronomy.org/jbeish/2027_MARS.htm>, gives retrograde
  2027-01-10 → 2027-04-01; this repo's RA turning points are 2027-01-13 and
  2027-04-04 (research 004). The 3-day offset is consistent with RA versus
  ecliptic-longitude stationary points; no date reaches the player anyway.

### Planetary positions — independently spot-checked

- **Status**: VERIFIED 2026-09-08 against In-The-Sky.org, not against the
  generator that produced them.
- Jupiter minimum distance **2027-02-11** vs opposition 2027-02-11 (exact);
  Mars **2027-02-20** vs opposition 2027-02-19; Saturn **2026-10-05** vs
  opposition 2026-10-04 — both within the 1-day sampling grid.
- Lunar perigee 2026-12-24 at 356,779 km and apogee 2027-01-07 at 406,564 km,
  both inside the true physical envelope.
- **Staleness check — done 2026-09-09, and the file is current.** A 1-in-37
  sample of Earth, Jupiter and Venus rows was recomputed from `de440s.bsp` with
  today's `orbital-positions.py`: maximum deviation **4.6e-7°** in longitude,
  **4.7e-9 AU** in distance, **4.8e-7** in RA/Dec — rounding only. This is a
  staleness check against the same generator, not an independence check;
  independence was done 2026-09-08 against In-The-Sky.org.
- **Not checked**: per-sample RA/Dec against an almanac.
- **Frame caveat — see "A year is one orbit" above.** `helioLonDegrees` is
  **J2000-ecliptic**, and Earth's heliocentric longitude is the Sun's geocentric
  longitude **+180°**. Both facts are silent traps: a naive reading mislabels
  every season by six months and puts two of the four crossings on the wrong
  calendar day. Read the generated `seasons` block, never an interpolated
  longitude crossing.

### Jupiter's Galilean moons

- **Claim** (re-scoped 2026-09-25 to ticket 006 claim 4): Io, Europa, Ganymede
  and Callisto circle Jupiter, each at its own pace, the closer ones faster. Their
  orbit sizes and Jupiter's radius set the J2 drawing at true relative scale.
  **Schematic and undated**: no periods, radii or dates on screen, and no
  "night to night" or "work out the period by watching" framing — that older
  wording is withdrawn.
- **Status**: **VERIFIED** (full page, 2026-09-25). Quotes, values and URLs are in
  "Jupiter level — the claims ticket 006 adopts", claim 4, below.
- **Storage**: hand-authored, cited rows in `data/reference/` (the same pattern as
  `data/reference/surface-gravity.json`: `value`, `unit`, `factSheetLabel`,
  `sourceUrl`, `accessed` per row) — **not `data/generated/`**, which is reserved
  for generator output. Values come from the NSSDC _Jovian Satellite Fact Sheet_,
  never from memory, and never from the JPL SSD mean-element "P" column (see the
  trap under claim 4).

### Gravity — air, not weight, separates the feather from the rock

- **Claim** (`fact.gravity-drop`): a rock lands before a feather on Earth
  **because of the air**, not because it is heavier. Remove the air and they land
  together.
- **Status**: **VERIFIED** — Galilean equivalence, uncontroversial.
- **The misconception this beat must not create.** Over a few metres a rock and a
  ball land indistinguishably. A puzzle in which the **heavier** object visibly
  wins teaches _heavy falls faster_ — the Aristotelian misconception, the same
  failure class as seasons-by-distance. **The content is built on `въздухът`,
  never on `тегло`.** Correct child-facing framing: „Перцето е леко и широко —
  въздухът го носи. Камъкът си пробива път през въздуха. Без въздух няма кой да
  ги раздели."
- **Apollo 15 — the vacuum case, and it is filmed.** Commander **David Scott**,
  **2 August 1971**, EVA-3, dropped a 1.32 kg aluminium geological hammer and a
  0.03 kg falcon feather from about 1.6 m; they landed together.
  - **Status**: **VERIFIED.** Apollo Lunar Surface Journal, _Apollo 15, EVA-3
    Close-out_, GET 167:22:06 — Scott: „a gentleman named Galileo…"; at 167:22:46
    „Which proves that Mr. Galileo was correct in his findings."
    <https://apollojournals.org/alsj/a15/a15.clsout3.html>
  - Masses and drop height from the Apollo 15 Preliminary Science Report, quoted
    in NASA Science, _The Apollo 15 Hammer-Feather Drop_, 16 July 2018:
    <https://science.nasa.gov/resource/the-apollo-15-hammer-feather-drop/>
  - Date derived independently: launch 1971-07-26 13:34 UTC + GET 167:22:06 =
    1971-08-02.
  - **The ALSJ moved.** Every `nasa.gov/history/alsj/…` URL now redirects to a
    landing page; cite `apollojournals.org`.
- **Why they fell together: no air to hold the feather — not "no air on the
  Moon".** (`fact.gravity-drop.apollo`; the Moon-level nudge of ticket 005, merged
  with `fact.gravity-drop`.)
  - **Claim**: on the Moon there is (almost) no air, so nothing holds the feather
    back; the hammer and the feather fall together because all objects fall at
    the same rate regardless of how heavy they are.
  - **Status**: **VERIFIED** for „почти няма въздух" and for „няма въздух, който
    да задържи перцето". **NOT ATTESTED** for the flat „На Луната няма въздух":
    NASA says the Moon _has_ an atmosphere, a very thin one (an exosphere).
    Checked 2026-09-25 by `astronomy-accuracy-checker`, **every quote read on the
    full fetched page**, not a search excerpt.
  - **The drop itself** — NASA Science, _The Apollo 15 Hammer-Feather Drop_
    (page modified 2025-02-12)
    <https://science.nasa.gov/resource/the-apollo-15-hammer-feather-drop/>:
    „Because they were essentially in a vacuum, there was no air resistance and
    the feather fell at the same rate as the hammer, as Galileo had concluded
    hundreds of years before - all objects released together fall at the same
    rate regardless of mass." Note **„essentially"**: NASA does not say
    "a vacuum", flat.
  - **What the Moon has instead of air** — NASA Science, _Moon Facts_ (modified
    2026-02-12) <https://science.nasa.gov/moon/facts/>: „The Moon has a very thin
    and tenuous atmosphere called an exosphere. It is not breathable." and
    „The Moon has a very thin and weak atmosphere."
  - NASA Science, _The Moon's Atmosphere_ (modified 2026-03-05)
    <https://science.nasa.gov/moon/lunar-atmosphere/>: „The lunar atmosphere is
    mostly an exosphere, which itself is mostly empty space. If you were to visit
    the Moon and walk around on its surface, you might think it had no atmosphere
    at all." and „The Moon's atmosphere contains about one million billion (10¹⁵)
    times fewer molecules per cubic centimeter than Earth's does."
  - **The Earth half, from the same astronaut** — ALSJ, _Apollo 15 EVA-3
    Close-out_ (URL above), Scott's later commentary on repeating the drop on a
    lake bed at Edwards: „And, of course, the feather floats down, because of the
    air."
  - **Wording guard.**
    - **Use** „…няма въздух, който да задържи перцето" (the NASA wording is
      literally „no air resistance"), or „На Луната почти няма въздух". Both may
      be joined: „На Луната почти няма въздух — няма кой да задържи перцето."
    - **Never** the flat „На Луната няма въздух" or „на Луната има вакуум": NASA
      says there is a thin atmosphere and the drop was „essentially" in a vacuum.
      Same rule as Mars („no 'Mars has no air'", below) and as water („never
      'no water on the Moon'", ticket 003).
    - **The „не защото е тежък" clause stays.** It is the Galilean-equivalence
      claim of the entry above, and NASA's „fall at the same rate regardless of
      mass" is the quoted source for it. Keep the cause on **въздуха**, never on
      **тегло**.
    - No „атмосфера", „екзосфера" or „10¹⁵" on screen: rule 2, and a child
      needs only „въздух".
- **Rule 2**: the masses and the drop height are for this file only. No number,
  and no use of `земно ускорение`, reaches the player — say **притегляне**.

### Surface gravity per body

- **Claim** (`fact.gravity-drop.bodies`): the same drop is slow and floating on
  the Moon, a little quicker on Mars, and far stronger on Jupiter.
- **Superseded for Jupiter by ticket 006 (2026-09-25).** `gravity-drop` is deleted
  (ADR 0006), and **`fact.gravity-drop.bodies` is deleted in the build**. The
  Jupiter half survives only as a new Jupiter completion-line key (e.g.
  `fact.jupiter.complete`): "Jupiter pulls much harder than Earth". **Only
  „дърпа" / „притегля"** — never falls, lands, stands or weighs, because Jupiter has
  no true surface. See claim 14 under "Jupiter level — the claims ticket 006
  adopts". The values below stay as the source for that line.
- **Status**: **VERIFIED** for Moon, Mars, Earth and Jupiter.
- **Source**: NASA/NSSDCA planetary fact sheets. **The live URLs are dead** — as
  of 2026-09-09 every `https://nssdc.gsfc.nasa.gov/planetary/factsheet/*` address
  302-redirects to `https://www.nasa.gov/nssdc/`. **Cite the dated Wayback
  snapshot**, e.g.
  <https://web.archive.org/web/20250802093603/https://nssdc.gsfc.nasa.gov/planetary/factsheet/>,
  and record the snapshot date per row.
- **Values, m/s²**: Sun 274.0 · Mercury 3.70 · Venus 8.87 · Earth 9.82 mean ·
  Moon 1.62 · Mars 3.73 mean · Jupiter 25.92 mean at 1 bar (23.12 equatorial) ·
  Saturn 11.19 mean at 1 bar (8.96 equatorial).
- **Saturn is NOT ATTESTED for this beat and must not appear in it.** The fact
  sheet's two columns straddle Earth in opposite directions — 11.19 m/s² is
  **1.14× Earth**, 8.96 m/s² is **0.92× Earth** — and the summary table publishes
  the _acceleration_ figure while the body page leads with _gravity_. So „на
  Сатурн би паднало по-бавно" is an artefact of a column choice, not a fact.
  Saturn also has no surface to fall to. **Use Moon, Mars and Jupiter only.**
- **Do not build a "which pulls harder" comparison from Mercury and Mars** — both
  round to 3.7 at summary precision (3.70 vs 3.73). The difference is invisible,
  the same trap as the Alioth/Dubhe 0.05-mag margin recorded below.
- **Storage**: `data/reference/surface-gravity.json` — hand-authored, deliberately
  **outside `data/generated/`**, which is reserved for generator output
  (`docs/architecture/data-flow.md`). Each row carries `value`, `unit: "m/s2"`,
  `factSheetLabel`, archived `sourceUrl` and `accessed`.

### A year is one orbit — and the season markers on it

- **Claim** (`fact.year-orbit`): one year is one trip around the Sun; four
  particular places on that trip are the solstices and the equinoxes.
- **Status**: **VERIFIED.** USNO, _The Seasons and the Earth's Orbit_:
  <https://aa.usno.navy.mil/faq/seasons_orbit> — „The length of the year from
  equinox to equinox … is called the tropical year, and its length is the basis
  for our Gregorian (civil) calendar."
- **Which year the game implies**: the **tropical** year (365.242 d), not the
  sidereal (365.256 d). This happens automatically if the orbit closes on the
  season art rather than on a star. Bulgarian is **тропическа година**, not
  "тропична" — metadata only, never player text.
- **DISPUTED — the naive derivation from `helioLonDegrees` produces wrong
  seasons.** Two independent traps, both silent:
  1. **The mapping is inverted by 180°.** Earth's heliocentric longitude is the
     Sun's geocentric longitude **+ 180°**, so Earth λ = 0 is the **September**
     equinox, 90 the **December** solstice, 180 the **March** equinox, 270 the
     **June** solstice. Verified against the committed file: the λ=0 crossing
     falls 2026-09-23/24. Coding "0 = пролетно равноденствие" mislabels every
     season by six months **and still validates**.
  2. **Wrong frame.** `data/scripts/orbital-positions.py:92` calls
     `ecliptic_latlon()` with no `epoch=`, so values are **J2000-ecliptic**, not
     ecliptic-of-date — a systematic **−0.3758°** measured at the September 2026
     equinox, putting each crossing ~0.39 day late. Combined with ±1 day sampling
     this gives the **wrong calendar day for the December solstice and the March
     equinox**. Confirmed by direct computation: at the emitted equinox instant
     `ecliptic_latlon()` returns Earth **359.6242°** while `epoch=t` returns
     exactly **360.0°**, and the Sun's geocentric longitude of date is
     **180.0057°** — both the frame offset and the +180° inversion, measured
     rather than argued.
- **Resolution**: the generator emits an explicit `seasons` block from Skyfield's
  `almanac.seasons`, and the payload declares its frame. The level reads a **named
  event**, never an interpolated longitude crossing.
- **True instants** (de440s, ecliptic of date): September equinox 2026-09-23
  00:05 UTC · December solstice 2026-12-21 20:50 UTC · March equinox 2027-03-20
  20:24 UTC · June solstice 2027-06-21 14:11 UTC.
- **Rule 2**: no date ever renders. Season art only.

### Day length varies with the season — because of the tilt

- **Claim** (`fact.day-length`): summer days are long and winter days short, for
  the **same** reason there are seasons at all — the tilt of Earth's axis.
- **Status**: **VERIFIED.** USNO Astronomical Applications, sun rise/set service:
  <https://aa.usno.navy.mil/data/Dur_OneYear> (machine endpoint
  `https://aa.usno.navy.mil/api/rstt/oneday`). Retrieved 2026-09-09 for Sofia,
  42.6977 °N / 23.3219 °E.
- **Causal link, same source**: „The solstices mark the two dates … on which the
  Earth's position in its orbit is such that its axis of rotation is most tilted
  toward or away from the Sun. These are the dates when the days are longest for
  the hemisphere tilted toward the Sun." One citation covers tilt → seasons **and**
  tilt → day length, which is the spine this beat closes.
- **Sofia, local time**: December solstice 2026-12-21, 07:54–16:56, **9 h 02 m**.
  March equinox 2027-03-20, 06:31–18:38, **12 h 07 m**. June solstice 2027-06-21,
  05:49–21:08, **15 h 19 m**. September equinox 2026-09-23, 07:15–19:23,
  **12 h 08 m**. Summer is about **1.7×** winter.
- **The equinox day is slightly longer than 12 hours** (12 h 07 m), because of
  refraction and the Sun's disc. **Do not draw the equinox arcs as exactly half.**
- **This beat must actively contradict the distance misconception** (`fact.day-length.distance`),
  the same duty as the seasons beat.
- **Rule 2**: the bars are **continuous unlabelled arcs** — no ticks, no segment
  count, no hours. A segmented clock face is an hour count in disguise.

### Through a small telescope — what a child will actually see

- **Claim** (`fact.telescope-saturn`, `fact.telescope-jupiter`): Saturn's rings
  and Jupiter's cloud belts are visible in a small telescope.
- **Status**: **VERIFIED**, and the honest version is better than the
  overstatement.
- **Saturn**: Sky & Telescope, Alan MacRobert, _Viewing Saturn: The Planet, Rings
  and Moons_ — „The rings of Saturn should be visible in even the smallest
  telescope at 25×. A good 3-inch scope at 50× can show them as a separate
  structure detached on all sides from the ball of the planet." So: **ears at the
  smallest aperture, a true detached ring at about 75 mm.**
- **Jupiter**: Sky & Telescope, Bob King, _Jupiter Is Outstanding at Opposition_ —
  „a sharp, gleaming disk striped with two dark belts … through my **2.4-inch
  refractor**." **60 mm shows the two equatorial belts.** No overstatement needed.
- **Composition**: NASA Science, _Saturn Facts_ — the rings are „billions of small
  chunks of ice and rock … ranging from tiny, dust-sized icy grains to chunks as
  big as a house" <https://science.nasa.gov/saturn/facts/>. _Jupiter Facts_ — the
  stripes are „cold, windy clouds of ammonia and water"; dark **belts**, light
  **zones**, flowing in opposite directions
  <https://science.nasa.gov/jupiter/jupiter-facts/>.
- **Ring tilt is favourable in this game's window.** Computed from the committed
  `de440s.bsp` with the IAU Saturn pole: ring opening **−8.3° (2026-09)**,
  **−14.1° (2027-09)**. Method validated against the known ring-plane crossing of
  2025-03-23, where it returns **+0.04°**. Art may show an open ring. Had this
  shipped in 2025 the honest picture would have been a line.
- **Pedagogically the point of the beat**: the real view is small and shimmering,
  not a Hubble poster (`fact.telescope-expectation`). Setting a child up for
  disappointment at their first real telescope is a failure even where no fact is
  wrong.
- Bulgarian: **пръстени**, **облачни пояси** (teach the word; „ивици" is the right
  register alongside it). Aperture is never mentioned to the player.

### The brightest "star" in the evening sky is usually a planet

- **Claim** (`fact.brightest-is-a-planet`): what looks like the brightest star is
  often not a star. Venus is brightest of all; when Venus is absent, Jupiter — and
  Jupiter outshines **Sirius**, the brightest true star.
- **Status**: **VERIFIED.** Venus max **−4.8** and Jupiter max **−2.94** (mean at
  opposition **−2.7**) from the NASA fact sheets — again via dated Wayback
  snapshots, see above. Sirius **−1.44** read from this repo's own
  `data/generated/stars.json` (HIP 32349).
- **The ordering is unconditional**: Jupiter is brighter than Sirius at **every**
  point of its cycle, not only near opposition — faintest **−1.70** against
  Sirius's −1.44. **Saturn peaks at +0.43 and is always fainter than Sirius**; do
  not include it. Mars reaches −2.94 only at a favourable opposition.
- **"Usually Venus" is false for this game's committed window, and the truth is
  better.** Computed for Sofia at the end of evening civil twilight across
  2026-09-08 → 2027-09-07: **Venus is above 10° on zero evenings** — it is a
  **morning** object from Nov 2026 to Feb 2027, which is to say it is literally
  **Зорница**. Evenings: no bright planet Sept 2026 – late Jan 2027 (brightest
  point is Arcturus, −0.05); **Jupiter dominates ≈145 evenings from early Feb to
  mid-June 2027**, and **Jupiter and Sirius stand together February–April** — a
  real side-by-side comparison from a Bulgarian back yard.
- **Misconception risk**: „planets are brighter than stars" invites _planets are
  intrinsically bright_. The wording must carry **reflected** and **near**
  (`fact.brightest-why`). `fact.zornitsa` already ships „не свети сама, а я огрява
  Слънцето" — extend it to Jupiter rather than restating it.
- **This completes a set already half-built.** `fact.zornitsa`: Venus is not a
  star. `fact.lazhi-kervan`: Sirius mistaken _for_ Venus. Jupiter is the third
  bright wanderer, and it is the one that beats the brightest real star. Three
  entries, one lesson.
- `data/generated/orbital-positions.json#/bodies/jupiter` already carries real
  `raHours`, `decDegrees` and `distanceAu`, so any design here uses real positions.
- **Rule 2**: magnitudes are for this file. No number reaches the screen.

### Back cover — seeing the worlds with your own eyes (ticket 009)

Adopted by `docs/wayfinder/road-to-v1/tickets/009-book-ending-and-navigation.md`
for the storybook's back cover. Checked 2026-09-26 by `astronomy-accuracy-checker`.
Observer: Bulgaria, about 42.7° N. **How they were checked**: pages marked
„(page read)" were fetched and the quoted sentence found in the page text. Pages
marked „(search excerpt)" were not fetched in this session: the session's fetch
hook blocked further page reads, so the quote is from a search result attributed to
that URL and may be lightly paraphrased. Content keys are **(key TBD by the
back-cover build)**. **Rule 2**: every number below stays in this file; no count,
duration, angle or date reaches the player.

#### 1. The Moon, Mars, Jupiter and Saturn can all be seen with the naked eye from Bulgaria

- **Status**: **VERIFIED**, in this wording only: all four can be seen with the
  naked eye, **not every night and not always together**. Saturn is a point of
  light; its rings need a telescope.
- **Naked eye**: NASA Science, _Planetary Alignments and Planet Parades_ (Preston
  Dyches, 2025-02-04), page read
  <https://science.nasa.gov/solar-system/skywatching/planetary-alignments-and-planet-parades/>:
  „Five planets are visible without optical aid: Mercury, Venus, Mars, Jupiter,
  and Saturn." Same page: „On most nights, weather permitting, you can spot at
  least one bright planet" and „While two or three planets are commonly visible …
  occasionally four or five bright planets can be seen simultaneously". That is
  the source for **not always together**.
- **Not every night — computed from this repo's data.** Solar elongation from
  `data/generated/orbital-positions.json` (Sun = Earth `helioLonDegrees` + 180°;
  planet longitude from `raHours`/`decDegrees`) over 2026-09-08 → 2027-09-07:
  **Saturn** passes within 15° of the Sun for 35 days (2027-03-22 → 2027-04-25,
  closest 2.2° on 2027-04-08); **Jupiter** for 27 days (2027-08-12 → the end of
  the window, closest 0.9° on 2027-08-31); **Mars** never comes closer than 49°
  in the window. Oppositions fall out of the same series at Saturn 2026-10-05,
  Jupiter 2027-02-11 and Mars 2027-02-20. These dates are derived from the
  committed ephemeris only and were **not** checked against an independent almanac
  in this pass; none reaches the player. Each planet is out of sight for weeks, so „tonight" must never appear.
- **Saturn is a point, and faint for its fame.** The rings: Sky & Telescope, _Viewing
  Saturn_ (already cited above, _Through a small telescope_): „visible in even the
  smallest telescope at 25×". Brightness: Saturn peaks at +0.43 and is **always
  fainter than Sirius** (_The brightest "star"_ above). Nothing on the cover may
  call Saturn bright or draw its rings as a naked-eye sight.
- **Guards**: name the four worlds and use no count word („четирите", „four
  worlds"). Never „tonight"/„довечера". The art may show Saturn's rings only in a
  telescope frame, never over a naked-eye sky.
- **Safe wording** (Bulgarian is a draft for the content pass): „Луната, Марс,
  Юпитер и Сатурн можеш да видиш с просто око — не всяка нощ и не винаги заедно.
  Сатурн е само точица светлина; пръстените му се виждат с телескоп."

#### 2. Away from lights and screens, your eyes adjust and you see many more, fainter stars

- **Status**: **VERIFIED** (search excerpt). The player line carries no duration.
- **Source**: Kalloniatis & Luu, _Light and Dark Adaptation_, Webvision, NCBI
  Bookshelf <https://www.ncbi.nlm.nih.gov/books/NBK11525/> (search excerpt): the
  dark-adaptation curve has a fast cone branch, then „the sensitivity of the rod
  pathway improves considerably after 5-10 minutes in the dark"; brighter
  pre-adapting light delays the rod branch and „the absolute threshold also takes
  longer to reach". Lower threshold = fainter stars = more stars.
- **Duration, for this file only**: most of the gain in about **20–30 minutes**,
  full rod sensitivity after roughly **20–40 minutes** in real darkness. This is a
  search-result summary that merged ScienceDirect Topics, _Dark Adaptation_, and
  Scientific American,
  <https://www.scientificamerican.com/article/experts-eyes-adjust-to-darkness/>,
  and **could not be pinned to one URL**. Read the Webvision page itself before
  any duration is used anywhere.
- **Screens**: white light undoes the adaptation (search excerpt, Almanac.com,
  _Adjusting to Darkness_). A phone screen is a bright light at close range; that
  is why the line names screens.
- **Safe wording**: „Отдалечи се от лампите и екраните и почакай. Очите ти
  постепенно свикват с тъмното и започват да виждат много повече звезди."

#### 3. The planets always appear near the band of sky the Sun and Moon cross

- **Status**: **VERIFIED**, with **near**, never **on**. The word „еклиптика" never
  reaches the player.
- **Source**: NASA Science, _Planetary Alignments and Planet Parades_, page read:
  „planets always appear along a line or arc across the sky. This occurs because
  the planets orbit our Sun in a relatively flat, disc-shaped plane … this disc
  appears as a line, which we call the ecliptic". NASA/GSFC _From Stargazers to
  Starships_, _The Path of the Sun, the Ecliptic_, page read
  <https://pwg.gsfc.nasa.gov/stargaze/Secliptc.htm>: the planets „are confined to
  a narrow strip"; „The path of the Sun across the celestial sphere is very close
  to that of the planets and the moon. Because of its relation to eclipses, that
  path is known as the ecliptic."
- **Why „near" and not „on" — NASA's own „along a line" is looser than the truth.**
  The Moon: NASA _Moon Fact Sheet_, page read (HTTP 200, 2026-09-26)
  <https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html>: „Inclination
  to ecliptic (deg) 5.145". Geocentric ecliptic latitude computed from the
  committed `raHours`/`decDegrees` (obliquity 23.4393°), 2026-09-08 → 2027-09-07:
  Moon **±5.29°**, Mars **−0.33° to +4.47°**, Jupiter **+0.54° to +1.07°**, Saturn
  **−2.72° to −2.23°** (Venus reaches −7.57°, Mercury ±4.7°). The Moon's ±5.29°
  matches the fact-sheet 5.145° plus its known wobble, which cross-checks the
  method. `orbital-positions.json` carries no latitude field; these were derived.
- **Safe wording**: „Планетите винаги са близо до пътя, по който Слънцето и Луната
  минават по небето." Art: a soft band, planets scattered near it, not beads on a
  line.

#### 4. Twinkling

- **„Planets don't twinkle" (absolute) — NOT ATTESTED.** Low planets twinkle, and
  small-disc Mars can: EarthSky, _Why do stars twinkle, but planets don't?_
  (Deborah Byrd, 2026-06-28), page read
  <https://earthsky.org/space/why-dont-planets-twinkle-as-stars-do/>: „Stars
  twinkle, while planets (usually) shine steadily" and „You might see planets
  twinkling if you spot them low in the sky … you're looking through more
  atmosphere". APOD 2011-04-28, _Scintillating_, page read
  <https://apod.nasa.gov/apod/ap110428.html>: turbulence makes the star Regulus
  scintillate „more readily than the planet" Mars, whose disc is „on average,
  less affected" — less, not never. Do not state the absolute form anywhere.
- **„Planets usually shine more steadily than stars, because they show a tiny disc
  and not a point" — VERIFIED.** EarthSky, same page: „Planets shine more steadily
  because they're closer to Earth and so appear not as pinpoints, but as tiny disks
  in our sky … The zigs and zags of light from a planetary disk cancel each other
  out". APOD 2011-04-28: „Though tiny, its disk is seen as a bundle of light rays
  that is substantially broader compared to a star's". University of
  Wisconsin–Madison, _Curiosities: Why do stars appear to twinkle?_, page read
  <https://news.wisc.edu/curiosities-why-do-stars-appear-to-twinkle-in-the-night-sky>:
  „these points average out, so planets generally don't twinkle nearly as much as
  stars."
- **Guard**: „usually" / „обикновено" is load-bearing; dropping it turns the
  VERIFIED claim into the NOT ATTESTED one. Never offer twinkling as a sure test
  for „is it a planet".
- **Safe wording**: „Планетите обикновено светят по-спокойно от звездите и
  блещукат по-малко, защото са мъничко кръгче, а не точка." („блещукат" is the
  everyday Bulgarian verb; „сцинтилация" is not for the player.)

#### 5. Anchor for ticket 012: how far people have travelled

- **As requested — „No human has travelled beyond the Moon; the last crewed lunar
  mission was Apollo 17 (December 1972)" — DISPUTED. Do not ship.** The second half
  has been false since April 2026. NASA, _NASA Welcomes Record-Setting Artemis II
  Moonfarers Back to Earth_, page read
  <https://www.nasa.gov/news-release/nasa-welcomes-record-setting-artemis-ii-moonfarers-back-to-earth/>:
  „Their lunar flyby took them farther than any humans have ever traveled before,
  surpassing the previous distance record set by Apollo 13 astronauts in 1970."
  NASA, _NASA's Artemis II Crew Eclipses Record for Farthest Human Spaceflight_,
  page read
  <https://www.nasa.gov/news-release/nasas-artemis-ii-crew-eclipses-record-for-farthest-human-spaceflight/>:
  launched April 1, splashdown April 10, farthest point „about 252,756 miles",
  and the crew „will be the first to see some parts of the far side of the Moon
  with human eyes". Artemis II is a crewed lunar mission, so Apollo 17 is not the
  last one. „Beyond the Moon" is also unsafe: Artemis II (and every Apollo crew
  that orbited) passed behind the Moon, farther from Earth than the Moon itself.
- **VERIFIED replacement 1 — the last Moon landing.** „The last people to walk on
  the Moon were the crew of Apollo 17, in December 1972." NASA, _Apollo 17_ mission
  page, page read <https://www.nasa.gov/mission/apollo-17/>: „Launch Dec. 7, 1972
  … Splashdown Dec. 19, 1972"; Cernan, „commander of the last Apollo mission to the
  Moon … the last person to leave his footprints on the surface of the Moon"; „the
  final lunar landing mission of the Apollo Program". Still true on 2026-09-26:
  NASA, _Artemis III_ mission page, page read
  <https://www.nasa.gov/mission/artemis-iii/>: launch 2027, „NASA will test one or
  both human landing systems in low Earth orbit". **Re-check before release**:
  this goes stale the day a crew lands.
- **VERIFIED replacement 2 — nobody has gone past the Moon's neighbourhood.**
  „No person has ever travelled farther than the Moon. The farthest trip, by the
  Artemis II crew in April 2026, looped around the Moon and came home." Sources as
  above. No year, distance or mission name needs to reach the player; the
  companion line can say „хората са стигали само до Луната — и никой още не е
  продължил нататък".

### Moon level — the claims ticket 003 adopts

Adopted by `docs/wayfinder/road-to-v1/tickets/003-moon-level-design.md` from
`docs/wayfinder/road-to-v1/research/003-moon-claims.md`. Checked 2026-09-25 by
`astronomy-accuracy-checker`. **How they were checked**: the full-page fetch was
blocked in that session, so every quote below is from a **search excerpt**
attributed to the URL given. The search tool can lightly paraphrase. Wherever an
excerpt could not be pinned to one URL, the entry says so.

**Full-page read, 2026-09-25 (main session, ticket 003).** Every entry in this
block was then confirmed on its fetched page: the maria (NASA moon-map), the
terminator (NASA viewing-tips: „Focus particularly along the terminator line…
long shadows"; „try phases other than the full Moon"), eclipse tilt (NASA
_Eclipses and the Moon_: „usually passes above or below the Sun… prevents us
from having monthly solar and lunar eclipses"), lunar eclipses at full Moon
(same page), the annular ring (NASA types), almost-same-size (NASA _Eclipses and
the Moon_: „about 400 times… almost perfectly block out the Sun"), each safety
part (NASA safety; AAS eye-safety and projection), earthshine (APOD 2025-04-03;
NASA viewing-tips), closest vs farthest (NASA supermoons: „14 percent doesn't
make a big difference in detectable size"), synchronous rotation and the lit far
side (NASA _Top Moon Questions_). The „(search excerpt)" tags below now mean
"first found by excerpt, since read on the page". Still unread: the Sky &
Telescope „mush" line (supporting only) and NASA SVS 4158 (not cited). Every
content key is **(key TBD by Moon build)** unless named.

**Hammer and feather (ticket 005: the Moon completion line).** The Apollo 15 drop and the „почти
няма въздух / няма въздух, който да задържи перцето" wording are recorded under
_Gravity — air, not weight_ above (VERIFIED, full-page read 2026-09-25). The flat
„На Луната няма въздух" is **NOT ATTESTED** and must not ship.

### The dark "seas" are old lava plains, not water

- **Claim** (key TBD by Moon build): the dark patches on the Moon (maria,
  „морета") are plains of solidified lava (basalt), not water.
- **Status**: **VERIFIED** (search excerpt).
- **Source**: NASA Science, _Moon Maps for International Observe the Moon Night_
  <https://science.nasa.gov/moon/observe-the-moon-night/moon-map/>: „Once thought
  to be seas of water, these are actually large, flat plains of solidified
  basaltic lava." The research file's three URLs (`/moon/facts/`,
  `/moon/composition/`, `/moon/viewing-tips/`) came up in the same searches with
  "vast plains of basaltic lava" wording, **but the excerpt did not pin the
  sentence to any one of them**. Cite the moon-map page.
- **Design constraints**: no ages (the sources disagree in range: "over 3 billion
  years" vs "4.2 and 1.2 billion years ago"). **Never "there is no water on the
  Moon"**, because polar ice exists (NASA, _Moon Water and Ices_). The claim is
  only that the _seas_ are not water.

### Relief shows best near the terminator; full Moon is flat

- **Claim** (key TBD by Moon build): craters and mountains stand out best along
  the line between day and night on the Moon, where shadows are long. At full
  Moon there are almost no shadows, so relief is hardest to see.
- **Status**: **VERIFIED** (search excerpt).
- **Source**: NASA Science, _Moon Viewing Tips_
  <https://science.nasa.gov/moon/viewing-tips/>: „The line between night and day
  on the Moon (called the terminator) is ideal for seeing lunar craters and
  mountains since very long shadows heighten the contrast of the features." and
  „For better viewing of craters and mountains, try phases other than the full
  Moon."
- **Sky & Telescope is supporting only.** An excerpt reads „Direct-on, shadowless
  lighting, which occurs at full Moon, transforms our satellite into gray-and-white
  mush". It could not be pinned to either `/observing/observing-the-fullmoon/` or
  `/astronomy-news/full-moon-fringe-benefits/`, so do not cite it by URL.
- **Design constraint**: never say "full Moon is useless". The same S&T material
  says the full Moon shows the maria shadings and the bright ray systems well.

### A solar eclipse happens only at new Moon, and not at every new Moon

- **Claim** (key TBD by Moon build): the Moon can hide the Sun only when it
  passes between the Sun and Earth, which is at new Moon. Because the Moon's
  orbit is tilted a little, it usually passes above or below the Sun, so most new
  Moons bring no eclipse.
- **Status**: **VERIFIED** (search excerpt).
- **Sources**: NASA Science, _Why Do Eclipses Happen?_
  <https://science.nasa.gov/eclipses/geometry/>: „During the new moon, the Moon
  usually passes below or above the Sun, and its shadow misses Earth." NASA
  Science, _Why Don't We Have a Solar Eclipse Every Month?_
  <https://science.nasa.gov/resource/why-dont-we-have-a-solar-eclipse-every-month/>:
  "the Moon as seen from Earth's perspective usually passes above or below the
  Sun when it passes between us and the Sun."
- **Design constraints**: the tilt is "a little". Draw no steep ramp and state no
  5°. The Moon's shadow on Earth may be drawn as a small patch, but do not claim
  it is "seen only there". That is true of totality, and this beat says nothing
  about totality.

### A lunar eclipse happens only at full Moon, and not at every full Moon

- **Claim** (key TBD by Moon build): Earth's shadow can fall on the Moon only
  when Earth is between the Sun and the Moon, which is at full Moon. Because of
  the same tilt, the Moon usually passes above or below the shadow.
- **Status**: **VERIFIED** (search excerpt) for "only at full Moon" and "not at
  every full Moon". The quantifier **"most"** full Moons is not in any quote
  found. Say **не всяко пълнолуние** („not every full Moon").
- **Sources**: NASA Science, _Eclipses and the Moon_
  <https://science.nasa.gov/moon/eclipses/>: „Lunar eclipses occur at the full
  Moon phase." … „the Moon doesn't always get in Earth's shadow because the
  Moon's path around Earth is tilted compared to Earth's orbit around the Sun."
  NASA Space Place, _Lunar Eclipses and Solar Eclipses_
  <https://spaceplace.nasa.gov/eclipses/en/>: „a full moon fades away as Earth's
  shadow covers it up". The "doesn't always" sentence came up in an excerpt
  that listed both pages, and it was not pinned to either one.
- `https://svs.gsfc.nasa.gov/4158` (research file) was **not** confirmed. The
  searches surfaced other SVS lunar-eclipse pages instead. Do not cite 4158
  until it has been read.
- **Design constraints**: the shadow always points straight away from the Sun.
  This entry is the counterweight to "Moon phases — illumination, not Earth's
  shadow" above. Earth's shadow on the Moon **is** an eclipse and **is not** a
  phase. The two must never share a picture.

### The Sun and Moon look almost the same size, and annular eclipses exist because of "almost"

- **Claim** (key TBD by Moon build): the Sun and Moon look almost the same size
  in our sky. When the Moon is farther from Earth it looks slightly smaller and
  leaves a ring of Sun uncovered.
- **Status**: **VERIFIED** (search excerpt). "Exactly the same size" stays **NOT
  ATTESTED** (see "Common sky myths" below).
- **Sources**: NASA Science, _Why Do Eclipses Happen?_
  <https://science.nasa.gov/eclipses/geometry/>: „Even though the Sun is about 400
  times bigger than the Moon, it is also about 400 times farther away. This makes
  the Sun and the Moon appear almost exactly the same size in our sky." NASA
  Science, _Types of Solar Eclipses_ <https://science.nasa.gov/eclipses/types/>:
  „An annular solar eclipse happens when the Moon passes between the Sun and
  Earth, but when it is at or near its farthest point from Earth. Because the Moon
  is farther away from Earth, it appears smaller than the Sun and does not
  completely cover the Sun." The two sentences came up in one combined excerpt
  listing both pages, so the page-by-page split is the most likely one but is not
  certain.
- **Design constraint**: no "400×" on screen (rule 2).

### Eclipse safety — each part checked separately

- **Claim** (key TBD by Moon build): never look straight at the Sun. Sunglasses,
  however dark, are not safe. Use eclipse glasses or a pinhole projector with
  your back to the Sun, and never look through the hole. Never look through
  binoculars, a telescope or a camera, even while wearing eclipse glasses. Do it
  with an adult.
- **Status**: **VERIFIED** (search excerpt), part by part:
  1. **Never look straight at the Sun**: NASA Science, _Eclipse Viewing Safety_
     <https://science.nasa.gov/eclipses/safety/>: „it is never safe to look
     directly at the eclipse without proper eye protection" (said of partial and
     annular eclipses).
  2. **Sunglasses are not safe**: same page, „Eclipse glasses are NOT regular
     sunglasses; regular sunglasses, no matter how dark, are not safe for viewing
     the Sun."
  3. **Pinhole, back to the Sun, not through the hole**: AAS, _Indirect Solar
     Viewing: Pinhole & Optical Projection_
     <https://eclipse.aas.org/eye-safety/projection>: „With the Sun at your back,
     you project sunlight through the hole(s) onto a surface and look at the solar
     image(s) on the surface." and „Do NOT look at the Sun through the
     pinhole(s)!" NASA's safety page says the same: „With the Sun at your back,
     you can then safely view the projected image."
  4. **Not through binoculars, a telescope or a camera, even with eclipse
     glasses**: NASA _Eclipse Viewing Safety_, above: „Do NOT look at the Sun
     through a camera lens, telescope, binoculars, or any other optical device
     while wearing eclipse glasses or using a handheld solar viewer — the
     concentrated solar rays will burn through the filter and cause serious eye
     injury."
  5. **With an adult — attested, so it stays in the string.** AAS, _How to View
     a Solar Eclipse Safely_ <https://eclipse.aas.org/eye-safety>: „Always
     supervise children using solar filters." Confirmed on the full page
     2026-09-25; the AAS line alone carries the claim. The NASA „supervise"
     wording and a Space Place „Ask an adult" line from the excerpts were **not**
     found on the fetched pages (`science.nasa.gov/eclipses/safety/`,
     `spaceplace.nasa.gov/eclipses/en/`), so neither is cited.
- **Design constraints**:
  - **"Never" through optics is a deliberate simplification.** NASA and Space
    Place both say optics are safe with a proper solar filter mounted **on the
    front** („use special filters over the lenses of cameras, telescopes, or
    binoculars"). The string may say "never through binoculars, a telescope or a
    camera **with eclipse glasses**", which is sourced. It must never claim that
    optics can never be made safe.
  - "Never look straight at the Sun" is unqualified only because the game says
    **nothing about totality**. Looking at totality is safe, and the 2027-08-02
    eclipse is only partial from Bulgaria. If totality is ever mentioned, this
    string must change.
  - No "ISO 12312-2" in child text.

### Earthshine — Earth lights the Moon's dark part

- **Claim** (key TBD by Moon build): sunlight reflected off Earth faintly lights
  the dark part of a crescent Moon.
- **Status**: **VERIFIED** (search excerpt).
- **Sources**: APOD 2025 April 3, _The Da Vinci Glow_
  <https://apod.nasa.gov/apod/ap250403.html>: „While only a sliver of the Moon's
  sunlit surface is visible, most of the Moon's disk can be seen by earthshine as
  light reflected from bright planet Earth illuminates the lunar nearside." NASA
  Earth Observatory, _Earthshine_ (ISS028-E-20073), reached at
  <https://earthobservatory.nasa.gov/images/83782/earthshine>. The research
  file's `science.nasa.gov/earth/earth-observatory/earthshine-83782/` is the same
  image ID, but that exact URL was not seen: „the moon's dark face is being dimly
  illuminated by 'earthshine'—light reflected off the Earth."
- **Design constraint**: the beat describes it without naming it. The research
  file keeps „пепелява светлина" out of player text, although APOD's "ashen
  glow" confirms it is a real synonym.

### Closest and farthest full Moons differ only a little in size

- **Claim** (key TBD by Moon build): a full Moon at its closest looks up to about
  14% wider than one at its farthest, which is hard to notice by eye.
- **Status**: **VERIFIED** (search excerpt).
- **Sources**: NASA Science, _Supermoons_ <https://science.nasa.gov/moon/supermoons/>:
  „At its closest point, the full Moon can appear up to 14 percent bigger and 30
  percent brighter than the faintest Moon of the year". NASA JPL Education, _What's
  a Supermoon and Just How Super Is It?_
  <https://www.jpl.nasa.gov/edu/resources/teachable-moment/whats-a-supermoon-and-just-how-super-is-it/>:
  „it would be difficult to tell the difference between an average full moon and
  a supermoon with the naked eye". The excerpt merged both pages, so the split
  follows the page titles and is most likely, but not certain.
- **Design constraints**: say closest and farthest, never "huge", and show no
  percentage (rule 2). Do not lift NASA's rising-Moon "double-take" line: the
  Moon looking bigger at the horizon is the Moon illusion, NOT ATTESTED as a real
  size change (see "Common sky myths" below).

### The Moon turns once per orbit, so one face always points at Earth

- **Claim** (key TBD by Moon build): the Moon spins once in the time it takes to
  go round Earth once, so the same side always faces us.
- **Status**: **VERIFIED** (search excerpt).
- **Source**: NASA Science, _Tidal Locking_
  <https://science.nasa.gov/moon/tidal-locking/>: „Earth's Moon rotates, but it
  takes precisely as long for the Moon to spin on its axis as it does to complete
  its monthly orbit around Earth." and „The same side of the Moon always faces
  Earth, because the Moon rotates exactly once each time it orbits our planet."
- **Design constraints**: never "the Moon doesn't rotate" (NOT ATTESTED, below).
  Wording about phases never uses „лице", so that "face" in the locking sense and
  the lit part in the phase sense do not blur together.

### The far side is fully lit at new Moon

- **Claim** (`fact.moon-far-side`, plus a key TBD by Moon build if the new-Moon
  detail gets its own string): the far side is not dark. At new Moon it is the
  side in full sunlight.
- **Status**: **VERIFIED** (search excerpt).
- **Source**: NASA Science, _Top Moon Questions_
  <https://science.nasa.gov/moon/top-moon-questions/>: „The far side of the Moon
  gets as much sunlight as the near side." and „When the far side is fully lit
  and the near side is dark, we call this a new Moon."
- **Design constraint**: never „тъмна страна". See "Moon phases" above.

### Mars level — the claims ticket 004 adopts

Adopted by `docs/wayfinder/road-to-v1/tickets/004-mars-level-design.md` from
`docs/wayfinder/road-to-v1/research/004-mars-claims.md`. Checked 2026-09-25 by
`astronomy-accuracy-checker`. **How they were checked**: every quote below was
read on the **full fetched page** (HTML downloaded, stripped to text, searched),
not taken from a search excerpt. Two NASA URLs in the research file are dead —
`mars.nasa.gov/all-about-mars/night-sky/retrograde/` redirects to _Mars Facts_ and
`mars.nasa.gov/resources/21869/mars-hoax/` redirects to a resources index — so
those two are cited through dated Wayback snapshots of the original pages. Sky &
Telescope's _An Observer's Guide to Mars_ returned **HTTP 403**, and a Wayback
request for that path returned 404, so it was **not read**; nothing below rests on it. Every
content key is **(key TBD by Mars build)**.

### Mars seems to turn back, but never does; Earth overtakes it on the inside

- **Claims** (research 004 rows 1–4): Mars sometimes appears to move backwards
  against the stars and then forwards again (1). Mars never really turns back; the
  look comes from Earth catching up and overtaking it (2). Earth overtakes on the
  inside, because its orbit is the inner one (3). Earth moves around the Sun
  faster than Mars (4).
- **Status**: **VERIFIED** (full page), all four.
- **Source**: NASA Mars Exploration, _Mars Retrograde_, Wayback snapshot
  <https://web.archive.org/web/20221205212053/https://mars.nasa.gov/all-about-mars/night-sky/retrograde/>:
  (1) „there are a couple of months when Mars' position from night to night seems
  to change direction and move east to west"; (2) „Did the planet really stop, back
  up, change its mind, and then continue to move forward? … Today we know what's
  going on. It's an illusion, caused by the ways that Earth and Mars orbit the
  sun." and „Earth comes up from behind and overtakes Mars"; (3) and (4) „The two
  planets are like race cars on an oval track. Earth has the inside lane and moves
  faster than Mars". APOD 2014-10-28 <https://apod.nasa.gov/apod/ap141028.html>
  supports (1): „Mars appeared to move backwards in the sky".
- **Second source for (4)**: NASA NSSDC, _Planetary Fact Sheet_
  <https://nssdc.gsfc.nasa.gov/planetary/factsheet/> (live), row „Orbital Velocity
  (km/s)": Earth **29.8**, Mars **24.1**. NASA _Mars Facts_
  <https://science.nasa.gov/mars/facts/>: „Mars takes longer to orbit the Sun
  (because it's farther away)". Numbers stay in this file (rule 2).
- **Wording guard, confirmed by the source**: the same NASA page says the dots
  make „either a loop or an open zigzag" — so never promise a loop. „Seems to",
  „turns back"; never „Mars stops" or „reverses"; „catches up and overtakes on the
  inside lane", which is the page's own race-track image. No dates.

### Mars never looks as big as the full Moon, not even at its closest

- **Claim** (row 5).
- **Status**: **VERIFIED** (full page).
- **Source**: NASA Mars Exploration, _Close Approach_, Wayback snapshot
  <https://web.archive.org/web/20221231080624/https://mars.nasa.gov/all-about-mars/night-sky/close-approach/>:
  „don't be fooled by the Mars Hoax! Since 2003, this urban legend has been
  circulated through email and social media every time Mars makes a close
  approach. The false message of the urban legend is that Mars will look as big as
  the Moon in our night sky. If that were true, we'd be in big trouble given the
  gravitational pulls on Earth, Mars, and our Moon!" The „every time Mars makes a
  close approach" carries the „not even at its closest" half. NASA _Mars Hoax_,
  Wayback <https://web.archive.org/web/20221202233134/https://mars.nasa.gov/resources/21869/mars-hoax/>,
  carries the same sentence.
- **Context for 2027**: ALPO <https://www.alpo-astronomy.org/jbeish/2027_MARS.htm>
  (full page): „The 2027 Mars apparition is considered Aphelic" and closest
  approach gives „an apparent planetary disk diameter of 13.8''". No sizes on
  screen; no drama.
- **Not used**: the JPL Night Sky Network page named in research 004 was not
  located or read. It is not needed.

### Through a small telescope, Mars is a small reddish disc (6′), and its darker patches show best at closest approach (7′)

Rows 6 and 7 were reworded by the owner on 2026-09-25 to what the pages carry.
Re-checked the same day by `astronomy-accuracy-checker`: both pages below were
downloaded (HTTP 200), stripped to text and searched. No search excerpt used.

- **Claim 6′** (R3): through a small telescope Mars looks like a small reddish
  disc, and its colour is the most striking thing about it.
- **Status**: **VERIFIED** (full page).
- **Source**: APOD 2003-08-19, _Mars Through a Small Telescope_
  <https://apod.nasa.gov/apod/ap030819.html>: „Viewed with the unaided eye or
  through a small telescope, possibly the most striking part of Mars' appearance
  is its red color." ALPO, _The 2026-2027 Aphelic Apparition of Mars_
  <https://www.alpo-astronomy.org/jbeish/2027_MARS.htm>: „it will swell from a
  small apparent disk of 6" in October14, 2026", and at closest approach „an
  apparent planetary disk diameter of 13.8''" — still a small disc (see row 5).
- **Wording guard**: APOD hedges („possibly the most striking"). Keep a hedge in
  Bulgarian — „може би най-забележителното", „първото, което ще забележиш" — not
  a flat superlative. „Reddish" is fine: it is weaker than APOD's „red color".
  APOD describes the record **2003** approach and a photograph made over three
  nights; its caption also lists „white polar caps" and „dark red areas" seen
  then. **Never promise the 2003 view, polar caps or named features for 2027.**
  Do not reuse APOD's explanation of the dark areas („relatively smooth
  lowlands"); the game does not say what the patches are.
- **Claim 7′** (R3 nudge): darker patches on Mars show best when Mars comes
  closest to Earth.
- **Status**: **VERIFIED** (full page), as the combination of two pages.
- **Source**: ALPO 2027 page, apparition table: at the 6″ start (2026 Oct 14),
  „Views of surface details not well defined"; at opposition (2027 Feb 19, 13.8″,
  one day before closest approach), „Views of surface details well defined".
  APOD 2003-08-19, written eight days before the 2003 closest approach:
  „Visible through the small telescope are … dark red areas". ALPO carries
  „best when closest"; APOD carries that the details include darker areas.
- **Wording guard**: no telescope sizes; no promise of what a particular
  telescope shows — ALPO's „well defined" is for „4-inch to 8-inch apertures
  telescopes and up". Do not cite ALPO's sentence „to a maximum diameter on July
  01, 2027": it contradicts the page's own table (13.8″ at closest approach on
  Feb 20; July 1 is when the disc falls back to 6″).

### Superseded: rows 6 and 7 as first worded — NEEDS SOURCE, do not ship

- **Claims** (rows 6–7, original wording): through a small telescope Mars is a
  small orange disc, sometimes with faint dark markings (6); bigger telescopes
  show more detail (7).
- **Status**: **SUPERSEDED** by 6′ and 7′ above. Never VERIFIED; the original
  wording stays **NEEDS SOURCE** and must not ship.
- **What was read**: ALPO _The 2026-2027 Aphelic Apparition of Mars_ (full page).
  It supports only the „small" part — „swell from a small apparent disk of 6" in
  October14, 2026" — and that the apparition „begins for observers using 4-inch to
  8-inch apertures telescopes and up … Views of surface details not well defined",
  becoming „well defined" at opposition. That ties detail to the **disc's size over
  the months**, not to aperture, so it does not carry row 7. It calls the disc
  „bright orange" **only during a great dust storm**, so it does not carry „orange"
  in general. „Faint dark markings" is not on the page.
- **What was not read**: Sky & Telescope, _An Observer's Guide to Mars_ — HTTP 403.
  This is also the only source behind the polar-cap NOT ATTESTED line below.
- **Also on the ALPO page, and a trap for the wording**: in 2027 „Astronomers will
  have an excellent view of the prominent north polar cap … because it will be
  tilted earthward". That is for 4–8 inch-and-up observers; it does not license a
  polar cap in a child's small telescope.
- **Closed by rewording**, not by a new source for the old wording: see 6′/7′.
  „Orange", „faint dark markings" and „bigger telescopes show more" remain
  unsourced.

### Mars is red because of rusty dust

- **Claim** (row 8): Mars is red because of rusty (iron oxide) dust.
- **Status**: **VERIFIED** (full page).
- **Source**: NASA Science, _Mars Facts_ <https://science.nasa.gov/mars/facts/>:
  „The reason Mars looks reddish is due to oxidization — or rusting — of iron in the
  rocks, regolith (Martian “soil”), and dust of Mars. This dust gets kicked up into
  the atmosphere and from a distance makes the planet appear mostly red." ESA,
  _Have we been wrong about why Mars is red?_ (2025)
  <https://www.esa.int/Science_Exploration/Space_Science/Mars_Express/Have_we_been_wrong_about_why_Mars_is_red>:
  „this red colour is due to rusted iron minerals in the dust".
- **Wording guard**: ESA's 2025 result is that the rust is likely **ferrihydrite**
  (a water-bearing iron oxide), not hematite. „Rust" / „ръжда" stays correct; never
  name hematite as the answer.

### Mars is a cold world (ships without „not because it is hot")

- **Claim as it ships** (row 9, corrected 2026-09-25): „Mars is a cold world",
  placed beside row 8 „red from rust". **VERIFIED** (full page). The „not because
  it is hot" half is **dropped** and must not ship.
- **Original claim** (row 9): Mars's redness is not because it is hot; Mars is a
  cold world.
- **Status of the original**: split.
  - „Mars is a cold world": **VERIFIED** (full page). NASA _Mars Facts_: „Mars — the
    fourth planet from the Sun — is a dusty, cold, desert world with a very thin
    atmosphere."
  - „Its redness is not because it is hot": **NEEDS SOURCE.** **No page read says
    this.** _Mars Facts_ gives rust as the cause and gives temperatures, but never
    says the colour is not heat. ESA's page does not say it either. Per research
    004's own guard, **drop „not heat"**. The game may place the two verified facts
    side by side (red from rust; a cold world) and let the child notice; it must not
    assert the negation as a sourced fact.
- No temperatures on screen.

### A camera on Mars saw a blue glow around the setting Sun

- **Claim** (row 10): Curiosity, in Gale Crater, photographed a sunset with a
  bluish glow around the Sun.
- **Status**: **VERIFIED** (full page).
- **Source**: the old `photojournal.jpl.nasa.gov/catalog/PIA19400` URL now
  redirects to NASA Science, _Sunset in Mars' Gale Crater_ (PIA19400)
  <https://science.nasa.gov/photojournal/sunset-in-mars-gale-crater/>. Full
  caption read: „NASA's Curiosity Mars rover recorded this view of the sun setting
  at the close of the mission's 956th Martian day, or sol (April 15, 2015), from
  the rover's location in Gale Crater." · „The color has been calibrated and
  white-balanced to remove camera artifacts. Mastcam sees color very similarly to
  what human eyes see, although it is actually a little less sensitive to blue than
  people are." · „That causes the blue colors in the mixed light coming from the
  sun to stay closer to sun's part of the sky, compared to the wider scattering of
  yellow and red colors. The effect is most pronounced near sunset".
- **Where the blue is**: near the Sun only („closer to sun's part of the sky"),
  strongest at sunset. **What the white balance means**: it removes camera
  artifacts, and the caption says Mastcam sees colour much like a human eye. So
  „white-balanced" must **not** be used to suggest the colour is fake, and the
  guard no longer mentions it (corrected 2026-09-25 in research 004 row 10).
  „A camera on Mars saw" stays the right hedge because it is one image, not a
  claim about every Martian sunset.
- **Never say or imply the Mars sky is blue.** NASA _Mars Facts_: „To our eyes,
  the sky would be hazy and red because of suspended dust instead of the familiar
  blue tint we see on Earth." Never „always"; no „Mars has no air" (the same page:
  „a thin atmosphere made up mostly of carbon dioxide, nitrogen, and argon").

### A day on Mars is only a little longer than a day on Earth

- **Claim** (row 11).
- **Status**: **VERIFIED** (full page).
- **Source**: NASA _Mars Facts_ <https://science.nasa.gov/mars/facts/>: „it
  completes one rotation every 24.6 hours, which is very similar to one day on
  Earth (23.9 hours)." „A little longer", no hours on screen.

### Jupiter level — the claims ticket 006 adopts

Adopted by `docs/wayfinder/road-to-v1/tickets/006-jupiter-level-design.md` from
`docs/wayfinder/road-to-v1/research/006-jupiter-claims.md` (claim numbers below are
that file's rows). Checked 2026-09-25 by `astronomy-accuracy-checker`. **Method:
full page** — every page was downloaded, stripped to text and searched; no status
rests on a search excerpt. All access dates are **2026-09-25**. Every content key
is **(key TBD by Jupiter build)** except where named.

**URL notes.** The NSSDC fact sheets under
`https://nssdc.gsfc.nasa.gov/planetary/factsheet/` **are live again** (HTTP 200 on
2026-09-25; they redirected on 2026-09-09), so they are cited live below; the
Wayback snapshots recorded under "Surface gravity per body" remain valid. Sky &
Telescope returns **HTTP 403** to scripts, so every S&T page is cited through a
dated Wayback snapshot.

Sources read in full, cited by short name:

- **[JF]** NASA, _Jupiter Facts_ <https://science.nasa.gov/jupiter/jupiter-facts/>
- **[NSN]** NASA Night Sky Network, _October's Night Sky Notes: From Galileo to
  Clipper, Exploring Jupiter's Moons_ (V. White, 2023)
  <https://science.nasa.gov/solar-system/skywatching/night-sky-network/octobers-night-sky-notes-from-galileo-to-clipper-exploring-jupiters-moons/>
- **[ST-BBB]** Sky & Telescope, J. Kelly Beatty, _How to See Jupiter: Big, Bright,
  and Beautiful_ (2014), Wayback 2024-07-16
  <https://web.archive.org/web/20240716160421/https://skyandtelescope.org/observing/jupiter-big-bright-and-beautiful-2/>
- **[ST-OPP]** Sky & Telescope, Bob King, _Jupiter Is Outstanding at Opposition_,
  Wayback 2025-12-07
  <https://web.archive.org/web/20251207132001/https://skyandtelescope.org/observing/jupiter-is-outstanding-at-opposition/>
- **[ST-GRS]** Sky & Telescope, J. Kelly Beatty, _Jupiter's Not-So-Great Red Spot_
  (2014), Wayback 2025-05-22
  <https://web.archive.org/web/20250522171752/https://skyandtelescope.org/astronomy-news/observing-news/jupiters-great-red-spot/>
- **[ST-TR]** Sky & Telescope, _Transit Times of Jupiter's Great Red Spot_, Wayback
  2026-01-06
  <https://web.archive.org/web/20260106055436/https://skyandtelescope.org/observing/interactive-sky-watching-tools/transit-times-of-jupiters-great-red-spot/>
- **[IO] [EU] [GA] [CA]** NASA _Io Facts_
  <https://science.nasa.gov/jupiter/jupiter-moons/io/facts/>, _Europa Facts_
  <https://science.nasa.gov/jupiter/jupiter-moons/europa/europa-facts/>,
  _Ganymede Facts_ <https://science.nasa.gov/jupiter/jupiter-moons/ganymede/facts/>,
  _Callisto Facts_ <https://science.nasa.gov/jupiter/jupiter-moons/callisto/facts/>
- **[ME]** NASA _Mercury Facts_ <https://science.nasa.gov/mercury/facts/>;
  **[EF]** NASA _Earth Facts_ <https://science.nasa.gov/earth/facts/>
- **[NSSDC-JS]** NASA NSSDC, _Jovian Satellite Fact Sheet_ (last updated
  2023-12-06) <https://nssdc.gsfc.nasa.gov/planetary/factsheet/joviansatfact.html>
- **[NSSDC-J]** NASA NSSDC, _Jupiter Fact Sheet_
  <https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html>;
  **[NSSDC-P]** _Planetary Fact Sheet_ (last updated 2025-03-18)
  <https://nssdc.gsfc.nasa.gov/planetary/factsheet/>; **[NSSDC-N]** _Notes on the
  Fact Sheets_ <https://nssdc.gsfc.nasa.gov/planetary/factsheet/planetfact_notes.html>
- **[SSD]** JPL SSD, _Planetary Satellite Mean Elements_
  <https://ssd.jpl.nasa.gov/sats/elem/> (cross-check only — see the trap in 4)
- **[VAN]** University of Illinois Physics Van, _Light From Planets and Stars_
  <https://van.physics.illinois.edu/ask/listing/14244>

#### 1. Through binoculars, up to four moons show as small dots in a line beside Jupiter

- **Status**: **VERIFIED** (full page).
- **Quotes**: [NSN] „Look a bit closer, with a pair of binoculars … you will likely
  see a line of smaller dots on one or both sides. … Jupiter … and its four largest
  moons"; „easily visible through a pair of modest binoculars or a small
  telescope". [ST-BBB] „If your binoculars are good quality and magnify at least
  seven times … Look closely to either side of Jupiter's disk — do you see a line
  of three or four tiny stars?"
- **Guard**: "up to four" (S&T's own „three or four"); binoculars, never the naked
  eye; never „звезди" (both pages say "stars" loosely — the game must not). Undated.

#### 2. Jupiter is a huge ball of gas; a small telescope shows a small disc with dark cloud belts when the air is steady (`fact.telescope-jupiter`)

- **Status**: **VERIFIED** (full page), including the two clauses that lacked a
  quote.
- **"Ball of gas"**: [ST-BBB] „Jupiter is a gas giant planet — it consists almost
  entirely of hydrogen and helium, nearly all the way down. The "surface" you see
  is actually the top layers of cloud decks"; [JF] „As a gas giant, Jupiter doesn't
  have a true surface. The planet is mostly swirling gases and liquids"; [ST-OPP]
  „Jupiter has no solid surface. Nothing but clouds and weather".
- **"When the air is steady"**: [ST-OPP] „Try to observe it every clear night if you
  can, the better to catch nights of calm and steady seeing when the planet sits
  rock-steady and sharp"; and „The big yellow planet rippled in the turbulent air
  like a flag in the wind". [ST-BBB] „Depending on the size of your scope and the
  quality of the night's seeing".
- **Belts in a small scope**: [ST-GRS] „Its two main cloud belts appear in most any
  backyard setup"; the 2.4-inch quote under "Through a small telescope" above.
- **Wording guard (LOW)**: [JF] says the deep interior is liquid („gases and
  liquids"; „an ocean made of hydrogen"). „Огромно кълбо от газ" is the gas-giant
  simplification [ST-BBB] itself uses and may ship; never extend it to "gas all the
  way to the centre". „Газов гигант" is the standard Bulgarian term if one is taught.

#### 3. The Great Red Spot is often pale and hard to see in a small telescope, and is well placed only while Jupiter's spin turns it toward us

- **Status**: **VERIFIED** (full page) **with a wording correction**: „often pale",
  not an unconditional „faint and pale".
- **Quotes**: [ST-TR] „in recent decades it has generally been a much less
  conspicuous pale tan"; „for something so famous, it can be surprisingly
  difficult to see"; „Features on Jupiter appear closer to the central meridian
  than to the limb — and thus are well placed for viewing — for 50 minutes before
  and after their transit times". [ST-BBB] colour „brick red (very rarely), pale
  orange tan (more often), pinkish tan, or an almost invisible creamy yellowish";
  „seeing the Great Red Spot is a challenge in a small telescope. Your best
  prospects will be when the spot appears near the middle of Jupiter's disk … The
  planet's rapid rotation means that these windows of opportunity last only a
  couple hours".
- **Counter-evidence, recorded**: [ST-OPP] (2019 season) says the spot „maintains
  its orange-red hue" and is „easy to see at 100× and higher in good seeing";
  [ST-GRS] notes it had „taken on a distinctly orange color" in 2014. The colour
  varies from year to year, so the art is pale-to-orange, never poster-red, and the
  text never says "always faint". **No size** („twice Earth" stays DISPUTED; [ST-BBB]
  repeats it and [ST-OPP] says „about 1.3 Earths" — they disagree, which confirms
  the DISPUTED entry).

#### 4. The four moons circle Jupiter, each at its own pace, closer ones faster; drawn at true relative scale

- **Status**: **VERIFIED** (full page). Values for `data/reference/` rows only —
  **never player text** (rule 2).
- **Quotes**: [EU] „every time Ganymede orbits Jupiter once, Europa orbits twice,
  and Io orbits four times"; [GA] „Ganymede completes an orbit around Jupiter about
  every seven Earth days (7.155)"; [CA] „Callisto takes about 17 (16.689) Earth days
  … Callisto is about 1.8 times farther from Jupiter than Ganymede, 2.8 times
  farther than Europa and 4.5 times farther than Io"; [EU] „Europa orbits Jupiter
  every 3.5 days". [IO] gives no period.
- **Values** ([NSSDC-JS], „Orbital Period* (days)", „Semi-major axis (10³ km)",
  „Semi-major axis (Jovian Radii)", „Radius (km)"; Jovian radius used there =
  71,492 km):

  | Moon     | Period (d) | a (10³ km) | a (R_J) | Radius (km) | NASA facts page cross-check            |
  | -------- | ---------- | ---------- | ------- | ----------- | -------------------------------------- |
  | Io       | 1.769138   | 421.8      | 5.91    | 1821.5      | „422,000 kilometers"; no period        |
  | Europa   | 3.551181   | 671.1      | 9.40    | 1560.8      | „671,000 kilometers"; „every 3.5 days" |
  | Ganymede | 7.154553   | 1070.4     | 14.97   | 2631.2      | „1,070,000 kilometers"; „7.155"        |
  | Callisto | 16.689017  | 1882.7     | 26.33   | 2410.3      | „1,883,000 kilometers"; „16.689"       |

- **Jupiter's radius**: [JF] „With a radius of 43,440.7 miles (69,911 kilometers)"
  — this is the **volumetric mean**; [NSSDC-J] „Equatorial radius (1 bar level)
  (km) 71,492", „Volumetric mean radius (km) 69,911". **Draw with 71,492 km** so the
  disc matches the R_J column above; mixing the two shifts every orbit by 2.3%.
- **Trap — do not use [SSD] "P" for Io and Europa.** The JPL mean-element table
  lists P = 1.762732 d (Io) and 3.525463 d (Europa) — 0.4% and 0.7% off the
  sidereal periods above (the mean elements are "a precessing ellipse … fit in a
  least squares sense" and the page warns they are "not intended for ephemeris
  computation"). Its semi-major axes (421,800 / 671,100 / 1,070,400 / 1,882,700 km)
  and Ganymede/Callisto periods agree with [NSSDC-JS]. Cite [NSSDC-JS].
- **Guard**: no periods, radii or dates on screen; the target line-up is generated
  from the model; Callisto is not drawn locked to the 1:2:4 rhythm (the resonance
  quote names only Io, Europa and Ganymede).

#### 5. We see the moons' orbits almost edge-on, so they appear strung along a line through Jupiter

- **Status**: **VERIFIED** (full page) — was NEEDS SOURCE.
- **Quotes**: [ST-BBB] „We see their orbits almost exactly edge on." — in the same
  passage as „a line of three or four tiny stars". [EU] „Jupiter's equator (and
  the orbital plane of its moons) is tilted … by only 3 degrees" — the four share
  one plane. The "so" is the geometry of a circle seen edge-on; the edge-on strip
  shows it.
- **Guard**: „almost" edge-on, never "exactly"; "along a line", never "in a
  perfectly straight row".

#### 6. Galileo saw the four moons move, worked out they circle Jupiter, and so showed that not everything circles Earth

- **Status**: **VERIFIED** (full page) **with a wording correction**.
- **Quotes**: [NSN] „Galileo famously chronicled the four moving dots near Jupiter
  and surmised that they were orbiting the distant world"; [ST-BBB] „he soon
  realized they were actually circling around Jupiter"; [IO] and [GA] (same
  sentence on both): „The discovery … was the first time a moon was discovered
  orbiting a planet other than Earth. The discovery … eventually led to the
  understanding that planets in our solar system orbit the Sun, instead of our
  solar system revolving around Earth."
- **Wording correction**: Galileo **saw the dots move and worked out** that they
  circle Jupiter (NSN „surmised") — not "saw them move around Jupiter". "Showed
  that not everything circles Earth" is carried by „a moon … orbiting a planet
  other than Earth". **Never** "proved Earth goes round the Sun" and never "first
  proof": NASA says only „eventually led to". No year on screen.

#### 7. Sometimes fewer than four show, because a moon can pass behind Jupiter or in front of it

- **Status**: **VERIFIED** (full page) — was NEEDS SOURCE.
- **Quotes**: [ST-BBB] „You'll probably see all four — but possibly only three
  depending on when you look. The count often changes from night to night (or if
  you're patient, even from hour to hour). That's because while orbiting Jupiter
  they sometimes glide in front of the planet, behind it, or through its shadow."
  [ST-OPP] „Don't expect to see all four all the time as one or other often pass in
  front or behind the planet."
- **Guard**: the page names a third cause — Jupiter's **shadow**. "Behind or in
  front" is true but not complete; never say those are the only reasons. The
  design's "a moon in front is never drawn as a bright dot over the disc" is an
  art caution, not a sourced claim.

#### 8 and 15. Ganymede is the largest moon in the Solar System and wider than Mercury; the J3 discs

- **Status**: **VERIFIED** (full page).
- **Quotes**: [GA] „Jupiter's moon Ganymede is the largest moon in our solar
  system, bigger than the planet Mercury and dwarf planet Pluto"; „Ganymede's
  diameter is about 3, 270 miles (5,260 kilometers)". [JF] „Ganymede is the largest
  moon in the solar system (even bigger than the planet Mercury)". [ME] „With a
  radius of 1,516 miles (2,440 kilometers)".
- **Drawing values**: Ganymede radius **2631.2 km** [NSSDC-JS] (diameter 5,262 km);
  Mercury diameter **4,879 km** [NSSDC-P]. Ratio **1.079** — about 8% wider, drawn
  true, never exaggerated.
- **Guard**: „по-широк" / „по-голям на ръст"; never heavier (NOT ATTESTED —
  Mercury's mass is about twice Ganymede's). Imagery public-domain, never AI.

#### 9. Planets shine only by reflected sunlight and look bright because they are far closer (`fact.brightest-why`)

- **Status**: **VERIFIED** (full page) — adds the quote the earlier entry lacked.
- **Quote**: [VAN] „Planets are not stars. They do not produce their own light,
  like stars. The light you see from planets … is that reflected from the sun";
  „to us the planets look as bright or brighter than most stars because they are
  much closer to us."
- **Guard**: carry both "reflected" and "near".

#### 9a. The brightest "star" in the evening can be a planet: Jupiter outshines Sirius

- **Status**: **VERIFIED** — rests on "The brightest "star" in the evening sky is
  usually a planet" above. Re-read today: [NSSDC-J] „Maximum apparent visual
  magnitude -2.94", „Apparent visual magnitude -2.7" (mean at opposition); Sirius
  −1.44 in `data/generated/stars.json` (HIP 32349, re-read). No Venus, no magnitudes.

#### 10. Jupiter and Sirius are both in the Bulgarian evening sky, February–April 2027, about 50° apart

- **Status**: **VERIFIED** (computed; data spot-checked independently).
- **Separation** from `orbital-positions.json#/bodies/jupiter` and Sirius in
  `stars.json`: **54.0° (02-01), 51.9° (03-01), 50.5° (04-01), 50.4° (04-15)**. Say
  "about 50°" only in this file; the scene draws the true angle.
- **Altitudes at the end of civil twilight, Sofia** (skyfield + committed
  `de440s.bsp`): 02-01 Sirius 11.6°, Jupiter **2.7°** (still rising); 03-01 27.8° /
  32.2°; 04-01 27.7° / 59.7°; 04-15 20.7° / 64.0°; 04-30 Sirius **9.8°**. So both
  are well up from **late February to mid-April**; early February needs an hour
  after dusk. No date on screen, so this changes nothing the player sees.
- **Frame — the guard needs correcting.** The committed Jupiter `raHours` /
  `decDegrees` match JPL Horizons **astrometric ICRF** positions (quantity 1) to
  0.0004 h and 0.002° on 2027-02-01, 03-01 and 04-15, and `distanceAu` to 10⁻⁶ AU.
  They differ from Horizons **apparent of-date** RA/Dec (quantity 2) by 0.025 h /
  0.12° — exactly the 2000→2027 precession. So the "apparent" in the file's
  `_readme` is skyfield's ICRS-frame apparent place, **not of-date**. Jupiter and
  Sirius are therefore already in the **same (ICRS/J2000) frame** and the
  separation above is frame-consistent. The guard should read "both ICRS", not
  "apparent RA/Dec vs catalogue epoch". Anyone converting one of them to of-date
  coordinates alone introduces a ~0.4° error.

#### 11. Jupiter spins faster than any other planet: it has the shortest day

- **Status**: **VERIFIED** (full page).
- **Quotes**: [JF] „Jupiter has the shortest day in the solar system. One day on
  Jupiter takes 9.9 hours"; [ST-BBB] „Among the planets, Jupiter has the fastest
  spin (once every 10 hours)". [NSSDC-P] Length of Day: Jupiter 9.9 h, Saturn
  10.7 h, the next shortest. No hours on screen.

#### 12. While Earth turns once, Jupiter turns more than twice, and both turn the same way

- **Status**: **VERIFIED** (full page).
- **Values**: [NSSDC-J] „Sidereal rotation period (hrs) 9.9250* 23.9345 0.415"
  (Jupiter, Earth, ratio; *System III). Earth/Jupiter = **2.41**. [EF] „it completes
  one rotation every 23.9 hours"; [JF] „9.9 hours".
- **Same direction**: [NSSDC-P] Rotation Period row: Earth **23.9**, Jupiter
  **9.9** (both positive; Venus −5832.5, Uranus −17.2); [NSSDC-N] „Negative numbers
  indicate retrograde (backwards relative to the Earth) rotation."
- **Guard**: the ratio is drawn, never stated; no hour marks. "More than twice" —
  never "two and a half".

#### 13. Jupiter's fast spin helps stretch its clouds into long bands

- **Status**: **VERIFIED** (full page) — was NEEDS SOURCE.
- **Quote**: [JF] „Jupiter's fast rotation – spinning once every 10 hours – creates
  strong jet streams, separating its clouds into dark belts and bright zones across
  long stretches." Same page, hedge: „Researchers are still trying to solve the
  mystery of how the jet streams form."
- **Guard**: "helps" — the spin drives the winds and the winds draw out the bands.
  Never "the spin paints the stripes", and never a full explanation of how the jets
  form (NASA calls that open).

#### 14. Jupiter pulls much harder than Earth (new completion-line key, e.g. `fact.jupiter.complete`)

- **Status**: **VERIFIED** (full page, live).
- **Values**: [NSSDC-J] „Gravity (mean, 1 bar) (m/s 2 ) 25.92 9.82 2.640";
  „Acceleration (eq., 1 bar) … 23.12 9.78 2.364". Either column gives "much
  harder" (2.4–2.6×). [JF] „As a gas giant, Jupiter doesn't have a true surface."
- **Guard**: only „дърпа" / „притегля". Never falls, lands, stands or weighs; no
  surface; no number. `fact.gravity-drop.bodies` is deleted in the build.

### Saturn level — the claims ticket 011 adopts

Adopted by `docs/wayfinder/road-to-v1/tickets/011-saturn-level-design.md` from
`docs/wayfinder/road-to-v1/research/011-saturn-claims.md` (claim numbers below are
that file's rows). Checked 2026-09-26 by `astronomy-accuracy-checker`. **Method:
full page**: every page was downloaded, stripped to text and searched. No status
rests on a search excerpt. All access dates are **2026-09-26**. Every content key
is **(key TBD by Saturn build)**. **Rule 2**: every number below stays in this
file.

**URL notes.** The NSSDC fact sheets are live (HTTP 200) and are cited live. Sky &
Telescope returns **HTTP 403** to scripts and In-The-Sky serves a bot wall
(Anubis), so both are cited through dated Wayback snapshots. Britannica returns
403 and is cited through Wayback. **PIA03156 is a Hubble Heritage image, not a
NASA/JPL spacecraft frame.** Its caption, read in full, contains neither "changes
angle" nor any ring thickness. Both phrases were misattributed to it by the
search-excerpt research. See the corrected myth and thickness rows below.

Sources read in full, cited by short name:

- **[PIA03156]** NASA Science, _A Change of Seasons on Saturn_ (PIA03156, 2001;
  credit „NASA and The Hubble Heritage Team (STScI/AURA)")
  <https://science.nasa.gov/resource/a-change-of-seasons-on-saturn/>
- **[SF]** NASA, _Saturn Facts_ <https://science.nasa.gov/saturn/facts/>
- **[TF]** NASA, _Titan Facts_ <https://science.nasa.gov/saturn/moons/titan/facts/>
- **[CR]** NASA Science, _Cassini: Saturn Rings_
  <https://science.nasa.gov/mission/cassini/science/rings/>
- **[DAPH]** NASA Science, _Ripples from Daphnis_
  <https://science.nasa.gov/resource/ripples-from-daphnis/>
- **[KEELER]** J. E. Keeler, _A Spectroscopic Proof of the Meteoric Constitution
  of Saturn's Rings_, ApJ 1, 416 (1895), ADS scan
  <https://articles.adsabs.harvard.edu/pdf/1895ApJ.....1..416K> (PDF, text layer
  read)
- **[SP-YR]** NASA Space Place, _How Long is a Year on Other Planets?_
  <https://spaceplace.nasa.gov/years-on-other-planets/en/>
- **[ITS-EQ]** In-The-Sky.org (D. Ford), _Equinox on Saturn_ (2025-05-06), Wayback
  2026-04-21
  <https://web.archive.org/web/20260421133803/https://in-the-sky.org/news.php?id=20250506_12_100>
- **[ITS-CONJ]** In-The-Sky.org, _Saturn at solar conjunction_ (2026-03-25),
  Wayback 2026-03-23
  <https://web.archive.org/web/20260323061543/https://in-the-sky.org//news.php?id=20260325_12_100>
- **[OBL]** Obliquity SkyEye, _Ring Plane Crossings of Saturn_
  <https://www.obliquity.com/skyeye/misc/ringcrossing.html>
- **[HST-RPX]** NASA Science, _Hubble Views Saturn Ring-Plane Crossing_ (1995)
  <https://science.nasa.gov/missions/hubble/hubble-views-saturn-ring-plane-crossing/>
- **[ESA-RPX]** ESA/Hubble, _Saturn ring-plane crossing_ (opo9525c)
  <https://esahubble.org/images/opo9525c/>
- **[BRIT-K]** Britannica Kids, _Saturn_, Wayback 2026-08-20
  <https://web.archive.org/web/20260820101434/https://kids.britannica.com/students/article/Saturn/345008>
- **[ES]** EarthSky, _Give me 5 minutes and I'll give you Saturn_ (2026-08-18)
  <https://earthsky.org/astronomy-essentials/give-me-five-minutes-ill-give-you-saturn/>
- **[ST-VS]** Sky & Telescope, Alan MacRobert, _Viewing Saturn: The Planet, Rings
  and Moons_ (2013), Wayback 2026-08-13
  <https://web.archive.org/web/20260813092125/https://skyandtelescope.org/stargazing-and-observing/celestial-objects-to-watch/viewing-saturn-the-planet-rings-and-moons/>
- **[BBC-M]** BBC Sky at Night, _How to observe Saturn's moons_
  <https://www.skyatnightmagazine.com/advice/skills/how-observe-saturn-moons>
- **[MVT]** NASA Science, _Moon Viewing Tips_ <https://science.nasa.gov/moon/viewing-tips/>
- **[NSSDC-R]** NASA NSSDC, _Saturnian Rings Fact Sheet_ (last updated
  2022-04-19) <https://nssdc.gsfc.nasa.gov/planetary/factsheet/satringfact.html>
- **[NSSDC-SS]** NASA NSSDC, _Saturnian Satellite Fact Sheet_ (last updated
  2025-07-22) <https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturniansatfact.html>
- **[NSSDC-S]** NASA NSSDC, _Saturn Fact Sheet_ (last updated 2025-03-18)
  <https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturnfact.html>
- **[NSSDC-M]** NASA NSSDC, _Moon Fact Sheet_ (last updated 2024-01-11)
  <https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html>
- **[PCK]** NAIF, `pck00011.tpc` (IAU WGCCRE 2015 rotation elements: Archinal et
  al., CeMDA 130, 22, 2018)
  <https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc>
- **[PIA06230]** NASA Science, _Cassini's View of Titan: Natural Color Composite_
  <https://science.nasa.gov/resource/cassinis-view-of-titan-natural-color-composite/>;
  JPL copy
  <https://www.jpl.nasa.gov/images/pia06230-cassinis-view-of-titan-natural-color-composite/>
- **[PIA20016]** NASA Photojournal, _Peering Through Titan's Haze_
  <https://science.nasa.gov/photojournal/peering-through-titans-haze/>
- **[PIA21923]** NASA Science, _Seeing Titan with Infrared Eyes_
  <https://science.nasa.gov/resource/seeing-titan-with-infrared-eyes/> (supporting)
- **[JPL-USE]** JPL, _Image Use Policy_ <https://www.jpl.nasa.gov/jpl-image-use-policy/>;
  **[NASA-USE]** NASA, _Images and Media_ guidelines
  <https://www.nasa.gov/nasa-brand-center/images-and-media/>
- **[HZN]** JPL Horizons API (observer, geocentric, astrometric), queried
  2026-09-26. Cross-check of the committed ephemeris only.

**Ephemeris spot-check.** Committed `data/generated/orbital-positions.json` Saturn
against [HZN] astrometric: 2026-10-05 RA 0.7381 h / Dec 1.811° / 8.43428 AU vs
0.7378 h / 1.808° / 8.43428 AU; 2027-01-15 0.5925 / 1.221 / 9.61847 vs 0.5926 /
1.222 / 9.61847; 2027-05-31 1.5109 / 6.999 / 10.04528 vs 1.5111 / 7.000 /
10.04527. Units correct (hours, degrees, AU); agreement within 0.0003 h and
0.003°.

#### 1. Saturn's axis keeps pointing the same way in space; the rings lie around its equator and share its tilt

- **Status**: **VERIFIED** (full page + IAU pole model).
- **Tilt and alternation**: [PIA03156] „Saturn's equator is tilted relative to its
  orbit by 27 degrees … As Saturn moves along its orbit, first one hemisphere,
  then the other is tilted towards the Sun." [SF] „Its axis is tilted by 26.73
  degrees with respect to its orbit". [NSSDC-S] „Obliquity to orbit (deg) 26.73".
- **Same direction in space**: [PCK] `BODY699_POLE_RA = (40.589 -0.036 0.)`,
  `BODY699_POLE_DEC = (83.537 -0.004 0.)` (degrees; rates per Julian century).
  Over one Saturn orbit (29.45 years) the pole moves about **0.001°** on the sky.
  "Keeps pointing the same way" is exact for the game. [HST-RPX] names a pole
  precession, but it is a timing detail of hours, not something the model draws.
- **Rings in the equator plane**: [OBL] „Because the rings are in the equatorial
  plane of Saturn, the angle of the rings relative to the Sun also varies between
  0° and 26.7°"; [ITS-EQ] „Saturn's rings are closely aligned with its equator";
  [BRIT-K] „The rings are thin and flat and always lie in the same plane as the
  planet's equator."
- **Guard**: [PIA03156] itself says the planet and rings „nod majestically". That
  is loose phrasing, like "changes angle", and must not be quoted.

#### 2. Over one trip round the Sun we see the rings from above, edge-on, from below, edge-on again, because our viewpoint moves

- **Status**: **VERIFIED** (full page).
- **Quotes**: [ITS-EQ] „This configuration arises twice within each orbit that
  Saturn makes around the Sun, just as the Earth has two equinoxes each year."
  [OBL] „Earth also observes ring plane crossings twice a Saturnian year … the
  Earth either experiences a single crossing event or a triple crossing event."
  [BRIT-K] „Viewers on Earth see the sunlit northern side of the rings for about
  15 years and then the sunlit southern side for about the next 15 years."
- **Viewpoint**: [ITS-EQ] „Our line of sight to Saturn is very closely aligned
  with the line between the Sun and Saturn, because Saturn's distance from the
  Sun and Earth is more than nine times greater than the distance between the
  Earth and Sun." That is the source for viewing the model from the Sun's side.
- **Guard**: "twice each trip". [ITS-EQ], [HST-RPX] and [ESA-RPX] all say „every
  15 years"; [OBL]'s table gives gaps of 15.6 and 13.4 years between Sun
  crossings. Do not copy the „every 15 years" line.

#### 3. Edge-on, the rings shrink to a very thin line that is very hard to see; they are still there

- **Status**: **VERIFIED** (full page) **with a wording correction**: the rings do
  not stop existing, but through a small telescope they can look gone. „They do
  not disappear" must mean "they are still there", never "you can still see them".
- **Quotes**: [ITS-EQ] „When they are viewed edge-on, they can become so thin as
  to be incredibly hard to see." [HST-RPX] „as Saturn approaches the equinoxes of
  its orbit, the rings appear thinner and are more difficult to see"; „Through the
  garden variety backyard telescope, Saturn's rings are much less prominent than
  usual, sometimes invisible"; „Saturn's rings remained virtually invisible as the
  Earth passed through the ring plane". [BRIT-K] „The rings are practically
  invisible when their thin edge is pointed directly at Earth". [ESA-RPX] (the
  Hubble image of 1995-05-22) shows the edge-on rings as a thin line; its caption
  says only „turned edge-on".
- **Guard**: the thin line is drawn in the diagram's inset, which is a model and
  not a telescope view. Never "a telescope always shows the line". Never
  „изчезват". [OBL] itself says „the rings vanish as they appear edge on", which
  is the phrasing this game avoids.

#### 4. In 2026–27 Earth sees the south face of the rings, narrowly open

- **Status**: **VERIFIED** (computed + full page). The monthly table the claims
  file asked for now exists.
- **Computation**: sub-Earth ring latitude from the committed Saturn RA/Dec and the
  [PCK] pole (J2000 values; the century rates are negligible), on the 8th of each
  month: 2026-09 −8.3°, 10 −7.3°, 11 −6.4°, 12 −6.1°, 2027-01 −6.5°, 02 −7.6°,
  03 −9.0°, 04 −10.6°, 05 −12.2°, 06 −13.4°, 07 −14.2°, 08 −14.4°, 09 −14.1°.
  Negative on every day of the window (south face), between 6.1° and 14.4°.
- **Independent check**: [ES] „They'll have a -7.5-degree tilt around
  opposition" (computed: −7.46° on 2026-10-04). [OBL] 2025-03-23 crossing „North →
  South", and the sequence ends „in 2032 when the south pole of Saturn will be
  most inclined toward Earth".
- **Consequence for the "opening steadily" row**: the table shows the rings
  **narrowing** from September to early December 2026, then opening. The Saturn
  myths row stays NEEDS SOURCE as instructed. This table is the evidence for
  whoever next reviews it.

#### 5. Of the five naked-eye planets, Saturn creeps among the stars far more slowly than Mars

- **Status**: **VERIFIED** (full page + committed data).
- **Quote**: [ES] „Saturn takes almost 30 years to orbit the sun. So it moves more
  slowly than the other bright planets in front of the fixed stars." The five:
  the VERIFIED back-cover row (NASA, _Planetary Alignments_).
- **Committed data, 2026-11-01 → 2027-05-31** (summed daily angular steps / net):
  Saturn 17.4° / 14.6°, Mars 57.8° / 18.1°.
- **Guard (HIGH, new)**: in this window **Jupiter moves no more than Saturn**
  (16.0° path, 4.1° net: it loops round its February opposition). S2 must compare
  Saturn with **Mars only**. A Jupiter panel would show the "slowest" claim
  failing on screen. „Най-бавната" stays qualified („от петте, които виждаме с
  просто око") and is taught as a general fact, not as something the window shows
  against every planet.

#### 6. Saturn is far from the Sun, so one trip round the Sun takes a very long time

- **Status**: **VERIFIED** (full page).
- **Quotes**: [SP-YR] „Planets that orbit farther from the Sun than Earth have
  longer years than Earth … This happens for two main reasons. If a planet is
  close to the Sun, the distance it orbits around the Sun is fairly short … The
  closer a planet travels to the Sun, the more the Sun's gravity can pull on the
  planet. The stronger the pull of the Sun's gravity, the faster the planet
  orbits." [SF] „9.5 astronomical units away from the Sun"; „about 29.4 Earth
  years". [NSSDC-S] sidereal period 10,755.699 d.

#### 7. For a few weeks in spring 2027 Saturn is too close to the Sun in our sky to see

- **Status**: **VERIFIED** (full page + independent almanac).
- **Quote**: [ITS-CONJ] (the 2026 conjunction; same mechanism) „At closest
  approach, Saturn will appear at a separation of only 2°07' from the Sun, making
  it totally unobservable for several weeks while it is lost in the Sun's glare."
- **Dates**: [HZN] solar elongation below 15° from **2027-03-22 to 2027-04-25**,
  minimum 2.25° on 2027-04-08. This matches the committed-data result in the
  back-cover row exactly. That row's "not checked against an independent almanac"
  caveat is now closed for Saturn.

#### 8. Titan is Saturn's largest moon, and it is wider than our Moon

- **Status**: **VERIFIED** (full page).
- **Quotes**: [TF] „Titan is the second largest moon in our solar system. Only
  Jupiter's moon Ganymede is larger, by just 2 percent. Titan is bigger than
  Earth's moon, and larger than even the planet Mercury"; „nearly 50 percent wider
  than Earth's moon".

#### 9. Titan has a thick atmosphere, and its haze hides the ground in ordinary light

- **Status**: **VERIFIED** (full page) **with a wording correction**: the haze
  hides the ground **seen from above** (from space). The ESA Huygens probe landed
  under the haze in 2005 ([TF] names its descent).
- **Quotes**: [TF] „the only moon with a thick atmosphere"; „surface is completely
  obscured by a golden hazy atmosphere"; „a thick, orange-colored haze that makes
  the moon's surface difficult to view from space. (Spacecraft and telescopes can,
  however, see through the haze at certain wavelengths of light outside of those
  visible to human eyes.)" [PIA21923] „Observing the surface of Titan in the
  visible region of the spectrum is difficult … small particles called aerosols in
  Titan's upper atmosphere strongly scatter visible light."

#### 10. Cassini saw Titan's surface through the haze in infrared light

- **Status**: **VERIFIED** (full page).
- **Quote**: [PIA20016] „A view at visible wavelengths (centered around 0.5
  microns) would show only Titan's hazy atmosphere … The near-infrared wavelengths
  in this image allow Cassini's vision to penetrate the haze and reveal the moon's
  surface." [PIA21923] „the VIMS instrument excelled, parting the haze to obtain
  clear images of Titan's surface."

#### 11. Our Moon shows craters when you look closer

- **Status**: **VERIFIED** (full page; the Moon row above rested on a search
  excerpt, and this read confirms it).
- **Quote**: [MVT] „Pick up a pair of binoculars, and the Moon transforms … Smooth-
  looking patterns of gray and white resolve into craters and large mountain
  ridges." Also: „for better viewing of craters and mountains, try phases other
  than the full Moon."
- **Guard**: draw the Moon disc part-lit or with terminator shadows, not flat full.

#### 12. Saturn's rings are not a solid disc: each piece goes round Saturn on its own

- **Status**: **VERIFIED** (full page).
- **Quotes**: [KEELER] „The hypothesis that the rings of Saturn are composed of an
  immense multitude of comparatively small bodies, revolving around Saturn in
  circular orbits, has been firmly established … a solid or fluid ring could not
  exist"; the spectrograms are „the first direct proof". [SF] „billions of small
  chunks of ice and rock"; „each ring orbits at a different speed around the
  planet."

#### 13. The inner pieces go round faster than the outer ones

- **Status**: **VERIFIED** (full page): primary source plus two NASA pages. S4
  stands.
- **Primary**: [KEELER] „if the ring rotated as a whole the velocity of the outer
  edge would exceed that of the inner edge … If, on the other hand, the ring is an
  aggregation of satellites revolving around Saturn, the velocity would be
  greatest at the inner edge"; „the photographs prove not only that the velocity
  of the inner edge of Saturn's ring exceeds the velocity of the outer edge, but
  that … the relative velocities at different parts are such as to satisfy
  Kepler's third law." His table: inner edge 21.01 km/s, outer edge 17.14 km/s.
- **NASA**: [CR] „The ring particles nearer Saturn move faster than the moonlet
  while those farther from Saturn move slower than the moonlet". [DAPH] „Material
  on the inner edge of the gap orbits faster than the moon … Material on the outer
  edge moves slower than the moon". [SP-YR] gives the same rule for planets.
- **Not usable**: [SF] says only „each ring orbits at a different speed", with no
  direction. JPL _Slower Spinning Rings_ (PIA03562) is about particle
  temperature and spin. It is not about orbital speed and must not be cited here.

#### 14. Saturn's tilt gives it seasons, just as Earth's tilt gives Earth seasons

- **Status**: **VERIFIED** (full page).
- **Quotes**: [PIA03156] „This cyclical change causes seasons on Saturn, just as
  the changing orientation of Earth's tilt causes seasons on our planet." [SF]
  „This means that, like Earth, Saturn experiences seasons."
- **Guard**: "like Earth", never "only because of the tilt". Saturn's orbital
  eccentricity is 0.054 ([NSSDC-S] mean elements), about three times Earth's.

#### 15. Through a small telescope Titan is only a dot; the game's Titan close-ups are spacecraft pictures

- **Status**: **VERIFIED** (computed + full page) **with a wording correction**:
  "through a small telescope", not "even through a telescope". [TF] says
  „Spacecraft **and telescopes** can … see through the haze" at non-visible
  wavelengths. Never "only a spacecraft can see Titan's ground".
- **Seen**: [ST-VS] „A 2-inch scope will show Titan." [BBC-M] „When you're gazing
  at it through your scope, you're not actually looking at Titan's surface but at
  its nitrogen-rich cloud tops"; mag +8.4.
- **Dot, computed**: Titan's diameter (2 × 2,575 km, [NSSDC-SS]) at the committed
  Saturn distances 8.434–10.378 AU is **0.84″–0.68″**. The Dawes limit of a 60 mm
  aperture is 116/60 = 1.9″, so Titan is unresolved in any small telescope.
- **Guard**: label every close-up a spacecraft view. [BBC-M] and search results
  call Titan "orangish" in a scope. Never promise the colour.

#### 16. Titan's orange haze colour, as drawn: Cassini ISS natural-colour frame PIA06230

- **Status**: **VERIFIED** (full page). **Pick: PIA06230**; alternate PIA14602.
- **Quote**: [PIA06230] „a combination of images taken through three filters that
  are sensitive to red, green and violet light. It shows approximately what Titan
  would look like to the human eye: a hazy orange globe surrounded by a tenuous,
  bluish haze. The orange color is due to the hydrocarbon particles". Instrument:
  Imaging Science Subsystem, Wide Angle; 2005-04-16.
- **Credit line (from the page)**: „NASA/JPL/Space Science Institute". Alternate
  PIA14602 _Hazy Orange Orb_
  <https://science.nasa.gov/resource/hazy-orange-orb/>: „natural color view",
  credit „NASA/JPL-Caltech/Space Science Institute".
- **Guard**: "what a spacecraft camera saw", never "what your telescope shows".

#### 17. The Moon's and Titan's radii, as drawn

- **Status**: **VERIFIED** (full page, live).
- **Values**: [NSSDC-SS] Titan radius **2,575 km**; [TF] „2,575 kilometers".
  [NSSDC-M] Moon volumetric mean radius **1,737.4 km** (equatorial 1,738.1).
  Ratio **1.482**, which matches [TF] „nearly 50 percent wider". The radius is the
  solid body; draw the haze as a thin rim outside it, not as a larger disc.

#### 18. The ring radii that set S4's relative speeds

- **Status**: **VERIFIED** (full page, live).
- **Values** [NSSDC-R] (km from Saturn's centre): Saturn equator **60,268**; C
  inner edge **74,658**; C outer = B inner edge **91,975**; B outer edge
  **117,507**; A outer edge **136,780**.
- **Speeds** (Kepler: v ∝ r^−½, from row 13), relative to the A outer edge: C
  inner **1.354**, B inner **1.220**, B outer **1.079**, A outer **1.000**.
  Periods C inner : A outer ≈ **1 : 2.48**. Computed at build time; never shown.

#### 19. Cassini visible and infrared Titan frames: licence and credit

- **Status**: **VERIFIED** (full page).
- **Infrared pick: PIA20016**, _Peering Through Titan's Haze_ (VIMS, T-114 flyby,
  2015-11-13). Credit line from the page: „NASA/JPL/University of Arizona/
  University of Idaho". Supporting: PIA21923 (six global VIMS mosaics from 13
  years), credit „NASA/JPL-Caltech/Stéphane Le Mouélic, University of Nantes,
  Virginia Pasek, University of Arizona" (JPL copy: „NASA/JPL-Caltech/University
  of Nantes/University of Arizona").
- **Visible pick: PIA06230** (row 16), „NASA/JPL/Space Science Institute".
- **Licence**: no page carries a copyright mark. [JPL-USE] „Unless otherwise
  noted, images and video on JPL public web sites … may be used for any purpose
  without prior permission". [NASA-USE] „NASA content … generally are not subject
  to copyright in the United States … NASA should be acknowledged as the source";
  third-party copyright material „will be marked". The university names are part
  of the credit line, so ship the credit exactly as the page gives it.
- **Guard (MEDIUM)**: PIA20016 is **false colour** („blue represents wavelengths
  centered at 1.3 microns, green … 2.0 microns, and red … 5.0 microns"). Label it
  as an infrared camera picture. A child must not read its colours as Titan's
  ground colours.

---

## Stars and constellations

### Orion's Belt — the brief's claim is FALSE, and the truth is better

- **Claim in the brief**: the belt's _brightest-looking_ point resolves into
  multiple stars as you zoom in.
- **Status**: **RESOLVED — the claim is false and was never shipped.** Verified
  2026-09-08.
- **What is actually true — the claim is exactly inverted.** The brightest belt
  star is **Alnilam (ε Ori, V = 1.69)** and it is the **only single star of the
  three**. Alnitak (ζ Ori) is second at V = 1.74 and has **four**
  components; Mintaka (δ Ori) is faintest at V = 2.25 and has **five**, in the
  hierarchy [(Aa1 + Aa2) + Ab] + (Ca + Cb). There is no reading of "brightest"
  — combined or primary-alone — under which the brief's version survives.
- **Source**: Oplištilová, Brož, Hummel et al., _"VLTI observations of the Orion
  Belt stars: I. ε Orionis"_, **A&A 704, A204 (2025)**,
  doi:10.1051/0004-6361/202556154 — ε Ori "represents the only massive single
  star in Orion's Belt". https://arxiv.org/abs/2507.02276
  **Magnitudes are quoted from Hipparcos I/239** (1.69 / 1.74 / 2.25), which is
  what `data/generated/stars.json` holds. SIMBAD (Ducati 2002) gives 1.77 for
  Alnitak and 2.23 for Mintaka on a different photometric system. The two agree
  on the only thing the game claims — the brightness _order_, and that the
  brightest is the single star — but the repo quotes the catalogue it ships.
- **The teaching point this unlocks**: the brightest-looking dot is the lonely
  one, and the faintest is a family of five. Brightness tells you nothing about
  how many stars are there. That is a better lesson than the brief's version.
- **Separations, if an Orion split is ever built** (from SIMBAD ICRS J2000,
  cross-checked against WDS/ORB6): δ Ori A–C **52.3″** (binoculars); δ Ori Aa–Ab
  **0.26″**; δ Ori Aa1–Aa2 spectroscopic + eclipsing, P = 5.7324 d. ζ Ori A–B
  **2.42″**; ζ Ori Aa–Ab **0.036″** (Hummel et al. 2013, A&A 554, A52),
  interferometry only. Use **Mintaka**, not Alnitak — ζ Ori's only
  amateur-reachable split is 2.42″ at a 1.7-mag contrast, which cannot be made
  honest at storybook zoom.

### Mizar and Alcor — the primary `zoom-split-star` target

- **Claim** (`fact.mizar-alcor.*`): what looks like one star in the handle of
  Колата separates into more stars at each level of magnification, and there are
  six in total.
- **Status**: **VERIFIED** 2026-09-08.
- **The zoom ladder, each rung sourced**:
  1. Naked eye — one point. Mizar, combined V = 2.04.
  2. Sharp eye or binoculars — Alcor appears at **708.6″ (11.8′)**, V = 3.99.
     Recomputed 2026-09-08 from `data/generated/stars.json` (HIP 65378, 65477):
     **708.6″ = 11.81′**, and independently from Hipparcos-2: 708.4″. Pinned by
     `tests/test_star_catalogue.py::test_mizar_and_alcor_are_708_arcsec_apart`.
     The classic eyesight test, confirmed experimentally: Bohigian, _"An Ancient
     Eye Test — Using the Stars"_, Surv. Ophthalmol. **53** (2008) 536.
  3. Small telescope — Mizar splits into A (V 2.22) and B (V 3.88) at **14.40″**
     (WDS 13239+5456 STF1744 AB, magnitudes 2.230 / 3.88; the 14.44″ previously
     recorded here is the same split at a different measurement epoch).
  4. Instruments only — Mizar A is a spectroscopic binary (P = 20.54 d, the
     **first ever discovered**), Mizar B likewise (P = 175.06 d), and Alcor has
     a red-dwarf companion at ~1″ (Zimmerman et al. 2010, ApJ 709, 733; Mamajek
     et al. 2010, AJ 139, 919).
  - **Six stars, all gravitationally bound** — 100% probability, Shaya & Olling
    2011, ApJS 192, 2. Distance ~83 ly.
    https://en.wikipedia.org/wiki/Mizar_and_Alcor
- **Why this and not a belt star**: Ursa Major is circumpolar from Bulgaria
  (42–44° N) — visible every clear night, all year. Orion is winter-only. A
  child can perform rung 2 the evening they play the level.
- **Wording constraint**: 11.8′ is about two-fifths of the Moon's diameter.
  Content must say Mizar and Alcor **look like** one star, never that they _are_
  one star, and rung 2 is "another appears beside it", not "it splits".

### The Pleiades — one smudge, a thousand stars

- **Claim** (`fact.kvachka`): the naked eye sees a handful, binoculars show
  dozens, and the cluster really contains far more.
- **Status**: VERIFIED. NASA, Messier 45: "contains over a thousand stars",
  ~445 ly, apparent magnitude 1.6, best observed in December.
  https://science.nasa.gov/mission/hubble/science/explore-the-night-sky/hubble-messier-catalog/messier-45/
  Naked-eye count 6–7 (Ангел Бонов). Galileo's _Sidereus Nuncius_ (1610) plate
  showed **36 stars beyond the six known**.
- **Culminates at 71.5°** from Bulgaria, best in the game's winter play season.
- **The folk count is reproducible from data, not merely attested.** A 1.5° cone
  search of HYG v4.4 on the cluster centre returns 4 stars at mag ≤ 4.0, **6 at
  ≤ 5.0, 7 including Pleione at ≤ 5.05**, 11 at ≤ 6.0 and 25 at ≤ 7.0. Георгиева's
  "кокошка с 6—7 пиленца" and Бонов's naked-eye 6–7 fall straight out of the
  catalogue at the naked-eye threshold. The folk name encodes a real magnitude
  limit, which is exactly the standard ADR 0005 sets for a folklore beat.

### Brightest stars, for the connect-the-dots level

- **Orion**: **Rigel (β Ori, V = 0.18)** is the brightest. Betelgeuse (α Ori) is
  the Bayer α but is usually _second_, V ≈ 0.50 mean, varying **0.0–1.6** — the
  widest range of any first-magnitude star (AAVSO VSX; en.wikipedia Betelgeuse).
  Hipparcos I/239 caught it at 0.45 — a single epoch of a variable star, which
  is why the range and not the number is what content may rely on. Rigel's 0.18
  is likewise Hipparcos; older references quote 0.13.
  Status VERIFIED. **A string saying Betelgeuse is Orion's brightest star is
  false and must not ship.**
- **Ursa Major**: Alioth (ε UMa, V = 1.76) is brightest, Dubhe (α UMa) 1.81.
  Status VERIFIED **but must not become a player task** — a 0.05-mag margin is
  invisible to the eye and to the screen, and asking a child to spot it teaches
  that magnitude differences are visible when they are not. Teach the shape.
  _Corrected 2026-09-08_: this entry previously said 1.77 / 1.79, a 0.02 margin.
  `data/generated/stars.json` (HYG v4.4, HIP 62956 and 54061) gives 1.76 / 1.81.
  The conclusion is unchanged and slightly better supported, but the repo must
  not hold two magnitude pairs that contradict each other.
- **Albireo (β Cyg)**: **DISPUTED — do not use.** Whether A and B form a
  physical binary or are an optical double is unresolved (Bastian & Anton 2018,
  A&A 620, L2; Gaia DR2 astrometric noise). Do not teach an unsettled binary as
  a binary.
- **Trapezium (θ¹ Ori)**: VERIFIED as a genuine multi-star split (A–B 8.85″,
  A–C 12.86″, C–D 13.41″). Good as a _second_ panel, not the primary — the
  nebulosity competes with the "one dot becomes several" reading, and six stars
  need ~5″ aperture.

---

## Star catalogue and constellation figures

Resolved 2026-09-08. This was the blocking entry: every constellation claim
above needs real positions and magnitudes, and rule 1 forbids typing them into a
scene. They are now generated by `data/scripts/star-catalogue.py`.

### What ships

| File                                      | Contents                                       | Size   |
| ----------------------------------------- | ---------------------------------------------- | ------ |
| `data/generated/stars.json`               | 2,851 stars, `[hip, raHours, decDegrees, mag]` | 106 KB |
| `data/generated/constellation-lines.json` | 88 figures as HIP polylines                    | 11 KB  |
| `data/generated/star-names.json`          | 2,106 designations — authoring metadata only   | 117 KB |

The magnitude cut is **5.5**, not the naked-eye 6.5. 6.5 is 8,921 stars and
draws an undifferentiated wash of dots; 5.5 draws a sky a child in a Bulgarian
town recognises. Every star any figure references is added back regardless of
magnitude, so lowering the cut further cannot break a constellation. Raise it
with `--mag 6.5` if a puzzle ever demonstrably needs it.

`star-names.json` is **authoring metadata, not player content**. Every
player-facing string lives in `content/bg/` per rule 3; this file exists so a
level author can find out which HIP number is Ригел without typing a position.

### A catalogue that was rejected — NOT ATTESTED as usable

**IAU/WGSN "Naked Eye Catalog" (NEC.csv, May 2025), exopla.net — REJECTED.**
It is the obvious candidate: IAU-published, cut at exactly V ≤ 6.5, carrying the
official proper names, HIP/HR/HD and distances. It is also **corrupt**. Cross-
matching all 8,895 rows carrying a HIP number against Hipparcos-2 finds **15
stars with grossly wrong right ascension, 11 of them by more than a degree** —
including **Mizar, off by 3.2° (11,545″)**, this game's primary
`zoom-split-star` target. Declination is correct in every case; it is an RA-only
corruption on a subset.

Recorded here so it is not re-proposed. The failure it would have produced is
the exact defect class rule 1 exists for: the file loads, validates against the
schema, passes every bounds check, and silently places Mizar three degrees from
Alcor instead of eleven arcminutes.

**This is why the generator verifies against a second source.** Checking a
catalogue against its own generator proves nothing. `star-catalogue.py` re-checks
every emitted position against Hipparcos-2 (VizieR I/311) at build time and
**fails the build** on any disagreement over 30″, excluding four
high-proper-motion stars whose HYG/Hipparcos epoch difference is real
(Groombridge 1830, 61 Cyg A and B, Keid). That allowlist is pinned by a test so
it cannot be used to wave a real error through.

### Two traps in the figure data

1. **Stellarium's `modern` skyculture mixes 19-digit Gaia DR3 `source_id`s into
   the same arrays as 5-digit HIP numbers** — 85 of its 997 ids. A naive
   `int → HIP` join drops those segments with no error and draws the
   constellation wrong. We take `modern_iau` (745 ids, all clean, none fainter
   than V 6.47), and the generator rejects any id over six digits regardless.
2. **HIP 55203 does not exist in Hipparcos.** `modern_iau` references it; the
   star is ξ UMa (Alula Australis), which HYG carries from Gliese with an empty
   `hip` field. Resolved through an HR/HD fallback, because dropping it silently
   removes a line from Ursa Major — the constellation the game teaches.

### Never call these figures official

Stellarium's skyculture is _named_ `modern_iau`, which invites the phrase. The
IAU standardised constellation **boundaries** (Delporte 1930) and has **never**
defined stick figures. `modern_iau`'s lines are 87/88 byte-identical to
`modern_st`, which is generated from Sky & Telescope's data. Content says "the
usual way these figures are drawn", never "the official IAU figures".

Boundaries are deliberately not generated. They are B1875 rectilinear arcs that
carve the sky into administrative regions, and they teach a child that a
constellation is a box.

### Licensing

HYG v4.4 and the Stellarium skyculture are both **CC BY-SA 4.0**. Share-alike is
viral over the derived files, so `data/generated/stars.json`,
`constellation-lines.json` and `star-names.json` are themselves offered under
CC BY-SA 4.0, and each carries its `license` and `attribution` in the file. This
does not touch the game code's licence. Nothing here is non-commercial.

### Downloads

`data/raw/` is gitignored, exactly like `data/ephemeris/`. Only the filtered
output in `data/generated/` is committed, so a clean checkout runs without ever
fetching these.

```bash
mkdir -p data/raw/{hyg,skyculture,wds}

# HYG v4.4 — note /media/ not /raw/: Codeberg serves LFS content only from
# /media/, and /raw/ returns a 133-byte pointer that parses as garbage.
curl -sL -o data/raw/hyg/hyg_v44.csv.gz \
  https://codeberg.org/astronexus/hyg/media/branch/main/data/hyg/CURRENT/hyg_v44.csv.gz
echo "00b349893b9a53106dd488d8371e8d2fa586043e500bb3cdb8bff3931682197d  data/raw/hyg/hyg_v44.csv.gz" | sha256sum -c

# Constellation figures
curl -sL -o data/raw/skyculture/modern_iau.json \
  https://raw.githubusercontent.com/Stellarium/stellarium/master/skycultures/modern_iau/index.json

# Verification oracle — MUST be a different source from the catalogue above
curl -sL -o data/raw/hyg/hip2_bright.tsv \
  'https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=I/311/hip2&Hpmag=%3C7.2&-out=HIP,RArad,DErad,Hpmag&-out.max=unlimited'

# Double stars
curl -sL -o data/raw/wds/orb6orbits.txt https://www.astro.gsu.edu/wds/orb6/orb6orbits.txt

venv/bin/python data/scripts/star-catalogue.py
```

`github.com/astronexus/HYG-Database` is **archived** (2025-02-14) and licensed
`NOASSERTION`. Codeberg is the live home. ORB6 is **not in VizieR** — the TAP
schema has ten WDS tables and zero ORB6 — so it comes direct from
astro.gsu.edu. `pas.rochester.edu`'s IAU-CSN mirror did not respond and is not
relied on.

---

## Bulgarian folklore — the bonus layer

Folklore claims are factual claims, and this audience will notice errors. None
of these is the lesson; each is attached to a lesson.

### Зорница and Вечерница — one planet, two names

- **Claim** (`fact.zornitsa`): Зорница (morning) and Вечерница (evening) are
  traditionally treated as two different stars, but are the same object — the
  planet Venus.
- **Status**: **VERIFIED.** Дарина Младенова, _Звездното небе над нас_, БАН 2006,
  с. 52–53 (via Бајић 2020, Proc. XII Serbian-Bulgarian Astronomical Conference,
  p. 158). Other attested Bulgarian names: Деница, Зора, Овчарската звезда,
  Вечерната звезда, Големата звезда.
- **Why it works**: the folklore creates the misconception and the astronomy
  resolves it. This is the model every other folklore beat is measured against.
- **The kinship detail from the brief — DISPUTED, and deliberately not told.**
  The brief has "Зорница = sister of the sun, Вечерница = sister of the moon".
  Two sources conflict:
  - **ИЕФЕМ–БАН** (Валентина Шарланова, "Космогония", citing Маринов, _Народна
    вяра и религиозни народни обичаи_, СбНУ т. 28, 1914): **all stars are the
    Sun's sisters**, and the Moon is herself the Sun's sister — so "sister of the
    Moon" has no slot. A folk song has the hero take from the Sun "his dear
    sister… вечерница и зорница".
  - **Иваничка Георгиева**, _Българска народна митология_, с. 29: "според някои
    вярвания те са две сестри: зорницата е спътница на брат си слънцето, а
    вечерницата — на месеца" — note her own hedge.
  - Јанковић (1951) has Даница as the Sun's sister and the Moon's **cousin**.
  - **Decision**: the game states only that folk tradition calls them sisters,
    and makes no claim about whose. Both sources agree on that much. Revisit only
    with Маринов in hand.

### Кумова слама — removed from the game

- **Status**: the name is **VERIFIED** as a Bulgarian folk name for the Milky Way
  (ИЕФЕМ–БАН; Ангел Бонов), alongside **Попова слама, Сламата, Пато**.
- **The brief was wrong twice**: "кум" is not "groom" — it is the _godfather /
  wedding sponsor_ (groom is "младоженец"), so the name means "the **godfather's**
  straw", a possessive naming the **victim**. And "a groom visiting his best man"
  omits the theft, which is the whole tale: a кумец takes straw from his
  кръстник in a bottomless basket, trails it across the sky, and is cursed.
- **Why it is out**: it teaches a moral about stealing, not about the Milky Way.
  No Bulgarian variant encodes "many stars" — Попова слама, Пато and the
  milk-of-the-moon version all fail the same test. **The fix is not folklore, it
  is Galileo**: the eye says smear, the tube says stars.
- **Trap**: a popular Bulgarian children's book is titled _"Съзвездието Кумова
  слама"_. The Milky Way is a galaxy seen edge-on from inside — **never** write
  съзвездие for it.

### Лъжи керван — Sirius mistaken for the morning star

- **Claim** (`fact.lazhi-kervan`): caravan drivers woke, saw a bright star in the
  east, took it for Зорница and set off far too early.
- **Status**: **VERIFIED.** Иваничка Георгиева, _Българска народна митология_,
  с. 29: "Лъжи керван, мами керван е звезда, вероятно Сириус…". Ангел Бонов
  gives the same tale in fuller form.
- **Why it works**: this is the Зорница pattern _running backwards_. There the
  folklore splits one object into two; here it fuses two into one. The same
  physics resolves both — Venus is tied to the Sun and can never be high in the
  east at midnight; Sirius is a star and can.
- **Checked against our own ephemeris** (Sofia, 2026): Sirius at morning twilight
  +5.3° on 20 Aug, +14.6° on 1 Sep, +26.7° on 22 Sep; at local midnight below
  the horizon until roughly early November. Both sources' timings hold.

### Квачката — the Pleiades as a hen with chicks

- **Claim** (`fact.kvachka`): the folk name is a hen with her chicks.
- **Status**: **VERIFIED.** Георгиева, с. 28: "Квачката (кокошка, стожари,
  власи, власци, влашкови) са съзвездието Плеяди"; бел. 111: "**съзвездието
  квачката се смята за кокошка с 6—7 пиленца**". Бонов: the brightest is the
  hen, the six fainter ones the chicks.
- **Why it works**: the folk name _encodes the naked-eye count_. Nobody has to be
  told the number — the name is the number, and the telescope then breaks it.
- **The seasonal calendar is VERIFIED and astronomically real.** Georgieva frames
  the cluster's heliacal setting and rising as dividing the year. Computed from
  our own `de440s.bsp` for Sofia 2026: Гергьовден (6 May) altitude +6.2° at
  Sun = −8°, gone by 15 May; летен Тодоровден (8 June) +4.2° at morning
  twilight, not yet visible on 1 June. Accurate to within days.
- **DO NOT REPEAT** Georgieva's line that the Pleiades rise _with the Sun_ at
  Димитровден. Read literally that is **false** — they are near opposition then
  (elongation 152.4° on 26 Oct; true opposition 17 Nov). Say they rise as it gets
  dark and are up all night.
- **"Бабите" is NOT ATTESTED** in either primary source. The forms власи /
  власци / влашкови are attested but their etymology is contested — do not gloss
  them as "Wallachian stars".

### Bulgarian constellation names

- **Orion = Рало / Ралица**; **Ursa Major = Колата**.
- **Status**: **VERIFIED (secondary)** — Христо Вакарелски, _Етнография на
  България_, София 1977, стр. 413, as cited by bg.wikipedia for both. Promote to
  primary once p. 413 is read directly.
- **Source, now fully identified**: доц. Ангел Бонов, _Митове и легенди за
  съзвездията_, София: „Наука и изкуство“, 1976, 281 с. Full text digitised at
  chitanka.info. His own chapter titles are „Орион (Ралица)“ and „Голяма мечка
  (Колата)“, so he independently attests both folk **names**.
  **Page numbers: NEEDS SOURCE** — the digitisation carries no pagination.
  **Caveat on his authority**: his 8-item bibliography contains **no Bulgarian
  ethnographic source at all**. He is a populariser, not an ethnographic primary,
  for the star-by-star assignment. The mapping as a whole is **NEEDS SOURCE**.

- **Ралица — Бонов's actual words**: рало = δ,ε,ζ (the Belt) + σ,θ,χ; орач =
  Сириус; остен = η,τ,β; кучето на орача = Процион; воловете = Бетелгейзе (α),
  Белатрикс (γ).
  **The χ component is DISPUTED and must not ship.** Checked against our own
  `data/generated/stars.json`: χ¹ Ori (HIP 27913) is Dec **+20.28°**, sitting
  **21.9° from Alnilam** — further than the whole Rigel–Betelgeuse span (18.6°).
  `data/generated/constellation-lines.json` places χ¹/χ² on Orion's **club**
  branch (`Xi–Chi-2–Chi-1–Nu`), while the leg branch is `Alnitak–Kap/Saiph`.
  Бонов's gloss "образуват десния крак" therefore contradicts his own letters.
  The star actually on the leg is **κ Ori / Saiph**, but **do not substitute it by
  reasoning** — that needs the print page.

- **Бонов's Greek letters in these two passages are demonstrably unreliable.**
  In the same book he writes „Мечката — звездата **Мицар (ξ)**“. Mizar is **ζ**
  UMa; ξ UMa is Alula Australis, not in the Dipper at all. Two wrong letters in
  the only two folk-mapping paragraphs is a pattern — either 1976 typesetting or
  the 2011 OCR. **No Greek letter from these passages may be transcribed into
  game data** until the print is read.

- **Колата — corrected. The earlier entry here misattributed a mapping to Бонов.**
  It previously read "колела = α,β,γ,δ; волове = ε,ζ; вълк = η", which is wrong on
  ε, ζ and η. Бонов verbatim: „Коларят — звездата η, Мечката — звездата Мицар (ξ),
  Волът — звездата ε, а кучето, което лае по мечката, е звездата Алкор.
  Останалите ярки звезди образуват Колата.“
  Вакарелски p. 413 (via bg.wikipedia) differs again: a wagon showing „колелата,
  воловете и вълк, който напада воловете“ — the wolf is in the scene, but **no
  star is named for it**.

- **"вълк" = η UMa is NOT ATTESTED.** Do not re-propose it. The wolf motif is
  attested for both figures, but attaching it to η specifically appears in no
  source — and Бонов contradicts it outright, giving η = Коларят.

- **The variant the game does not tell**: Бонов tells the **wide** variant — a
  ~30°-wide scene spanning three IAU constellations (Alnilam→Procyon is 31.4°).
  **The game tells the narrow variant (Орион = Рало)**, following Вакарелски
  p. 413: „осем звезди, в които се виждат орач, остен, а понякога и вълци“ —
  **which eight is not stated**, so the narrow star list is NEEDS SOURCE.
  Corroboration for the wide reading is now better than blog-level: a НАО Рожен
  contributor on forum.starrydreams.com thread 5211.

- **"Косери" is NOT ATTESTED for Orion.** Do not use it.

- **Mizar = "Мечката" / Alcor = "кучето" — upgraded from PLAUSIBLE to
  Бонов-attested** (1976, verbatim, quoted above; the ξ typo affects the letter,
  not the proper names). The tale attached: a bear ate one ox, the youth harnessed
  the bear in its place, it pulled sideways, „за това в съзвездието колата е
  разкривена“. **The dog barking at the bear _is_ Alcor** — the folk name is the
  naked-eye split, which makes this a genuine ADR 0005 pass for the
  `zoom-split-star` beat.

- **Terminology, so it is not mangled later**: a **рало** is an ard (symmetrical
  scratch plough), never a плуг (mouldboard). An **остен** is the ox-goad, not the
  plough handle. Note the collision between **Коларят** (η UMa, per Бонов) and the
  constellation **Колар (Auriga)**, which Бонов also uses.

- **Closing the star-by-star mapping needs a library visit** — Дарина Младенова,
  „Български диалектни названия на съзвездието Орион“, _Българска реч_ I/1995,
  кн. 2, с. 23–24, is the highest-value acquisition; then Йордан Д. Ковачев,
  СбНУ т. 30, 1914 (**note: not Богомил Ковачев**, who was one of Бонов's 1976
  reviewers — conflating them would fabricate a citation). **Not scheduled.**
  Folklore is a bonus layer, not the lesson (ADR 0005), and no puzzle is blocked
  on this: `connect-the-dots` uses the IAU figures in
  `data/generated/constellation-lines.json`.

### Стожер for the Pole Star — NOT ATTESTED

- Investigated because it is an appealing metaphor: a стожер is the pole at the
  centre of a threshing floor that everything turns around, which would be a
  beautiful and astronomically apt folk name for the celestial pole.
- **It is not one.** Речник на българския език (ИБЕ–БАН) records **no
  astronomical sense** for стожер. Worse for the hypothesis, **стожари** is
  attested as a name for the **Pleiades** (Георгиева, с. 28) — the opposite slot.
- **No Bulgarian folk name for Polaris was found** in Георгиева, Бонов, the ИБЕ
  dictionary, or Младенова's bibliography.
- Recorded here so it is not re-proposed. The image may be used as the game's own
  teaching metaphor ("небето се върти като харман около кол"), never as a folk
  name.

---

## Claims ruled out during v1 roster research

Surfaced by `docs/wayfinder/road-to-v1/research/002-what-each-world-can-teach.md` on 2026-09-25. Each source was
confirmed from a search excerpt, not a full page fetch. Recorded now so that nobody proposes them again. The
candidate beats in that file are **not** entered here: a claim enters this register only when a design ticket adopts
it.

### Common sky myths — NOT ATTESTED

Each of these claims was checked and found false or unsupported. Do not state any of them.

- „Марс ще изглежда голям колкото пълната Луна" (Mars will look as big as the full Moon). This is a hoax: NASA,
  _Mars Hoax_ <https://mars.nasa.gov/resources/21869/mars-hoax/> (dead since; read in full 2026-09-25 via Wayback
  <https://web.archive.org/web/20221202233134/https://mars.nasa.gov/resources/21869/mars-hoax/>, see "Mars level").
- "The sky on Mars is blue." NASA _Mars Facts_ <https://science.nasa.gov/mars/facts/> (full page, 2026-09-25): „To
  our eyes, the sky would be hazy and red because of suspended dust". The blue in PIA19400 is only near the setting
  Sun.
- "The Moon doesn't rotate." It turns once per orbit: NASA, _Tidal Locking_
  <https://science.nasa.gov/moon/tidal-locking/>.
- "The Moon is bigger at the horizon." This is an illusion: NASA, _The Moon Illusion_.
- "A supermoon is huge." It is at most about 14% wider than the smallest full Moon: NASA, _Supermoons_
  <https://science.nasa.gov/moon/supermoons/>.
- "Mercury is the hottest planet." Venus is: NASA, _Venus Facts_ <https://science.nasa.gov/venus/venus-facts/>.
- "The Sun and Moon are _exactly_ the same size in the sky." NASA says "almost exactly", and annular eclipses exist
  because they are not: NASA, _Why Do Eclipses Happen?_ <https://science.nasa.gov/eclipses/geometry/>.
- "The 2027-08-02 solar eclipse is total from Bulgaria." It is **partial** there: timeanddate, Sofia 2027-08-02.
- "A small telescope shows Mars's polar cap." That needs a 4–6 inch telescope and excellent seeing: Sky & Telescope,
  _An Observer's Guide to Mars_. (Search excerpt only: the page returned HTTP 403 on 2026-09-25 and has not been
  read. The ruling stands until a read page says otherwise.) APOD 2003-08-19 (read in full) does show „white polar
  caps" through a small telescope, but at the record 2003 approach and as a photograph over three nights; it is not a
  promise for a child's eye in 2027.
- "Distance plays no part in seasons, anywhere." False for Mars, where eccentricity matters: NASA, _Helio and You:
  Seasons on Earth, Mars, and Beyond_. Earth's wording (`fact.seasons.distance`, „почти не се променя", "barely
  changes") is specific to Earth and stays correct.
- "The Galilean moons are visible to the naked eye" (for a child). Say binoculars: NASA Night Sky Network, _From
  Galileo to Clipper_.

### Phobos as "the only moon that orbits faster than its planet spins" — DISPUTED

- NASA, _Phobos in Orbit around Mars_, makes the claim.
- Jupiter's Metis and Adrastea, Uranus's Cordelia and Neptune's Naiad appear to contradict it. That is general
  knowledge, not yet sourced: verify against the JPL satellite tables.
- Do not state it either way until it is resolved.

### "A day on Venus is longer than its year" — DISPUTED

- It is true only for one rotation measured against the stars (≈243 days against ≈225).
- A sunrise-to-sunrise day is ≈117 Earth days (NEEDS SOURCE), which is _shorter_ than the year. So the plain phrase
  misleads.
- "Venus spins backwards" is sourced (NASA, _Venus Facts_) and is the safe claim.

### Jupiter myths — NOT ATTESTED

Surfaced by `docs/wayfinder/road-to-v1/research/007-what-jupiter-can-teach.md` on 2026-09-25, from search excerpts.
Do not state any of them.

- "Jupiter has no seasons." Its seasons are milder, not absent: NASA, _Jupiter Facts_ ("not as extreme"); NASA,
  _Hubble Monitors Changing Weather and Seasons at Jupiter and Uranus_.
- "The Great Red Spot is easy to see, and red, in a small telescope." It is pale salmon and a small-scope challenge,
  visible only while it faces us: Sky & Telescope, _Jupiter's Not-So-Great Red Spot_; _Transit Times of Jupiter's
  Great Red Spot_.
- "Four Galilean moons are always visible." Say "up to four": one can be behind Jupiter, in front of it, or in its
  shadow. The mechanisms were VERIFIED on 2026-09-25 (claim 7 of the ticket 006 section).
- "Ganymede is heavier than Mercury." Only "wider" is sourced (NASA, _Ganymede Facts_). The mass comparison is NEEDS SOURCE and must not be stated.
- "A dropped stone lands on Jupiter." Jupiter has no true surface (NASA, _Jupiter Facts_), so there is no honest
  `gravity-drop` scene at Jupiter. `fact.gravity-drop.bodies` is **deleted** in the build (ticket 006); the pull fact
  moves to a new Jupiter completion-line key (e.g. `fact.jupiter.complete`), worded with „дърпа" / „притегля" only.

### "The Great Red Spot is twice as wide as Earth" — DISPUTED

- NASA, _Jupiter Facts_ says so.
- NASA's Hubble release (_Hubble Shows … Great Red Spot Is Smaller than Ever_) says the spot now holds "just over one
  Earth".
- The spot is shrinking. Quote no size; "bigger than Earth" is safe.

### Saturn myths — NOT ATTESTED

Surfaced by `docs/wayfinder/road-to-v1/research/010-what-saturn-can-teach.md` on 2026-09-26, from search excerpts.
Do not state any of them.

- "Saturn would float in a bathtub." NASA _Saturn Facts_ says it, from mean density below water's, but Saturn is not a
  rigid body and its dense core would sink: IFLScience, _Is NASA's Claim That Saturn Could Float On Water Really
  True?_; BBC Sky at Night, _Saturn could float on water_.
- "The rings vanish every 15 years." The gaps between edge-on views alternate at about 13.7 and 15.7 years, and some
  crossings are triple (2038–39): Obliquity SkyEye, _Ring Plane Crossings of Saturn_; In-The-Sky. Say "twice each trip
  around the Sun".
- "The rings disappear completely." Edge-on, they become a thin line that is hard to see: ESA/Hubble _opo9525c_; NASA,
  _Hubble Views Saturn Ring-Plane Crossing_. The rings are still there, but a backyard telescope may not show them at all
  ("sometimes invisible", same NASA page; claim 3 of the ticket 011 section).
- "The rings tip / change angle." Saturn's axis keeps pointing the same way; our viewpoint moves round the orbit.
  Corrected 2026-09-26 on a full read: the _PIA03156_ caption (a Hubble Heritage image) does not say "changes angle".
  It says the planet and rings "nod majestically", which is the same loose phrasing. Do not quote either.
- "The rings open a little more every month in 2026–27." Earth's own orbit adds a yearly wobble (about 0.37° on
  2025-11-23, after the March crossing: AAQ). **NOT ATTESTED** (2026-09-26): the monthly computation in claim 4 of the
  ticket 011 section shows the rings narrowing from −8.3° (Sep 2026) to −6.1° (Dec 2026) before opening to −14.4°
  (Aug 2027). Do not state it.
- "Titan is the largest moon." Ganymede is slightly larger: NASA, _Titan Facts_.
- "Titan is heavier than Mercury." Titan is slightly wider, with about half Mercury's mass: NASA, _Titan Facts_.
- "Titan is the only moon with an atmosphere." NASA says the only moon with a **thick** atmosphere; the word „плътна"
  is required: NASA, _Titan Facts_.
- "Saturn's hexagon can be seen in a telescope." It sits at the north pole, turned away from Earth through 2026–27, and
  no source makes it a small-telescope sight.

### Saturn's ring thickness — DISPUTED

- NASA _Saturn Facts_ gives "typically about 30 feet (10 meters) in the main rings"; NSSDC _Saturnian Rings Fact Sheet_
  lists 5–30 m by ring; In-The-Sky _Equinox on Saturn_ says "no more than a kilometer thick". Attribution corrected
  2026-09-26 on a full read: the 10 m figure is not on the _PIA03156_ page, which gives no thickness.
- Quote no figure. "Very thin for how wide they are" is the safe claim, once a design ticket adopts it.

---

## Terminology

Standard Bulgarian, checked against bg.wikipedia's own astronomy articles.

| English                            | Bulgarian                          | Note                                                            |
| ---------------------------------- | ---------------------------------- | --------------------------------------------------------------- |
| Solar System                       | Слънчева система                   |                                                                 |
| Milky Way                          | Млечен път                         | Кумова слама is the _folk_ name, never a replacement            |
| Mercury / Venus / Earth / Mars     | Меркурий / Венера / Земя / Марс    |                                                                 |
| Jupiter / Saturn                   | Юпитер / Сатурн                    |                                                                 |
| Moon / Sun                         | Луна / Слънце                      | folk texts use Месечина; keep that inside quoted folklore only  |
| morning / evening star             | Зорница / Вечерница                |                                                                 |
| Orion's Belt                       | Поясът на Орион                    | not "Коланът"                                                   |
| asterism                           | астеризъм                          | the Belt is an asterism, not a constellation                    |
| open cluster                       | разсеян звезден куп                | not "отворен куп", never "клъстер"                              |
| double / multiple star             | двойна / кратна звезда             | use кратна for 3+, not "множествена"                            |
| magnitude                          | звездна величина                   | correct term, but **must never appear in player text** (rule 2) |
| supergiant                         | свръхгигант                        |                                                                 |
| Alnitak / Alnilam / Mintaka        | Алнитак / Алнилам / Минтака        |                                                                 |
| Rigel / Betelgeuse / Mizar / Alcor | Ригел / Бетелгейзе / Мицар / Алкор |                                                                 |
| far side of the Moon               | далечната страна                   | never "тъмната страна"                                          |

**"кум" ≠ groom.** кум = godfather / wedding sponsor; кумец = the man whose
wedding he sponsored; младоженец = groom. This error is in the brief.

---

## Data sources

| What                    | Source                    | Notes                                                                                                                                                                                      |
| ----------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Planetary positions     | JPL DE440s via Skyfield   | `data/ephemeris/`, gitignored. Covers 1849–2150.                                                                                                                                           |
| Planet and moon imagery | NASA                      | Public domain. Real Mars must look like real Mars — imagery is never AI-generated.                                                                                                         |
| Star catalogue          | HYG v4.4 (CC BY-SA 4.0)   | **VERIFIED** 2026-09-08. `data/raw/hyg/`, gitignored; filtered into `data/generated/stars.json` by `data/scripts/star-catalogue.py`. See "Star catalogue and constellation figures" below. |
| Constellation figures   | Stellarium `modern_iau`   | CC BY-SA 4.0. 88 figures as HIP polylines → `data/generated/constellation-lines.json`. **Not an IAU standard** — the IAU defined boundaries, never stick figures.                          |
| Double-star separations | WDS / ORB6 (USNO)         | Public domain. `data/raw/wds/`. The authority for Mizar A/B and the Orion belt splits.                                                                                                     |
| Position verification   | Hipparcos-2, VizieR I/311 | van Leeuwen 2007. Deliberately a different source from HYG — the build fails if they disagree by more than 30″.                                                                            |
