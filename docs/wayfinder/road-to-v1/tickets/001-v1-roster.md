---
id: "001"
title: Which worlds make the v1 roster, and in what order
type: grilling
status: open
assignee: ""
blocked_by: ["002"]
---

## Question

Which worlds get a storybook page in v1, and in what order? Earth is first and the Moon second, both guided at 1.0.
Every other page is open at 0.7; that gating is a fixed input.

Decide, using research 002's honest-beat list:

- **The Sun**: its own level, or a backdrop to the others?
- **Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune**: in or out. A world with no honest beat in 002 is out.
- **Which moons count as major**, and whether any moon gets its own page or appears inside its planet's level.
- **Order**: where Mars sits. If Mars is not page 3, restate the ADR 0006 anchor as "by the third roster level's
  build". If Mars is cut, ticket 004 closes out of scope.
- **Content keys for worlds that are cut**: `content/bg/levels.json` already names Jupiter and Saturn. A cut world's
  keys go, per the "no stubs" bar.

Constraints: rule 6; a world whose beats need data that does not exist yet has to say what data (the round-1 pivot
bars new pipeline).
