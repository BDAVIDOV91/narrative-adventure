---
id: "005"
title: Apply the ADR 0006 trigger to the designed levels
type: grilling
status: open
assignee: ""
blocked_by: ["001", "003", "004"]
---

## Question

Apply ADR 0006's trigger to the levels designed by its anchor. The trigger: any type not reused on a second level by
the Mars build is deleted. The anchor is the Mars build, or the third roster level if ticket 001 restated it.

This ticket applies the trigger; it does not reopen it. For each of the seven types, record which designed levels use
it, then keep or delete it.

- **Start with `zoom-split-star`.** It has zero Earth uses, so it needs two uses across the designed levels, each on
  a solar-system target. Mizar/Alcor is stellar and outside rule 6.
- **Any exception** to the trigger needs an explicit reason.

Record the verdict as an amendment to `docs/adr/0006-seven-puzzle-types-not-thirteen.md`, then prune the schema enum
in the build that follows.
