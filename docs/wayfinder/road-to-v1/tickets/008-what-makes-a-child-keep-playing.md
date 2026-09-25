---
id: "008"
title: What makes a child want to keep playing
type: grilling
status: closed
assignee: owner
blocked_by: []
---

## Question

Beyond the next page and the fact strings, what reward loop makes an 11–12 year old *want* to keep playing, and
what does each beat hand out?

The owner raised this on 2026-09-25, while ticket 003 was being resolved. Settled inputs, not to be re-asked:

- **The kind of pull:** curiosity and collection, like a sky album the child fills, noticed things kept, hidden
  optional finds, and the book's pages coming alive. **No compulsion mechanics:** no streaks, no daily-login
  pressure, no timers, no random loot, and nothing that punishes stopping (UK Children's Code, EU DSA dark patterns;
  CLAUDE.md rule 8).
- **The owner's own idea to grill:** achievements that also *help*. Gathering enough of them earns hints to spend on
  a later level when the child is stuck. Grill it or a similar idea.

Decide:

- what counts as an achievement (a solved optional beat, a hidden find, a noticed thing), and where it is shown;
- whether and how achievements convert to hints, and what a hint is (it must not give the answer away, or it
  becomes a lock with a key rather than a lesson);
- how the collection is shown without a number or counter (rule 2 applies to any display a child reads as a score);
- how it interacts with the gate: hints must never let a child skip a **required** marker's lesson, and optional
  markers still never carry a level on their own;
- storage: `localStorage` only, nothing leaves the device (rule 8);
- content: every string through `content/bg/` (rule 3).

Consult `puzzle-pedagogy-reviewer` on the hint design. It likely touches the book's through-line fog patch ("The
book's through-line, ending and navigation"); say so if the answer settles part of it.

## Resolution

Grilled with the owner on 2026-09-26 in three rounds (Q1–Q11). `puzzle-pedagogy-reviewer` was consulted on the hint
design. Two `challenger` agents both returned "revise", and the owner answered their four open points (Q12–Q15).
Reasoning and rejected options: [ADR 0007](../../../adr/0007-hints-are-free-not-earned.md). No new astronomy claim was
adopted, so `docs/sources.md` is unchanged.

**The pull is the book filling in.**

- Every solved marker, required or optional, lights an element of its world's storybook page.
- Tapping a lit element shows the marker's `reward.fact` plus its second idea.
- There is no album screen and no counter, in digits or in words. Unlit elements are invisible or plain background,
  never empty outlines.
- No new hidden finds in v1: the designed optional markers are the finds.
- Nothing new is stored. The collection is derived from `solved[]` in `src/shared/game-state.ts`. At build, the
  `solvedCount` doc comment ("you have found 3 things here") is reworded to match.

**Hints are free, never earned** (the owner's hint-currency idea is rejected: it is a counter, it helps the child who
needs help least, and it creates scarcity).

- **Nudge** (the designed stall nudge; companion tiers keep their 09-09 meaning): it appears by itself on a stall and
  only _points_, naming where to look or what to try. It never carries a fact.
- **Hint step:** a second tap of the companion brings it up, on every level. It is outside the tier-count seam, and
  there is no cost and no limit. It narrows **what** to try, never **how far**:

| Type | The hint step may | It must never |
| ---- | ----------------- | ------------- |
| `rotate-match` | pulse the reference feature to align (crater + star arrow, lit hemisphere, Red Spot) | show a ghost of the target pose |
| `connect-the-dots` | glow a region (R1a: the whole path segment) | draw the line or mark the next dot |
| `parallax-compare` | highlight the feature to compare, equally on both sides (J4: both bright dots) | show which one is bigger or brighter |
| `trajectory-match` | pulse the time control | show a direction or snap |
| `telescope-focus` | pulse the focus control | show a direction or auto-focus |

The schema constrains the hint step to a per-type enum that carries no values.

- **„Спомни си…“ cards:** a marker may name one earlier marker (e.g. `remembers`). When that marker is solved, its card
  replaces the hint step's text; it does not add a step.
  - The card recalls a skill or an already-verified idea. It has its own content key and passes `astronomy-report`.
  - The one pair fixed now is Earth `earth-telescope-focus` → Jupiter J1. Its card recalls the skill (blurry, then
    sharp at the edge), with no Saturn fact and no ring image.
  - Every other pair is chosen at build in plan mode and reviewed by `puzzle-pedagogy-reviewer`.
- **The gate is untouched:** hints never solve, and the threshold counts `solved ∩ required`. Hint use is never stored.

**Amends settled tickets:**

- **003/004/006:** "a second idea goes to that marker's nudge" becomes "a second idea goes to that marker's album
  card". Every nudge in those tables is rewritten at build to point only.
- **09-09 Companion:** it gains the hint step. Its tiers are unchanged.

**Build notes:**

- `earth-sundial` and `earth-day-night-spin` both reward `fact.day-night`, so their album cards would repeat. Resolve
  this at build.
- Per-marker page art joins the "Imagery and data per level" fog.

**Fog:** this settles the _page display_ part of "The book's through-line, ending and navigation". The ending and the
narrow-width layout graduate to [The book's ending and navigation](009-book-ending-and-navigation.md).
