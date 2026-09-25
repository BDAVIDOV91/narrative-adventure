---
id: "003"
title: Moon level design: beats, types and the required spine
type: grilling
status: open
assignee: ""
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
