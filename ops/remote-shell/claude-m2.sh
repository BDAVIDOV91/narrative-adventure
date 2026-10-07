#!/usr/bin/env bash
# claude-m2.sh — start a Claude Code session whose Bash commands run on the M2.
#
#   ./ops/remote-shell/claude-m2.sh          # normal: preflight, then launch
#   ./ops/remote-shell/claude-m2.sh --probe  # log argv to ops/remote-shell/argv.log, run everything locally
#   ./ops/remote-shell/claude-m2.sh --local  # the wrapper in local mode (HEAVY still guarded)
#   ./ops/remote-shell/claude-m2.sh --force  # launch despite a PARTIAL preflight
#
# Any other argument is passed to claude. Plain `claude` still gives a normal all-local session: the redirect is
# opt-in per session and never global, so the M2 being off cannot break M1-only work.
# Ported from pdfx. Test seam: CLAUDE_M2_PREFLIGHT (test-pin-list.sh points it at a stub).

set -uo pipefail
REPO="/home/technojihad/narrative-adventure"
cd "$REPO" || exit 1
PREFLIGHT="${CLAUDE_M2_PREFLIGHT:-./ops/remote-shell/preflight.sh}"

MODE="remote"
FORCE=0
PASS=()
for a in "$@"; do
  case "$a" in
    --probe) MODE="probe" ;;
    --local) MODE="local" ;;
    --force) FORCE=1 ;;
    *) PASS+=("$a") ;; # pdfx passed its own flags on to claude too
  esac
done

REMOTE_SHELL_MODE="$MODE" "$PREFLIGHT"
STATE=$?

case "$STATE" in
  0)
    echo
    echo "Preflight READY. Launching with Bash routed to the M2."
    ;;
  10)
    cat <<'MSG'

Preflight says UNBOOTSTRAPPED — the M2 is down, or its environment was never built.

Refusing to launch in remote mode: every Bash command would fail.
Bring-up: docs/handoffs/2026-10-01-m2-offload-plan.md step 3b. Or run plain `claude`.
MSG
    exit 10
    ;;
  20)
    if [ "$FORCE" = 0 ]; then
      cat <<'MSG'

Preflight says PARTIAL — something above is broken or missing.

Refusing to launch. A half-configured redirect is the bad case: commands may run locally with no error and no RAM
benefit, and you would not notice. Fix what is marked [FAIL] / [ -- ] above, or:
  ./ops/remote-shell/claude-m2.sh --force   (launch anyway, you accept the risk)
  claude                                    (normal all-local session)
MSG
      exit 20
    fi
    echo
    echo "PARTIAL preflight overridden with --force. You accept the risk."
    ;;
  *)
    echo "preflight exited $STATE — refusing to launch."
    exit "$STATE"
    ;;
esac

# MUST be the bash-named symlink. Claude Code honours CLAUDE_CODE_SHELL only when the path contains "bash" or "zsh";
# with any other name it falls back to the normal shell SILENTLY, and every command runs on M1 (pdfx 2026-08-23).
export CLAUDE_CODE_SHELL="$REPO/ops/remote-shell/bash-remote-shell.sh"
export REMOTE_SHELL_MODE="$MODE"
echo "CLAUDE_CODE_SHELL=$CLAUDE_CODE_SHELL"
echo "REMOTE_SHELL_MODE=$REMOTE_SHELL_MODE"
echo "Pinned to M1: git · free · npm run dev · hook tests · wayfinder viewer · preflight · mutagen · mem-guard"
echo "Guarded on M1: any pinned command that also runs tests, a build, the dev server or a generator"
echo
exec claude "${PASS[@]}"
