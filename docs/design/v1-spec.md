# The v1 spec — what road-to-v1 decided

This is the settled v1 spec that [road-to-v1](../wayfinder/road-to-v1/MAP.md) found its way to. It gathers the twelve
closed tickets and their amendments in one place. **Where tickets conflict, the later one wins**, and this file applies
that already. Each section names its source tickets (`T001`…`T012` =
`docs/wayfinder/road-to-v1/tickets/NNN-*.md`). A ticket holds the reasoning. This file holds the answer. If they ever
disagree, the ticket is the authority and this file has a bug.

It is the first fixed input of the [v1-build map](../wayfinder/v1-build/MAP.md). Do not re-derive anything here in a
build session.

## 1. What was decided

### The roster (T001, amended by T009, T010, T011)

| Page | World      | Mode        | Gate    | Pass rule                               |
| ---- | ---------- | ----------- | ------- | --------------------------------------- |
| 1    | Earth      | guided      | 1.0     | all 4 required (spine, in order)        |
| 2    | Moon       | guided      | 1.0     | all 3 required (spine, in order)        |
| 3    | Mars       | open        | 0.7     | R1a, then any 3 of R1b, R3, R2, R6      |
| 4    | Jupiter    | open        | 0.7     | J1, then any 3 of J2, J3, J4, J7        |
| 5    | Saturn     | open        | 0.7     | S1, then any 2 of S2, S3, S4            |
| —    | Back cover | not a world | derived | opens when Saturn is `completed` (T009) |

- Gates count `solved ∩ required` (09-09 handoff, `meetsThreshold` in `src/shared/game-state.ts`). Optional markers
  never carry a level on their own.
- Companion tiers: Earth 3 (arrival, nudge, fact; 09-09). Moon, Mars, Jupiter and Saturn 2 (nudge, fact). The tier
  count is level data. The tickets' fixed 2 supersede the handoff's "drop a tier per level until only the fact
  remains" (T003, T004, T006, T011 over 09-09 :168-169).
- One `reward.fact` per marker. A marker's second idea goes on its **album card**, not in its nudge (T008 amends T003,
  T004 and T006).
- Major moons are the large round ones: the Moon, the Galilean moons, Titan, Triton. Phobos is not one. No moon besides
  ours gets a page (T001).

### Earth — 9 beats (09-09 handoff, less `earth-gravity-drop` per T005)

Content fixed by the 09-09 handoff and `src/scenes/earth/earth-data.json`. Not reopened.

| Marker                    | Type / renderer                     | Required | Fact                                              |
| ------------------------- | ----------------------------------- | -------- | ------------------------------------------------- |
| `earth-sundial`           | `rotate-match` `sundial`            | 1st      | `fact.day-night`                                  |
| `earth-day-night-spin`    | `rotate-match` `day-night`          | 2nd      | `fact.day-night` (repeat: resolve at build, T008) |
| `earth-seasons-globe`     | `rotate-match` `seasons-tilt`       | 3rd      | `fact.seasons`                                    |
| `earth-day-length`        | `parallax-compare`                  | 4th      | `fact.day-length`                                 |
| `earth-orbit-year`        | `trajectory-match`, `dataRef` Earth | no       | `fact.year-orbit`                                 |
| `earth-moon-phase`        | `rotate-match` `moon-phase`         | no       | `fact.moon-phases`                                |
| `earth-twilight-zornitsa` | `trajectory-match`, `dataRef` Venus | no       | `fact.zornitsa`                                   |
| `earth-big-dipper`        | `connect-the-dots`                  | no       | `fact.ursa-major-shape`                           |
| `earth-telescope-focus`   | `telescope-focus`                   | no       | `fact.telescope-saturn`                           |

- `earth-gravity-drop` is deleted (T005). The Зорница beat is Earth's only folklore beat and stays (ADR 0005).
- `fact.telescope-saturn` art shows a narrowly open south face for 2026–27, not the poster view (T010, T011).
- The constellation beat keeps per-latitude visibility (#25) as build work (T012 Q23).
- **Earth's build scope** (owner, 2026-09-26, listing only, nothing reopened):
  - the T005 prune;
  - 09-09 phase-2 #3–#9, which ends at 3 beats playable (handoff :277);
  - engines and renderers for the other six beats;
  - #25;
  - Earth's share of T008 and T012: a hint step and page element per marker, album cards, the `fact.day-night` repeat,
    the `earth-telescope-focus` → J1 card, the Earth memory and the storybook intro.
- `ui.puzzle.coming-soon` may exist only while Earth has stubs; it is gone by v1 (T001 and the finish bar over 09-09
  task #3).

### Moon (T003, amended by T005, T008)

| Marker                 | Type                                                                          | Required / opens | Teaches                                        | Fact                                                                                                |
| ---------------------- | ----------------------------------------------------------------------------- | ---------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| M1 The Moon turns      | `rotate-match` `orbitAngle`; crater points at a fixed star arrow              | 1st              | it does turn, once per trip                    | it turns once per trip around Earth                                                                 |
| M3 Shadow or phase     | `rotate-match` `orbitAngle`; Earth's shadow drawn, passive side-on tilt inset | 2nd              | phases are not Earth's shadow                  | shadow ≠ phase; not every full Moon has an eclipse                                                  |
| M2 The far side is lit | `rotate-match` `orbitAngle`, top-down                                         | 3rd              | no "dark side"                                 | `fact.moon-far-side`                                                                                |
| Solar eclipse          | `rotate-match` `orbitAngle`; Moon's shadow on Earth, tilt inset               | optional, open   | only at new Moon, not every one                | Sun and Moon look _almost_ the same size; **safety string, own key, shown whenever the beat opens** |
| M5 Near and far        | `parallax-compare`, discs from `bodies.moon.distanceAu`                       | optional, open   | "a supermoon is huge" is false                 | the size difference is small                                                                        |
| M9 Seas and craters    | `telescope-focus`; full-Moon crater slides in on solve                        | optional, open   | maria are lava; relief shows at the terminator | maria are lava                                                                                      |

- Spine chains M1 → M3 → M2 through `reward.unlocks`.
- Album second ideas (from the old nudges): M3 earthshine (described, never named); M5 annular ring; M9 shadows at the
  terminator. Every nudge is rewritten to only point.
- **Completion line** (T005): `fact.gravity-drop` + `.apollo` merged into one new key, shown when the spine is done.
  It keeps „Не защото е тежък", says „притегляне", and says „няма въздух, който да задържи перцето" or „почти няма
  въздух". Never the flat „На Луната няма въздух" (NOT ATTESTED).
- `level.moon.blurb` is rewritten: the lit part changes, the face stays.

### Mars (T004, amended by T008)

| Marker                          | Type                                                                                                   | Opens     | Teaches                          | Fact                                           |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ | --------- | -------------------------------- | ---------------------------------------------- |
| R1a Mars's path among the stars | `connect-the-dots`, ~15–25 dots from committed Mars RA/Dec, Nov 2026–May 2027, real `stars.json` field | start     | Mars seems to turn back          | an illusion: Earth catches up and overtakes    |
| R1b Why it turns back           | `trajectory-match`, sight line onto the star strip                                                     | after R1a | Mars never really reverses       | Earth moves faster than Mars                   |
| R3 Mars in a telescope          | `telescope-focus`                                                                                      | start     | a small red disc, not the photos | red from rust; a cold world                    |
| R2 Never as big as the Moon     | `parallax-compare`, one true scale                                                                     | start     | the hoax is false                | the hoax is false                              |
| R6 Blue sunset                  | `parallax-compare`, PIA19400                                                                           | start     | "Mars sunsets are red"           | a camera on Mars saw blue near the setting Sun |

- All five required. Album second ideas: R1a Earth has the inside lane; R3 dark patches best when Mars is closest; R2
  not even at its closest; R6 a Mars day is a little longer.
- `level.mars.blurb` becomes "seems to" (e.g. „сякаш тръгва назад").

### Jupiter (T006, amended by T008)

| Marker                  | Type                                                                            | Opens    | Teaches                            | Fact                                                              |
| ----------------------- | ------------------------------------------------------------------------------- | -------- | ---------------------------------- | ----------------------------------------------------------------- |
| J1 The ladder           | `telescope-focus`, three rungs: eye → binoculars → small telescope              | start    | not a star; not Hubble pictures    | `fact.telescope-jupiter`                                          |
| J2 The moons move       | `trajectory-match`, four moons top-down + edge-on strip; match a target line-up | after J1 | the dots are moons, and they move  | seen edge-on they line up; Galileo worked out they circle Jupiter |
| J3 Ganymede vs Mercury  | `parallax-compare`, one true scale                                              | start    | a moon can be bigger than a planet | the largest moon, wider than Mercury                              |
| J4 Brighter than Sirius | `parallax-compare`, wide Feb–Apr 2027 sky at true separation; binocular circle  | start    | planets reflect sunlight           | `fact.brightest-why`                                              |
| J7 The fast spin        | `rotate-match` `drives: spin`; Earth globe turns once per round                 | start    | days differ                        | the shortest day of any planet                                    |

- All five required. Album second ideas: J1 the Red Spot is often pale; J2 up to four show, one can hide behind or in
  front; J3 a moon can outsize a planet; J4 a key trimmed from `fact.brightest-is-a-planet` without Venus; J7 the spin
  helps stretch the clouds.
- **Completion line** (T006 note on T005): a new key, "Jupiter pulls much harder than Earth". `fact.gravity-drop.bodies`
  is deleted. `data/reference/surface-gravity.json` stays.
- Sirius is a foil, not a target (rule 6).

### Saturn (T011, confirming T010)

| Marker                     | Type                                                                                                       | Opens    | Teaches                    | Fact                                                   |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- | -------- | -------------------------- | ------------------------------------------------------ |
| S1 The rings come and go   | `rotate-match`, new renderer **`ring-view`** pinned to `orbitAngle`, `targets: 3`; solve on the inset view | start    | the rings never tip        | they keep facing one way; we see another side          |
| S2 The slowest wanderer    | `connect-the-dots`, two panels at one angular scale, Mars's loop pre-drawn faint                           | start    | planets wander differently | the slowest of the five naked-eye planets              |
| S3 The moon wrapped in fog | `parallax-compare`, Moon vs Titan at true scale, PIA06230 then PIA20016                                    | start    | moons can have air         | Titan's thick air hides its ground from ordinary light |
| S4 The rings are a swarm   | `trajectory-match`, three ring pieces; speeds from cited radii                                             | after S1 | the rings are not solid    | each piece circles on its own; inner ones go faster    |

- All four required. Album second ideas: S1 Saturn has seasons too; S2 the gap is the Sun's glare; S3 the only moon with
  a _thick_ atmosphere; S4 people learned it from the rings' light.
- **Completion line**: Saturn's tilt gives it seasons, like Earth's. "Like", never "only".

## 2. The five-type verdict (T005, ADR 0006)

| Type               | Earth | Moon                | Mars   | Jupiter | Saturn | Verdict     |
| ------------------ | ----- | ------------------- | ------ | ------- | ------ | ----------- |
| `rotate-match`     | 4     | M1, M3, M2, eclipse | —      | J7      | S1     | keep        |
| `connect-the-dots` | 1     | —                   | R1a    | —       | S2     | keep        |
| `parallax-compare` | 1     | M5                  | R2, R6 | J3, J4  | S3     | keep        |
| `trajectory-match` | 2     | —                   | R1b    | J2      | S4     | keep        |
| `telescope-focus`  | 1     | M9                  | R3     | J1      | —      | keep        |
| `zoom-split-star`  | —     | —                   | —      | —       | —      | **deleted** |
| `gravity-drop`     | 1     | —                   | —      | —       | —      | **deleted** |

- **Reopens ticket 005 if the build cuts** R1a, R1b, both M9 and R3, or all of M5, R2 and R6. Jupiter and Saturn
  markers on a deleted type then reopen too (R1b → J2, S4; M9+R3 → J1; M5+R2+R6 → J3, J4, S3; R1a → S2).
- **If a build overruns**, the Moon's eclipse beat is cut first (T003).
- Post-anchor levels (Jupiter, Saturn) design on the five only. A revival reopens T005, argued in ADR 0006.
- `sources.md` gains a **RETIRED** status: true, not shipped, with the reason. Mizar/Alcor is RETIRED.

## 3. Cross-cutting systems

**Hints (T008, ADR 0007).** Free, never earned, never stored, never shown as a count.

- The nudge appears on a stall and only points.
- The hint step comes on a second tap of the companion, on every level. It narrows _what_ to try, never _how far_.
  The schema holds a per-type enum that carries no values:
  - `rotate-match`: pulse the reference feature, never a ghost of the target;
  - `connect-the-dots`: glow a region, never the line or the next dot;
  - `parallax-compare`: highlight the feature equally on both sides, never which one wins;
  - `trajectory-match`: pulse the time control, never a direction or snap;
  - `telescope-focus`: pulse the focus control, never a direction or auto-focus.
- „Спомни си…“ cards: a marker may name **one** earlier marker (`remembers`, a single id). Once that marker is
  solved, its card replaces the hint step's text. Fixed pairs: J1 remembers `earth-telescope-focus`, and S4 remembers
  `earth-telescope-focus` ("countless pieces"). T011's second S4 link, to J2, was dropped (owner, 2026-09-26: one link
  per marker, as T008 and T011's own table row say). Other pairs are chosen in plan mode and reviewed by
  `puzzle-pedagogy-reviewer`.

**The album (T008).**

- Every solved marker lights an element of its page art. Tapping a lit element shows its fact plus the second idea.
- Unlit elements are invisible or plain background, never outlines. There is no album screen and no counter.
- It is derived from `solved[]`, so nothing new is stored. Reword the `solvedCount` doc comment.

**The book (T009).**

- **The grid:**
  - pages wrap into a grid, with columns chosen from width and height, header included;
  - it fits with no scrolling down to 360px portrait;
  - text keeps a floor (names about 16px), and a tile drops its blurb when the blurb cannot fit;
  - the layout re-runs on Phaser `resize`.
- Open pages are bright. Closed pages are dim, showing the name only. „Заключено" is dropped. A bookmark ribbon marks the
  newest open page, or the back cover once it is open.
- **The back cover:**
  - non-tappable, always last, with no `-data.json` and no `sceneKey`;
  - opens on Saturn's `completed` and never re-locks in v1, with no new `localStorage` field;
  - art: textless vignettes of completed worlds only; a closed cover is plain and dim;
  - companion lines ask the child to show it these worlds in the real sky with someone from home (claims 1–4 of
    `sources.md` "Back cover"). They name the worlds, use no count word, and never say "tonight".

**The companion (T012, ADR 0008).**

- The tiny AI lives in the old telescope of **Сияна**, a fictional amateur astronomer in Bulgaria. They were separated,
  and v1 never says why. The dimming star is gone.
- **Intro:** one or two storybook lines, shown while every level has an empty `solved`. It does not repeat Earth's
  arrival line.
- **Five memories**, one per world:
  - each is an element inside the page art, lit by `completed`, and never a new row;
  - it glows once when that `completed` flips, worked out from stored state;
  - tapping it opens a card: a textless vignette plus at most two short sentences;
  - the facts are Earth's shadow at dusk, the Moon moving east among the stars, Mars brightening then fading, a moon's
    shadow crossing Jupiter, and the Cassini line through the open rings;
  - the Earth memory names Сияна for a child who skipped the intro.
- **Back cover:** one line quoting Сияна (the sky is best shown to someone) before T009's lines.
- **Voice:** memories are past and undated, in the companion's gender-neutral first person. Сияна is feminine, quoted in
  the present. The companion is never „спътник". Memories never add companion speech inside a level.

## 4. Ruled out, and why

- **Beats:** Moon M6, M7, M8, any dated eclipse, and „пепелява светлина". Mars R5 (it became R6's album idea), R7
  (air trap), R8 (needs an oval orbit) and R9 (Phobos). Jupiter J5 and J6 (folded into J1), J8 (unsourced), J9 (oval,
  "no seasons" trap), J10 (repeats R1) and J11 (no surface). Saturn S5 (overlaps; flattening NEEDS SOURCE), faintness vs
  Sirius, density, the hexagon, standalone seasons or spin, Enceladus, and Jupiter as an S2 contrast.
- **Types:** `zoom-split-star` has no solar-system use by the anchor. `gravity-drop` has no second level.
- **Systems:** the hint currency (a counter that rewards the child who needs help least; ADR 0007); new hidden finds;
  requiring optional markers for the back cover (a hidden checklist).
- **Story:** an astronaut partner (would need near-future fiction); death as the cause; any reunion promise; the
  "how far people have travelled" anchor, now RETIRED.
- **Scope, post-v1:** the Sun (+ Mercury, the owner's preference), Venus, Uranus, Neptune (no honest beat), Pluto (an
  optional bonus page, needs rule 6 amended), the companion finale (finding Сияна), English, deploy, sound, the latitude
  picker, and new folklore.

## 5. Constraints the decision carries

**Global:**

- No number, date, unit, count, ratio or percentage on screen (rule 2), not even in words.
- 2D Phaser for every new renderer. Three.js only for a single body (rule 9).
- Astronomical imagery is real, public-domain or licensed, degraded honestly, never AI-generated, and each image has an
  imagery entry in `sources.md`.
- No folklore beat after Earth. At most a sourced folk name in a fact string.
- Every string is a `content/bg/` key. Every adopted claim is VERIFIED before it ships.

**Schema pins, each with a RED/GREEN validator test:**

- `drives` has no `rotation`.
- Moon renderers and `ring-view` are pinned to `orbitAngle` (reject `spin` and `tilt`). J7 is pinned to `spin`.
- The per-round eclipse/ordinary-month flag goes in the `rotate-match` config (T003).
- The schema's moon-phase description ("only moon-phase is pinned") is updated when `ring-view` joins (T011).
- Validate `remembers` and the hint-step enum.
- Reachability: an `unlocks` chain never makes a threshold unreachable once its head is solved. R1a, J1 and S1 are in
  every passing set, and each level's data states that.

**Per level:**

- **Earth:** its guards live in the 09-09 handoff, not in a ticket:
  - the astronomy corrections (:115-128): `moon-phase` never rotates the Moon, and `seasons-tilt` contradicts the
    distance idea with no exaggerated ellipse;
  - the rule 2 leaks (:145-150): season art, never a date string, and an unlabelled daylight arc;
  - data sourcing (:172-186): real photography only, and every entry VERIFIED before its string.
- **Moon:**
  - Earth's shadow always points away from the Sun; the side-on inset is authoritative.
  - The tilt inset is passive, "a little", with no ephemeris.
  - Say "not every", never "most". No 14%, 5° or 400×.
  - Never "exactly the same size", "doesn't rotate", „тъмна страна", or "no water".
  - Phase wording never uses „лице".
  - M9 imagery looks like a telescope view.
  - The safety string: never at the Sun, never with sunglasses; certified glasses or a pinhole with your back to the Sun;
    never through optics; with an adult; nothing about totality; no ISO code.
- **Mars:**
  - Never "stops" or "reverses", and never "loop".
  - No dates on dots or slider.
  - R2 is at one true scale.
  - R3 never promises 2003-style views or features, keeps „може би най-забележителното", and never names the dark
    patches.
  - R6's blue is only near the setting Sun; never "the sky is blue" or "no air".
- **Jupiter:**
  - The moons are „спътници", never stars, and "up to four".
  - The J2 solve compares strip positions, never the hidden time. A moon in front is never a bright dot.
  - Galileo "worked out", never "saw them go round".
  - The Red Spot is "often pale", with no size.
  - J3 says „по-широк", never heavier.
  - J4 is never „до Сириус"; both are in the J2000 frame.
  - J7 has no hour marks and says "helps stretch".
  - Never "gas all the way to the centre". The completion line says only „дърпа"/„притегля".
- **Saturn:**
  - S1 is a circular orbit and never `tilt`. Never „изчезват", "every 15 years", or "open a little more every month". The
    thin line appears only in the inset.
  - S2 is "slowest of the five", and the gap is never "stopped".
  - S3 never says "largest" or "heavier"; it says „плътна"; PIA20016 is labelled infrared.
  - S4 never says "spin like a record", and has no piece sizes.
  - No ring thickness.
  - Credit lines are required for PIA06230 and PIA20016.
- **Companion and back cover:**
  - Saturn is a point of light to the eye; its rings appear only in telescope frames.
  - Say „обикновено" for steadier planets; never "planets don't twinkle".
  - Planets are "near", never "on", the Sun's path.
  - The Apollo 17 / "how far people travelled" anchor is RETIRED; reviving it means re-checking it first (Artemis).

## 6. Build follow-up inventory

The raw list the v1-build map schedules. It is deduplicated from every ticket's build follow-ups, the road-to-v1 Notes
and its struck imagery patch (`road-to-v1/MAP.md:106-137`).

- **Prune (T005):**
  - drop both types' enum entries and schema branches; seven → five in the enum description;
  - delete `src/puzzles/zoom-split-star/`, `earth-gravity-drop` and `puzzle.earth.gravity-drop.label`;
  - delete `fact.gravity-drop`, `.apollo`, `.bodies` and `fact.mizar-alcor.1-4`;
  - fix `tests/test_validate_levels.py` and the `game-state.test.ts` fixture;
  - update the star-catalogue rationale (do not grow the file);
  - `sources.md`: the RETIRED rows and re-keys listed in T005;
  - docs: "seven" → "five" (CLAUDE.md, README, `docs/design/*`, `challenger.md`, checker memory); correct
    `puzzle-types.md`'s Moon `gravity-drop`.
- **Earth (the widened scope in §1: phase-2 #3–#9, then the rest):**
  - the overlay, companion box (`content/bg/companion.json` plus its `content.ts` import) and progress write;
  - widen `planet-render` with the disposal proof;
  - the NASA Earth texture;
  - three `rotate-match` renderers, each played;
  - beat 4's `dataRef` to `seasons`;
  - a pedagogy pass;
  - reduced motion;
  - latent bugs 4, 5, 7, 8 and 10;
  - remove `ui.puzzle.coming-soon` by v1;
  - resolve the `fact.day-night` repeat;
  - engines and renderers for the six beats #6 does not build (`parallax-compare`, two `trajectory-match`,
    `connect-the-dots`, `telescope-focus`, the `moon-phase` renderer), plus #25.
- **Schema:** everything in §5's pins; the hint-step enum; `remembers`; `ring-view`; Moon renderer(s) or view modes;
  three-rung `telescope-focus`; multi-body `trajectory-match`; two-panel `connect-the-dots`; J7 spin renderer.
- **Data:**
  - the `dataRef` seam to `data/reference/`, or a sibling loader, with a RED/GREEN test. This supersedes the 09-09
    handoff's "`dataRef` resolves under `data/generated/` only" (:172-176; T006, T011);
  - radius rows for the Moon, Mars, Jupiter, Ganymede, Mercury and Titan;
  - the Galilean periods and orbit radii (NSSDC, not JPL's mean-element column);
  - Jupiter's and Earth's rotation periods;
  - the C, B and A ring radii;
  - `saturn-ring-geometry.json`, with a test that the start renders a narrow south face;
  - trim or re-document the Moon and Mars rows of `surface-gravity.json` and `tests/test_reference_data.py:91`
    (T006);
  - `test_reference_data.py` for all of it.
- **Content:**
  - facts, pointing nudges, album keys, labels and completion lines per level;
  - the eclipse safety key;
  - body names (Ganymede, Mercury, Titan);
  - blurbs: Moon and Mars rewritten, Jupiter and Saturn new, each with a claim check;
  - the companion intro, five memories and the back-cover lines;
  - drop `ui.book.locked`;
  - `pedagogy-report` and `astronomy-report` on every batch.
- **Storybook:** Jupiter's and Saturn's pages with real `sceneKey`s; the grid; the back cover; the ribbon; memory
  elements; the intro.
- **Imagery (placeholder allowed until replaced):**
  - per-marker page art;
  - the Earth texture;
  - M9 frames (telescope-like);
  - an R3 disc frame (honestly degraded HST, or licensed);
  - PIA19400;
  - J1 rung-3 frames;
  - the J7 close-up;
  - Ganymede and Mercury discs;
  - the J4 sky frame;
  - PIA06230 and PIA20016;
  - five Сияна vignettes (hand-drawn from a cited reference or real photos);
  - back-cover vignettes;
  - Earth's telescope-Saturn art.
  - All go through `process-textures.py` at ≤2048px WebP, each with a `sources.md` imagery entry.
- **Agent memory:**
  - the checker's Galilean, NSSDC, J2000 and JPL-column notes (T006);
  - PIA03156, ring-speed and Wayback notes (T011);
  - the settled-sources and folk-figures lines (T005).
