#!/usr/bin/env bash
# Regression test for ops/remote-shell/remote-shell.sh: the PIN LIST, the HEAVY auto-guard and the fail-closed paths.
# Ported from pdfx (ops/remote-shell/test-pin-list.sh) for the M2 offload phase, plan
# docs/handoffs/2026-10-01-m2-offload-plan.md step 2.
#
# Two kinds of case:
#   * explain cases: REMOTE_SHELL_MODE=explain prints PIN, PIN+GUARD or REMOTE and exits without running anything.
#   * executed cases: the wrapper really runs, but every command is the neutral form `: <cmd>; touch "$MARK"`, and
#     ssh/mutagen are stubs on the REMOTE_SHELL_SSH / REMOTE_SHELL_MUTAGEN seams. Nothing leaves the machine and no
#     real git, npm or vitest runs, even if the wrapper regresses (this file runs inside husky's ops branch).
[ -n "${BASH_VERSION:-}" ] || { echo "test-pin-list.sh: run with bash" >&2; exit 1; }
set -uo pipefail
# A claude-m2 session exports these; an inherited value would leak into the cases.
unset REMOTE_SHELL_MODE REMOTE_SHELL_HOST REMOTE_SHELL_SYNC REMOTE_SHELL_LOG MEM_GUARD_MIN_MB MEM_GUARD_MEMINFO
unset REMOTE_SHELL_SSH REMOTE_SHELL_MUTAGEN CLAUDE_M2_PREFLIGHT

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
W="$HERE/remote-shell.sh"
REPO="$(cd "$HERE/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
pass=0
fail=0
ok() { printf '  ok    %s\n' "$1"; pass=$((pass + 1)); }
bad() { printf '  FAIL  %s\n' "$1"; fail=$((fail + 1)); }

# check <PIN|PIN+GUARD|REMOTE> <description> <command>. STRICT: the output must be exactly the token and rc 0, so a
# wrapper that crashes cannot pass a REMOTE expectation (fix 8).
check() {
  local expect="$1" desc="$2" cmd="$3" out rc
  out=$(REMOTE_SHELL_MODE=explain timeout 10 "$W" -c -l "$cmd" 2>&1)
  rc=$?
  if [ "$rc" = 0 ] && [ "$out" = "$expect" ]; then
    ok "$desc ($expect)"
  else
    bad "$desc: expected=$expect got='$out' rc=$rc"
  fi
}

# --- stubs and fixtures ------------------------------------------------------------------------------------------
STUB="$TMP/stub"
mkdir -p "$STUB"
SSH_LOG="$TMP/ssh.log"
# Stub ssh: `ssh ... host true` answers reachability with $STUB_SSH_RC; any other call is LOGGED, never eval-ed.
cat >"$STUB/ssh" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >>"$SSH_LOG"
last="${!#}"
if [ "$last" = true ]; then exit "${STUB_SSH_RC:-0}"; fi
exit 0
EOF
# Stub mutagen: `sync flush` exits $STUB_FLUSH_RC.
cat >"$STUB/mutagen" <<'EOF'
#!/usr/bin/env bash
exit "${STUB_FLUSH_RC:-0}"
EOF
chmod +x "$STUB/ssh" "$STUB/mutagen"
export SSH_LOG

LOW="$TMP/meminfo-low"
printf 'MemTotal: 7864320 kB\nMemAvailable: 1048576 kB\n' >"$LOW"

# run <expect-rc> <expect-marker: yes|no> <description> [env...] -- <command>. Runs from $REPO unless RUN_CWD is set.
run() {
  local erc="$1" emark="$2" desc="$3"
  shift 3
  local envs=()
  while [ "$1" != "--" ]; do envs+=("$1"); shift; done
  shift
  local cmd="$1" rc got
  rm -f "$TMP/mark"
  # Seams first, the case's own env after: `env` lets a later assignment win, so a case can override a stub.
  (cd "${RUN_CWD:-$REPO}" && env REMOTE_SHELL_SSH="$STUB/ssh" REMOTE_SHELL_MUTAGEN="$STUB/mutagen" "${envs[@]}" \
    REMOTE_SHELL_LOG="$TMP/argv.log" timeout 10 "$W" -c -l "$cmd" >/dev/null 2>"$TMP/err")
  rc=$?
  got=no
  [ -e "$TMP/mark" ] && got=yes
  if [ "$rc" = "$erc" ] && [ "$got" = "$emark" ]; then
    ok "$desc (rc=$rc marker=$got)"
  else
    bad "$desc: expected rc=$erc marker=$emark, got rc=$rc marker=$got; stderr: $(tr '\n' ' ' <"$TMP/err")"
  fi
}
M="touch '$TMP/mark'"

echo "PIN LIST (explain)"
check PIN "bare git" 'git status'
check PIN "git behind a double quote" 'bash -c "git diff"'
check PIN "git behind -C" 'git -C /home/technojihad/narrative-adventure log --oneline -3'
check PIN "git add -A" 'git add -A'
check PIN "git commit (husky guards its own heavy lines)" 'git commit -m "docs: x"'
check PIN "git commit message naming pytest" 'git commit -m "test: pytest covers it"'
check PIN "git add of vitest.config.ts" 'git add vitest.config.ts'
check PIN "git log --grep=pytest" 'git log --grep=pytest'
check REMOTE "github.com is not git" 'curl -sI https://github.com'
check PIN "free -h" 'free -h'
check PIN "/proc/meminfo" 'cat /proc/meminfo'
check PIN "free behind a quote" 'bash -c "free -m"'
check PIN "snapshot CREATION" 'SNAPSHOT_FILE=/home/technojihad/.claude/shell-snapshots/a.sh; echo x'
check REMOTE "snapshot-source prefix stays remote" \
  'source /home/technojihad/.claude/shell-snapshots/snapshot-bash-1-x.sh 2>/dev/null || true && echo hi'
check PIN ".claude/projects/" 'cat ~/.claude/projects/-home-technojihad-narrative-adventure/memory/MEMORY.md'
check PIN "hook test (sh)" 'sh .claude/hooks/test-block-dangerous-git.sh'
check PIN "hook test, no git in its name" 'bash .claude/hooks/test-wayfinder-frontier.sh'
check PIN "husky hook test" 'sh .husky/test-pre-commit-scope.sh'
check REMOTE "a hook itself stays remote" 'bash .claude/hooks/wayfinder-frontier.sh'
check PIN "viewer test" 'node --test ops/wayfinder-viewer/wayfinder-view.test.mjs'
check PIN "third-party viewer" 'node ~/tools/wayfinder-viewer/server.js'
check REMOTE "the maps stay remote" 'ls docs/wayfinder'
check PIN "npm run test:ops (node --test, no guard)" 'npm run test:ops'
check PIN "npm run wayfinder" 'npm run wayfinder'
check PIN "preflight (relative)" 'ops/remote-shell/preflight.sh'
check PIN "preflight (absolute)" '/home/technojihad/narrative-adventure/ops/remote-shell/preflight.sh; echo "exit=$?"'
check PIN "preflight behind a quote" 'bash -c "./ops/remote-shell/preflight.sh"'
check PIN "the pin test itself" 'bash ops/remote-shell/test-pin-list.sh'
check PIN "launcher" './ops/remote-shell/claude-m2.sh'
check PIN "mutagen" 'mutagen sync list'
check REMOTE "setup-m2.sh stays remote (characterization)" 'bash ops/remote-shell/setup-m2.sh'
check PIN "wrapper to the M2: exempt from HEAVY" \
  "REMOTE_SHELL_MODE=remote ops/remote-shell/remote-shell.sh -c 'hostname; npx vitest run'"
check REMOTE "playwright runs on the M2 (flipped from pdfx)" 'npx playwright test'

echo "HEAVY auto-guard (explain)"
check PIN+GUARD "npm run dev" 'npm run dev'
check PIN+GUARD "npm run dev with args" 'npm run dev -- --port 5174'
check PIN+GUARD "npm run dev behind a quote" 'bash -c "npm run dev"'
check REMOTE "npm run dev:x does not over-match" 'npm run dev:x'
check REMOTE "npm run dev-x does not over-match" 'npm run dev-x'
check PIN+GUARD "the guard wrapping npm test" 'ops/mem-guard/mem-guard.sh -- npm test'
check PIN "the guard's own test is not guarded" 'bash ops/mem-guard/test-mem-guard.sh'
check PIN+GUARD "git add && npm test" 'git add -A && npm test'
check PIN+GUARD "free && vitest" 'free -h && npx vitest run'
check PIN+GUARD "git status; npm run build" 'git status; npm run build'
check PIN+GUARD "git; pytest" 'git status && venv/bin/python -m pytest'
check PIN+GUARD "git; a generator" 'git status && venv/bin/python data/scripts/orbital-positions.py'
check PIN+GUARD "git; lint" 'git diff && npm run lint'

echo "REMOTE"
check REMOTE "npm test" 'npm test'
check REMOTE "npx vitest run" 'npx vitest run'
check REMOTE "pytest" 'venv/bin/python -m pytest'
check REMOTE "npm run build" 'npm run build'
check REMOTE "echo" 'echo hello'

echo "Fail closed (executed, stubs only)"
run 127 no "unknown mode, pinned command" REMOTE_SHELL_MODE=bogus -- ": git status; $M"
run 127 no "unknown mode, unpinned command" REMOTE_SHELL_MODE=bogus -- ": echo; $M"
run 127 no "mode unset + M2 unreachable" STUB_SSH_RC=255 -- ": echo; $M"
run 127 no "remote + mutagen missing (characterization)" REMOTE_SHELL_MODE=remote \
  REMOTE_SHELL_MUTAGEN=/nonexistent/mutagen -- ": echo; $M"
run 127 no "remote + flush fails (characterization)" REMOTE_SHELL_MODE=remote STUB_FLUSH_RC=1 -- ": echo; $M"
for c in '' '-l' '-o'; do
  rm -f "$TMP/mark"
  (cd "$REPO" && env STUB_SSH_RC=255 REMOTE_SHELL_SSH="$STUB/ssh" REMOTE_SHELL_MUTAGEN="$STUB/mutagen" \
    timeout 10 "$W" -c $c >/dev/null 2>&1)
  rc=$?
  if [ "$rc" = 127 ]; then ok "empty/flags-only invocation '-c $c' refuses (127)"; else bad "'-c $c': rc=$rc"; fi
done

: >"$SSH_LOG"
run 0 no "remote reachable: dispatched, not run locally" REMOTE_SHELL_MODE=remote -- ": echo; $M"
if grep -q "REMOTE CWD MISSING ON M2" "$SSH_LOG" && ! grep -q "|| cd '" "$SSH_LOG"; then
  ok "dispatch fails loud on a missing remote cwd (no \$REPO fallback)"
else
  bad "dispatch line: $(tail -1 "$SSH_LOG")"
fi

: >"$SSH_LOG"
RUN_CWD="$TMP" run 127 no "cwd outside the repo refuses" REMOTE_SHELL_MODE=remote -- ": echo; $M"
if [ ! -s "$SSH_LOG" ]; then ok "outside the repo, ssh is never called"; else bad "ssh called from outside the repo"; fi

echo "Pins and the guard (executed)"
run 0 yes "a pin runs locally with the M2 down" STUB_SSH_RC=255 -- ": git status; $M"
run 75 no "pinned HEAVY under the floor refuses" MEM_GUARD_MEMINFO="$LOW" -- ": git add -A && : npm test; $M"
run 75 no "pinned dev under the floor refuses (never starts Vite)" MEM_GUARD_MEMINFO="$LOW" -- ": npm run dev; $M"
run 0 yes "MEM_GUARD_MIN_MB prefix overrides the floor" MEM_GUARD_MEMINFO="$LOW" -- \
  "MEM_GUARD_MIN_MB=1 : npm run dev; $M"
run 75 no "local mode guards an unpinned HEAVY command" REMOTE_SHELL_MODE=local MEM_GUARD_MEMINFO="$LOW" -- \
  ": npx vitest run; $M"
run 0 yes "local mode runs a light command" REMOTE_SHELL_MODE=local MEM_GUARD_MEMINFO="$LOW" -- ": echo; $M"

echo "setup-m2.sh refuses on M1 (stubs only, never a real install)"
# Every toolchain binary setup could call is a stub that only touches a marker, and the cwd is a mktemp dir, so a
# regression cannot run `npm ci` or `uv venv` against this checkout (CF-2 2).
TOOLS="$TMP/tools"
mkdir -p "$TOOLS" "$TMP/home-m1/.ssh" "$TMP/home-plain"
for t in uv npm npx node python3 pip; do
  printf '#!/bin/sh\ntouch "%s/called-%s"\n' "$TMP" "$t" >"$TOOLS/$t"
  chmod +x "$TOOLS/$t"
done
printf 'Host m2\n  HostName 100.64.0.1\n' >"$TMP/home-m1/.ssh/config"
NOMUT="$TMP/nomutagen"
mkdir -p "$NOMUT"
setup_case() { # setup_case <description> <HOME> <PATH>
  local desc="$1" home="$2" path="$3" rc called
  rm -f "$TMP"/called-*
  (cd "$TMP" && env HOME="$home" PATH="$path" timeout 10 /bin/bash "$HERE/setup-m2.sh" >"$TMP/out" 2>&1)
  rc=$?
  called=$(ls "$TMP"/called-* 2>/dev/null | wc -l)
  if [ "$rc" != 0 ] && [ "$called" = 0 ] && grep -q 'REFUSED: this looks like M1' "$TMP/out"; then
    ok "$desc (rc=$rc, no tool called)"
  else
    bad "$desc: rc=$rc tools_called=$called out=$(head -3 "$TMP/out" | tr '\n' ' ')"
  fi
}
setup_case "an ssh alias 'Host m2' means M1" "$TMP/home-m1" "$TOOLS:/usr/bin:/bin"
cp "$STUB/mutagen" "$NOMUT/mutagen"
setup_case "a mutagen CLI on PATH means M1" "$TMP/home-plain" "$TOOLS:$NOMUT:/usr/bin:/bin"

echo "preflight and launcher (stubs only)"
out=$(env REMOTE_SHELL_SSH="$STUB/ssh" REMOTE_SHELL_MUTAGEN="$STUB/mutagen" STUB_SSH_RC=255 \
  timeout 20 "$HERE/preflight.sh" 2>&1)
rc=$?
if [ "$rc" = 10 ] && [ "$(tail -1 <<<"$out")" = "STATE=UNBOOTSTRAPPED" ]; then
  ok "preflight: M2 unreachable -> STATE=UNBOOTSTRAPPED, exit 10"
else
  bad "preflight unreachable: rc=$rc last='$(tail -1 <<<"$out")'"
fi

CL="$TMP/claude-bin"
mkdir -p "$CL"
printf '#!/bin/sh\nprintf "%%s\\n" "$*" >"%s/claude-args"\n' "$TMP" >"$CL/claude"
chmod +x "$CL/claude"
for code in 10 20 33; do
  printf '#!/bin/sh\necho STATE=STUB\nexit %s\n' "$code" >"$TMP/fake-preflight"
  chmod +x "$TMP/fake-preflight"
  rm -f "$TMP/claude-args"
  env PATH="$CL:$PATH" CLAUDE_M2_PREFLIGHT="$TMP/fake-preflight" timeout 10 "$HERE/claude-m2.sh" >/dev/null 2>&1
  rc=$?
  if [ "$rc" = "$code" ] && [ ! -e "$TMP/claude-args" ]; then
    ok "launcher refuses on preflight exit $code (rc=$rc, claude never started)"
  else
    bad "launcher on preflight $code: rc=$rc claude_started=$([ -e "$TMP/claude-args" ] && echo yes || echo no)"
  fi
done
printf '#!/bin/sh\necho STATE=READY\nexit 0\n' >"$TMP/fake-preflight"
rm -f "$TMP/claude-args"
env PATH="$CL:$PATH" CLAUDE_M2_PREFLIGHT="$TMP/fake-preflight" timeout 10 "$HERE/claude-m2.sh" --probe --resume x \
  >/dev/null 2>&1
if [ -e "$TMP/claude-args" ] && [ "$(cat "$TMP/claude-args")" = "--resume x" ]; then
  ok "launcher strips its own --probe before exec claude"
else
  bad "launcher passed to claude: '$(cat "$TMP/claude-args" 2>/dev/null)'"
fi

echo "  ----"
printf '  pass=%s fail=%s\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
