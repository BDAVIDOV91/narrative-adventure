---
name: astronomy-report
description: Use before any commit that touches content/, data/generated/ or docs/sources.md, to verify every astronomy and folklore claim against a real source. Produces the Science Accuracy, Data Verification, Folklore Accuracy and Terminology sections, grounded in the actual diff.
---

# Astronomy Accuracy Report

This project's equivalent of a security review. In an education game for children, a claim
that ships without a source is a claim nobody checked, and wrong astronomy taught to an
11-year-old is the most severe defect the project can produce.

Produce this from the **actual change**, never from a template.

## Step 1 — Ground in the diff

```bash
git diff --cached --stat
git diff --cached -- content/ data/generated/ docs/sources.md src/puzzles/
```

List every claim added or changed. Read `docs/sources.md` — the register of what has
already been checked, including entries already marked DISPUTED.

## Step 2 — Check each claim

For every factual statement in the diff, verify concretely and cite `file:line`:

- **True?** Against a named authoritative source, not recall.
- **Registered?** Present in `docs/sources.md` and marked VERIFIED — not NEEDS SOURCE, and
  never DISPUTED.
- **Misconception risk?** The live ones: seasons caused by distance rather than axial tilt;
  Moon phases caused by Earth's shadow rather than illumination; the "dark side" of the
  Moon; orbits drawn as pronounced ellipses.
- **Numbers?** From `data/generated/` or a cited source — never from memory.
- **Folklore?** Bulgarian cultural claims are factual claims. Traced to a named
  ethnographic source, and where variants exist, the game tells one and knows which.
- **Terminology?** Standard Bulgarian astronomy terms, not literal translations.

For generated data, spot-check values against an **independent** almanac — not against the
generator that produced them. Units: RA in hours (0-24), Dec in degrees (-90..90),
distances in AU.

Deep verification is the `astronomy-accuracy-checker` agent's job; spawn it when a claim
needs real research rather than a lookup.

## Step 3 — Output

### 1. SCIENCE ACCURACY
Each claim rated LOW / MEDIUM / HIGH / CRITICAL, with `file:line`, its source, and a fix.
A false statement a child will believe is CRITICAL however small it looks.

### 2. DATA VERIFICATION
What was spot-checked, against what, and the result.

### 3. FOLKLORE ACCURACY
Each Bulgarian cultural claim, its status, its source.

### 4. TERMINOLOGY
Each new term: correct, or what it should be.

## Rules

- No finding without evidence — cite `file:line` and the source, or mark it PLAUSIBLE.
- "No issues" is valid **only** after the checklist was actually walked. Say what was
  checked, so a clean pass is distinguishable from a skipped one.
- A CRITICAL finding, or any claim still NEEDS SOURCE or DISPUTED, should not ship. Say so
  plainly and let the user decide — this reports, it does not block.
- When a claim is confirmed, update `docs/sources.md`: status, source, date.
