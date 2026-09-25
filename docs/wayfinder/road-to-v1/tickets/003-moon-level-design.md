---
id: "003"
title: Moon level design: beats, types and the required spine
type: grilling
status: closed
assignee: owner
blocked_by: ["002"]
---

## Question

What does the Moon level teach that Earth's `moon-phase` beat does not, and through which existing types?

The Moon is guided at 1.0 of its **required** markers. Decide:

- the beats;
- the type for each;
- which beats form the required spine;
- the companion tier count.

Fixed:

- Earth's `moon-phase` beat stays on Earth (a settled input). If both levels touch phases, say how the two relate.
- Nothing rotates the Moon: `drives` has no `rotation`. Phases are orbit angle only.
- `gravity-drop` never models mass. Its vacuum panel is anchored to Apollo 15.

Candidates come from research 002. Keeping a type alive is not a design goal.

The level blurb in `content/bg/levels.json` ("сменя лицето си всяка нощ") points at phases, and may need rewording to
match. That is content, not a decision.

Candidates added by ticket 001:

- **The Sun–Moon almost-same-size beat.** Never "exactly" the same size: that wording is NOT ATTESTED.
- **The partial solar eclipse from Bulgaria on 2027-08-02.** It is always "partial". It is the Moon passing between
  the Sun and Earth, on the same `orbitAngle` drag as M3.

If either is adopted:

- **A safety string is mandatory.** It must be sourced from NASA or AAS eclipse safety, name a safe method (pinhole
  projection, or certified eclipse glasses with an adult), and never suggest sunglasses.
- **No Sun through `telescope-focus`** or any other zoom type.
- **This ticket cannot close** while that string is NEEDS SOURCE.
- **The eclipse wording must survive the date passing:** the game may ship after 2027-08-02.

Close only when every claim the design adopts is VERIFIED in `docs/sources.md`.

## Resolution

Grilled with the owner on 2026-09-25 in three rounds, then challenged by two `challenger` agents (both "revise"), whose
four open points the owner answered. Claims: [research/003-moon-claims.md](../research/003-moon-claims.md), all ten
VERIFIED in `docs/sources.md` ("Moon level — the claims ticket 003 adopts"), with every quote read on its page.

**The level.** Guided, 1.0 of required markers. Companion: **2 tiers** (nudge + fact). One `reward.fact` per marker;
a second idea goes to that marker's nudge.

| Marker | Type | Required | Teaches | Fact / nudge |
| ------ | ---- | -------- | ------- | ------------ |
| M1 The Moon turns | `rotate-match` `orbitAngle` | yes, 1st | "The Moon doesn't rotate" is false. A fixed distant-star arrow is drawn; each round's target is "the crater points at the star", so the child *sees* the Moon turn | Fact: it turns once per trip around Earth |
| M3 Shadow or phase | `rotate-match` `orbitAngle`: phase rounds, Earth's shadow drawn, passive side-on tilt inset | yes, 2nd | Phases are not Earth's shadow; doubles as the phase recap for a child who skipped Earth's optional `earth-moon-phase` | Fact: shadow ≠ phase (Earth's shadow on the Moon is an eclipse, and not every full Moon has one). Nudge: earthshine, described, never named |
| M2 The far side is lit | `rotate-match` `orbitAngle`, top-down panel | yes, 3rd | No "dark side" | Fact: existing `fact.moon-far-side` |
| Solar eclipse | `rotate-match` `orbitAngle`: the Moon's shadow on Earth, passive tilt inset | no | Only at new Moon, and not every new Moon | Fact: Sun and Moon look *almost* the same size. **Safety string is its own key, shown whenever the beat opens, not gated on solving** |
| M5 Near and far Moon | `parallax-compare` | no | "A supermoon is huge" is false: closest vs farthest differ only a little | Fact: the size difference. Nudge: when the far Moon crosses the Sun, a ring of Sun shows (annular) |
| M9 Seas and craters | `telescope-focus` | no | The "seas" are old lava; relief shows best along the day–night line | Focus the quarter-Moon crater; on solve, the same crater at full Moon slides in beside it (a reveal, not a second interaction). Fact: maria are lava. Nudge: shadows at the terminator |

Spine chains through `reward.unlocks`: M1 → M3 → M2. The optional markers are open from the start, as on Earth.

**Out:** M6 horizon Moon, M7 daytime Moon, M8 hammer and feather (it only repeats Earth), any dated eclipse (no
2027-08-02 string), and the term „пепелява светлина".

**Guards the build must hold:**

- No `rotation` drive. Every Moon renderer (new enum value or `moon-phase` view mode, the build plan's choice) is
  pinned to `orbitAngle` in the schema, with a RED/GREEN validator test rejecting `spin` and `tilt`.
- Earth's shadow always points straight away from the Sun. The top-down view never shows the Moon darkened inside
  the shadow on an ordinary month; the side-on inset is authoritative.
- The tilt inset is passive and schematic. Each round's config presets it as an "eclipse month" or an "ordinary
  month" (a per-round flag added to the rotate-match config). No ephemeris, no second drag; solving depends only on
  the phase match. The tilt is "a little", never a steep ramp.
- Wording: "not every full/new Moon", never "most" (not in the sources). The Moon's shadow on Earth is a small patch,
  with no "seen only there".
- Safety string: never look straight at the Sun; not with sunglasses, however dark; certified eclipse glasses or a
  pinhole with your back to the Sun, never looking through the hole; never through binoculars, a telescope or a
  camera, not even with eclipse glasses; with an adult (AAS). Nothing about totality. No "ISO 12312-2" in child text.
- No numbers on screen: no 14%, 5° or 400×. Never "exactly the same size", never "doesn't rotate", never "тъмна
  страна", never "no water on the Moon".
- Phase wording never uses „лице": that is M1's word for the near side.
- Moon `rotate-match` renderers are 2D Phaser. Three.js is only for a single-body view, if any (rule 9).
- M9 imagery must look like a telescope view (Earth-based photos, or LRO scaled down), not orbital close-ups.
- M5's discs come from `bodies.moon.distanceAu` via `dataRef`, never a remembered percentage.

**Input to ticket 005.** The Moon uses `rotate-match`, `parallax-compare` (M5) and `telescope-focus` (M9). It does
not use `gravity-drop`, `trajectory-match` or `zoom-split-star`. M5 and M9 were chosen for their astronomy, and 005
counts them, so cutting either during the build reopens 005. If the build overruns, the eclipse beat is cut first.

**Build follow-ups, beside the map and not tickets:**

- **First content fix:** `level.moon.blurb` (`content/bg/levels.json:6`, "сменя лицето си всяка нощ") contradicts M1.
  Rewrite it to say the lit part changes and the face stays.
- The `rotate-match` schema change: Moon renderer(s) or view modes, the `orbitAngle` pin and its test, and the
  per-round eclipse/ordinary flag.
- New `content/bg` fact, nudge and safety keys.
- `docs/design/puzzle-types.md:14` lists `gravity-drop` on the Moon; M8 is cut, so correct it.
- Mechanical texture processing for M9 and M5 via `process-textures.py`, once the fog below settles which frames.
