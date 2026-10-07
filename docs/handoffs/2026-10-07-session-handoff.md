# Session handoff — 2026-10-07

## Where things stand

**M2 offload is done, on the original exit** (`v1-build-spec.md` §4; T006 Amendment 2). Start SHA `c0db095`. The
M2 came online, so the 2026-10-01 deferral was lifted and the M2 catch-up gate before merge 1 is dissolved.

| Commit    | What                                                                                          |
| --------- | --------------------------------------------------------------------------------------------- |
| `5b7b3a0` | the plan folds both challenger rounds; T006 Amendment 2; spec :97, :147-148, :152-154 amended |
| `9619505` | `ops/mem-guard/` — the MemAvailable guard (RED 0/13 → GREEN 13/13)                            |
| `8cdc47a` | `ops/remote-shell/remote-shell.sh` + `test-pin-list.sh` (RED 36/68 on the pdfx port → 69/69)  |
| `9ca2e60` | `preflight.sh`, `claude-m2.sh`, `setup-m2.sh`, `mutagen.yml` (RED 69/76 → 76/76, stubs only)  |
| `b29df10` | fix: `setup-m2.sh` finds uv under the wrapper's non-login PATH (RED 76/77 → 77/77)            |
| `9de6fc3` | husky: the ops branch runs both new tests; vitest and pytest run through mem-guard            |
| (docs)    | CLAUDE.md "Two-machine offload" section and commands; README checks; this handoff             |

The resume plan was challenged again (CF-2, both revise). Its fixes are folded into
[`2026-10-01-m2-offload-plan.md`](2026-10-01-m2-offload-plan.md), which stays the phase's plan of record.

## Exit report (original items)

1. On M1, through mem-guard: `npm run validate`, vitest (21), pytest (88) and `validate-levels.py` are green.
2. All five hook tests, `test-pin-list.sh` (77), `test-mem-guard.sh` (13) and the viewer `node --test` are green.
3. Reduced path: none. The phase adds no animation.
4. Router over `c0db095..HEAD` plus `CLAUDE.md`/`README.md`: **no report routes**. The diff touches only `ops/`,
   `.husky/`, docs, `CLAUDE.md` and `README.md`, none of which the router's patterns match. The shipped game is
   unchanged.
5. Dev walk (Playwright MCP, `npm run dev` through mem-guard, M1, 2.3 GB available): the book opened; tapping Earth
   opened EarthScene with **9 markers** and the Cyrillic "Назад" label. Console: the known favicon 404 (fixed in E1) and
   WebGL ReadPixels performance notes only.
6. `ops/remote-shell/preflight.sh` → **STATE=READY, exit 0**: 17 ok, 0 fail, 0 missing. The pre-bring-up run was
   UNBOOTSTRAPPED (exit 10), as designed.
7. **The vitest run proven by hostname:** through the wrapper, `ran on: Bobby` (M1 is `TechnoJihad`), 21/21 green,
   and vitest's exit code 0 came back through the wrapper.
8. M2 footprint (M2 data only): `npx vitest run --maxWorkers=4`, nproc 4. MemAvailable dropped 166 MB from 11061 MB.
   The **M1** samples, taken by accident when the wrapper correctly pinned a script that named `/proc/meminfo`: drops
   of 360 MB and 434 MB from about 2.9 GB, with 4 workers. These feed E1's floor re-tune.
9. Parity: pytest 88 passed / 0 skipped on **both** machines (`data/raw` is synced, so the Hipparcos oracle test runs
   on the M2); vitest 21/21 on both.
10. `CLAUDE_CODE_SHELL` inside a real session: see "Pending owner item" below.
11. README updated (the Checks list and an offload paragraph).

## Pending owner item

- **Exit item 10.** Run `./ops/remote-shell/claude-m2.sh`, ask for `hostname`, and record the answer (expect `Bobby`).
  Then run `./ops/remote-shell/claude-m2.sh --probe` and one `echo probe`, and have Claude read
  `ops/remote-shell/argv.log`: the argv shape (`-c -l <cmd>`) and the cwd-file path must still match the wrapper's
  regex `/tmp/claude-[A-Za-z0-9_.-]+-cwd`. If the path changed (this Claude Code's temp tree is `/tmp/claude-1000/…`),
  that is a bug: RED/GREEN on the regex.

## The exact next step

**E1 Overlay** (`v1-build-spec.md` §4). Its entry now includes:

- peak RSS on both machines (the M2 is online);
- setting the mem-guard floor from the measured **M1** peak.

The suite's first run is on the M2.

## Settled — do not re-ask

- Everything in the 2026-10-01 handoff's settled list, except that the M1-complete amendment is lifted.
- **T006 Amendment 2** (owner, 2026-10-07): the M2 is online. M2 offload exits on the original items, the catch-up
  gate is dissolved, and E1 entry needs the M2 again. Amendment 1 returns only if the M2 goes offline.
- **Q4** (owner, 2026-10-07): a pinned command that is also HEAVY runs through mem-guard; `local` and `probe` guard
  every HEAVY command.
- **`git commit` is guarded inside husky, not in the wrapper** (owner, 2026-10-07): docs-only commits never block.
- The mutagen session `narrative-adventure` exists (created 2026-10-07, `two-way-resolved`, the M2 is Tailscale peer
  `bobby`). The M2 is bootstrapped: venv (uv), `node_modules` (`npm ci`), de440s.
- **The npm audit advisories are deferred** (owner, 2026-10-07): see "Left over".

## Owner items

- Push `development` (this phase's commits, on top of `fc75eba`).
- Exit item 10 (above).
- Before merge 1 (E4): the GitHub merge-commit default message "Pull request title".

## Left over

- **`npm audit`: 5 high-severity advisories**, on both machines and older than this phase: braces → micromatch →
  lint-staged ≤16.3.4, and source-map-js ≤1.2.1. Both are dev-only, so nothing reaches the shipped game. Deferred by
  the owner. A fix goes through ADR 0004 and `security-audit`.
- **The wrapper's reachability probe reads stdin** (inherited from pdfx): `ssh m2 true` swallows piped input, so
  `cmd | remote-shell.sh -c 'bash -s'` gets nothing. Claude Code always runs Bash with stdin from `/dev/null`, so
  sessions are unaffected. If it ever matters, add `-n` to the probe and to the cwd-mirror ssh, with a case.
- **Pin side effects worth knowing:** a command that merely _names_ `/proc/meminfo`, `free`, `mem-guard` or `git`
  (even in a comment) runs on M1. This is the safe direction, by design.
- Latent bugs 4, 5 (E1), 7, 8 (E2) and 10 (E5) are still open, as scheduled.
