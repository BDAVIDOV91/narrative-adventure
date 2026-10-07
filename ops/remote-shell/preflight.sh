#!/usr/bin/env bash
# preflight.sh — state detection + readiness checks for the M1 -> M2 offload. It never changes anything.
#
# The final line is  STATE=<UNBOOTSTRAPPED|PARTIAL|READY>  and the exit code matches: 10 / 20 / 0.
# ops/remote-shell/claude-m2.sh launches only on READY. Pinned to M1 in remote-shell.sh: it grades whichever machine
# it runs on (pdfx 2026-08-26).
#
# Ported from pdfx (ops/remote-shell/preflight.sh). The production-containment (.env) section is gone: this repo has
# no credentials. Test seams: REMOTE_SHELL_SSH and REMOTE_SHELL_MUTAGEN (test-pin-list.sh points them at stubs).

set -uo pipefail

REPO="/home/technojihad/narrative-adventure"
HOST="${REMOTE_SHELL_HOST:-m2}"
SYNC="${REMOTE_SHELL_SYNC:-narrative-adventure}"
WRAPPER="$REPO/ops/remote-shell/remote-shell.sh"
SSH="${REMOTE_SHELL_SSH:-ssh}"
MUTAGEN="${REMOTE_SHELL_MUTAGEN:-mutagen}"
# M1's toolchain (2026-10-01). The M2 must match: a version drift reads as a code defect.
NODE_WANT="v22.17.0"

PASS=0
FAIL=0
MISSING=0
ENV_MISSING=0
ok() { printf '  [ ok ] %s\n' "$*"; PASS=$((PASS + 1)); }
bad() { printf '  [FAIL] %s\n' "$*"; FAIL=$((FAIL + 1)); }
gone() { printf '  [ -- ] %s\n' "$*"; MISSING=$((MISSING + 1)); }
rssh() { "$SSH" -o BatchMode=yes -o ConnectTimeout=5 "$HOST" "$@"; }

echo "M1 -> M2 preflight  ($(date -Is))"
echo

# --- 1. transport ---------------------------------------------------------
echo "transport"
if grep -qE "^Host[[:space:]]+$HOST([[:space:]]|$)" ~/.ssh/config 2>/dev/null; then
  ok "ssh alias '$HOST' defined"
else
  gone "ssh alias '$HOST' not in ~/.ssh/config"
fi

if command -v tailscale >/dev/null 2>&1; then
  if tailscale status >/dev/null 2>&1; then ok "tailscale up on M1"; else bad "tailscale installed but not connected"; fi
else
  gone "tailscale not installed on M1"
fi

M2_UP=0
if rssh true 2>/dev/null; then
  ok "ssh $HOST reachable, key auth, no prompt"
  M2_UP=1
else
  gone "ssh $HOST unreachable (M2 off, no sshd, or key not installed)"
fi

# --- 2. M2 environment ----------------------------------------------------
echo
echo "M2 environment"
if [ "$M2_UP" = 1 ]; then
  R_USER=$(rssh whoami 2>/dev/null)
  [ "$R_USER" = "technojihad" ] && ok "M2 user is technojihad (path parity)" \
    || bad "M2 user is '$R_USER', must be technojihad"

  for pair in "repo:$REPO" "venv:$REPO/venv" "node_modules:$REPO/node_modules" \
    "de440s:$REPO/data/ephemeris/de440s.bsp"; do
    what="${pair%%:*}"
    path="${pair#*:}"
    if rssh "test -e '$path'" 2>/dev/null; then
      ok "$what present on M2"
    else
      gone "$what missing on M2 at $path (mutagen not synced, or run setup-m2.sh)"
      ENV_MISSING=$((ENV_MISSING + 1))
    fi
  done

  # Toolchain parity, read the way a login shell sees it.
  for pair in "node:node --version" "python3:python3 --version" "uv:uv --version"; do
    tool="${pair%%:*}"
    cmd="${pair#*:}"
    L=$(eval "$cmd" 2>/dev/null || echo missing)
    R=$(rssh "bash -lc '$cmd'" 2>/dev/null || echo missing)
    [ "$L" = "$R" ] && ok "$tool parity ($L)" || bad "$tool drift — M1 '$L' vs M2 '$R'"
  done

  if rssh "test -x '$REPO/node_modules/.bin/playwright'" 2>/dev/null; then
    if rssh "ls ~/.cache/ms-playwright 2>/dev/null | grep -q headless_shell" 2>/dev/null; then
      ok "playwright headless shell installed on M2"
    else
      bad "playwright present but no headless shell (setup-m2.sh installs it)"
    fi
  else
    echo "  [info] no playwright in node_modules yet; the headless shell check starts at E1"
  fi
else
  gone "skipped — M2 unreachable"
fi

# --- 3. sync --------------------------------------------------------------
echo
echo "sync"
if command -v "$MUTAGEN" >/dev/null 2>&1; then
  ok "mutagen installed on M1"
  if "$MUTAGEN" sync list "$SYNC" >/dev/null 2>&1; then
    LIST=$("$MUTAGEN" sync list "$SYNC" 2>/dev/null)
    ST=$(grep -iE '^Status:' <<<"$LIST" | head -1 | sed 's/^Status:[[:space:]]*//')
    case "$ST" in
      *"Watching for changes"*) ok "sync '$SYNC' watching" ;;
      *) bad "sync '$SYNC' status: ${ST:-unknown}" ;;
    esac
    CF=$(grep -ci 'conflict' <<<"$LIST" || true)
    [ "${CF:-0}" -eq 0 ] && ok "no sync conflicts" || bad "$CF sync conflict line(s) — resolve first"
  else
    gone "no mutagen session named '$SYNC'"
  fi
else
  gone "mutagen not installed on M1"
fi

# --- 4. wrapper -----------------------------------------------------------
echo
echo "wrapper"
[ -x "$WRAPPER" ] && ok "wrapper present and executable" || gone "wrapper missing at $WRAPPER"
echo "  [info] REMOTE_SHELL_MODE=${REMOTE_SHELL_MODE:-remote (default)}"

# --- 5. THE PROOF ---------------------------------------------------------
# Every check above can pass while commands quietly still run on M1. Verify by hostname, never by inference. The
# wrapper's mode is forced to remote for these probes, whatever the caller exported.
echo
echo "redirect proof"
if [ "$M2_UP" = 1 ] && [ -x "$WRAPPER" ]; then
  M1H=$(hostname)
  VIA=$(cd "$REPO" && REMOTE_SHELL_MODE=remote "$WRAPPER" -c 'hostname' 2>/dev/null | tail -1)
  if [ -n "$VIA" ] && [ "$VIA" != "$M1H" ]; then
    ok "commands land on M2 — wrapper returned '$VIA', M1 is '$M1H'"
  else
    bad "wrapper returned '$VIA' but M1 is '$M1H' — commands are NOT landing on the M2"
  fi
  # The dispatch is a NON-login `ssh host "cd …; cmd"`. If the M2's ~/.bashrc returns early for non-interactive
  # shells before nvm loads, node and npx are missing exactly where the wrapper runs them, while the login-shell
  # parity check above still passes (CF-2 9).
  NV=$(cd "$REPO" && REMOTE_SHELL_MODE=remote "$WRAPPER" -c 'command -v npx >/dev/null && node --version' 2>/dev/null \
    | tail -1)
  [ "$NV" = "$NODE_WANT" ] && ok "dispatch shell resolves npx and node $NV" \
    || bad "dispatch shell node is '${NV:-missing}', want $NODE_WANT — load nvm above the M2's interactive guard"
else
  gone "skipped — needs M2 up and the wrapper present"
fi

# --- verdict --------------------------------------------------------------
# UNBOOTSTRAPPED is decided from the M2 itself (down, or its env never built), not from a count of misses, which
# shifts every time a check is added or removed (fix 10).
echo
echo "----------------------------------------------------------------"
printf 'pass=%s  fail=%s  missing=%s\n' "$PASS" "$FAIL" "$MISSING"
if [ "$M2_UP" = 0 ] || [ "$ENV_MISSING" -gt 0 ]; then
  echo "STATE=UNBOOTSTRAPPED"
  exit 10
elif [ "$FAIL" -gt 0 ] || [ "$MISSING" -gt 0 ]; then
  echo "STATE=PARTIAL"
  exit 20
else
  echo "STATE=READY"
  exit 0
fi
