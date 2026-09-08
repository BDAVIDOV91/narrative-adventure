---
name: qa-report
description: Use as the release gate before a milestone or merge to main — runs every automated check, then walks the manual checks automation cannot cover (zoom transition, Cyrillic rendering on the real machine, a level completing end to end, save and reload).
---

# QA Report

The release gate. Automated checks catch what they were written to catch; this covers the
rest, including the things that can only be confirmed by actually playing.

## Step 1 — Automated gates

Run all of them and report real output. Do not summarise a failure as a pass.

```bash
npm run validate                                     # tsc + eslint + prettier
npm run build                                        # production build + chunk sizes
.venv/bin/python -m pytest                           # 15 regression tests
.venv/bin/python data/scripts/validate-levels.py     # every level against the schema
.venv/bin/black --check data/scripts tests
.venv/bin/flake8 data/scripts tests
sh .husky/test-pre-commit-scope.sh                   # the hook logic itself
```

## Step 2 — Data freshness

Generated data must still match what its generator produces.

```bash
.venv/bin/python data/scripts/orbital-positions.py
git diff --stat data/generated/
```

A diff here means the committed data is stale, or the generator changed and the data was
not regenerated. Either way it is a finding.

## Step 3 — Manual checks

Automation cannot confirm these. Start the game and actually look.

```bash
npm run dev    # http://localhost:5173/
```

- [ ] **Cyrillic renders** — every glyph, in the real font, on this machine. No blank boxes,
      no fallback substitution. Check a string with Зорница, Вечерница, Слънчева система.
- [ ] **Storybook opens** and the page titles read correctly in Bulgarian.
- [ ] **Zoom transition** into a level runs and returns.
- [ ] **The player moves**, and diagonal movement is not faster than straight.
- [ ] **A level completes** — every marker reachable, the unlock threshold actually fires.
- [ ] **Save and reload** — progress survives a refresh; a cleared `localStorage` starts
      cleanly rather than crashing.
- [ ] **No console errors.**
- [ ] **Frame rate is acceptable on this APU**, not on an imagined machine.
- [ ] **Text wraps** rather than clipping — Bulgarian runs longer than English.

## Step 4 — Domain reports

Run whichever apply to what changed:

- `astronomy-report` — content or generated data touched
- `pedagogy-report` — puzzles or Bulgarian text touched
- `perf-report` — assets or Three.js touched
- `privacy-guard` — always, and especially when a dependency was added

## Step 5 — Output

```markdown
### AUTOMATED
| Gate | Result |
|---|---|
<real results, failures quoted verbatim>

### DATA FRESHNESS
<regenerated diff, or "no drift">

### MANUAL
<each check, pass/fail, with what was observed>

### DOMAIN REPORTS
<which were run and their verdicts>

### RELEASE VERDICT
<ready, or the specific blockers>
```

## Rules

- Quote failing output exactly. Never describe a failure as a pass.
- An unchecked manual item is **not** a pass — mark it "not checked" and say why.
- The manual section is the point of this skill. Skipping it makes the whole report
  worthless, because the automated gates already run in the pre-commit hook.
