---
id: "011"
title: Saturn level design: beats, types and the required/optional split
type: grilling
status: closed
assignee: owner
blocked_by: ["010"]
---

## Question

Design Saturn's level the way tickets 004 and 006 designed Mars and Jupiter. That covers the beats, their types, which
are required, the spine, and the companion tier count.

Constraints, not to be re-asked:

- Everything in [What Saturn can teach, deep](010-what-saturn-can-teach.md), including its fail condition: if 010 found
  fewer than three honest required beats, close this ticket out of scope instead.
- The five kept types only. Once Saturn's types are known, append a Saturn reverse-dependency line to ADR 0006
  "When to revisit" (like Jupiter's).
- Hints and nudges follow ticket 008 and ADR 0007. Every adopted claim is VERIFIED by `astronomy-accuracy-checker`
  before this ticket closes.
- Saturn is the last world page. The back cover follows it and unlocks when Saturn is completed (ticket 009).

## Resolution

Grilled with the owner on 2026-09-26 in three rounds (Q1–Q10), then challenged by two `challenger` agents. Both
returned "revise"; the owner answered their four open points (C1–C4), and every other finding was folded in as a wording
or plan fix. Claims: [research/011-saturn-claims.md](../research/011-saturn-claims.md). All nineteen are VERIFIED in
`docs/sources.md` ("Saturn level — the claims ticket 011 adopts"), and every quote was read on its full page.

**Saturn stays in v1 on four required beats.** The 010 fail line did not trigger. S2 is not a Mars repeat (Q1): it is
the same interaction teaching a new lesson, "far means slow". S4's claim, that the inner ring pieces go faster, is
VERIFIED from Keeler 1895 (ApJ 1, 416) and NASA _Cassini: Saturn Rings_.

**The level.** Open, 0.7 of required markers. **All four markers are required**, so the child needs 3 of 4. S4 opens only
after S1, so every passing set contains S1: the real rule is **S1 (the spine), then any 2 of S2, S3 and S4**. The
completion line therefore always follows the S1 lesson. Companion: **2 tiers** (nudge + fact), one `reward.fact` per
marker. Hints are free per ADR 0007.

| Marker | Type | Opens | Teaches | Fact / nudge / album second idea |
| ------ | ---- | ----- | ------- | -------------------------------- |
| S1 The rings come and go | `rotate-match`, new renderer **`ring-view`**, pinned in the schema to `drives: orbitAngle` like `moon-phase`. `targets: 3`: open from above, a thin line, open from below. An oblique three-quarter view of a circular orbit, with the axis arrow parallel all the way round. Saturn starts at its real place; the "what we see" inset updates live. The solve compares the inset view (opening and face) within a tolerance, never the hidden orbit angle, so either edge-on position counts | start | "The rings tip"; "the rings vanish" | Fact: the rings never tip; they keep facing the same way in space, and we see them from a different side as Saturn goes round. Nudge: points at the fixed axis arrow. Album: Saturn has seasons too |
| S2 The slowest wanderer | `connect-the-dots`, **two side-by-side panels at one angular scale**, each on its own real star field, over R1a's months (Nov 2026 – May 2027). Mars's loop is pre-drawn faint; the child connects Saturn's short creep. The spring gap reads as hidden in the Sun's glare | start | "All planets wander alike" | Fact: of the five planets we see without a telescope, Saturn is the slowest; it is far away, so one trip round the Sun takes very long. Nudge: points at Mars's panel. Album: the gap is the Sun's glare |
| S3 The moon wrapped in fog | `parallax-compare`: our Moon and Titan at one true scale, with "look closer" on each. The Moon shows craters; Titan shows only haze (PIA06230). After the solve comes an infrared view through the haze (PIA20016), labelled an infrared spacecraft picture. Every Titan close-up is labelled a spacecraft view | start | "Moons have no air"; "a bigger telescope shows everything" | Fact: Saturn's largest moon has air so thick that, from above, ordinary light cannot show its ground; cameras that see infrared light can. Nudge: points at the Moon's craters. Album: the only moon with a _thick_ atmosphere |
| S4 The rings are a swarm | `trajectory-match`, mirroring J2: a top-down ring with three marked pieces (inner, middle, outer) that start in a row. The child moves time to a target arrangement in which the inner piece has pulled ahead. Speeds are computed at build time from the cited ring radii, never stated | after S1 | "The rings are a solid disc" | Fact: each piece circles Saturn on its own, and the inner ones go faster. „Спомни си“ recalls Earth's `fact.telescope-saturn` for "countless pieces" instead of restating it. Nudge: points at the inner piece. Album: people found this out by studying the rings' light |

**Completion line:** a new key (e.g. `fact.saturn.complete`): Saturn's tilt gives it seasons, just as Earth's tilt gives
Earth seasons. It says "like", never "only". The back cover unlocks next (ticket 009).

**Out:**

- S5, Saturn's own ladder: it overlaps Earth's beat and J1, and the flattened disc is NEEDS SOURCE.
- Faintness against Sirius: back-cover line only.
- Density ("would float").
- The hexagon.
- A standalone seasons or fast-spin beat.
- Enceladus.
- Jupiter as an S2 contrast: from Nov 2026 to May 2027 it moves no further than Saturn, because it loops round its
  February opposition.

**Guards the build must hold:**

- No numbers on screen: no years, dates, angles, radii, speeds, ratios or counts.
- S1:
  - never `drives: tilt`; a circular orbit, never an oval;
  - never "the rings never moved" or "you moved";
  - never „изчезват": „не изчезват" means only "they are still there", never "you can still see them";
  - the thin line lives in the inset diagram, never in a telescope view;
  - never "every 15 years" (the cited ESA and NASA pages say it; do not copy it);
  - never "the rings open a little more every month" (NOT ATTESTED).
- S2:
  - never „най-бавната планета" unqualified; it is the slowest of the five;
  - the frames are apparent RA/Dec against catalogue-epoch stars, as J4;
  - the small backward drift is not re-explained;
  - the gap is never "Saturn stopped".
- S3:
  - never "the largest moon" or "heavier";
  - "thick" (плътна) is required;
  - "through a small telescope Titan is a dot", never "even through a telescope";
  - never "only spacecraft can see the ground";
  - PIA20016's colours are false, so it is labelled an infrared picture;
  - the orange is never promised in a small telescope.
- S4:
  - never "the rings spin" or "turn like a record";
  - no piece sizes;
  - the target is generated from the model.
- No ring thickness (DISPUTED).
- S1, S3 and S4 draw in 2D Phaser (rule 9).
- Imagery is public domain with its credit line, degraded honestly, never AI:
  - PIA06230: "NASA/JPL/Space Science Institute";
  - PIA20016: "NASA/JPL/University of Arizona/University of Idaho".
- No folklore beat.

**ADR 0006, reverse dependency.** Saturn uses `rotate-match`, `connect-the-dots`, `parallax-compare` and
`trajectory-match`. Its uses change no reopen set. If the build cuts a set and deletes its type, this ticket reopens
for the Saturn markers on that type: R1a → S2; M5, R2 and R6 → S3; R1b → S4. S1 is on Earth's own `rotate-match`
engine, which is in no set. Recorded in ADR 0006 "When to revisit".

**Build follow-ups, beside the map and not tickets:**

- **Schema:** add the `ring-view` renderer value, pinned to `orbitAngle`, with a RED/GREEN validator test. Update the
  schema's moon-phase description, which says only moon-phase is pinned.
- **Data (`data/reference/`, cited rows):**
  - `saturn-ring-geometry.json`: obliquity 26.73°, the IAU pole (NAIF pck00011, rotated into ecliptic-of-J2000 to
    match `helioLonDegrees`), and the 2025-03-23 crossing and 2025-05-06 equinox anchors;
  - a test that the start position renders a narrow south face, consistent with the monthly table;
  - the Moon/Titan radii (NSSDC);
  - the C inner, B and A outer ring radii (NSSDC _Saturnian Rings_);
  - `tests/test_reference_data.py` coverage for all of these.
- **The `dataRef` seam** to `data/reference/`, shared with ticket 006.
- **Gate:** S1 carries `reward.unlocks: [<s4-id>]`. A reachability test asserts that S1 is in every passing set. The
  level data states its reliance on S1.
- **Content:**
  - four facts, four nudges, four album second-idea keys and four `puzzle.saturn.*.label` keys;
  - the completion line;
  - a Titan body name;
  - `remembers` links: S4 → J2, and S4 → Earth's telescope-Saturn marker;
  - `level.saturn.blurb` (with a claim check), Saturn's storybook page and a real `sceneKey`;
  - the hint-step enum value per marker;
  - run `pedagogy-report` and `astronomy-report` on all of it.
- **Imagery:** PIA06230 and PIA20016 through `process-textures.py`, at most 2048px WebP. Earth's `fact.telescope-saturn`
  art shows a narrowly open south face for 2026–27.
- **`astronomy-accuracy-checker` agent memory:**
  - PIA03156 is a Hubble Heritage image, and its caption says "nod majestically";
  - NASA _Saturn Facts_ gives no direction for ring speeds;
  - S&T, In-The-Sky and Britannica need Wayback.
