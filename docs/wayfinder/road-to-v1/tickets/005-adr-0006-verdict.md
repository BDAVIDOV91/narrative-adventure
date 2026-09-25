---
id: "005"
title: Apply the ADR 0006 trigger to the designed levels
type: grilling
status: closed
assignee: owner
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


## Resolution

Grilled with the owner on 2026-09-25, then challenged by two `challenger` agents. Both said "revise". Their two open
points (where the air lesson goes, and how retired claims are marked) were answered by the owner. The verdict is an
amendment to [ADR 0006](../../../adr/0006-seven-puzzle-types-not-thirteen.md) ("the trigger applied").

**Verdict: five types kept, two deleted, no exceptions.**

| Type | Earth | Moon | Mars | Verdict |
| ---- | ----- | ---- | ---- | ------- |
| `rotate-match` | 4 | M1, M3, M2, eclipse | — | keep |
| `connect-the-dots` | 1 | — | R1a | keep |
| `parallax-compare` | 1 | M5 | R2, R6 | keep |
| `trajectory-match` | 2 | — | R1b | keep |
| `telescope-focus` | 1 | M9 | R3 | keep |
| `zoom-split-star` | 0 | — | — | **delete** |
| `gravity-drop` | 1 | — | — | **delete** |

**Reopens if the build cuts** R1a (`connect-the-dots`), R1b (`trajectory-match`), both M9 and R3 (`telescope-focus`),
or all of M5, R2 and R6 (`parallax-compare`). Ticket 003 and ticket 004 say any cut reopens it; this narrows that to the
sets that actually kill a type.

**Where `gravity-drop`'s facts go:**

- **`fact.gravity-drop` + `fact.gravity-drop.apollo`** merge into one string: the **Moon level's completion line**,
  shown once the spine (M1 → M3 → M2) is finished. Every child reads it, and no hint is displaced. Not a nudge: a
  stall-only nudge on M2 would be off-topic and unseen by a child who solves it quickly. This is not M8 revived; it is
  a line, not a beat. Guards:
  - keep the explicit „Не защото е тежък" clause, the only refutation of "heavy falls faster";
  - „притегляне", never „тегло" or „земно ускорение"; no numbers, no masses, no drop height;
  - the Moon's air: „няма въздух, който да задържи перцето" and/or „почти няма въздух" (VERIFIED, `docs/sources.md:169`,
    NASA's "no air resistance" and "very thin"). The flat „На Луната няма въздух", which opens today's
    `content/bg/facts.json:18`, is **NOT ATTESTED** and must not ship. Never „вакуум", „атмосфера" or „екзосфера".
- **`fact.gravity-drop.bodies`** is handed to ticket 006 (Jupiter) as a candidate. It is not adoptable verbatim, and
  Jupiter may say only "pull", never falls or lands. `data/reference/surface-gravity.json` and
  `tests/test_reference_data.py:30` stay until 006 decides; if 006 declines, the claim is marked RETIRED. Until then
  the key is knowingly unreferenced.

**`docs/sources.md` handling** (owner): a new **RETIRED** status meaning "true, not shipped; reason: …", distinct from
NOT ATTESTED (false). Mizar/Alcor becomes RETIRED (rule 6). The air/Apollo and surface-gravity entries stay live.

**This supersedes** the "What the prune strands" bullet on `docs/sources.md` above. The air/Apollo and surface-gravity
entries are not retired, and the "`fact.gravity-drop.bodies` stays" line is `:1286` (after this ticket's sources entry), not `:1009`.

**Build follow-ups** (the prune, through plan mode and two challengers; defects go by RED/GREEN):

- **Schema**: drop both enum entries and branches (`schemas/level-data.schema.json:134-140,148-154,171,173`). Change
  the enum description at `:176` from seven to five. `tests/test_validate_levels.py:69,81-86,212`.
- **Code and data**:
  - delete `src/puzzles/zoom-split-star/` and `earth-gravity-drop` (`src/scenes/earth/earth-data.json:161-173`);
  - delete `puzzle.earth.gravity-drop.label` (`content/bg/puzzles.json:9`);
  - in `src/shared/game-state.test.ts`, swap in another optional marker for the fixture (lines 24, 64, 75).
- **Content**: a new Moon completion-line key plus a level-complete hook. Delete `fact.gravity-drop`,
  `fact.gravity-drop.apollo` and `fact.mizar-alcor.1-4`. Run `pedagogy-report` and `astronomy-report` on the new
  string.
- **Sources**:
  - add the RETIRED status to the vocabulary table;
  - mark Mizar/Alcor RETIRED (`:846`) and re-note `:954` and `:1188`;
  - reword `:221` away from "the same drop";
  - add research 007's Saturn/Jupiter clarifying line at `:238`;
  - update `:1286`;
  - re-key the air/Apollo entry from a beat to the completion line (`:148`).
- **Star catalogue**: rewrite the `zoom-split-star` rationale in `data/scripts/star-catalogue.py:13` (grandfathered at
  500 lines; do not grow it) and `tests/test_star_catalogue.py`.
- **Docs**:
  - "seven" → "five" in `CLAUDE.md:95-100`, `README.md:66`, `docs/design/puzzle-types.md:3,17` and
    `docs/design/earth-level-brief.md:26,42,54,56,86-104`;
  - the `surface-gravity.json` readme line "feeds the gravity-drop beat".
- **Agent config**: `.claude/agents/challenger.md:61` (its type list was already stale), and in
  `.claude/agent-memory/astronomy-accuracy-checker/`, `settled-sources.md:11` and `bulgarian-folk-figures.md:39`.

**Ticket 006 note (2026-09-25):** Jupiter adopts `fact.gravity-drop.bodies`'s claim as a new completion-line key, so
the claim is not RETIRED; `fact.gravity-drop.bodies` itself is deleted in the build. Jupiter's type uses and the reverse
dependency on this verdict are recorded in ticket 006 and in ADR 0006 "When to revisit".
