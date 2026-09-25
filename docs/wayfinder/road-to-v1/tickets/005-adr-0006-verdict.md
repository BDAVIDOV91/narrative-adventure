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

Settled by ticket 001:

- **Jupiter is page 4, after the anchor**, so its use does not count. A post-anchor level designs only from surviving
  types, and cannot revive a deleted one.
- **The owner accepts that `zoom-split-star` is deleted.** The prune build removes what it strands:
  - `fact.mizar-alcor.1-4` (`content/bg/facts.json`);
  - the Mizar and Alcor claim in `docs/sources.md`, which is to be marked as retired, not deleted, so it is not
    re-proposed;
  - its schema branch and enum entry (`schemas/level-data.schema.json`);
  - the `zoom-split-star` rationale in `data/scripts/star-catalogue.py` and `tests/test_star_catalogue.py`.
- **Every type except `rotate-match`** has exactly one Earth use (`src/scenes/earth/earth-data.json`). Each of the
  other types survives only through a Moon or Mars reuse.

Record the verdict as an amendment to `docs/adr/0006-seven-puzzle-types-not-thirteen.md`, then prune the schema enum
in the build that follows.
