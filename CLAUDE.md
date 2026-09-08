# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A browser-based, story-driven astronomy education game for Bulgarian children
(~11-12). The game is framed as a magical storybook: the book is the level-select
screen, and tapping a page zooms into that world, played from a top-down view.

**Working title**: Звездната книга (placeholder — not final branding).

The brief's framing governs every decision: _"meant to be genuinely finished, not
an infinite scope-creep exercise."_ When a choice is between shipping and
elaborating, ship.

## Commands

```bash
# Game
npm run dev            # Vite dev server on http://localhost:5173
npm run build          # tsc --noEmit + production build
npm run validate       # type-check + lint + format:check — the gate
npm run lint           # eslint, --max-warnings 0
npm run format         # prettier --write

# Python (build-time only — see the boundary rule below)
uv venv venv && uv pip install -r requirements.txt     # first-time setup
venv/bin/python data/scripts/orbital-positions.py      # regenerate ephemeris
venv/bin/python data/scripts/star-catalogue.py         # regenerate star data
venv/bin/python data/scripts/validate-levels.py        # validate every level
venv/bin/python data/scripts/process-textures.py       # NASA sources -> WebP
venv/bin/python -m pytest                              # regression suite
venv/bin/python -m pytest -m "not integration"         # skip ephemeris-dependent
venv/bin/python -m pytest tests/test_validate_levels.py::test_unknown_puzzle_type_is_rejected   # one test
venv/bin/black data/scripts tests                      # format (defaults, 88)
venv/bin/flake8 data/scripts tests                     # lint (max-line-length 100)

# Hook regression tests
sh .husky/test-pre-commit-scope.sh
sh .claude/hooks/test-block-dangerous-git.sh
```

## Architecture

### The boundary rule — no runtime Python (mandatory)

Python is a **build-time toolchain**. No Python process runs while the game is
being played. Scripts write files into the repo; the browser reads those files.

> If the output can be computed once and committed, it is a build step. If it
> would need to respond to a player action, redesign it into precomputed data.

Every astronomy quantity this game teaches is deterministic, so this always
holds. There is no backend, no database, no accounts, no API.
See `docs/adr/0001-python-is-build-time-only.md`.

### Data flow

```
JPL de440s      HYG v4.4 + Stellarium      NASA raw imagery
 ephemeris       figures (data/raw/,         (gitignored)
                  gitignored)
     |                   |                        |
orbital-             star-                  process-
positions.py       catalogue.py             textures.py
     |                   |                        |
     |          verified vs Hipparcos-2           |
     |          (build fails on mismatch)         |
     |                   |                        |
data/generated/*.json  <-+          assets/images/nasa/*.webp
        \______________  ______________/
                       \/
        src/scenes/<level>/<level>-data.json
             (references generated data via `dataRef`)
                       |
                 Phaser scenes
        (+ Three.js, lazily, single objects only)
```

Generated files **are committed** — they are the game's input, and a clean
checkout must run without Python. Details in `docs/architecture/data-flow.md`.

### Level data

A level is `src/scenes/<id>/<id>-data.json`, validated against
`schemas/level-data.schema.json`. `unlockThreshold` is `1.0` for the two guided
levels (Earth, Moon) and `0.7` for open-exploration levels — the brief's
forgiving gate, kept as data so both kinds share one code path.

### The five puzzle types

`rotate-match`, `connect-the-dots`, `parallax-compare`, `zoom-split-star`,
`trajectory-match`. Each is built once and reskinned per planet. The schema
enforces the list. **A sixth type is a one-off that needs its own maintenance
forever** — adding one is a deliberate decision, never a drive-by.

## Rules

### 1. Scientific accuracy (mandatory)

Wrong astronomy taught to a child is this project's most severe defect — the
equivalent of a security hole, and it gets the same treatment.

- Every claim the game states goes in `docs/sources.md` with a real source and a
  status. **A claim marked NEEDS SOURCE or DISPUTED must not ship.**
- Numbers come from `data/generated/` or a cited source, never from memory.
- Two live misconceptions the content must actively contradict: seasons caused by
  distance rather than axial tilt, and Moon phases caused by Earth's shadow
  rather than illumination.
- Bulgarian folklore claims are factual claims too, and this audience will notice.

**The astronomy is the lesson; folklore is a bonus layer.** A folklore beat earns
its place only when learning the folklore and learning the astronomy are the
_same act_. Зорница/Вечерница passes — the folklore creates the misconception and
the astronomy resolves it. Кумова слама failed and was cut: a moral tale about
theft that teaches nothing about the Milky Way. See
`docs/adr/0005-folklore-must-carry-astronomy.md`.

`docs/sources.md` uses a fourth status, **NOT ATTESTED**, for claims investigated
and found unsupported — so an appealing idea that turns out to be false is not
re-proposed later. Check it before adding a folk name.

### 2. Hide the math (mandatory)

No equations, typed numbers, displayed units or formulas ever reach the player.
Sliders, drag-and-drop, rotating models and visual comparison only. A child
should feel they _noticed_ something, not that they did homework. A puzzle that
is mathematically faithful but shows a number has failed this rule.

### 3. Bulgarian only, nothing hardcoded (mandatory)

Bulgarian is the only locale. No English UI, no language switcher.

- **No player-facing string in a `.ts` file.** Everything resolves through
  `src/shared/content.ts` to `content/bg/*.json`. Keys stay ASCII; values Cyrillic.
- Any new font must be verified for Cyrillic coverage, including Bulgarian glyph
  forms — some Cyrillic fonts default to Russian shapes. A Latin-only font renders
  every string as blank boxes.
- **Never bake text into generated art** — generators mangle Cyrillic. Generate
  textless art, render strings at runtime.
- Bulgarian runs longer than English: containers wrap and grow, never fixed-width.

### 4. Raise issues when found — interview mode, not prose (mandatory)

Anything that needs the owner's answer, decision, or manual action must be asked via
`AskUserQuestion` **at the moment it is found** — mid-task, mid-session, mid-anything. Do
not bank it for the next summary or checkpoint.

Applies to: a defect found while implementing something else; a plan premise that turns out
to be false; a fork where two readings mean materially different work; an astronomy claim
that turns out to be unsourced; anything needing a call, a credential, or hands-on action.

**Especially while a background command or subagent is busy** (a test run, a build, a
research agent). That wait is dead time otherwise — ask then, and the answer arrives while
the work runs, instead of finishing the wait and only then asking.

Format: numbered questions, the recommended option **first** and labelled "(Recommended)",
the reason, and what would change the pick. Keep working on whatever does not depend on the
answer.

Do **not** flag these in prose ("worth noting…", "one thing I want to flag…") — that reads
as informational and gets skimmed. An interview blocks and gets answered.

For a decision with many branches, use the `grilling` skill: it works the design tree in
rounds, asking the whole answerable frontier at once. Use `grill-with-adr` when the decision
is one a future reader would otherwise relitigate.

### 5. PER FIX — the RED/GREEN rule (mandatory)

Bug found → **write a test that catches it (RED — it must fail on the old code)**
→ fix the bug → that test goes GREEN → run the full suite to confirm nothing else
broke → commit, and the test stays in the suite forever.

**No fix ships without its own regression test. If it shipped untested, it isn't
done.** A test that passes both before and after the fix is not a regression test.

### 6. Scope boundary

Solar system only for v1 — Sun, planets, major moons. Interstellar content is a
stretch goal for a future version and must not be built toward now.

### 7. Git

`main` is merge-only; work happens on `development`, feature branches
`feat/<kebab-slug>`. Conventional Commits, subject written as a declarative
sentence.

**Never push.** The owner performs every push themselves. Commit, then say it is
ready. Enforced by `.claude/hooks/block-dangerous-git.sh`, which also blocks
`gh pr create`, `git stash`, `git reset --hard`, `git clean -f`, `git branch -D`
and `git checkout/restore .`. When a call is BLOCKED: do not retry it, do not
rephrase it, do not edit the hook.

After big changes: ask whether to commit, and update `README.md` with what changed.

### 8. Privacy

The game makes **zero network requests** and collects **nothing** about a child.
Progress lives in `localStorage` and never leaves the device. Do not add
analytics, telemetry, crash reporting, or a CDN-loaded font — self-host fonts in
`assets/fonts/`. Under GDPR children's data carries the heaviest obligations, and
the safest position is the one this project already holds. Guarded by the
`privacy-guard` skill.

### 9. Hardware budget

Target: 4 cores, ~1.9 GB free RAM, AMD Radeon integrated APU. Textures capped at
2048px WebP via `process-textures.py`. Three.js stays behind the dynamic import in
`src/shared/planet-render.ts` and renders **single objects** — a planet, not a
system. Dispose geometry, material, texture and renderer on close: a leaked WebGL
context here is a crash, not a slowdown.

## Review gates

Both are non-blocking — they report, the owner decides.

**Plan checkpoint** (`PostToolUse(ExitPlanMode)`): after a plan is approved, ask
"Challenge the plan or proceed?". On Challenge, spawn **two** `challenger` agents
in parallel on the plan file; when both return, post a combined summary and both
verdicts, then append `## Challenger Findings` to the plan file and fold accepted
fixes inline — **never overwrite the original plan**.

**Pre-commit** (`PreToolUse(Bash)` on `git commit`): injects the RED/GREEN
checklist, and routes to the domain skills the staged files call for.

| Staged                                                   | Skill              |
| -------------------------------------------------------- | ------------------ |
| `content/`, `data/generated/`, `docs/sources.md`         | `astronomy-report` |
| `src/puzzles/`, `content/bg/`                            | `pedagogy-report`  |
| `assets/`, `planet-render.ts`, `package.json`            | `perf-report`      |
| `src/`, `package.json`, `requirements.txt`, `index.html` | `privacy-guard`    |
| before a milestone or merge to main                      | `qa-report`        |

Agents: `challenger`, `astronomy-consultant` (consulted _during_ design),
`astronomy-accuracy-checker` (verifies _after_), `puzzle-pedagogy-reviewer`,
`perf-budget-checker`.

Every report grounds findings in the actual diff and cites `file:line`, or marks
them PLAUSIBLE. **"No issues" is valid only after the checklist was actually
walked — say what was checked**, so a clean pass is distinguishable from a
skipped one.

## Conventions

Carried over from `pdf_data_extractor_v2` for consistency with how the owner
already works: Conventional Commits; `main` ← `development`; scoped pre-commit
with a `PRECOMMIT_DRY_RUN=1` escape hatch; every hook has a sibling `test-*.sh`;
flake8 `max-line-length = 100`, `extend-ignore = E203,W503` with Black on
defaults; strict tsconfig including `noUncheckedIndexedAccess` and
`exactOptionalPropertyTypes`; kebab-case filenames via `unicorn/filename-case`;
and dependency pins that carry the reason inline.

Dependency pins are exact (`save-exact=true`) and several are deliberately not
latest — see `docs/adr/0004-dependency-pins-and-their-constraints.md` before
bumping anything.

## ENFORCEMENT

- These rules apply to all future development in this repository.
- They must be followed automatically without needing to be restated.
- If any future prompt conflicts with these rules: **these rules take priority.**
