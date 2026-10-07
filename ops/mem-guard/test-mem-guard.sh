#!/usr/bin/env bash
# Regression test for ops/mem-guard/mem-guard.sh (M2 offload plan, step 1).
# Offline and instant: every case reads a fixture meminfo file through the MEM_GUARD_MEMINFO seam.
[ -n "${BASH_VERSION:-}" ] || { echo "test-mem-guard.sh: run with bash" >&2; exit 1; }
set -uo pipefail
# A claude-m2 session exports these; an inherited value would leak into the cases.
unset REMOTE_SHELL_MODE REMOTE_SHELL_HOST REMOTE_SHELL_SYNC REMOTE_SHELL_LOG MEM_GUARD_MIN_MB MEM_GUARD_MEMINFO

GUARD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/mem-guard.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
PASS=0
FAIL=0

ok() { PASS=$((PASS + 1)); echo "  ok   $1"; }
bad() { FAIL=$((FAIL + 1)); echo "  FAIL $1"; }

# meminfo <file> <MemAvailable kB>: a fixture with the real file's neighbouring lines.
meminfo() {
  printf 'MemTotal:        7864320 kB\nMemFree:          204800 kB\nMemAvailable:    %s kB\nBuffers:           51200 kB\n' \
    "$2" >"$1"
}

LOW="$TMP/low"
meminfo "$LOW" 1048576 # 1024 MB
HIGH="$TMP/high"
meminfo "$HIGH" 3145728 # 3072 MB
EXACT="$TMP/exact"
meminfo "$EXACT" $((1536 * 1024))
NOLINE="$TMP/noline"
printf 'MemTotal:        7864320 kB\nMemFree:          204800 kB\n' >"$NOLINE"

echo "mem-guard:"

# 1. Below the floor: refuses with 75, and the command never runs.
M="$TMP/m1"
out=$(MEM_GUARD_MEMINFO="$LOW" bash "$GUARD" -- touch "$M" 2>&1)
rc=$?
if [ "$rc" = 75 ] && [ ! -e "$M" ] && grep -q 'REFUSED: MemAvailable=1024 MB < floor 1536 MB' <<<"$out" \
  && grep -q 'MEM_GUARD_MIN_MB' <<<"$out"; then
  ok "below the floor refuses (75), names the measured value and the override"
else bad "below the floor: rc=$rc out=$out"; fi

# 2. Above the floor: runs, and the exit code passes through.
MEM_GUARD_MEMINFO="$HIGH" bash "$GUARD" -- bash -c 'exit 3' >/dev/null 2>&1
rc=$?
if [ "$rc" = 3 ]; then ok "above the floor runs; exit code 3 survives"; else bad "exit passthrough: rc=$rc"; fi

# 3. Exactly at the floor runs (the comparison is in kB, with no MB rounding).
M="$TMP/m3"
MEM_GUARD_MEMINFO="$EXACT" bash "$GUARD" -- touch "$M" >/dev/null 2>&1
if [ -e "$M" ]; then ok "exactly at the floor runs"; else bad "exactly at the floor refused"; fi

# 4. One kB under the floor refuses.
ONEUNDER="$TMP/oneunder"
meminfo "$ONEUNDER" $((1536 * 1024 - 1))
M="$TMP/m4"
MEM_GUARD_MEMINFO="$ONEUNDER" bash "$GUARD" -- touch "$M" >/dev/null 2>&1
rc=$?
if [ "$rc" = 75 ] && [ ! -e "$M" ]; then ok "one kB under the floor refuses"; else bad "one kB under: rc=$rc"; fi

# 5. MEM_GUARD_MIN_MB overrides the floor.
M="$TMP/m5"
MEM_GUARD_MEMINFO="$LOW" MEM_GUARD_MIN_MB=512 bash "$GUARD" -- touch "$M" >/dev/null 2>&1
if [ -e "$M" ]; then ok "MEM_GUARD_MIN_MB=512 lets a 1024 MB machine run"; else bad "override ignored"; fi

# 6. A missing MemAvailable line refuses (fail closed).
M="$TMP/m6"
out=$(MEM_GUARD_MEMINFO="$NOLINE" bash "$GUARD" -- touch "$M" 2>&1)
rc=$?
if [ "$rc" = 75 ] && [ ! -e "$M" ]; then ok "missing MemAvailable refuses"; else bad "missing line: rc=$rc out=$out"; fi

# 7. An unreadable meminfo refuses.
M="$TMP/m7"
MEM_GUARD_MEMINFO="$TMP/does-not-exist" bash "$GUARD" -- touch "$M" >/dev/null 2>&1
rc=$?
if [ "$rc" = 75 ] && [ ! -e "$M" ]; then ok "unreadable meminfo refuses"; else bad "unreadable: rc=$rc"; fi

# 8. A garbage floor refuses.
for floor in abc 1.5 -1 ''; do
  M="$TMP/m8"
  rm -f "$M"
  MEM_GUARD_MEMINFO="$HIGH" MEM_GUARD_MIN_MB="$floor" bash "$GUARD" -- touch "$M" >/dev/null 2>&1
  rc=$?
  if [ "$rc" = 75 ] && [ ! -e "$M" ]; then ok "floor '$floor' refuses"; else bad "floor '$floor': rc=$rc"; fi
done

# 9. No command: usage, exit 2.
MEM_GUARD_MEMINFO="$HIGH" bash "$GUARD" >/dev/null 2>&1
rc1=$?
MEM_GUARD_MEMINFO="$HIGH" bash "$GUARD" -- >/dev/null 2>&1
rc2=$?
if [ "$rc1" = 2 ] && [ "$rc2" = 2 ]; then ok "no command exits 2"; else bad "no command: rc=$rc1/$rc2"; fi

# 10. An argument with spaces survives, and the leading -- is optional.
M="$TMP/with space"
MEM_GUARD_MEMINFO="$HIGH" bash "$GUARD" -- touch "$M" >/dev/null 2>&1
M2="$TMP/no dashes"
MEM_GUARD_MEMINFO="$HIGH" bash "$GUARD" touch "$M2" >/dev/null 2>&1
if [ -e "$M" ] && [ -e "$M2" ]; then ok "arguments with spaces survive; -- optional"; else bad "argv re-split"; fi

echo "mem-guard: $PASS passed, $FAIL failed"
[ "$FAIL" = 0 ]
