# M2 offload (v1-build-spec §4; T006 Amendment 2, 2026-10-07)

**Start SHA:** `c0db095a7c85aa909019f8ca8bb952a8592ce381` (recorded at entry, T006 d1).

## Context

The M2 offload phase sits between E0 and E1. It ports pdfx's remote-shell wrapper so heavy Bash runs leave M1.

- **2026-10-01:** the M2 was offline. The T006 amendment had this phase build its M1 side and exit M1-complete. The plan
  was challenged, then paused before any code.
- **2026-10-07:** the M2 is online (Tailscale peer `bobby`, ssh alias `m2`, mutagen 0.18.1 already serving pdfx). The
  owner chose the **original exit**: `preflight.sh` READY and the vitest run proven on the M2 by hostname. T006
  Amendment 2 records this; Amendment 1's rules return only if the M2 goes offline again.

The wrapper still **fails closed**: when the M2 is unreachable it runs nothing on M1 that the pin list does not name.

Source to port: `~/pdf_data_extractor_v2/ops/remote-shell/` at HEAD (`remote-shell.sh`, its `bash-remote-shell.sh`
symlink, `test-pin-list.sh`, `preflight.sh`, `claude-m2.sh`, `setup-m2.sh`) and `.claude/remote-shell/mutagen.yml`.
The port leaves out everything pdfx added after 10-01 that is pdfx-only: the night-root dispatch
(`NIGHT_ROOT_PREFIX`, `3f56e373`), `m2gate`, `allnighter`, the prod backfill pins and `preflight-card`. It keeps the
here-string match and its pipefail note.

### Owner decisions this session (2026-10-01, do not re-ask)

1. **Guard floor:** a provisional **1536 MB** of MemAvailable, overridable per run with `MEM_GUARD_MIN_MB`. It is
   **re-tuned at E1 entry** from the measured peak RSS (peak plus a margin). A refusal prints the measured value and
   the override.
2. **Wrapper modes:** the default (mode unset) is `remote`, and it refuses when the M2 is unreachable. An unknown mode
   refuses. `local` (the "go local" kill switch) and `probe` (argv logging, for re-checking the calling convention at
   exit 10) run only when exported explicitly.
3. **Auto-guard:** the wrapper runs the pinned `npm run dev` through the MemAvailable guard. Widened by decision 4.

### Owner decisions 2026-10-07 (do not re-ask)

4. **Q4 → auto-guard heavy.** A pinned command that also matches `HEAVY` runs through mem-guard. `local` mode guards
   every HEAVY command.
5. **The original exit:** preflight READY + vitest proven on the M2 by hostname (T006 Amendment 2).
6. **`git commit` is guarded inside husky, not in the wrapper.** `.husky/pre-commit` runs its vitest and pytest calls
   through `mem-guard.sh`, so docs-only commits never block.
7. **Claude creates the mutagen session.** The owner runs the M2-side commands (`setup-m2.sh`, PATH fixes) over AnyDesk.

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
| `.husky/pre-commit`                           | ops branch runs both new tests; vitest/pytest run through mem-guard            |
| `.husky/test-pre-commit-scope.sh`             | asserts both (RED first)                                                       |
| `CLAUDE.md`, `README.md`                      | new "Two-machine offload" section; commands; hook-test list                    |
| `docs/design/v1-build-spec.md`                | E1 floor clause (M1 peak RSS); :97, :147-148, :152-154 amended 2026-10-07      |
| `docs/wayfinder/v1-build/tickets/006-…`       | Amendment 2 — the M2 is online                                                 |
| `docs/handoffs/2026-10-07-session-handoff.md` | new: M2 offload done on the original exit, E1 is next                          |

Each new script stays well under 300 lines.

## Steps (each lands RED → GREEN, one commit per step)

### 1. MemAvailable guard (`ops/mem-guard/`)

- `mem-guard.sh [--] <cmd...>`:
  - It reads `MemAvailable` from `${MEM_GUARD_MEMINFO:-/proc/meminfo}`; the meminfo path is the test seam.
  - The floor is `${MEM_GUARD_MIN_MB:-1536}`, with a "provisional, re-tuned at E1 entry" comment. The comparison is in
    kB (`floor*1024`), with no MB rounding (fix 15).
  - Below the floor it prints `[mem-guard] REFUSED: MemAvailable=<n> MB < floor <f> MB`, plus the override line, and
    exits 75. At or above the floor it `exec`s the command, so the exit code survives.
  - It fails closed: a missing or unparsable `MemAvailable`, or a non-integer floor, refuses with a message. With no
    command it prints usage and exits 2.
- `test-mem-guard.sh` uses fixture meminfo files in a mktemp dir. Cases:
  - below the floor refuses, and the marker command never runs;
  - above the floor runs, and the exit code passes through (`bash -c 'exit 3'` returns 3, fix 15);
  - exactly at the floor runs;
  - `MEM_GUARD_MIN_MB` overrides the floor;
  - a missing `MemAvailable` line refuses;
  - a garbage floor refuses;
  - no arguments exits 2;
  - an argument with spaces survives (`"$@"`, not a re-split).
- The test starts with a bash-only guard, `[ -n "${BASH_VERSION:-}" ] || { echo "run with bash" >&2; exit 1; }`
  (fix 16), then
  `unset REMOTE_SHELL_MODE REMOTE_SHELL_HOST REMOTE_SHELL_SYNC REMOTE_SHELL_LOG MEM_GUARD_MIN_MB MEM_GUARD_MEMINFO`
  (CF-2 13).
- RED: write the test first. It fails because there is no script yet. Then GREEN.

### 2. The wrapper and `test-pin-list.sh` (`ops/remote-shell/`)

- `REPO=/home/technojihad/narrative-adventure`, hardcoded (CF-2 7). `REMOTE_SHELL_SYNC` defaults to
  `narrative-adventure`, and the host defaults to `m2`.
- **Modes:** `${REMOTE_SHELL_MODE:-remote}`, **validated right after the argv parse**, before both the pins and
  explain (fix 4).
  - `remote` and `explain` are the routing modes.
  - `local` and `probe` are opt-in. Probe logs to `${REMOTE_SHELL_LOG:-$REPO/ops/remote-shell/argv.log}`; `*.log` is
    already gitignored (fix 18).
  - Any other value → `[remote-shell] FATAL: unknown REMOTE_SHELL_MODE` → exit 127, and nothing runs.
- **The boundary class** `B='([[:space:];&|)"'\''`]|$)'`is one shared variable (fix 2).`\b`would match`dev:x`,
`dev-x`and`test:ops`.
- **Pins** (each with its one-line "why" comment, pdfx style):
  - `SNAPSHOT_FILE=`;
  - `\bgit\b`;
  - `\bfree\b` and `/proc/meminfo`;
  - `DEV_RE='npm run dev'"$B"`. `npm run dev` with two spaces is a documented hole;
  - `npm run (test:ops|wayfinder)$B`: their command lines never name the viewer (`package.json:20-21`, fix 3);
  - hook tests, written as regexes: `\.claude/hooks/test-[A-Za-z0-9_-]+\.sh` and `\.husky/test-[A-Za-z0-9_-]+\.sh`;
  - `wayfinder-viewer`, which covers `ops/wayfinder-viewer/` and `~/tools/wayfinder-viewer`;
  - **by name** (fix 1): `ops/remote-shell/(preflight|test-pin-list|claude-m2|remote-shell|bash-remote-shell)\.sh`.
    Preflight grades whichever machine it runs on (pdfx 2026-08-26). `setup-m2.sh` stays **remote**;
  - `\bmutagen\b`;
  - `mem-guard` (a guard routed to the M2 would grade the M2's memory);
  - `\.claude/projects/`.
- **HEAVY** (Q4, CF-2 4). It covers `npm (run )?(test|build|validate|lint|type-check)$B`, `npm t$B`,
  `npx (vitest|tsc|eslint|vite|playwright)$B`, `(^|[;&|] *)vitest$B`, `-m pytest$B`, `vite preview`, `data/scripts/`
  and `DEV_RE`.
  - Not `git commit`: husky guards its own heavy lines (decision 6).
  - Exempt: a command whose first word is `remote-shell.sh`, `bash-remote-shell.sh` or `preflight.sh`, because that
    work runs on the M2.
- **Dispatch of a pinned command:**
  - HEAVY → `exec "$REPO/ops/mem-guard/mem-guard.sh" -- /bin/bash -c "$CMD"`;
  - otherwise → `exec /bin/bash -c "$CMD"`.
  - `local` mode applies the same rule to **every** command, pinned or not (fix 13).
  - A leading `MEM_GUARD_MIN_MB=<int> ` in CMD is stripped and exported to mem-guard. That is the per-run override
    (CF-2 6).
- **Explain mode** prints exactly `PIN`, `PIN+GUARD` or `REMOTE` (CF-2 3).
- **Fail closed** (remote dispatch). The test seams are `REMOTE_SHELL_SSH` (default `ssh`), covering reachability,
  dispatch and the cwd mirror, and `REMOTE_SHELL_MUTAGEN` (default `mutagen`), covering `command -v` and flush (fix 5).
  Every failure below exits 127 unless noted:
  - `$PWD` is not under `$REPO`;
  - the M2 is unreachable;
  - mutagen is missing;
  - the flush fails;
  - remote side: `cd '$REMOTE_PWD' || { echo 'REMOTE CWD MISSING ON M2' >&2; exit 97; }; $CMD`, with **no** `$REPO`
    fallback (CF-2 7).
  - There is never a local fallback. The cwd-file mirror and the exit-code capture carry over unchanged.
- **`test-pin-list.sh`**:
  - It starts with the bash-only guard (fix 16) and the `unset` line (CF-2 13).
  - `check()` is strict: the output must be exactly the expected token with rc 0, or the case FAILs (fix 8).
  - **Explain cases** (offline, instant):
    - git: bare, behind quotes, behind `-C`, `git status`/`add -A`/`diff`/`log`; `github.com` → REMOTE;
      `git commit -m "pytest"`, `git add vitest.config.ts` and `git log --grep=pytest` → PIN;
    - free: `free -h`, `cat /proc/meminfo`, `bash -c "free -m"`;
    - dev: `npm run dev`, `npm run dev -- --port 5174`, `npm run dev` behind a quote → PIN+GUARD;
      `npm run dev:x` and `npm run dev-x` → REMOTE;
    - `npm run test:ops` and `npm run wayfinder` → PIN;
    - hook tests: `sh .claude/hooks/test-block-dangerous-git.sh`, `bash .claude/hooks/test-wayfinder-frontier.sh`,
      `sh .husky/test-pre-commit-scope.sh` → PIN; `.claude/hooks/wayfinder-frontier.sh` → REMOTE;
    - viewer: `node --test ops/wayfinder-viewer/wayfinder-view.test.mjs` and the `~/tools/wayfinder-viewer` path → PIN;
      `ls docs/wayfinder` → REMOTE;
    - offload files: `ops/remote-shell/preflight.sh` (relative, absolute, quoted), `mutagen sync list` → PIN;
      `bash ops/remote-shell/setup-m2.sh` → REMOTE (characterization, CF-2 15);
      `REMOTE_SHELL_MODE=remote ops/remote-shell/remote-shell.sh -c 'hostname; npx vitest run'` → PIN, because the
      exemption applies;
    - the guard: `ops/mem-guard/mem-guard.sh -- npm test` → PIN+GUARD;
    - HEAVY compounds: `git add -A && npm test`, `free -h && npx vitest run`, `git status; npm run build` → PIN+GUARD;
    - snapshot creation → PIN, and the snapshot-source prefix → REMOTE;
    - `.claude/projects/` → PIN;
    - **flipped from pdfx:** `npx playwright test` → REMOTE;
    - remote: `npm test`, `npx vitest run`, `venv/bin/python -m pytest`, `npm run build`, `echo hello`.
  - **Executed cases.** Each runs under `timeout 10` from a mktemp cwd, in the neutral form
    `: <cmd>; touch "$MARK"`, with a stub ssh/mutagen on the seams. Nothing reaches the network or runs real work
    (fix 6, CF-2 2).
    - unknown mode, with a pinned marker and with an unpinned one → 127, no marker;
    - mode unset (`env -u REMOTE_SHELL_MODE`) + stub ssh exiting 255 → 127, no marker;
    - remote + reachable stub ssh + a missing mutagen → 127, no marker (characterization);
    - a stub mutagen whose flush fails → 127, no marker (characterization);
    - remote reachable: the stub ssh logs its argv without eval-ing; the dispatch line carries
      `REMOTE CWD MISSING ON M2` and no `|| cd`; no local marker;
    - `$PWD` outside `$REPO` → 127, ssh never called;
    - an empty CMD, flags only, and a trailing `-o` → remote → 127, never local;
    - remote + pinned `: git status; touch "$MARK"` → runs locally (a pin still works with the M2 down);
    - pinned HEAVY `: git add -A && : npm test; touch "$MARK"` + an under-floor `MEM_GUARD_MEMINFO` fixture → 75, no
      marker;
    - `MEM_GUARD_MIN_MB=1 : npm run dev; touch "$MARK"` + the under-floor fixture → runs (override honoured);
    - `REMOTE_SHELL_MODE=local` + `: npx vitest run; touch "$MARK"` + the under-floor fixture → 75, no marker.
- **RED:** the test is written first against a straight port of pdfx plus the seams. These cases fail: unknown mode,
  unset-mode refusal, playwright → REMOTE, every PIN+GUARD case and its executed twin, the `test:ops`/`wayfinder` pins,
  `dev:x`/`dev-x`, the outside-`$REPO` refusal, the cwd fail-loud, the override, and `local` guarding. Then GREEN.

### 3. Preflight, launcher, setup, mutagen config

- `preflight.sh` checks:
  - transport: ssh alias, tailscale, reachability;
  - the M2 env;
  - sync: the session is watching and has no conflicts;
  - the wrapper is executable;
  - the hostname proof, via `REMOTE_SHELL_MODE=remote`.
- Preflight exit codes: 10, 20, 0. Every ssh goes through the `REMOTE_SHELL_SSH` seam (CF-2 8).
  - The M2 env checks: the user is `technojihad`, the repo is at `$REPO`, `venv/`, `node_modules/`,
    `data/ephemeris/de440s.bsp`; node, python3 and uv parity.
  - **Dispatch-shape check** (CF-2 9): `REMOTE_SHELL_MODE=remote "$WRAPPER" -c 'command -v npx && node --version'`
    must print v22.17.0. The M2's non-login ssh shell may not load nvm.
  - The headless shell is checked only once `node_modules/.bin/playwright` exists. Until E1 it prints `[info]`.
  - The `.env` containment section is deleted.
  - **UNBOOTSTRAPPED** comes from `M2_UP=0` or a missing M2 env check, not from the `MISSING≥4` count (fix 10).
- `claude-m2.sh`: a port with the repo path swapped. The banner's pinned list matches the new pins.
  - It filters its own flags (`--probe`) before `exec claude` (CF-2 8).
  - It refuses on UNBOOTSTRAPPED and on PARTIAL.
  - Its default branch is `*) echo "preflight exited $STATE"; exit "$STATE" ;;` (fix 9).
  - The `CLAUDE_M2_PREFLIGHT` seam points it at a stub.
- `setup-m2.sh`:
  - **Its first statement is the M1 refusal** (fix 1, CF-2 2): it refuses if `command -v mutagen` succeeds, or if
    `~/.ssh/config` has `Host m2`.
  - Path and toolchain parity: node v22.17.0, npm 11.14.1, Python 3.12.3, uv 0.8.0 (fix 18).
  - `uv venv venv && uv pip install -r requirements.txt`, then `npm ci`.
  - de440s is fetched into `data/ephemeris/` with `Loader('data/ephemeris')('de440s.bsp')`, matching
    `orbital-positions.py:79-86`. The generator is **not** run.
  - `npx playwright install --only-shell` runs **only if** `node_modules/.bin/playwright` exists; otherwise it prints a
    "deferred to E1" note (ADR 0004).
  - The `.env` generation and leak guard are deleted.
- `mutagen.yml`:
  - Mode `two-way-resolved`, as pdfx uses.
  - It ignores `venv`, `node_modules`, `dist`, `dist-ssr`, `.vite`, `data/ephemeris`, `assets/images/nasa/raw`,
    `.playwright-mcp`, `graphify-out`, `.env*` (with `!.env.example`), `__pycache__`, `.pytest_cache`, `*.log`, and
    pdfx's key-material patterns (fix 18).
  - **`data/raw` is synced**, so the Hipparcos oracle test runs on both machines (CF-2 12).
  - It keeps `vcs: false`, with a comment that git is pinned for exactly that reason.
- Tests added to `test-pin-list.sh` (all with stubs, never real installs):
  - `setup-m2.sh` from a mktemp cwd, with `PATH` stubs for `uv/npm/npx/node/python3` that only touch markers, and a
    stub `HOME`. Case one: `.ssh/config` has `Host m2`. Case two: a stub `mutagen` is on `PATH`. Both → refusal text,
    and no stub marker. RED: the stubs are called.
  - `preflight.sh` with a stub ssh exiting 255 → `STATE=UNBOOTSTRAPPED`, exit 10.
  - `claude-m2.sh` with a stub preflight exiting 20, then 33 → refuses with that code, and a stub `claude` never runs.
- `bash -n` on every script. The yml is not covered by `format:check`, and `package.json` stays untouched (fix 14).

### 3b. M2 bring-up (2026-10-07)

1. Tailscale and the `m2` alias are already live.
2. Claude runs `mutagen sync create --name narrative-adventure -c ops/remote-shell/mutagen.yml
/home/technojihad/narrative-adventure m2:/home/technojihad/narrative-adventure`, then `mutagen sync flush`.
3. The owner runs `ops/remote-shell/setup-m2.sh` on the M2 (AnyDesk), and fixes the M2's PATH if the dispatch-shape
   check fails.
4. Claude runs `ops/remote-shell/preflight.sh` and expects READY.
5. The owner launches `ops/remote-shell/claude-m2.sh`, runs `hostname` there, and pastes it. A `--probe` launch
   follows. Claude reads `argv.log` and checks that the cwd-file regex matches the observed path. If it does not, that
   is a bug: RED/GREEN.

### 4. Husky wiring

- RED: `test-pre-commit-scope.sh` gains two assertions:
  - the ops branch runs `ops/remote-shell/test-pin-list.sh` and `ops/mem-guard/test-mem-guard.sh`;
  - husky's vitest and pytest lines run through `ops/mem-guard/mem-guard.sh` (decision 6).
- A scoping case (`ops/remote-shell/remote-shell.sh` → `plan: ops=1`) is characterization (fix 17).
- GREEN: the `RUN_OPS` branch adds both tests, and the vitest/pytest lines go `bash ops/mem-guard/mem-guard.sh -- …`.

### 5. Docs

- **CLAUDE.md** gets a new section, `## Two-machine offload (M1 ↔ M2)`, before "Review gates":
  - **Launch:** `./ops/remote-shell/claude-m2.sh`. Preflight states: READY, PARTIAL, UNBOOTSTRAPPED.
  - **Kill switch:** "go local" means `REMOTE_SHELL_MODE=local`, or plain `claude`.
  - **The pin list:** guarded by `test-pin-list.sh`, and never changed without a case.
  - **Fail closed:** the default mode is remote, there is no silent local fallback, an unknown mode refuses, and a
    missing remote cwd exits 97.
  - **Why it fits `Bash(ssh:*)`:** the transport lives only inside the reviewed, tested wrapper and `preflight.sh`
    (fix 12). Claude never runs a direct `ssh`.
  - **Two traps carried from pdfx:**
    - `CLAUDE_CODE_SHELL` needs "bash" in the path, so always use the symlink;
    - the redirect is proven by hostname, never inferred.
  - **The guard:**
    - A pinned HEAVY command is auto-guarded.
    - Plain `claude` sessions call `ops/mem-guard/mem-guard.sh -- <cmd>` explicitly, and never chain work onto a
      pinned command (fix 12).
    - The floor is provisional at 1536 MB, with a per-run override (`MEM_GUARD_MIN_MB=<n>` prefix), and is re-tuned at
      E1 from the M1 peak.
    - The documented holes: `npm run  dev` with two spaces, and a bare `vite`.
  - Husky runs vitest and pytest on M1 at commit, through the guard.
  - **Status:** live; READY on 2026-10-07.
  - The Commands block's hook-test list gains `bash ops/remote-shell/test-pin-list.sh` and
    `bash ops/mem-guard/test-mem-guard.sh`.
- **README:** the Checks list gains the two tests. A short "Two-machine offload" paragraph points at CLAUDE.md.
- **`v1-build-spec.md`:**
  - The E1 entry gains "set the mem-guard floor from the measured **M1** peak RSS (owner, 2026-10-01)".
  - `:97`, `:147-148` and `:152-154` get "Amended 2026-10-07 (T006 Amendment 2)".
- **Handoff:** a new `docs/handoffs/2026-10-07-session-handoff.md` records the commits, the exit report, decisions 4-7,
  and that E1 is next.

## Exit (original items, T006 Amendment 2)

1. `npm run validate`, `npm test`, `venv/bin/python -m pytest` and `validate-levels.py` are green on M1.
2. Every hook test is green, plus `bash ops/remote-shell/test-pin-list.sh` and `bash ops/mem-guard/test-mem-guard.sh`.
3. Reduced path: none. The phase adds no animation.
4. Router over the diff: `PRECOMMIT_STAGED="$(git diff --name-only c0db095..HEAD)"` fed to
   `.claude/hooks/precommit-checks-reminder.sh` with a `git commit` stdin. Every routed report is walked and clean.
5. Dev walk: `free -h` first, then Playwright MCP against `npm run dev` on M1. The book opens, and Earth shows 9
   markers. This is a no-regression check.
6. `ops/remote-shell/preflight.sh` → `STATE=READY`, exit 0.
7. **The vitest run proven by hostname:** `REMOTE_SHELL_MODE=remote ops/remote-shell/remote-shell.sh -c 'hostname;
npx vitest run'` prints the M2's hostname (≠ M1's), and vitest is green. Inside `claude-m2.sh`, the owner's pasted
   `hostname` (3b.5) proves the session redirect.
8. M2 footprint: `MemAvailable` sampled during `npx vitest run --maxWorkers=4` through the wrapper. This is M2 data
   only; E1 re-tunes the floor from the M1 peak.
9. One M2 run of vitest + pytest, with pass and skip counts compared against M1. The Playwright suite's first run is
   E1's, on the M2.
10. `argv.log` from the probe launch confirms the `CLAUDE_CODE_SHELL` convention and the cwd-file regex.
11. README updated. Ask whether to commit after the large change (rule 7). Never push.

## Challenger Findings

Two `challenger`s ran on 2026-10-01: A on coverage, B on feasibility. **Both said revise, with high confidence.** Scope
coverage is complete; the defects are in fail-closed paths, regexes and the RED baselines. The owner paused the session
before the fixes were folded in. **All of them were folded inline on 2026-10-07**, and the list below stays as the
record.

### Owner decision Q4 (answered 2026-10-07: option 1, auto-guard heavy — decision 4)

- **Q4. Compound or over-matched pinned commands** (A1, B8). The pin test is a substring match over the whole command,
  so `git add -A && npm test`, `free -h && npx vitest run` and `npx vitest run src/git-x.test.ts` would run the vitest
  on M1. That breaks "runs nothing on M1 that the pin list does not name". The options:
  1. **(Recommended)** Any pinned command that also matches a HEAVY regex
     (`vitest|pytest|npm (run )?(test|build|validate)|playwright|vite preview|npm run dev`) runs through mem-guard.
     This also covers `git commit` → husky.
  2. Refuse heavy pinned compounds, carving out `git commit` and `npm run dev`.
  3. Accept pdfx's behaviour and only document it.

### Accepted fixes (all folded 2026-10-07; fix 11 reworked by CF-2 1, fix 18's REPO by CF-2 7)

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

## Challenger Findings 2 (CF-2, 2026-10-07)

A second pair of `challenger`s ran on the resume plan: A on coverage, B on feasibility. **Both said revise, with high
confidence.** All folded inline above.

Owner answer during the challenge: **`git commit` is guarded inside husky, not in the wrapper.** `.husky/pre-commit`
wraps only its vitest/pytest calls in `mem-guard.sh`, so docs commits never block. Every finding below is accepted and
folded into the sections above (where marked) and into the repo plan in step 0.

1. **Spec is stale (A1, B7).** The step-0 docs commit adds "Amended 2026-10-07 (T006 Amendment 2)" at
   `v1-build-spec.md:97` (drop the catch-up gate Extra), `:147-148` and `:152-154`. The repo plan also rewrites its
   Context (:7-11), decision 2 (:22-23), the Files row (:54, the 10-07 handoff), step 3's M1 observation (:157-159,
   kept as an optional pre-bring-up record) and step 5 (:183-190).
2. **No RED or regression case runs real work (A2, A3, B1, B2).**
   - Every executed case is the neutral form `: <cmd>; touch "$MARK"`, run from a mktemp cwd under `timeout 10`.
   - `setup-m2.sh`'s M1 refusal is its **first statement**.
   - Its test puts stub `uv/npm/npx/node/python3/mutagen` on `PATH`; each stub only touches a marker. Two triggers are
     tested: `Host m2` in the stub `HOME`'s `.ssh/config`, and `command -v mutagen`. The test asserts the refusal text
     and that no stub marker appears.
3. **Explain gets a third token, `PIN+GUARD` (A4, B1).** `check()` accepts exactly `PIN`, `PIN+GUARD` or `REMOTE` with
   rc 0. Q4/HEAVY cases are tested in explain mode; one executed case per path (pinned, `local`) proves the guard is
   wired (exit 75, no marker).
4. **HEAVY regex (A5, A6, B8), using the shared `B` boundary class `([[:space:];&|)"'\`]|$)`.**
   - It covers `npm (run )?(test|build|validate|lint|type-check)B`, `npm tB`, `npx (vitest|tsc|eslint|vite|playwright)B`,
     `(^|[;&|] *)vitestB`, `-m pytestB`, `vite preview`, `data/scripts/` and DEV_RE.
   - It does **not** cover `git commit` (owner).
   - Exempt: a command whose first word is `remote-shell.sh`, `bash-remote-shell.sh` or `preflight.sh`, since that
     work runs on the M2.
   - Cases: `npm run test:ops` → `PIN`, `git add vitest.config.ts` → `PIN`, `git log --grep=pytest` → `PIN`,
     `git commit -m "pytest"` → `PIN`, the exit-7 wrapper command → `PIN`.
   - Accepted holes, documented next to the "never chain" note: `npm run dev` with two spaces, and a bare `npx vite`
     without the npx prefix.
5. **`local` mode** guards any HEAVY command, pinned or not (A4).
6. **Per-run override (B5).** The wrapper strips a leading `MEM_GUARD_MIN_MB=<int> ` from CMD and passes it to
   mem-guard. A case covers it. The refusal message names this form.
7. **Fail-closed cwd (A10, B6).**
   - Remote side: `cd '$REMOTE_PWD' || { echo 'REMOTE CWD MISSING ON M2' >&2; exit 97; }; $CMD`, with no `$REPO`
     fallback.
   - `REPO` stays hardcoded. Remote dispatch refuses with 127 when `$PWD` is not under `$REPO`.
   - Stub-ssh case for both. This replaces minor fix 18's "resolve REPO relative to the script".
8. **Preflight and launcher are testable offline (A9).** `REMOTE_SHELL_SSH` seams every ssh in `preflight.sh`. Cases: a
   stub exiting 255 → `STATE=UNBOOTSTRAPPED`, exit 10. The launcher given a stub preflight (`CLAUDE_M2_PREFLIGHT` seam)
   exiting 20 or 33 refuses with that code. The launcher filters its own flags (`--probe`) before `exec claude` (B10).
9. **`npx` in the dispatch shell (B4).** Preflight adds a check in the exact dispatch shape:
   `REMOTE_SHELL_MODE=remote "$WRAPPER" -c 'command -v npx && node --version'`, which must print v22.17.0. If it
   fails, setup-m2 or the owner fixes the M2's PATH. The dispatch is not changed to `bash -lc`.
10. **RSS (A7, B3).**
    - Exit 8 becomes "M2 footprint: `MemAvailable` sampled every 0.2 s during `npx vitest run --maxWorkers=4` through
      the wrapper (drop = before − min). This is M2 data only."
    - The E1 clause keeps "**M1** peak RSS".
    - `/usr/bin/time` is dropped.
11. **Exit 10 is an owner step in 3b (A7, B10).** The owner launches `claude-m2.sh`, runs `hostname`, and pastes the
    output. A `--probe` launch follows. Claude reads `argv.log` and asserts that the cwd-file regex matches the observed
    path (`/tmp/claude-1000/…`). If it does not, that is a bug: RED/GREEN on the regex.
12. **Parity (B11).** `data/raw` is synced: it is public HYG/Stellarium data, about 15 MB. Exit 9 compares pass and skip
    counts between M1 and the M2.
13. **Env hygiene (B12).** Both tests start with
    `unset REMOTE_SHELL_MODE REMOTE_SHELL_HOST REMOTE_SHELL_SYNC REMOTE_SHELL_LOG MEM_GUARD_MIN_MB MEM_GUARD_MEMINFO`.
14. **Amendment 2 (A8).** T006's "one suite run on the M2" means the Playwright suite. It moves to E1's first exit (on
    the M2) and is named there as not proven here.
15. **RED labels (B9).** `setup-m2.sh` → remote is characterization.
16. **CLAUDE.md (A11)** keeps both halves of fix 12: plain `claude` sessions call `mem-guard.sh` explicitly, and work is
    never chained onto a pinned command.
17. **Step 3b, concrete:** Claude runs
    `mutagen sync create --name narrative-adventure -c ops/remote-shell/mutagen.yml /home/technojihad/narrative-adventure m2:/home/technojihad/narrative-adventure`
    (owner chose "Claude runs it"). The `pdfx` session shows `two-way-resolved`; Tailscale (peer `bobby`) and the `m2`
    alias are already live. The owner then runs `setup-m2.sh` on the M2.
18. **Step 4 adds** a RED assertion: husky's vitest and pytest lines run through `ops/mem-guard/mem-guard.sh`.
