---
id: "001"
title: Which worlds make the v1 roster, and in what order
type: grilling
status: closed
assignee: owner
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

## Resolution

Grilled with the owner on 2026-09-25, in four rounds plus two follow-ups after the challengers.

**The v1 roster, in order:**

| Page | World   | Gate |
| ---- | ------- | ---- |
| 1    | Earth   | 1.0  |
| 2    | Moon    | 1.0  |
| 3    | Mars    | 0.7  |
| 4    | Jupiter | 0.7  |

The whole solar system is the long-term goal. Everything beyond these four is a post-v1 expansion, charted later as a
fresh map.

- **The Sun** gets no page in v1.
  - When it does get one, the owner prefers a **Sun + Mercury** page. That is an input to the post-v1 map, not a
    binding decision.
  - The **Sun–Moon almost-same-size** beat and the **partial** solar eclipse from Bulgaria on 2027-08-02 go to the
    Moon design ticket as candidates.
  - "Exactly the same size" is NOT ATTESTED (`docs/sources.md`, "Claims ruled out during v1 roster research").
- **Major moons** are the large round moons: the Moon, the Galilean moons, Titan and Triton.
  - **Phobos is not one**, so beat R9 drops.
  - No moon besides ours gets a page. The Galilean moons and Ganymede live inside Jupiter's level.
- **The ADR 0006 anchor stays "the Mars build"**, since Mars is page 3. Nothing is restated.
- **`zoom-split-star` has no use by the anchor**, so ticket 005 deletes it, and the owner accepts that.
  - Research 002's "lives only if Jupiter does" was necessary, not sufficient: Jupiter is page 4, after the anchor, so
    its use does not count.
  - Jupiter stays on the roster for its astronomy, and it designs only from types that survive 005.
- **Correction, recorded so it is not re-asked.** `zoom-split-star` never served Earth via Orion's Belt.
  - The brief's belt claim is FALSE (`docs/sources.md`, "Orion's Belt").
  - Mizar/Alcor replaced it as the target.
  - None of Earth's ten fixed beats uses the type.
  - Putting Mizar on Earth would reopen a fixed input, and the owner did not take that.
- **Finish bar clarified.** No `level.<world>.*` key and no storybook page for an off-roster world. A fact string
  rewarded by a roster beat may mention any solar-system body, which keeps Earth's `fact.telescope-saturn`.
- **Added:** research ticket 007 (a deep Jupiter pass) and grilling ticket 006 (Jupiter level design, blocked by 005
  and 007).

**Build follow-ups, beside the map and not tickets:**

- ~~Remove `level.saturn.name` (`content/bg/levels.json:12`, its only reference).~~ Keep it: Saturn joined v1 (see the amendment below).
- Add `level.jupiter.blurb`, plus Jupiter's page in `src/scenes/storybook-scene.ts`.
- `ui.puzzle.coming-soon` (`content/bg/ui.json:8`) must be gone by v1. It belongs to the Earth build.

## Amendment (2026-09-26, ticket 009)

The owner added **Saturn to v1** while grilling
[The book's ending and navigation](009-book-ending-and-navigation.md) (Q5, Q8, Q17). The table above now reads:

| Page | World   | Gate |
| ---- | ------- | ---- |
| 1    | Earth   | 1.0  |
| 2    | Moon    | 1.0  |
| 3    | Mars    | 0.7  |
| 4    | Jupiter | 0.7  |
| 5    | Saturn  | 0.7  |

A back cover, not a world, follows the last world page.

- **The type verdict stands.** Saturn comes after the Mars anchor, exactly as Jupiter does.
  - It designs from the five types kept by 005 only.
  - Reviving a deleted type would reopen 005 explicitly, argued in ADR 0006, and is outside this map.
- **Saturn is conditional.** [What Saturn can teach, deep](010-what-saturn-can-teach.md) must find at least three honest
  required beats on the kept types. If it does not, Saturn returns to post-v1, and this amendment is reverted.
- **Titan** is a major moon and a Saturn candidate. It no longer waits out of scope.
- **Build follow-ups amended:**
  - ~~Remove `level.saturn.name`~~: keep it.
  - Add `level.saturn.blurb` and Saturn's page in `src/scenes/storybook-scene.ts`.
