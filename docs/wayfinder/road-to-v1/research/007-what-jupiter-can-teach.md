---
ticket: "007"
title: What Jupiter can teach, deep
status: done
---

# Research 007: what Jupiter can teach, deep

Produced by the `astronomy-consultant` agent on 2026-09-25 as a deep pass on Jupiter, roster page 4 (open level,
`unlockThreshold` 0.7). The main session wrote it here because the agent has no write tools. It follows the format of
research 002's Moon and Mars sections.

**This is a list of candidates, not design facts.** 002's rule applies: a claim enters `docs/sources.md` only when a
design ticket adopts it, and only after `astronomy-accuracy-checker` has VERIFIED it.

**What "VERIFIED" means here.** A context-mode hook blocked `WebFetch` in this session, so none of these pages was
fetched in full. Every VERIFIED below rests on search-engine excerpts of the named page, or on rows already in
`docs/sources.md`. Read it as "the source states it, per the excerpt". The checker must fetch each page.

**Walls applied:**

- Rule 2.
- No folklore beats.
- No new pipeline.
- No nightly Galilean positions.
- Binoculars, not the naked eye, for the moons.
- `gravity-drop` never models mass.
- `zoom-split-star` is not used, because it is being deleted.

## Jupiter (deep)

### What is actually happening

- **A gas giant with no surface.** Jupiter is mostly gas and liquid, and it "doesn't have a true surface" (NASA,
  _Jupiter Facts_).
- **Belts and zones.**
  - The stripes are ammonia and water clouds: dark belts and light zones.
  - Strong jet streams, driven by the fast spin, pull them into long bands (`docs/sources.md:249-252`).
- **Fast spin.**
  - One turn takes about 9.9 hours, the shortest day of any planet (NASA, _Jupiter Facts_).
  - The spin makes the equator bulge, so the disc is about 7% wider than it is tall (Sky & Telescope, _How to See
    Jupiter_).
- **The Great Red Spot.**
  - It is a storm larger than Earth, watched for more than 300 years.
  - It is shrinking: Hubble now puts it at "just over one Earth" wide.
  - In a small telescope it is pale salmon, low in contrast, and "a challenge". It is visible only while the spin
    carries it across the side facing us, which puts it near the middle of the disc for about 50 minutes either side
    of its transit (Sky & Telescope).
- **The tilt is only about 3°.**
  - Jupiter "spins nearly upright and does not have seasons as extreme as other planets do" (NASA, _Jupiter Facts_).
  - It still has _some_ seasons.
  - Its orbit is also more eccentric than Earth's, so the "tilt only" story is incomplete here, as it is for Mars.
- **The Galilean moons.**
  - Io, Europa, Ganymede and Callisto orbit close to Jupiter's equatorial plane. Their orbits are seen from Earth
    almost edge-on, which is why they appear as dots in a line on one or both sides of the planet.
  - The line itself is sourced (NASA Night Sky Network, _From Galileo to Clipper_). The edge-on explanation is
    standard geometry but is not yet sourced.
  - Each night they change sides and order. Sometimes one hides behind Jupiter, crosses in front of it, or sits in its
    shadow, so a child may see fewer than four.
  - Periods: Io about 42.5 hours, Europa about 3.5 days, Ganymede about 7.155 days, Callisto about 16.7 days.
  - Io, Europa and Ganymede are in a 4:2:1 resonance. Callisto is not.
- **Ganymede** is the largest moon in the Solar System and is wider than Mercury: about 5,260 km across against
  Mercury's 4,880 km, so roughly 8% wider. Mercury is much denser and more massive (general knowledge, unsourced).
- **Brightness.** Jupiter shines by reflected sunlight. It outshines Sirius at _every_ point of its cycle
  (`docs/sources.md:265-296`).
- **The 2026–27 apparition from Bulgaria.**
  - Solar conjunction was 2026-07-29, so Jupiter is a morning object at the start of the data window.
  - Opposition is 2027-02-11. Closest approach per In-The-Sky is 2027-02-10; `docs/sources.md:85` has 02-11, a
    one-day sampling difference.
  - It dominates the evening sky from early February to mid-June 2027, and stands with Sirius February to April.
  - Next solar conjunction: 2027-08-31 (In-The-Sky).
  - Retrograde runs around opposition, inside the data window. The stationary dates are not sourced.

### Candidate beats

The "Status" column covers the claim. "Types" gives the type, then → the fallback type.

| #   | Beat | Types | Misconception | Source | Status | Data |
| --- | ---- | ----- | ------------- | ------ | ------ | ---- |
| J1 | **The ladder (spine anchor).** (1) Naked eye: one steady, very bright point. (2) Binoculars: up to four dots in a line, one undated schematic arrangement. (3) Small telescope: a small disc with two dark belts | `telescope-focus`, three rungs → `parallax-compare` (three panels; the child matches view to instrument) | "It's a star"; "a telescope shows Hubble pictures" | NSN, _From Galileo to Clipper_; S&T, _Jupiter Is Outstanding at Opposition_ (`docs/sources.md:244-246`) | VERIFIED (rungs 2 and 3) | Real imagery for rung 3; rung 2 is schematic |
| J2 | **The moons move: a circle seen edge-on is a line.** Top-down panel of four moons circling at their true _relative_ speeds, beside an edge-on "what you see" strip; the child drags time until the strip matches a target line-up | `trajectory-match` → `rotate-match` `orbitAngle` with a new renderer (a schema change) | "The dots are stars"; "moons stay put"; "there are always four" | NASA _Io_, _Europa_, _Ganymede_, _Callisto Facts_ | Periods VERIFIED by excerpt, which **closes #20 for a schematic use** (checker to fetch). Edge-on explanation: NEEDS SOURCE | A cited `data/reference/` periods row (not a pipeline). **No dated positions** |
| J3 | **Ganymede is wider than Mercury.** Two discs at one scale; drag a ring to find the bigger one | `parallax-compare` → no fallback (it degrades to a fact string on J1 rung 2) | "Moons are always smaller than planets" | NASA _Ganymede Facts_; NASA _Mercury Facts_ | VERIFIED (excerpt) | A radii row. **The margin is only ~8%**, so draw carefully and do not exaggerate |
| J4 | **Brighter than the brightest star.** Real evening sky, February to April 2027: Jupiter and Sirius; the child picks which is the planet, then the "why" card | `parallax-compare` → no fallback (fact string on J1 rung 1; `fact.brightest-is-a-planet` / `-why` exist) | "Planets shine by themselves"; "the brightest dot is a star" | `docs/sources.md:265-296` | VERIFIED | **Exists:** Jupiter RA/Dec; Sirius from `stars.json`. Frame note below |
| J5 | **Cloud belts.** The rung-3 payoff of J1 | inside J1 | "Jupiter is solid, like Earth" | `docs/sources.md:233-263`, `fact.telescope-jupiter` | VERIFIED | Real imagery |
| J6 | **The Red Spot is shy.** Optional: the spot is faint and pale, and only on view while it faces us | hint on J1 rung 3, or folded into J7 → fact string | "The Red Spot is big and red in any telescope" | S&T, _Jupiter's Not-So-Great Red Spot_; S&T, _Transit Times …_ | VERIFIED (excerpt). **Size wording: see false claim 1** | Real imagery. Art must be pale, not poster-red |
| J7 | **A fast spin.** Spin Jupiter until the Red Spot faces the viewer. A paired Earth globe turns once in the time Jupiter turns more than twice. There are no clocks | `rotate-match` `day-night` reskin, `drives: spin` → fact string | "Every planet's day is about as long as ours" | NASA _Jupiter Facts_; S&T _Transit Times_ | VERIFIED (excerpt) | A period row. **If the `day-night` art is Earth-specific, a Jupiter skin plus a paired globe is a new renderer (a schema change)** |
| J8 | **The squashed disc.** A fact on J7, or shown on J1 rung 3 | fact string, no type | "Planets are perfect spheres" | S&T, _How to See Jupiter_ | Shape VERIFIED. **"Visible in a small telescope": NEEDS SOURCE** | None |
| J9 | **Almost upright.** Tilt Jupiter to its real tilt beside Earth's: barely tipped, so its seasons are mild | `rotate-match` `seasons-tilt` reskin, `drives: tilt` → no fallback | Extends Earth's tilt lesson | NASA _Jupiter Facts_; NASA _Hubble Monitors … Seasons at Jupiter_ | VERIFIED. **High risk:** see below | None |
| J10 | **The slow loop.** Jupiter's retrograde loop over the window: smaller and slower than Mars's | `trajectory-match` (reuses R1) → no fallback | "Planets really go backwards" | NASA _Mars Retrograde_ (`docs/sources.md:74-79`) | Mechanism VERIFIED. **Stationary dates: NEEDS SOURCE** | **Exists:** Jupiter RA/Dec; Earth and Jupiter `helioLonDegrees` |
| J11 | **Dropping a stone on Jupiter** | `gravity-drop` → **no honest version** | — | `data/reference/surface-gravity.json:63-72` | **NOT ATTESTED as a scene** | See below |

**On J11, `gravity-drop` at Jupiter.** Keep the existing _fact_ (`fact.gravity-drop.bodies`). Build no drop _scene_:

- There is no ground, so the stone never lands.
- The air is deep and thick, so neither `air: false` nor `air: true` is honest. This is the same trap as Mars (R7) and
  Titan.

`docs/sources.md:162` gives "Saturn has no surface" as one reason to exclude Saturn, then approves Jupiter. That reads
as inconsistent. The reference row resolves it: Saturn fails on the column ambiguity, and Jupiter only ever appears in
a fact string. Worth one clarifying line in `sources.md` when ticket 005 is decided.

### Misconception risks

- **J9 is the Mars R8 trap again.**
  - "Jupiter has no seasons" is false; NASA's own Hubble article speaks of seasons at Jupiter.
  - Wording must be comparative: "almost upright, so its seasons are much milder than ours".
  - Never draw an oval orbit. If J9 needs the eccentricity story to stay honest, cut it.
- **J2 can teach "moons sit still" or "always four"** if the strip is a static picture.
  - The schematic must move, must carry "up to four", and must once show a moon passing behind the disc.
  - It must never carry a date or a "tonight's view" label.
  - Callisto must not be drawn locked into the 4:2:1 rhythm.
- **J2's dots must never be called stars.**
- **J3 can teach "bigger means heavier".** Say „по-широк" or „по-голям на ръст", never anything about weight. An 8%
  difference drawn honestly is subtle; do not inflate it.
- **J4 can teach "planets glow".** The reveal must carry `fact.brightest-why`, as `docs/sources.md:286-289` requires.
- **J6/J7 art.** A poster-red spot twice Earth's size sets up the disappointment `fact.telescope-expectation` warns
  about.
- **J7's paired globes must not show hour marks.** Rule 2 treats a segmented dial as a number.
- **J10.** The top-down view must show Jupiter moving forward throughout, as in R1.

### Do not claim

- that the Great Red Spot is "twice as wide as Earth", or give any fixed size. "Bigger than Earth" is safe;
- that the Red Spot is easy to see, or red, in a small telescope;
- that Jupiter has no seasons;
- that the Galilean moons are visible to the naked eye;
- that there are always four moons, or any arrangement "for tonight" or for any date;
- that the moons are stars;
- that Ganymede is heavier than, or "outweighs", Mercury;
- that Jupiter shines by its own light. The "failed star" framing was not investigated;
- that a stone lands on Jupiter, or anything about falling through Jupiter's air;
- any date or period on screen (rule 2), or any unsourced stationary date anywhere;
- that the squashed disc is visible in a small telescope, until that is sourced.

## Verdict: can Jupiter carry a required spine using only `rotate-match`?

**No.**

- Only J7 (spin) and J9 (tilt) are honest `rotate-match` beats, and J9 is high-risk.
- Neither teaches what Jupiter is uniquely for: a "star" that is a world with moons.

**What depends on 005:**

| Type | Beats it carries | If 005 prunes it |
| ---- | ---------------- | ---------------- |
| `telescope-focus` | J1 and J5, which are the natural spine; J6 as a hint | J1 falls back to a three-panel `parallax-compare`, which is weaker but honest |
| `trajectory-match` | J2, the strongest new lesson and Galileo's own evidence; J10 | J2 needs a new `rotate-match` renderer (a schema change); J10 dies |
| `parallax-compare` | J3 and J4; the fallback for J1 | J3 and J4 become fact strings |
| `gravity-drop` | nothing | no loss |

**The recommended spine at 0.7** is J1 (ladder), J2 (moons move), J4 (Sirius) and J7 (spin), with J3 as an extra.
That needs `telescope-focus`, `trajectory-match` and `parallax-compare` to survive. At minimum it needs
`parallax-compare` plus a new `rotate-match` renderer.

**If 005 keeps only `rotate-match`**, Jupiter is not a viable open level. Either cut it from the roster, or rebuild it
as J1 as a fact card plus J7, with every beat required.

## Claims found false or unsupported

1. **"The Great Red Spot is twice as wide as Earth"** (NASA _Jupiter Facts_). NASA's own Hubble release says it now
   holds "just over one Earth". The facts page is out of date. **DISPUTED**: do not quote a size.
2. **"Jupiter has no seasons."** FALSE. NASA says "not as extreme".
3. **"The Red Spot is easily seen, and red."** Unsupported. S&T calls it a small-scope challenge and pale salmon.
4. **"You can see the stone land on Jupiter."** There is no surface: **NOT ATTESTED** as a scene.
5. **"Four moons are always visible."** FALSE. Say "up to four". The mechanisms (transit, occultation, eclipse) are
   NEEDS SOURCE if the game ever states _why_.
6. **"Ganymede is bigger, so heavier, than Mercury."** Only "wider" is sourced.
7. **"Opposition and closest approach are the same day."** In-The-Sky puts perigee on 02-10 and opposition on 02-11.
   It is harmless because no date is shown.

## Data gaps

- **Galilean periods.** A hand-authored `data/reference/` row, like `surface-gravity.json`: four periods, each with its
  NASA page URL and access date. This is not a pipeline, and it closes `docs/sources.md` #20 for a schematic beat.
  Dated positions still need a satellite ephemeris, which stays barred.
- **Radii rows:** Ganymede and Mercury (J3); Jupiter's equatorial and polar radii, if J8 is drawn to scale.
- **Rows for Jupiter's rotation period (J7) and axial tilt (J9).**
- **Jupiter retrograde stationary dates (J10).** Derive them from the committed RA series and cross-check against
  In-The-Sky.
- **The frame trap, twice:**
  - J10 mixes J2000-ecliptic `helioLonDegrees` with apparent RA/Dec. Declare each panel's frame.
  - J4 mixes apparent RA/Dec for Jupiter with catalogue-epoch positions for Sirius (about 0.3° of precession,
    invisible in art, but declare it).
- **Evening visibility for Sofia** (J4, and any "go and look" hook). The February–June figure in
  `docs/sources.md:278-285` was computed once and never committed. Reusing it as a sourced statement is fine;
  regenerating it is an owner build-time decision.
- **The window covers about 30° of Jupiter's orbit.** No beat can show a full Jupiter year.

## Bulgarian terms

Confidence is moderate. Check against bg.wikipedia before shipping.

- **Голямото червено петно** (the Great Red Spot).
- **Галилееви спътници.** Use "спътници" in facts.
- **облачни пояси**, already in use.
- **бинокъл** (binoculars).
- **противостояние** (opposition), for metadata only.

## Sources

Every source below was checked from search excerpts, not fetched in full.

- NASA, _Jupiter Facts_: <https://science.nasa.gov/jupiter/jupiter-facts/>
- NASA, _Hubble Shows … Great Red Spot Is Smaller than Ever…_:
  <https://science.nasa.gov/missions/hubble/hubble-shows-that-jupiters-great-red-spot-is-smaller-than-ever-seen-before/>
- NASA, _Hubble Monitors Changing Weather and Seasons at Jupiter and Uranus_:
  <https://science.nasa.gov/missions/hubble/hubble-monitors-changing-weather-and-seasons-at-jupiter-and-uranus/>
- NASA, _Ganymede Facts_: <https://science.nasa.gov/jupiter/jupiter-moons/ganymede/facts/>
- NASA, _Io Facts_: <https://science.nasa.gov/jupiter/jupiter-moons/io/facts/>
- NASA, _Europa Facts_: <https://science.nasa.gov/jupiter/jupiter-moons/europa/europa-facts/>
- NASA, _Callisto Facts_: <https://science.nasa.gov/jupiter/jupiter-moons/callisto/facts/>
- NASA, _Mercury Facts_: <https://science.nasa.gov/mercury/facts/>
- NASA Night Sky Network, _From Galileo to Clipper_:
  <https://science.nasa.gov/solar-system/skywatching/night-sky-network/octobers-night-sky-notes-from-galileo-to-clipper-exploring-jupiters-moons>
- Sky & Telescope, _Transit Times of Jupiter's Great Red Spot_:
  <https://skyandtelescope.org/observing/interactive-sky-watching-tools/transit-times-of-jupiters-great-red-spot/>
- Sky & Telescope, _Jupiter's Not-So-Great Red Spot_:
  <https://skyandtelescope.org/astronomy-news/observing-news/jupiters-great-red-spot/>
- Sky & Telescope, _How to See Jupiter: Big, Bright, and Beautiful_:
  <https://skyandtelescope.org/observing/jupiter-big-bright-and-beautiful-2/>
- In-The-Sky.org: opposition 2027-02-11, perigee 2027-02-10, solar conjunction 2027-08-31.
- Repo:
  - `docs/sources.md:85`, `:104-111`, `:143-162`, `:233-296`, `:736-737`
  - `data/reference/surface-gravity.json:63-72`
  - `content/bg/facts.json:19,22,42,43`
  - `schemas/level-data.schema.json:61-99`
