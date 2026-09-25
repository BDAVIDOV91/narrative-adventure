---
name: pedagogy-report
description: Use before any commit that touches src/puzzles/ or Bulgarian content, to audit the hide-the-math rule, discoverability without instructions, natural child-facing Bulgarian, and the forgiving unlock gate.
---

# Puzzle Pedagogy Report

A puzzle can be correct, fast and still fail here. Produce this from the actual change.

## Step 1 — Ground in the diff

```bash
git diff --cached -- src/puzzles/ content/bg/ src/scenes/
```

## Step 2 — Walk the checklist

### Hide the math — the brief's hardest rule
No equations. No typed numbers. No displayed units. No formulas. Interaction is sliders,
drag-and-drop, rotation or visual comparison; feedback is visual, not a score or a
percentage.

The test: **would a child feel they noticed something, or that they did homework?** A
puzzle that is mathematically faithful but shows a number has failed. Say so plainly.

### Solvable without instructions
Is the goal apparent from looking? Is there an affordance showing what can be dragged or
rotated? Does a wrong attempt teach, or merely fail? Could a child who does not read
fluently still progress?

If the puzzle needs a paragraph of explanation, it needs a redesign — not a better
paragraph.

### Bulgarian for an 11-12 year old
Vocabulary a Bulgarian child that age actually has. Natural Bulgarian, not English
translated word-for-word — calques, English sentence rhythm and borrowed idioms all read
wrong to a native child. Standard astronomy terms. Sentences short enough to read while
playing.

### No leaked English
Every player-facing string resolves through `src/shared/content.ts`. Grep `src/` for quoted
display strings that never reach `content/bg/`. No English placeholder that could ship.

### Forgiving
`unlockThreshold` 0.7 for open levels, 1.0 for the two guided ones. No dead ends. Failure
is neutral, never punished.

### Teaches the right thing
Does solving it require the concept, or can it be brute-forced? A puzzle solvable by
wiggling until it clicks teaches wiggling.

Spawn the `puzzle-pedagogy-reviewer` agent for a full review of a substantial puzzle.

## Step 3 — Output

Sections: HIDE THE MATH / DISCOVERABILITY / BULGARIAN / FORGIVENESS / TEACHES THE RIGHT
THING, each finding with `file:line`, marked **must fix** or **nice to have**, then an
explicit WHAT WAS CHECKED list.

## Rules

- Quote the actual Bulgarian string when reporting a language finding.
- No finding without a location.
- Do not pad. A short honest list beats a long one.
