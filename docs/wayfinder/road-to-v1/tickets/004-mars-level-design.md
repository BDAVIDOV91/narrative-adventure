---
id: "004"
title: Mars level design: beats and types
type: grilling
status: open
assignee: ""
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
