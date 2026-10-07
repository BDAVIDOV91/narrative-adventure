#!/usr/bin/env bash
# setup-m2.sh — bootstrap the M2 as the execution target for this repo.
#
# RUN ON THE M2:  cd ~/narrative-adventure && ./ops/remote-shell/setup-m2.sh
# Prereq:         the mutagen session `narrative-adventure` exists and has finished its first pass.
#
# Rebuilds what the sync deliberately excludes (venv, node_modules, the de440s ephemeris). Ported from pdfx; the
# sandbox .env generation and its leak guard are gone, because this repo has no credentials.
# Deliberately NOT pinned in remote-shell.sh: from a claude-m2 session it is routed to the M2, where it belongs.

# --- 0. refuse on M1 (FIRST, before anything can run) ------------------------------------------------------
# On M1 the path and user checks below both pass, so without this a stray run would `uv venv` and `npm ci` over
# M1's own venv and node_modules. M1 is the machine with the mutagen CLI and the ssh alias to the M2; the M2 carries
# only the mutagen agent and has no alias to itself. Test: ops/remote-shell/test-pin-list.sh (stubs only).
if command -v mutagen >/dev/null 2>&1 || grep -qE '^Host[[:space:]]+m2([[:space:]]|$)' "$HOME/.ssh/config" 2>/dev/null; then
  echo "setup-m2.sh: REFUSED: this looks like M1 (a mutagen CLI or a 'Host m2' ssh alias is present)." >&2
  echo "setup-m2.sh: run it on the M2. From a claude-m2 session the wrapper routes it there." >&2
  exit 3
fi

set -euo pipefail

REPO="/home/technojihad/narrative-adventure"
# 2026-10-07: routed through the wrapper, this runs in a NON-login ssh shell, whose PATH lacks ~/.local/bin, where
# the uv installer puts uv. It died "uv missing" on an M2 that had uv. Test: test-pin-list.sh.
export PATH="$HOME/.local/bin:$PATH"

say() { printf '\n=== %s\n' "$*"; }
die() {
  printf '\nFATAL: %s\n' "$*" >&2
  exit 1
}

# --- 1. path parity -----------------------------------------------------------------------------------------
# The wrapper's whole translation scheme is "the same path on both machines".
say "Checking path parity"
[ "$PWD" = "$REPO" ] || die "Must run from $REPO (currently $PWD)."
[ "$(whoami)" = "technojihad" ] || die "User must be 'technojihad', got '$(whoami)'."
echo "ok: $REPO as $(whoami)"

# --- 2. toolchain parity with M1 (2026-10-01) --------------------------------------------------------------
# A version mismatch produces test failures that read as code defects.
say "Checking toolchain parity"
check() {
  local name="$1" want="$2" got="$3"
  if [ "$got" = "$want" ]; then echo "ok:   $name $got"; else echo "WARN: $name is '$got', M1 has '$want'"; fi
}
check node "v22.17.0" "$(node --version 2>/dev/null || echo missing)"
check npm "11.14.1" "$(npm --version 2>/dev/null || echo missing)"
check python "Python 3.12.3" "$(python3 --version 2>/dev/null || echo missing)"
check uv "uv 0.8.0" "$(uv --version 2>/dev/null || echo missing)"
command -v uv >/dev/null 2>&1 \
  || die "uv missing — install uv 0.8.0 (curl -LsSf https://astral.sh/uv/0.8.0/install.sh | sh), then re-run."
command -v npm >/dev/null 2>&1 || die "npm missing — install node v22.17.0 (nvm install 22.17.0), then re-run."

# --- 3. rebuild what the sync excludes ----------------------------------------------------------------------
say "Rebuilding venv (excluded from sync)"
[ -d venv ] || uv venv venv
VIRTUAL_ENV="$REPO/venv" uv pip install -r requirements.txt

say "Installing node_modules (excluded from sync)"
npm ci

# --- 4. the de440s ephemeris --------------------------------------------------------------------------------
# The same loader data/scripts/orbital-positions.py uses (_load_ephemeris). The generator itself is NOT run: its
# output is committed, and it is regenerated on purpose, never as a side effect of setup.
say "Fetching de440s into data/ephemeris/ (one-time, ~32 MB)"
mkdir -p data/ephemeris
if [ -f data/ephemeris/de440s.bsp ]; then
  echo "ok:   de440s already present"
else
  ./venv/bin/python -c "from skyfield.api import Loader; Loader('data/ephemeris')('de440s.bsp')"
fi

# --- 5. the Playwright headless shell (from E1) ------------------------------------------------------------
# Only once @playwright/test is a pinned dependency (E1). Fetching it before then would be an unpinned download
# (ADR 0004).
if [ -x node_modules/.bin/playwright ]; then
  say "Installing the Playwright headless shell"
  npx playwright install --only-shell chromium
else
  say "Playwright headless shell: deferred to E1 (no @playwright/test in node_modules yet)"
fi

say "M2 ready"
cat <<'NEXT'
Next, from M1 (never infer the redirect, prove it):
  ops/remote-shell/preflight.sh          # expect STATE=READY
NEXT
