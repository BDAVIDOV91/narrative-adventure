#!/usr/bin/env bash
# remote-shell.sh — routes Claude Code's Bash tool to the M2, except for pinned commands, which run on M1.
#
# Activated by ops/remote-shell/claude-m2.sh, which exports
#   CLAUDE_CODE_SHELL=/home/technojihad/narrative-adventure/ops/remote-shell/bash-remote-shell.sh
# (the symlink: CLAUDE_CODE_SHELL needs "bash" in the path).
#
# Ported from pdfx (~/pdf_data_extractor_v2/ops/remote-shell/remote-shell.sh) for the M2 offload phase. Plan:
# docs/handoffs/2026-10-01-m2-offload-plan.md. The pdfx-only parts (night root, m2gate, allnighter, production pins)
# are left out. Test: ops/remote-shell/test-pin-list.sh — never change a pin, a mode or a guard without a case there.
#
# ---------------------------------------------------------------------------
# MODES  (REMOTE_SHELL_MODE)
#   remote  DEFAULT. pinned -> M1, everything else -> M2. M2 unreachable -> FATAL, never a local fallback.
#   explain print the routing decision (PIN | PIN+GUARD | REMOTE) and exit WITHOUT running anything.
#   local   run everything on M1 (the "go local" kill switch). HEAVY commands still go through mem-guard.
#   probe   like local, but log the exact argv to $LOG (re-checks the CLAUDE_CODE_SHELL calling convention).
# Any other value refuses (127). Owner decision 2026-10-01: an unconfigured wrapper fails CLOSED. pdfx defaults to
# probe; here the M2 exists, so an unset mode means remote, and remote refuses when the M2 is down.
# ---------------------------------------------------------------------------

set -uo pipefail

MODE="${REMOTE_SHELL_MODE:-remote}"
REMOTE_HOST="${REMOTE_SHELL_HOST:-m2}"
# Hardcoded, not resolved from the script's path: path parity with the M2 is the whole translation scheme, and a
# worktree elsewhere does not exist on the M2 (remote dispatch refuses outside $REPO, below).
REPO="/home/technojihad/narrative-adventure"
LOG="${REMOTE_SHELL_LOG:-$REPO/ops/remote-shell/argv.log}"
SYNC_NAME="${REMOTE_SHELL_SYNC:-narrative-adventure}"
# Test seams: test-pin-list.sh points these at offline stubs.
SSH="${REMOTE_SHELL_SSH:-ssh}"
MUTAGEN="${REMOTE_SHELL_MUTAGEN:-mutagen}"
GUARD="$REPO/ops/mem-guard/mem-guard.sh"

# --- capture the RAW invocation before anything consumes it ---------------
# pdfx 2026-08-23: the parse loop below shifts $@ to empty, so capture first.
ORIG_ARGC=$#
ORIG_ARGV=$(printf '[%s]' "$@")

# --- extract the command --------------------------------------------------
# Observed (pdfx probe, 2026-08-23): `-c <command>` and `-c -l <command>` (the -l comes AFTER -c). Flags are flags
# wherever they appear; the command is the first non-flag argument.
CMD=""
while [ $# -gt 0 ]; do
  case "$1" in
    -o | -O) shift ;; # option takes a value; drop both
    -*) : ;;          # any flag (-c, -l, -i, -s, -lc, …)
    *) [ -z "$CMD" ] && CMD="$1" ;;
  esac
  shift || break
done

# --- the mode is validated FIRST, before the pins and before explain (fix 4) ---
case "$MODE" in
  remote | explain | local | probe) ;;
  *)
    echo "[remote-shell] FATAL: unknown REMOTE_SHELL_MODE='$MODE' (remote|explain|local|probe). Nothing ran." >&2
    exit 127
    ;;
esac

# --- per-run guard override ------------------------------------------------
# `MEM_GUARD_MIN_MB=<n> <cmd>` would only reach the inner bash, never mem-guard, and Claude Code does not keep an
# `export` between calls. So a LEADING assignment is lifted out of CMD and handed to mem-guard.
if [[ "$CMD" =~ ^MEM_GUARD_MIN_MB=([0-9]+)[[:space:]]+(.*)$ ]]; then
  export MEM_GUARD_MIN_MB="${BASH_REMATCH[1]}"
  CMD="${BASH_REMATCH[2]}"
fi

# --- patterns ---------------------------------------------------------------
# B: the end of a word for npm script names. `\b` also fires before `:` and `-`, so `npm run dev\b` matched
# `dev:x` and `dev-x`, and `npm test\b` matched `test:ops` (fix 2).
B='([[:space:];&|)"'\''`]|$)'
# The pinned dev server. Holes, documented: `npm run  dev` (two spaces) and a bare `vite`.
DEV_RE="npm run dev$B"

# PIN LIST: these ALWAYS run on M1. A substring match on the whole command, so it over-matches in the safe
# direction (it costs a RAM saving, never correctness).
#  - SNAPSHOT_FILE=: Claude Code CREATES its shell snapshot with this; it sources M1's ~/.bashrc and writes under M1's
#    ~/.claude. Match the assignment only: every ordinary call is PREFIXED with `source <snapshot>`, and matching
#    that pinned everything (pdfx 2026-08-23).
#  - \bgit\b, whole: .git is synchronised while the worktrees differ (M2 lacks every ignored path), so reads on the
#    M2 lie and writes escape into the shared index (pdfx 2026-08-26). \b does not match github.com.
#  - free, /proc/meminfo: they grade the machine they run on; the RAM question is always about M1.
#  - DEV_RE: the dev server is played on M1 (rule 5; CLAUDE.md "played via npm run dev").
#  - npm run (test:ops|wayfinder): they run the wayfinder viewer, which lives on M1 only, without naming it.
#  - hook tests: they pipe JSON into a script; seconds, no RAM, no reason for the sync round trip.
#  - wayfinder-viewer: ops/wayfinder-viewer/ and ~/tools/wayfinder-viewer (M1 only, never synced).
#  - ops/remote-shell/ BY NAME: preflight grades whichever machine it runs on (pdfx 2026-08-26), and the wrapper,
#    its test and the launcher are M1 tools. setup-m2.sh is deliberately NOT pinned: it bootstraps the M2.
#  - mutagen: the CLI lives on M1; the M2 carries only the agent.
#  - mem-guard: a guard routed to the M2 would grade the M2's memory.
#  - .claude/projects/: auto-memory and transcripts exist only on M1.
PINNED_PATTERNS="SNAPSHOT_FILE=|\\bgit\\b|\\bfree\\b|/proc/meminfo|$DEV_RE|npm run (test:ops|wayfinder)$B"
PINNED_PATTERNS+='|\.claude/hooks/test-[A-Za-z0-9_-]+\.sh|\.husky/test-[A-Za-z0-9_-]+\.sh|wayfinder-viewer'
PINNED_PATTERNS+='|ops/remote-shell/(preflight|test-pin-list|claude-m2|remote-shell|bash-remote-shell)\.sh'
PINNED_PATTERNS+='|\bmutagen\b|mem-guard|\.claude/projects/'

# HEAVY (owner Q4, 2026-10-07): a command that would load M1. Pinned or local, it runs through mem-guard, so
# `git add -A && npm test` cannot sneak vitest onto M1 behind the git pin. Not `git commit`: husky guards its own
# vitest/pytest lines, so a docs-only commit never blocks (owner, 2026-10-07).
HEAVY="npm (run )?(test|build|validate|lint|type-check)$B|npm t$B|npx (vitest|tsc|eslint|vite|playwright)$B"
HEAVY+="|(^|[;&|][[:space:]]*)vitest$B|-m pytest$B|vite preview|data/scripts/|$DEV_RE"
# Exempt: the wrapper or preflight invoked as a command. Their heavy text is the M2's payload, not M1's load.
HEAVY_EXEMPT='(remote-shell|preflight)\.sh'

# here-string, NOT `printf "$CMD" | grep -Eq`: under pipefail a SIGPIPE from grep -q's early exit turns a MATCH
# into "no match" (pdfx 2026-09-15).
matches() { grep -Eq -- "$1" <<<"$CMD"; }
is_heavy() { matches "$HEAVY" && ! matches "$HEAVY_EXEMPT"; }

run_local() {
  if is_heavy; then exec "$GUARD" -- /bin/bash -c "$CMD"; fi
  exec /bin/bash -c "$CMD"
}

# --- probe / local: everything on M1, HEAVY still guarded (fix 13) ----------
if [ "$MODE" = "probe" ]; then
  {
    printf '=== %s\n' "$(date -Is)"
    printf 'argc=%s\n' "$ORIG_ARGC"
    printf 'argv=%s\n' "$ORIG_ARGV"
    printf 'shell=%s\n' "$0"
    printf 'PWD=%s\n' "$PWD"
    printf 'stdin_tty=%s\n' "$([ -t 0 ] && echo yes || echo no)"
    printf 'parsed CMD=%s\n' "$CMD"
  } >>"$LOG" 2>/dev/null
  run_local
fi
if [ "$MODE" = "local" ]; then run_local; fi

if matches "$PINNED_PATTERNS"; then
  if [ "$MODE" = "explain" ]; then
    if is_heavy; then echo "PIN+GUARD"; else echo "PIN"; fi
    exit 0
  fi
  echo "[remote-shell] PINNED to M1 — running locally." >&2
  run_local
fi

if [ "$MODE" = "explain" ]; then echo "REMOTE"; exit 0; fi

# --- remote dispatch: every failure is FATAL, never a local fallback -----------

# 0. path parity is the translation scheme; outside $REPO there is nothing on the M2 to cd into.
case "$PWD/" in
  "$REPO/"*) ;;
  *)
    echo "[remote-shell] FATAL: cwd '$PWD' is outside $REPO, which is the only synced tree. Refusing." >&2
    exit 127
    ;;
esac

# 1. reachability: a silent fallback would reintroduce the OOM with no explanation.
if ! "$SSH" -o BatchMode=yes -o ConnectTimeout=5 "$REMOTE_HOST" true 2>/dev/null; then
  echo "[remote-shell] FATAL: $REMOTE_HOST unreachable. Refusing to run locally." >&2
  echo "[remote-shell] Check: tailscale status / ops/remote-shell/preflight.sh" >&2
  echo "[remote-shell] Go local for one session: export REMOTE_SHELL_MODE=local (or run plain claude)" >&2
  exit 127
fi

# 2. close the sync race: an unflushed edit means the M2 tests a stale file, and that failure looks real.
if command -v "$MUTAGEN" >/dev/null 2>&1; then
  "$MUTAGEN" sync flush "$SYNC_NAME" >/dev/null 2>&1 || {
    echo "[remote-shell] FATAL: mutagen flush failed for session '$SYNC_NAME'." >&2
    echo "[remote-shell] Refusing to dispatch — the M2 may hold stale files." >&2
    exit 127
  }
else
  echo "[remote-shell] FATAL: mutagen not found on M1." >&2
  exit 127
fi

# 3. dispatch. No pipe on purpose: `cmd | tail` has eaten an exit code before.
REMOTE_PWD="$PWD"

# Claude Code appends `pwd -P >| /tmp/claude-<id>-cwd` to every command and reads the file back. Run on the M2,
# that file is written on the M2, so mirror it back. The exit code is captured FIRST.
CWD_FILE=$(printf '%s' "$CMD" | grep -oE '/tmp/claude-[A-Za-z0-9_.-]+-cwd' | tail -1)

# A missing cwd on the M2 FAILS LOUD (97). pdfx's `|| cd '$REPO'` fallback ran commands silently in the wrong
# tree (pdfx 3f56e373, 2026-10-04).
"$SSH" "$REMOTE_HOST" "cd '$REMOTE_PWD' || { echo 'REMOTE CWD MISSING ON M2' >&2; exit 97; }; $CMD"
RC=$?

if [ -n "$CWD_FILE" ]; then
  "$SSH" -o BatchMode=yes "$REMOTE_HOST" "cat '$CWD_FILE' 2>/dev/null" >"$CWD_FILE" 2>/dev/null || true
fi

exit $RC
