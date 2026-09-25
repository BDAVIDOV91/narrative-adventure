---
id: "006"
title: Jupiter level design: beats, types and the required/optional split
type: grilling
status: closed
assignee: owner
blocked_by: ["005", "007"]
---

## Question

What does the Jupiter level teach, and through which types? Jupiter is roster page 4 and open at 0.7 (ticket 001).
Decide:

- the beats;
- the type for each;
- the required/optional split;
- the companion tier count.

Candidates come from research 007, plus the Jupiter rows of research 002. Keeping a type alive is not a design goal.

Fixed:

- **Only types that survive ticket 005.**
  - Jupiter comes after the ADR 0006 anchor, so its use cannot revive a deleted type.
  - `zoom-split-star` is gone.
- **The moons.** The Galilean moons are "up to four" points in one undated, schematic arrangement.
  - Nightly positions would need a new pipeline, which is barred.
  - Binoculars, never the naked eye (NOT ATTESTED in `docs/sources.md`).
  - Never call the moons stars.
- **Hide the math.** Ganymede against Mercury, and Jupiter against Sirius, are visual comparisons only. No radius,
  magnitude or period on screen.
- **Physical constants.** Radii and the Galilean periods (#20, NEEDS SOURCE) are cited `data/reference/` rows.
- **Content.** Every string is a `content/bg/` key.
  - `fact.telescope-jupiter` (VERIFIED, `docs/sources.md` "Through a small telescope") is not yet wired to any beat, so it is free to adopt.
  - Earth's telescope beat rewards Saturn.
- **No folklore beats.**
- **The data window** is 365 days, which shows only about 30° of Jupiter's orbit.

If research 007 finds too few honest beats for a required spine, raise it with the owner through `AskUserQuestion`.
This does not reopen ticket 001; it reports what the designed level can carry.

Close only when every claim the design adopts is VERIFIED in `docs/sources.md`.

Settled by ticket 004: Mars reuses `telescope-focus`, `trajectory-match` and `parallax-compare`, so all three types
Jupiter's spine needs (research 007) have a second level. Jupiter's viability condition is met, pending 005.

Settled by ticket 005:

- **Five types survive**: `rotate-match`, `connect-the-dots`, `parallax-compare`, `trajectory-match`,
  `telescope-focus`. `gravity-drop` and `zoom-split-star` are deleted, so the "`gravity-drop` never models mass" wall
  is retired.
- **Candidate fact: `fact.gravity-drop.bodies`** (Moon slow, Mars faster, Jupiter much stronger pull), backed by
  `data/reference/surface-gravity.json`. It is not adoptable verbatim, since two thirds of it is about the Moon and
  Mars. A Jupiter use may say only "pull", never falls or lands (no true surface; `docs/sources.md:1286`). The value is
  the 1-bar row. A rewrite is a new string and needs its own wording check. If this ticket declines it, the claim is
  marked RETIRED and the build deletes the reference file and its test.

## Resolution

Grilled with the owner on 2026-09-25 in three rounds, then challenged by two `challenger` agents (both "revise"),
whose six open points the owner answered. Claims: [research/006-jupiter-claims.md](../research/006-jupiter-claims.md),
all sixteen VERIFIED in `docs/sources.md` ("Jupiter level — the claims ticket 006 adopts"), every quote read on its
full page. #20 ("Jupiter's Galilean moons") is re-statused VERIFIED for a schematic, undated use.

**The level.** Open, 0.7 of required markers. **All five markers are required**, so the child needs 4 of 5. J2 opens
only after J1, so the real rule is **J1 (the spine), then any 3 of J2, J3, J4 and J7**. Companion: **2 tiers** (nudge +
fact), one `reward.fact` per marker.

| Marker | Type | Opens | Teaches | Fact / nudge |
| ------ | ---- | ----- | ------- | ------------ |
| J1 The ladder | `telescope-focus`, three rungs in one marker: eye → binoculars → small telescope; solved when the telescope rung is sharp | start | "It's a star"; "a telescope shows Hubble pictures" | Fact: `fact.telescope-jupiter`. Nudge: the Red Spot is often pale and hard to see, and on view only while it faces us |
| J2 The moons move | `trajectory-match`: a top-down panel with the four moons at true relative scale and speed, beside an edge-on strip; the child moves time until the strip matches a target line-up | after J1 | "The dots are stars"; "moons stay put"; "always four" | Fact (new): the dots are moons; we see their orbits almost edge-on, so they line up; Galileo saw the dots move and worked out that they circle Jupiter. Nudge (new): up to four show; a moon can be behind Jupiter or in front of it |
| J3 Ganymede is wider than Mercury | `parallax-compare`: two discs at one true scale | start | "Moons are always smaller than planets" | Fact (new): the largest moon, wider than Mercury. Nudge (new): a moon can be bigger than a planet |
| J4 Brighter than Sirius | `parallax-compare`: a wide evening sky, Feb–Apr 2027, Jupiter and Sirius at their true separation (about 50°); the child points a binocular circle at each bright dot, and one shows up to four moons in a line | start | "Planets shine by themselves"; "the brightest dot is a star" | Fact: `fact.brightest-why`. Nudge: a new key trimmed from `fact.brightest-is-a-planet`, without Venus |
| J7 The fast spin | `rotate-match`, `drives: spin`: the child drags Jupiter and a paired Earth globe turns in step but slower; **a round ends when Earth has made one full turn**, while the Red Spot sweeps past twice and a bit more | start | "Every planet's day is about as long as ours" | Fact (new): the shortest day of any planet. Nudge (new): the fast spin helps stretch its clouds into long stripes |

**Completion line:** a new key (e.g. `fact.jupiter.complete`), "Jupiter pulls much harder than Earth", shown when the
gate is met (4 of 5). `fact.gravity-drop.bodies` is deleted in the build. `data/reference/surface-gravity.json` stays.

**Out:** J9 tilt (the "no seasons" trap, and it needs the walled-off oval orbit), J10 slow loop (repeats Mars R1;
stationary dates unsourced), J11 drop (no surface), J8 squashed disc (not sourced as visible in a small telescope). J5
and J6 are not beats; they fold into J1.

**Sirius in J4 is a foil, not a target** (rule 6). The child's target is Jupiter. Sirius is already VERIFIED and
shipped in `fact.lazhi-kervan`. This is not the Mizar/Alcor case that deleted `zoom-split-star`.

**Guards the build must hold:**

- No numbers on screen: no periods, hours, radii, magnitudes, dates or percentages. No hour marks on J7's globes.
- The moons are never called stars („спътници"). "Up to four", never "four". J2's strip moves and once shows a moon
  passing behind the disc; a moon in front is never drawn as a bright dot over it. Hiding behind or in front are never
  presented as the only reasons (Jupiter's shadow is a third). No date, no "tonight". Callisto is not locked to the
  others' rhythm.
- J2: the target line-up is generated from the model at build time. The solve compares strip positions within a
  tolerance, never the hidden time (front/back mirror states look the same). Galileo "worked out" that the moons
  circle Jupiter; never "saw them go round", never "proved Earth goes round the Sun".
- J1: rung 2 (binoculars) is one undated, schematic arrangement, with no belts. Rung 1 shows no twinkle contrast.
  Moons never with the naked eye. Any reveal text on rungs 1–2 needs a claim row.
- The Red Spot: "often pale and hard to see" in telescope frames. No size claim ("twice Earth" is DISPUTED). The J7
  close-up is real processed imagery framed as seen up close, never a bleached NASA image.
- J3: „по-широк" or „по-голям на ръст", never heavier. The ~8% margin is drawn true.
- J4: never "beside" or „до Сириус"; a wide view at the true separation. Jupiter and Sirius are both in the J2000 frame
  (the checker compared the committed positions with JPL Horizons), so do not convert only one. The reveal carries
  `fact.brightest-why`.
- J7: Earth at true relative size or in a separate inset; both turn the same way. The ratio is drawn, never stated.
  "Helps stretch", since how the jets form is still an open question.
- "Ball of gas" may ship, but never "gas all the way to the centre".
- The completion line says only „дърпа" or „притегля": never falls, lands, stands or weighs.
- J3 and J7 draw in 2D Phaser (rule 9). Imagery is public-domain or licensed, degraded honestly, never AI.
- No folklore beat.

**ADR 0006, reverse dependency.** Jupiter's uses change no reopen set. If the build cuts a set and deletes its type,
this ticket reopens for the Jupiter markers on it: R1b → J2; M9 and R3 → J1; M5, R2 and R6 → J3 and J4. Recorded in
ADR 0006 "When to revisit".

**Build follow-ups, beside the map and not tickets:**

- Data: cited `data/reference/` rows for the Galilean periods and orbit radii, and for the radii of Jupiter (71,492 km
  equatorial), Ganymede and Mercury. Also Jupiter's and Earth's rotation periods. Take the values from the NSSDC
  _Jovian Satellite Fact Sheet_; never from JPL's mean-element period column, which is 0.4–0.7% off.
- **The `dataRef` seam** resolves only under `data/generated/` (schema and `data/scripts/validate-levels.py:164-172`).
  Extend it to `data/reference/` with a RED/GREEN validator test, or add a sibling loader. The Moon and Mars radius
  rows need the same.
- Configs: `telescope-focus` with three rungs, `trajectory-match` driving four bodies, `parallax-compare` for the disc
  pair and for the binocular sky. For J7, a `rotate-match` renderer value (or a Jupiter skin on `day-night`), pinned to
  `spin`.
- Gate: J1 carries `reward.unlocks: [<j2-id>]`. Add a validator test that the chain never makes the threshold
  unreachable, and state the level's reliance on J1 in its data.
- Content: new keys for the J2, J3 and J7 facts and nudges, the J4 nudge, the completion line, five
  `puzzle.jupiter.*.label` keys, and body names for Ganymede and Mercury. Run `pedagogy-report` and `astronomy-report`
  on them. `level.jupiter.blurb` is ticket 001's follow-up and needs a claim check.
- Delete `fact.gravity-drop.bodies`. Trim or re-document the Moon and Mars rows of `surface-gravity.json` and
  `tests/test_reference_data.py:91`.
- `astronomy-accuracy-checker` agent memory: the Galilean entry is settled, the NSSDC sheets are live again, the
  ephemeris is in the J2000 frame, and the JPL period column is off.
