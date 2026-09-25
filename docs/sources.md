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

- **Claim**: Io, Europa, Ganymede and Callisto shift position night to night;
  their orbital periods can be deduced from watching them.
- **Status**: **NEEDS SOURCE** for the specific periods. The four names and
  Galileo's discovery are uncontroversial; the numbers the puzzle depends on
  must come from a cited source (JPL) and be generated into
  `data/generated/`, never typed from memory.

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
- **Rule 2**: the masses and the drop height are for this file only. No number,
  and no use of `земно ускорение`, reaches the player — say **притегляне**.

### Surface gravity per body

- **Claim** (`fact.gravity-drop.bodies`): the same drop is slow and floating on
  the Moon, a little quicker on Mars, and far stronger on Jupiter.
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
  shadow. The mechanisms are NEEDS SOURCE if the game ever explains why.
- "Ganymede is heavier than Mercury." Only "wider" is sourced (NASA, _Ganymede Facts_). The mass comparison is NEEDS SOURCE and must not be stated.
- "A dropped stone lands on Jupiter." Jupiter has no true surface (NASA, _Jupiter Facts_), so there is no honest
  `gravity-drop` scene at Jupiter. `fact.gravity-drop.bodies` stays.

### "The Great Red Spot is twice as wide as Earth" — DISPUTED

- NASA, _Jupiter Facts_ says so.
- NASA's Hubble release (_Hubble Shows … Great Red Spot Is Smaller than Ever_) says the spot now holds "just over one
  Earth".
- The spot is shrinking. Quote no size; "bigger than Earth" is safe.

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
