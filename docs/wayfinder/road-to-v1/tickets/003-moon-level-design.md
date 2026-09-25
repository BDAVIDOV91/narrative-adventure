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

Close only when every claim the design adopts is VERIFIED in `docs/sources.md`.
