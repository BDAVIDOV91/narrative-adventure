# M2 offload — M1 side (v1-build-spec §4, as amended by T006 2026-10-01)

**Start SHA:** `c0db095a7c85aa909019f8ca8bb952a8592ce381` (recorded at entry, T006 d1).

## Context

The M2 offload phase sits between E0 and E1. It ports pdfx's remote-shell wrapper so heavy Bash runs leave M1. The M2
is offline, so the T006 amendment (ticket 006, end of file) has this phase build everything that runs on M1 and exit
**M1-complete**. Two items move to the M2 catch-up gate before merge 1: `preflight.sh` READY, and the vitest run proven
by hostname. With the M2 down, the wrapper must **fail closed**: it runs nothing on M1 that the pin list does not name.
E1 then enters without the M2, and the suite runs on M1 behind the MemAvailable guard.

Source to port: `~/pdf_data_extractor_v2/ops/remote-shell/` (`remote-shell.sh`, its `bash-remote-shell.sh` symlink,
`test-pin-list.sh`, `preflight.sh`, `claude-m2.sh`, `setup-m2.sh`) and `.claude/remote-shell/mutagen.yml`.

### Owner decisions this session (2026-10-01, do not re-ask)

1. **Guard floor:** a provisional **1536 MB** of MemAvailable, overridable per run with `MEM_GUARD_MIN_MB`. It is
   **re-tuned at E1 entry** from the measured peak RSS (peak plus a margin). A refusal prints the measured value and
   the override.
2. **Wrapper modes:** the default (mode unset) is `remote`, and it refuses when the M2 is unreachable. An unknown mode
   refuses. `local` (the "go local" kill switch) and `probe` (argv logging, for re-checking the calling convention at
   the catch-up gate) run only when exported explicitly.
3. **Auto-guard:** the wrapper runs the pinned `npm run dev` through the MemAvailable guard.

### Port decisions (mine, following the spec's strip list)

- **Carried as generic infrastructure:** the `SNAPSHOT_FILE=` pin, the `preflight.sh` and `mutagen` pins, the
  `.claude/projects/` pin, the argv parser, the cwd-file mirror, and the fatal checks on reachability and mutagen flush.
- **Dropped with `playwright`**, since the suite runs on the M2: `test:e2e` and `e2e:production`.
- **Dropped because the files do not exist here:** `deploy-service`, `decision-log-report`, `precompact`,
  `compact-resume`, `claude-md-map-check`, `ops/latency`, `ops/iam`, `doc-freshness` and `pii-redaction`.
- **Stripped per spec:** yarn, `nc-*`, the Supabase and `.env` checks, and the gcloud, prisma and knavision pins.
- `mutagen.yml` lives at `ops/remote-shell/mutagen.yml`, so the whole offload sits in one directory that a single pin
  covers.

## Files

| Path                                          | What                                                                           |
| --------------------------------------------- | ------------------------------------------------------------------------------ |
| `ops/mem-guard/mem-guard.sh`                  | new: the MemAvailable guard (`mem-guard.sh -- <cmd>`)                          |
| `ops/mem-guard/test-mem-guard.sh`             | new: its sibling test                                                          |
| `ops/remote-shell/remote-shell.sh`            | ported deny-list wrapper, fail-closed                                          |
| `ops/remote-shell/bash-remote-shell.sh`       | symlink → `remote-shell.sh` (`CLAUDE_CODE_SHELL` needs "bash" in the path)     |
| `ops/remote-shell/test-pin-list.sh`           | pin cases + fail-closed cases                                                  |
| `ops/remote-shell/preflight.sh`               | ported; transport, M2 env, sync, wrapper, hostname proof                       |
| `ops/remote-shell/claude-m2.sh`               | ported launcher; refuses on UNBOOTSTRAPPED/PARTIAL                             |
| `ops/remote-shell/setup-m2.sh`                | ported M2 bootstrap: `uv venv`, `npm ci`, de440s, headless shell (conditional) |
| `ops/remote-shell/mutagen.yml`                | ported sync config                                                             |
| `.husky/pre-commit`                           | the `^ops/` branch also runs both new tests                                    |
| `.husky/test-pre-commit-scope.sh`             | asserts the ops branch runs them (RED first)                                   |
| `CLAUDE.md`, `README.md`                      | new "Two-machine offload" section; commands; hook-test list                    |
| `docs/design/v1-build-spec.md`                | the E1 entry gains "set the guard floor from the measured peak RSS"            |
| `docs/handoffs/2026-10-01-session-handoff.md` | updated: M2 offload is M1-complete, E1 is next                                 |

Each new script stays well under 300 lines.

## Steps (each lands RED → GREEN, one commit per step)

### 1. MemAvailable guard (`ops/mem-guard/`)

- `mem-guard.sh [--] <cmd...>`:
  - It reads `MemAvailable` from `${MEM_GUARD_MEMINFO:-/proc/meminfo}`; the meminfo path is the test seam.
  - The floor is `${MEM_GUARD_MIN_MB:-1536}`, with a "provisional, re-tuned at E1 entry" comment.
  - Below the floor it prints `[mem-guard] REFUSED: MemAvailable=<n> MB < floor <f> MB`, plus the override line, and
    exits 75. At or above the floor it `exec`s the command, so the exit code survives.
  - It fails closed: a missing or unparsable `MemAvailable`, or a non-integer floor, refuses with a message. With no
    command it prints usage and exits 2.
- `test-mem-guard.sh` uses fixture meminfo files in a mktemp dir. Cases:
  - below the floor refuses, and the marker command never runs;
  - above the floor runs, and the exit code passes through (a `exit 3` command returns 3);
  - exactly at the floor runs;
  - `MEM_GUARD_MIN_MB` overrides the floor;
  - a missing `MemAvailable` line refuses;
  - a garbage floor refuses;
  - no arguments exits 2;
  - an argument with spaces survives (`"$@"`, not a re-split).
- RED: write the test first. It fails because there is no script yet. Then GREEN.

### 2. The wrapper and `test-pin-list.sh` (`ops/remote-shell/`)

- `REPO=/home/technojihad/narrative-adventure`, `REMOTE_SHELL_SYNC` defaults to `narrative-adventure`, and the host
  defaults to `m2`.
- **Modes:** `${REMOTE_SHELL_MODE:-remote}`.
  - `remote` and `explain` are the routing modes.
  - `local` and `probe` are opt-in. Probe logs to `${REMOTE_SHELL_LOG:-$REPO/ops/remote-shell/argv.log}`; add that
    path to `.gitignore`, although `*.log` is already ignored.
  - Any other value → `[remote-shell] FATAL: unknown REMOTE_SHELL_MODE` → exit 127, and nothing runs.
- **Pins:**
  - `SNAPSHOT_FILE=`;
  - `\bgit\b`;
  - `\bfree\b` and `/proc/meminfo`;
  - `npm run dev` with a boundary, so `npm run dev:x` does not over-match;
  - hook tests: `.claude/hooks/test-*.sh` and `.husky/test-*.sh`;
  - `wayfinder-viewer`, which covers `ops/wayfinder-viewer/` and `~/tools/wayfinder-viewer`;
  - `ops/remote-shell/`, which covers the wrapper's own tests, `preflight.sh` and `setup` (preflight grades whichever
    machine it runs on: pdfx 2026-08-26);
  - `\bmutagen\b`;
  - `mem-guard` (a guard routed to the M2 would grade the M2's memory);
  - `.claude/projects/`.
  - Each pin keeps its one-line "why" comment, in pdfx style.
- **Auto-guard:** a pinned command that matches `npm run dev` is `exec`ed as
  `"$REPO/ops/mem-guard/mem-guard.sh" -- /bin/bash -c "$CMD"`. Every other pin `exec`s `/bin/bash -c "$CMD"`.
- **Fail closed** (remote dispatch), with test seams `REMOTE_SHELL_SSH` (default `ssh`) and `REMOTE_SHELL_MUTAGEN`
  (default `mutagen`):
  - the M2 is unreachable → FATAL, exit 127;
  - mutagen is missing → FATAL, exit 127;
  - the flush fails → FATAL, exit 127;
  - there is never a local fallback. The cwd-file mirror and the exit-code capture carry over unchanged.
- **`test-pin-list.sh`**, in explain mode, offline and instant. Cases:
  - git: bare, behind quotes, behind `-C`, `git status`/`add -A`/`diff`/`log`; `github.com` stays remote;
  - free: `free -h`, `cat /proc/meminfo`, `bash -c "free -m"`;
  - dev: `npm run dev`, `npm run dev -- --port 5174`, `npm run dev` behind a quote; `npm run dev:x` → remote;
  - hook tests: `sh .claude/hooks/test-block-dangerous-git.sh` (it names git, so add the non-git
    `bash .claude/hooks/test-wayfinder-frontier.sh` too), `sh .husky/test-pre-commit-scope.sh`; a hook itself
    (`.claude/hooks/wayfinder-frontier.sh`) → remote;
  - viewer: `node --test ops/wayfinder-viewer/wayfinder-view.test.mjs` and the `~/tools/wayfinder-viewer` path;
    `ls docs/wayfinder` → remote;
  - the offload's own files: `ops/remote-shell/preflight.sh` (relative, absolute and quoted), `mutagen sync list`;
  - the guard: `ops/mem-guard/mem-guard.sh -- npm test`;
  - snapshot creation → pin, the snapshot-source prefix → remote;
  - `.claude/projects/` → pin;
  - **flipped from pdfx:** `npx playwright test` → **remote**;
  - remote: `npm test`, `npx vitest run`, `venv/bin/python -m pytest`, `npm run build`, `echo hello`.
- **Fail-closed cases** (they execute the wrapper with stubs and never touch the network):
  - unknown mode → exit 127, and a marker file is not created;
  - mode unset + a stub ssh that exits 255 → exit 127, no marker, so the default is remote and refuses;
  - remote + reachable stub ssh + a missing mutagen → 127, no marker;
  - a stub mutagen whose flush fails → 127, no marker;
  - remote + pinned `echo` → runs locally (a pin still works with the M2 down);
  - pinned `npm run dev` + the guard under its floor (`MEM_GUARD_MEMINFO` fixture) → 75, so the auto-guard is wired.
- RED: the test is written first against a straight port of pdfx (default `probe`, playwright pinned), and these cases
  fail: unknown mode, unset-mode refusal, playwright → remote, the dev auto-guard. Then GREEN.

### 3. Preflight, launcher, setup, mutagen config

- `preflight.sh`: transport (ssh alias, tailscale, reachability); the M2 env; sync (session watching, no conflicts);
  the wrapper is executable; the hostname proof via `REMOTE_SHELL_MODE=remote`. Same exit codes: 10, 20, 0.
  - The M2 env checks: the user is `technojihad`, the repo is at `$REPO`, `venv/`, `node_modules/`,
    `data/ephemeris/de440s.bsp`; node, python3 and uv parity.
  - The headless shell is checked only once `node_modules/.bin/playwright` exists. Until E1 it prints `[info]`.
  - The `.env` containment section is deleted.
- `claude-m2.sh`: a straight port with the repo path swapped. The banner's pinned list matches the new pins.
- `setup-m2.sh`:
  - path and toolchain parity: node v22.17.0, npm 11.14.1, Python 3.12.3, uv;
  - `uv venv venv && uv pip install -r requirements.txt`, then `npm ci`;
  - de440s fetched into `data/ephemeris/` by the same skyfield loader `orbital-positions.py` uses (check its loader
    call first, and do **not** run the generator);
  - `npx playwright install --only-shell` **only if** `node_modules/.bin/playwright` exists, otherwise a "deferred
    to E1" note. That avoids an unpinned fetch (ADR 0004).
  - The `.env` generation and leak guard are deleted.
- `mutagen.yml` ignores `venv`, `node_modules`, `dist`, `dist-ssr`, `.vite`, `data/ephemeris`, `data/raw`,
  `assets/images/nasa/raw`, `.playwright-mcp`, `graphify-out`, `.env*` (with `!.env.example`), `__pycache__`,
  `.pytest_cache` and `*.log`. It keeps `vcs: false`, mirroring pdfx, and a comment says git is pinned for exactly that
  reason.
- Check: `bash -n` on every script, and `npm run format:check` covers the yml.
- **M1 observation for the exit report:** run `ops/remote-shell/preflight.sh; echo "exit=$?"` and expect
  `STATE=UNBOOTSTRAPPED` with exit 10. Then confirm that `claude-m2.sh` refuses to launch (exit 10). Both are the
  fail-closed behaviour with the M2 offline. Never a direct `ssh`.

### 4. Husky wiring

- RED: `test-pre-commit-scope.sh` gains the assertion "the ops branch runs `ops/remote-shell/test-pin-list.sh` and
  `ops/mem-guard/test-mem-guard.sh`", plus a scoping case (`ops/remote-shell/remote-shell.sh` → `plan: ops=1`). It
  fails on the current hook.
- GREEN: the `RUN_OPS` branch adds `bash ops/remote-shell/test-pin-list.sh` and `bash ops/mem-guard/test-mem-guard.sh`.

### 5. Docs

- **CLAUDE.md** gets a new section, `## Two-machine offload (M1 ↔ M2)`, after "Hardware budget" or before "Review gates":
  - **Launch:** `./ops/remote-shell/claude-m2.sh`. Preflight states: READY, PARTIAL, UNBOOTSTRAPPED.
  - **Kill switch:** "go local" means `REMOTE_SHELL_MODE=local`, or plain `claude`.
  - **The pin list:** guarded by `test-pin-list.sh`, and never changed without a case.
  - **Fail closed:** the default mode is remote, there is no silent local fallback, and an unknown mode refuses.
  - **Why it fits `Bash(ssh:*)`:** the deny rule stops Claude from typing an ssh command. The transport lives only
    inside the reviewed, tested wrapper, and Claude never runs a direct `ssh`.
  - **Two traps carried from pdfx:**
    - `CLAUDE_CODE_SHELL` needs "bash" in the path, so always use the symlink;
    - the redirect is proven by hostname, never inferred.
  - **The guard:** heavy or 3D runs on M1 go `ops/mem-guard/mem-guard.sh -- <cmd>`. The floor is provisional at
    1536 MB and re-tuned at E1. The suite fallback (§2 item 5) runs through it.
  - Husky still runs vitest and pytest on M1 at commit.
  - **Status:** M1-complete, and the M2 catch-up gate comes before merge 1.
  - The Commands block's hook-test list gains `bash ops/remote-shell/test-pin-list.sh` and
    `bash ops/mem-guard/test-mem-guard.sh`.
- **README:** the Checks list gains the two tests. A short "Two-machine offload" paragraph points at CLAUDE.md.
- **`v1-build-spec.md` E1 entry:** add one clause, "set the mem-guard floor from the measured M1 peak RSS (owner,
  2026-10-01)".
- **The handoff:** M2 offload exits M1-complete. Record the commits and the exit report. Update the settled list with
  the three decisions above. The next step is E1.

## Exit (M1-complete, per amendment)

1. `npm run validate`, `npm test`, `venv/bin/python -m pytest`, and `validate-levels.py` are green.
2. Every hook test is green, plus `bash ops/remote-shell/test-pin-list.sh` and `bash ops/mem-guard/test-mem-guard.sh`.
3. Reduced path: none. The phase adds no animation.
4. Router over the diff: `PRECOMMIT_STAGED="$(git diff --name-only c0db095..HEAD)"` fed to
   `.claude/hooks/precommit-checks-reminder.sh` with a `git commit` stdin. Every routed report is walked and clean.
5. Dev walk: `free -h` first, then Playwright MCP against `npm run dev` on M1. The book opens, and Earth shows 9
   markers. No game code changed, so this is a no-regression check.
6. M1 observations: preflight shows UNBOOTSTRAPPED with exit 10, and the launcher refuses. Both are recorded.
7. **Deferred to the M2 catch-up gate (before merge 1):**
   - preflight READY;
   - a vitest run proven on the M2 by the hostname check;
   - M2 peak RSS;
   - one M2 suite run;
   - re-running `probe` once, to re-confirm the `CLAUDE_CODE_SHELL` argv convention on the current Claude Code.
8. README updated. Ask whether to commit after the large change (rule 7). Never push.

## Challenger Findings

Two `challenger`s ran on 2026-10-01: A on coverage, B on feasibility. **Both said revise, with high confidence.** Scope
coverage is complete; the defects are in fail-closed paths, regexes and the RED baselines. The owner paused the session
before the fixes were folded in, so the accepted fixes below are written out here and not yet applied inline above.
The next session folds them in first.

### Open owner decision (asked, not yet answered)

- **Q4. Compound or over-matched pinned commands** (A1, B8). The pin test is a substring match over the whole command,
  so `git add -A && npm test`, `free -h && npx vitest run` and `npx vitest run src/git-x.test.ts` would run the vitest
  on M1. That breaks "runs nothing on M1 that the pin list does not name". The options:
  1. **(Recommended)** Any pinned command that also matches a HEAVY regex
     (`vitest|pytest|npm (run )?(test|build|validate)|playwright|vite preview|npm run dev`) runs through mem-guard.
     This also covers `git commit` → husky.
  2. Refuse heavy pinned compounds, carving out `git commit` and `npm run dev`.
  3. Accept pdfx's behaviour and only document it.

### Accepted fixes (mechanical; fold them in at the start of the next session)

1. **Narrow the `ops/remote-shell/` directory pin** (A9, B1).
   - Pin by name: `ops/remote-shell/(preflight|test-pin-list|claude-m2|remote-shell|bash-remote-shell)\.sh`. The
     directory pin would run `setup-m2.sh` on M1, where its PWD and whoami checks both pass.
   - `setup-m2.sh` stays remote. It gains an M1 refusal: refuse if `command -v mutagen` succeeds, or if `~/.ssh/config`
     has `Host m2`.
   - Add the case `bash ops/remote-shell/setup-m2.sh` → remote.
2. **Dev pin regex** (A8, B2). `npm run dev([[:space:];&|)"'\`]|$)`, because `\b`matches`dev:x`and`dev-x`. It is one
shared variable, used by both the pin and the auto-guard. A comment notes that `npm run dev`(two spaces) and`npx vite` are not caught.
3. **Pin `npm run (test:ops|wayfinder)`** (A7, B3), with a boundary and cases. `package.json:20-21` run the viewer, but
   their command line never names it.
4. **Validate `REMOTE_SHELL_MODE` first** (A2), right after the parse and before both the pins and explain. Test an
   unknown mode with a pinned marker and with an unpinned one.
5. **RED baseline = the pdfx port plus the seams** (A3, B6).
   - `REMOTE_SHELL_SSH` covers all three ssh sites: reachability, dispatch and the cwd mirror.
   - `REMOTE_SHELL_MUTAGEN` covers both mutagen sites: `command -v` and flush.
   - No RED run touches the network. The "mode unset" case uses `env -u REMOTE_SHELL_MODE`.
   - Label the mutagen-missing and flush-fail cases as characterization, not RED.
6. **The dev auto-guard test never starts Vite** (A4, B5). It uses `: npm run dev; touch "$MARK"` with an under-floor
   fixture. Every case that executes the wrapper is wrapped in `timeout 10`.
7. **New cases** (A5):
   - remote reachable: the stub ssh logs the dispatch without eval-ing it, and no local marker appears;
   - an empty CMD, flags only, and a trailing `-o` all land on remote, then 127, and never run locally;
   - compound commands, per Q4.
8. **Strict `check()`** (A6). The output must be exactly `PIN`, or exactly `REMOTE` with rc 0. Anything else FAILs, so a
   wrapper crash cannot pass a `remote` expectation.
9. **Launcher default branch** (A10). `*) echo "preflight exited $STATE"; exit "$STATE" ;;`.
10. **Preflight's UNBOOTSTRAPPED decision** (A14, B7). Decide it from `M2_UP=0` plus the missing M2-env checks, not from
    the `MISSING≥4` count, which shifts once the `.env` section is gone. The exit report records the state actually
    observed. The launcher must refuse on both UNBOOTSTRAPPED and PARTIAL.
11. **The spec contradicts the amendment** (A11). Amend `docs/design/v1-build-spec.md:63-65`, `:424` and `:425` to point
    at the catch-up gate.
12. **The CLAUDE.md ssh rationale** (A12) names the scripts that hold the transport: the wrapper **and** `preflight.sh`.
    It also tells plain `claude` sessions to call `mem-guard.sh` explicitly and never to chain work onto a pinned
    command (B8).
13. **The `local` mode applies the dev auto-guard too** (B8).
14. **Format coverage** (B4). `format:check` does not glob yml (`package.json:17-18`). Either add `yml`, which stages
    `package.json` and routes security-audit, privacy-guard and perf-report, or drop the claim. Recommendation: drop
    the claim and keep `package.json` untouched.
15. **mem-guard details** (B9). Use `bash -c 'exit 3'`, not `exit 3`. Compare in kB, so the floor is `1536*1024` kB.
16. **A bash-only guard on top of both new tests** (B10). `[ -n "${BASH_VERSION:-}" ] || exit 1`, with a message.
17. **Step 4's scoping case is characterization** (A13, B11). Only the grep assertion is RED.
18. **Minor fixes** (A13, B12):
    - write the hook-test pins as regexes;
    - drop the `.gitignore` edit, which `*.log` already covers;
    - keep pdfx's key-material ignores in `mutagen.yml`;
    - note that `REPO` is hardcoded (a worktree execs the main checkout's guard), or resolve it relative to the script;
    - pin the uv version (0.8.0) in setup's parity checks.

### Checks that held (B)

- The snapshot-source prefix and the cwd suffix hit no new pin. That was grepped against pdfx's `argv.log`.
- `\bfree\b` only over-matches cheap reads. `\bgit\b` does not match `.gitignore` or `github.com`.
- The exit code survives `exec` → mem-guard `exec` → `bash -c`. 75 (EX_TEMPFAIL) is sensible.
- The de440s path is `Loader('data/ephemeris')('de440s.bsp')`, matching `orbital-positions.py:79-86`, and it does not
  run the generator.
- Toolchain: node v22.17.0, npm 11.14.1, Python 3.12.3, uv 0.8.0.
- No planned command trips `block-dangerous-git.sh` or the deny list. Keep `rm -rf` inside the scripts' traps.
- Every file stays under 300 lines.
