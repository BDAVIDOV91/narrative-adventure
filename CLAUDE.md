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
npm test               # vitest run — the TypeScript regression suite (rule 5)

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
sh .claude/hooks/test-precommit-checks-reminder.sh
sh .claude/hooks/test-settings-hardening.sh
bash .claude/hooks/test-wayfinder-frontier.sh   # bash-only: under sh it exits 0 having run nothing
bash ops/remote-shell/test-pin-list.sh          # the M2 offload's pin list + fail-closed paths (stubs only)
bash ops/mem-guard/test-mem-guard.sh            # the MemAvailable guard

# Two-machine offload (see the section below)
./ops/remote-shell/claude-m2.sh                 # a session whose Bash runs on the M2
ops/remote-shell/preflight.sh                   # READY / PARTIAL / UNBOOTSTRAPPED
ops/mem-guard/mem-guard.sh -- <cmd>             # a heavy run on M1, refused below the floor
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

`rotate-match`, `connect-the-dots`, `parallax-compare`, `trajectory-match`,
`telescope-focus`. Each is built once and reskinned per planet. The schema
enforces the list, and constrains each type's `config` in its own branch. **A
sixth type is a one-off that needs its own maintenance forever** — adding one is
a deliberate decision, never a drive-by.

A **beat** is level content; a **type** is code maintained forever. Four of
Earth's nine beats are one interaction — rotate a model until it matches a
reference — so they are one engine with four renderers, not four types. Review
trigger: **any type not reused on a second level by the Mars build gets deleted.**
It fired once: `zoom-split-star` and `gravity-drop` were deleted (road-to-v1
ticket 005). See `docs/adr/0006-seven-puzzle-types-not-thirteen.md`.

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

**Tests passing ≠ the game working.** A scene or puzzle change is done only when it
has been played via `npm run dev` (after `free -h`, for anything 3D). Before
re-fixing anything, and on the third failed fix, follow
`.claude/rules/development-practices.md`.

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

**Session handoffs live in the repo, not in a scratch directory.** Write them to
`docs/handoffs/YYYY-MM-DD-session-handoff.md`, dated for the day the handoff is
written. A handoff in `~/.claude/plans/` is invisible to everyone but the session
that made it and is lost on a clean checkout; in `docs/` it is versioned,
reviewable, and a fresh session can be pointed at it by path. Carry forward what
is settled, what is left over, and what must not be re-asked — a handoff that
only lists tasks makes the next session re-derive the decisions.

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

## Two-machine offload (M1 ↔ M2)

Heavy Bash runs leave M1 for the M2 (Tailscale peer `bobby`, ssh alias `m2`, mutagen session
`narrative-adventure`, same path on both machines). Live since 2026-10-07; the plan is
`docs/handoffs/2026-10-01-m2-offload-plan.md`.

- **Launch:** `./ops/remote-shell/claude-m2.sh`. It runs `preflight.sh` and launches only on READY;
  PARTIAL, UNBOOTSTRAPPED or any other code refuses. The redirect is opt-in per session.
- **Kill switch:** "go local" means `REMOTE_SHELL_MODE=local` (or `claude-m2.sh --local`), or plain
  `claude`.
- **Fail closed:** the default mode is remote. The M2 unreachable, mutagen missing or a failed flush
  refuses (127); a cwd missing on the M2 refuses (97); an unknown mode refuses. There is never a
  silent local fallback.
- **The pin list** (git, `free`, `npm run dev`, hook tests, the wayfinder viewer, the offload's own
  scripts, mutagen, mem-guard, `~/.claude/projects/`) runs on M1. It is guarded by
  `test-pin-list.sh` and never changes without a case there.
- **Why it fits `Bash(ssh:*)`:** the deny rule stops Claude typing an ssh command. The transport
  lives only inside the reviewed, tested `remote-shell.sh` and `preflight.sh`. Never a direct `ssh`.
- **Two traps carried from pdfx:** `CLAUDE_CODE_SHELL` needs "bash" in the path, so always use the
  `bash-remote-shell.sh` symlink; and the redirect is proven by hostname, never inferred.
- **The guard:** `ops/mem-guard/mem-guard.sh -- <cmd>` refuses (75) below a MemAvailable floor,
  provisional 1536 MB, re-tuned at E1 entry from the measured M1 peak. Override one run with a
  leading `MEM_GUARD_MIN_MB=<MB>`. A pinned or local command that is HEAVY (tests, builds, lint,
  the dev server, `data/scripts/`) is guarded automatically. In a plain `claude` session, call the
  guard explicitly for any heavy or 3D run, and never chain work onto a pinned command
  (`git add -A && npm test` would run the tests on M1). Holes: `npm run  dev` (two spaces), a bare
  `vite`.
- **Husky** still runs on M1 at commit, because git is pinned; its vitest and pytest lines go
  through the guard. A docs-only commit never blocks.
- **Bootstrap** a fresh M2: create the mutagen session (the command is in
  `ops/remote-shell/mutagen.yml`), then run `ops/remote-shell/setup-m2.sh` on the M2 (through the
  wrapper works). It refuses on M1.

## Review gates

Both are non-blocking — they report, the owner decides.

**Plan checkpoint** (`PostToolUse(ExitPlanMode)`): after a plan is approved, ask
"Challenge the plan or proceed?". On Challenge, spawn **two** `challenger` agents
in parallel on the plan file; when both return, post a combined summary and both
verdicts, then append `## Challenger Findings` to the plan file and fold accepted
fixes inline — **never overwrite the original plan**.

**Pre-commit** (`PreToolUse(Bash)` on `git commit`): injects the RED/GREEN
checklist, and routes to the domain skills the staged files call for.

| Staged                                                              | Skill              |
| ------------------------------------------------------------------- | ------------------ |
| `content/`, `data/generated/`, `data/reference/`, `docs/sources.md` | `astronomy-report` |
| `src/puzzles/`, `content/bg/`                                       | `pedagogy-report`  |
| `assets/`, `planet-render.ts`, `package.json`                       | `perf-report`      |
| `src/`, `package.json`, `requirements.txt`, `index.html`            | `privacy-guard`    |
| `package.json`, `package-lock.json`, `requirements.txt`             | `security-audit`   |
| before a milestone or merge to main                                 | `qa-report`        |

Agents: `challenger`, `astronomy-consultant` (consulted _during_ design),
`astronomy-accuracy-checker` (verifies _after_), `puzzle-pedagogy-reviewer`,
`perf-budget-checker`.

Every report grounds findings in the actual diff and cites `file:line`, or marks
them PLAUSIBLE. **"No issues" is valid only after the checklist was actually
walked — say what was checked**, so a clean pass is distinguishable from a
skipped one.

## Wayfinder — the map decides, plan mode builds

Work too big for one session is charted as a **wayfinder map** of decision
tickets under `docs/wayfinder/<slug>/`, one ticket resolved per session. Triggers
and the viewer: `docs/wayfinder/QUICKSTART.md`. `/wayfinder` is owner-typed —
suggest it, never start it.

Size the work before choosing a mode:

| Work                                                   | Mode                      |
| ------------------------------------------------------ | ------------------------- |
| Trivial: one file, obvious change                      | do it directly            |
| Moderate: a few files, clear scope, ≤ 4 open decisions | plan mode (+ challengers) |
| Can't fit one session, or ≥ 5 linked open decisions    | suggest a wayfinder map   |
| A bug                                                  | rule 5, never a ticket    |

A settled ticket is a decision: do not re-derive it in a later session. When a
map is clear, the build goes through plan mode with two `challenger`s.
v1 build order: `docs/design/v1-build-spec.md`, one phase per plan-mode session.
Adopted-rules files live in `.claude/rules/` (loaded by path).

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
