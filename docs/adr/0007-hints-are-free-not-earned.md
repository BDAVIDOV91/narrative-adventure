# 0007 — Hints are free for every child, never earned or spent

- **Status**: accepted
- **Date**: 2026-09-26
- **Amends**: the 09-09 handoff's Companion section (adds a hint step beside its
  tiers), and the "second idea goes to that marker's nudge" line in tickets
  003/004/006 of `docs/wayfinder/road-to-v1/`

## Context

Wayfinder ticket 008 asked what makes an 11–12 year old _want_ to keep playing.
The owner's own idea: achievements (solved optional beats, found things) add up
to hints the child can spend on a later level when stuck. It is an appealing
loop: exploration pays off later.

Pulling the other way: rule 2 (nothing a child reads as a score), rule 8 and the
children's-code position against compulsion mechanics, and the brief's
forgiving gate. `puzzle-pedagogy-reviewer` rated the earned pool
"must not ship as proposed".

## Decision

- **Hints are free and escalate, for every child, on every level:**
  1. the designed **stall nudge**, which appears by itself. A nudge only
     _points_ (where to look, what to try). It never carries a fact.
  2. a visual **hint step** on a second tap of the companion. It narrows
     **what** to try, never **how far**:
     - `rotate-match`: pulse the reference feature to align. Never a ghost
       of the target pose.
     - `connect-the-dots`: glow a region. Never draw the line.
     - `parallax-compare`: highlight the feature to compare, equally on both
       sides. Never show which one wins.
     - `trajectory-match` and `telescope-focus`: pulse the control. Never
       show a direction, snap or auto-focus.
     - The schema constrains the hint step to a small per-type enum that
       carries no values.
- **„Спомни си…“ cards.** A marker may name one earlier marker. If that marker is
  solved, a card recalling it replaces the hint step's text. The card recalls a
  skill or an already-verified idea, and has its own content key.
- **Achievements feed the collection only.** Every solved marker lights an
  element of its world's storybook page. Tapping the element shows its fact and
  the marker's second idea. There is no counter, in digits or words, and no
  visible empty slot.
- Companion _tiers_ (arrival / nudge / fact, count as level data) keep their
  09-09 meaning. The hint step sits outside that seam and is never removed.
- Hints never solve. The gate still counts `solved ∩ required`. Hint use is never
  stored.

## Why

The earned pool failed on three counts:

- **It is a counter.** However it is drawn (lanterns, a jar of stars), a child
  reads a spendable balance as a score. That breaks rule 2.
- **It helps the child who needs help least.** A struggling child skips
  optional beats, earns nothing, and meets a hard required beat with an
  empty pool. Being stuck becomes a punishment.
- **Spending creates scarcity.** "Save it for later" is loss aversion, a
  compulsion pattern this project refuses (rule 8, UK Children's Code, EU DSA).

What survives of the idea is its core intuition, that what you did earlier helps
you later. It lives on as „Спомни си“ cards, tied to what was learned rather
than to a currency. A free hint step sits under those cards, so no child's help
depends on optional play.

**Moving second ideas off the nudge.** A nudge that teaches a second fact
cannot unstick anyone. Examples: Mars R6 "a Mars day is a little longer",
Jupiter J7 "the fast spin helps stretch its clouds". Those ideas are VERIFIED
and are kept: they move to the album card, where they are read after solving.

**Rejected alternatives, and what would have made them win:**

- **The earned pool.** It would have won only if hints were a pure bonus on top
  of a free floor _and_ drawn with no quantity. At that point it is no
  longer a pool.
- **Direction arrows in the hint step.** They would have won if play-testing
  showed a trajectory or focus beat unsolvable without them. For Mars
  retrograde, the direction of time is half the lesson.

## Consequences

- The build needs:
  - a hint-step enum per type in `schemas/level-data.schema.json`;
  - a `remembers` field on markers;
  - a second-idea content key per marker;
  - page art with one element per marker.
- Every nudge in tickets 003/004/006 is rewritten to point, at build time.
- No new `localStorage` field. The collection is derived from `solved[]`.
- Two Earth markers share `fact.day-night`, so their album cards would repeat.
  The build must resolve that.

## When to revisit

- Play-testing shows children never tap the companion, so the hint step is
  never found.
- A beat proves unsolvable under "what, not how far".
- The owner asks for a visible reward for optional play beyond the lit page.
