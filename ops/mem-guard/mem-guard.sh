#!/usr/bin/env bash
# mem-guard.sh [--] <cmd...>: run <cmd> only if M1 has enough free memory for it.
#
# Why: M1 has ~1.9 GB free on an integrated APU, and a heavy run (vitest, pytest, a build, the dev server, a 3D
# check) that pushes it into swap or the OOM killer takes the whole machine down (CLAUDE.md rule 9). The guard reads
# MemAvailable, the kernel's own estimate of what can be allocated without swapping, and refuses below a floor.
#
# Floor: MEM_GUARD_MIN_MB, default 1536. PROVISIONAL (owner, 2026-10-01): re-tuned at E1 entry from the measured M1
# peak RSS plus a margin. A refusal exits 75 (EX_TEMPFAIL: try again later) and prints the measured value and the
# override. It fails closed: an unreadable meminfo, a missing MemAvailable line or a non-integer floor all refuse.
# At or above the floor it `exec`s the command, so the command's own exit code is the guard's exit code.
#
# Test seam: MEM_GUARD_MEMINFO (default /proc/meminfo). Test: ops/mem-guard/test-mem-guard.sh
set -uo pipefail

if [ "${1:-}" = "--" ]; then shift; fi
if [ "$#" -eq 0 ]; then
  echo "usage: mem-guard.sh [--] <cmd...>   (floor: MEM_GUARD_MIN_MB, default 1536)" >&2
  exit 2
fi

refuse() {
  echo "[mem-guard] REFUSED: $1" >&2
  echo "[mem-guard] override for one run: MEM_GUARD_MIN_MB=<MB> (prefix it to the command)" >&2
  exit 75
}

# `-` not `:-`: an EMPTY floor is a mistake to refuse, not a request for the default.
FLOOR_MB="${MEM_GUARD_MIN_MB-1536}"
case "$FLOOR_MB" in
  '' | *[!0-9]*) refuse "floor MEM_GUARD_MIN_MB='$FLOOR_MB' is not a whole number of MB" ;;
esac

MEMINFO="${MEM_GUARD_MEMINFO:-/proc/meminfo}"
[ -r "$MEMINFO" ] || refuse "cannot read $MEMINFO"
AVAIL_KB=$(awk '$1 == "MemAvailable:" { print $2; exit }' "$MEMINFO")
case "$AVAIL_KB" in
  '' | *[!0-9]*) refuse "no MemAvailable line in $MEMINFO" ;;
esac

# Compare in kB: rounding MemAvailable down to MB first would refuse a machine sitting exactly on the floor.
FLOOR_KB=$((10#$FLOOR_MB * 1024))
if [ "$AVAIL_KB" -lt "$FLOOR_KB" ]; then
  refuse "MemAvailable=$((AVAIL_KB / 1024)) MB < floor $FLOOR_MB MB"
fi

exec "$@"
