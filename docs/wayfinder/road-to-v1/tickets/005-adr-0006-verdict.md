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
- **Earth's uses** (`src/scenes/earth/earth-data.json`): `rotate-match` four, `trajectory-match` two (orbit-year,
  Зорница), every other type one, `zoom-split-star` none. Every type survives only through a Moon or Mars reuse.
  (Corrected by ticket 004's challenger; it previously said "exactly one" for all but `rotate-match`.)

Record the verdict as an amendment to `docs/adr/0006-seven-puzzle-types-not-thirteen.md`, then prune the schema enum
in the build that follows.

Settled by ticket 003:

- **The Moon uses** `rotate-match` (M1, M3, M2, eclipse), `parallax-compare` (M5 near/far) and `telescope-focus`
  (M9 seas and craters). It does not use `gravity-drop`, `trajectory-match` or `zoom-split-star`.
- M5 and M9 were chosen for their astronomy. If the build cuts either, this verdict reopens.

Settled by ticket 004 (owner, 2026-09-25):

- **Mars uses** `connect-the-dots` (R1a, the path among the stars), `trajectory-match` (R1b, why it turns back),
  `telescope-focus` (R3) and `parallax-compare` (R2, R6). It does not use `rotate-match`, `gravity-drop` or
  `zoom-split-star`.
- **`connect-the-dots` survives solely on R1a**, which is a split of research 002's single retrograde beat R1 into
  "see it" and "why". The owner chose the split for its teaching order (real observers plotted the path, then explained
  it) and saw the type-survival caveat when choosing. Cutting R1a in the build deletes the type and reopens this ticket;
  so does cutting R1b, R3, R2 or R6.
- **`gravity-drop` has no second level.** Mars's R7 was cut on its astronomy: it repeats Earth's Mars rung, and
  Mars's thin real air makes neither air flag honest. The owner accepts that the trigger deletes the type, and that
  this overrides MAP.md's fixed input "Earth's ten beats": `earth-gravity-drop` goes, and Earth ships nine.
  - **Delete the type, move the facts.** The "air, not weight" lesson and the Moon/Mars/Jupiter pull comparison move
    onto existing markers' `reward.fact` or nudge. This ticket settles the placement key by key. Loss accepted: the
    lesson becomes something the child reads, not something they play.
  - **What the prune strands**, beside the facts:
    - `earth-gravity-drop` (`src/scenes/earth/earth-data.json:161-173`);
    - `puzzle.earth.gravity-drop.label` (`content/bg/puzzles.json:9`);
    - the schema branch (`schemas/level-data.schema.json:148-154`) and enum entry (`:173`);
    - `data/reference/surface-gravity.json` and `tests/test_reference_data.py:30`, unless a moved fact still reads it;
    - `tests/test_validate_levels.py:81-86` (uses `gravity-drop` as the accepted-type example);
    - the `src/shared/game-state.test.ts` optional-marker fixture (`earth-gravity-drop`, lines 24, 64, 75);
    - `docs/sources.md`: the air/Apollo 15 and surface-gravity entries are **marked retired, not deleted**, like
      Mizar/Alcor, and the "`fact.gravity-drop.bodies` stays" line (`:1009`) is updated to agree;
    - docs naming the type: `CLAUDE.md:96-98`, `docs/adr/0006-seven-puzzle-types-not-thirteen.md:27,29,41` (":29"
      says all ten Earth beats ship), `docs/design/puzzle-types.md`, `docs/design/earth-level-brief.md:42,86`;
    - the MAP.md wall "`gravity-drop` never models mass", and ticket 006's copy of it, both retire with the type.

