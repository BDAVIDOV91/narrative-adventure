---
id: "004"
title: Mars level design: beats and types
type: grilling
status: closed
assignee: owner
blocked_by: ["001", "002"]
---

## Question

What does the Mars level teach, and through which existing types? Mars is open at 0.7. Decide:

- the beats;
- the type for each;
- the required/optional split;
- the companion tier count.

From ticket 001 this takes Mars's roster slot and whether it is still the ADR 0006 anchor level. If 001 cuts Mars,
close this ticket out of scope.

- **Retrograde** (the blurb, "понякога тръгва назад по небето") is the leading candidate, not a commitment. It is
  sourced in `docs/sources.md`, and `helioLonDegrees` for Earth and Mars already exists.
- Check `gravity-drop` reuse (Mars 3.73 m/s² is VERIFIED) against the walls: never mass, and never a Mars-vs-Mercury
  "which pulls harder" comparison.

Candidates come from research 002. Keeping a type alive is not a design goal.

Settled by ticket 001:

- **Mars is roster page 3**, and it stays the ADR 0006 anchor.
- **Phobos is not a major moon**, so beat R9 is out.

Close only when every claim the design adopts is VERIFIED in `docs/sources.md`.

Settled by ticket 003: the Moon already reuses `parallax-compare` and `telescope-focus`. `gravity-drop` and
`trajectory-match` have no Moon use, so Mars is their only possible second level (ticket 005). That is an input, not a
design goal: a Mars beat still earns its place on its astronomy.

## Resolution

Grilled with the owner on 2026-09-25 in three rounds, then challenged by two `challenger` agents (both "revise"), whose
two open points the owner answered (the R1a gate, and where `gravity-drop`'s facts go). Claims:
[research/004-mars-claims.md](../research/004-mars-claims.md), every adopted claim VERIFIED in `docs/sources.md`
("Mars level — the claims ticket 004 adopts"), with every quote read on its full page.

**The level.** Open, 0.7 of required markers. **All five markers are required.** R1b opens only after R1a, so the real
rule is **R1a (the spine), then any 3 of R1b, R3, R2 and R6**. Companion: **2 tiers** (nudge + fact), one
`reward.fact` per marker.

| Marker | Type | Opens | Teaches | Fact / nudge |
| ------ | ---- | ----- | ------- | ------------ |
| R1a Mars's path among the stars ("see it") | `connect-the-dots` | start | Mars seems to turn back against the stars | Fact: it's an illusion; Earth catches up with Mars and overtakes it. Nudge: Earth has the inside lane |
| R1b Why it turns back ("why") | `trajectory-match` | after R1a | "Mars really reverses" is false | Fact: Earth moves faster than Mars |
| R3 Mars in a telescope | `telescope-focus` | start | A telescope shows a small red disc, not the photos | Fact: red from rust; Mars is a cold world. Nudge: darker patches show best when Mars comes closest |
| R2 Never as big as the Moon | `parallax-compare` | start | The "Mars as big as the Moon" hoax | Fact: the hoax is false. Nudge: not even at its closest |
| R6 Blue sunset | `parallax-compare` | start | "Mars sunsets are red" | Fact: a camera on Mars saw blue near the setting Sun. Nudge: a Mars day is a little longer than ours |

**Why R1 is two beats.** Real observers plotted the path first and explained it afterwards; the child does the same.
R1a's own fact carries the debunk, so reaching it alone still teaches the truth.

**Out:** R7 falling on Mars (it repeats Earth's Mars rung, and Mars's thin real air makes neither air flag honest), R8
Mars seasons (it needs the walled-off orbit oval), R5 as a beat (it repeats Earth's day length; it is now R6's nudge)
and R9 Phobos (ticket 001).

**Guards the build must hold:**

- Never "Mars stops" or "reverses". The top-down panel keeps Mars moving forward the whole time.
- R1a: about 15–25 dots, Nov 2026 – May 2027, subsampled from committed Mars RA/Dec and drawn against real
  `stars.json` background stars (Regulus is beside the path). No numbers or dates on the dots; the order cue is
  visual (the next dot glows, or the dots appear night by night). Say "turns back", never "loop".
- R1b: the Earth→Mars sight line is drawn onto the star strip. Solve = scrub to the moment the sky dot turns back.
  No date on the time slider.
- R2: the Mars-beside-Moon panel is at one true scale. Any enlarged near/far view is framed as a telescope circle,
  never beside the Moon. Discs come from `distanceAu` plus cited radius rows.
- R3: never promise the 2003 view, polar caps or named features for 2027 (a small, aphelic opposition). Never
  "not because it is hot" (no sourced page states it). No telescope sizes. Keep APOD's hedge ("possibly the most
  striking"): „може би най-забележителното", never a flat superlative. Never say what the dark patches are (APOD's
  "smooth lowlands" is not reused). Never cite ALPO's "largest on July 01, 2027" sentence (its own table contradicts it).
- R6: the blue is near the setting Sun. Never say or imply that the Mars sky is blue (NASA: "hazy and red"). "A camera
  on Mars saw"; never "always". No "Mars has no air".
- No numbers anywhere: no dates, sizes, speeds, hours or temperatures.

**Input to ticket 005** is recorded there: Mars uses `connect-the-dots`, `trajectory-match`, `telescope-focus` and
`parallax-compare`. `connect-the-dots` survives on R1a alone. `gravity-drop` has no second level: the type is deleted
and its facts move to other markers.

**Build follow-ups, beside the map and not tickets:**

- Reword `level.mars.blurb` (`content/bg/levels.json:9`) to "seems to" (e.g. „сякаш тръгва назад"), with
  `pedagogy-report` on the wording.
- `connect-the-dots` reads dots from two sources: the star catalogue (Big Dipper) and the ephemeris via
  `dataRef: orbital-positions.json#/bodies/mars` (Mars). The `dataRef` seam already exists, so no schema change is
  needed.
- A validator test: a `reward.unlocks` chain must never make the threshold unreachable once its head is solved, and
  Mars's reliance on R1a is stated in the level data.
- A Mars radius row, the Moon radius row (shared with ticket 003), the R3 disc frame (public-domain NASA/HST,
  degraded honestly and documented, or licensed, never AI) and PIA19400: all in MAP fog "Imagery and data".
- The dead `mars.nasa.gov` URLs are cited as Wayback copies in `docs/sources.md`.
