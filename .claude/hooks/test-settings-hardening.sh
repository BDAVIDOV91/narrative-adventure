#!/bin/sh
# Guards the agent-config hardening applied after the 2026-09-09 AgentShield audit.
# See docs/security/agent-config-audit.md for why each assertion exists.
#
# The assertions target .claude/settings.json, which is tracked, so a fresh clone
# inherits the hardening. .claude/settings.local.json is gitignored but takes
# precedence at runtime, so it is checked only for overrides that would undo it.
#
# Run: sh .claude/hooks/test-settings-hardening.sh

set -u

ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/../.." && pwd)"
SHARED="$ROOT/.claude/settings.json"
LOCAL="$ROOT/.claude/settings.local.json"
MCP="$ROOT/.mcp.json"

FAILURES=0

fail() {
  echo "FAIL: $1"
  FAILURES=$((FAILURES + 1))
}

pass() {
  echo "ok: $1"
}

# --- MCP servers are not auto-approved --------------------------------------
# enableAllProjectMcpServers:true approves any server .mcp.json declares, with no
# human review step. A branch or clone could then introduce a server that runs on
# session start.
if [ ! -f "$SHARED" ]; then
  fail "settings.json not found at $SHARED"
elif python3 -c "
import json, sys
with open('$SHARED') as fh:
    cfg = json.load(fh)
sys.exit(0 if cfg.get('enableAllProjectMcpServers') is False else 1)
"; then
  pass "settings.json disables project MCP auto-approval"
else
  fail "settings.json does not set enableAllProjectMcpServers to false"
fi

# --- the deny list is present and non-empty ---------------------------------
# An empty deny list leaves the allow list as the only control, and the allow list
# permits Bash(npx:*), which executes arbitrary remote packages. Denials belong in
# the tracked file so they are reviewable and survive a clone.
if [ -f "$SHARED" ]; then
  if python3 -c "
import json, sys
with open('$SHARED') as fh:
    cfg = json.load(fh)
deny = cfg.get('permissions', {}).get('deny', [])
sys.exit(0 if len(deny) > 0 else 1)
"; then
    pass "settings.json carries a non-empty deny list"
  else
    fail "settings.json has no non-empty permissions.deny"
  fi

  # Rule 7 is enforced by block-dangerous-git.sh; the deny entry is the second layer.
  if grep -q 'Bash(git push' "$SHARED"; then
    pass "deny list blocks git push (rule 7)"
  else
    fail "deny list does not block git push"
  fi
fi

# --- the local override does not undo the hardening -------------------------
# settings.local.json is gitignored and takes precedence at runtime, so it can
# silently re-enable what the tracked file disables. Absence is fine.
if [ ! -f "$LOCAL" ]; then
  pass "no settings.local.json override present"
elif python3 -c "
import json, sys
with open('$LOCAL') as fh:
    cfg = json.load(fh)
sys.exit(0 if cfg.get('enableAllProjectMcpServers') is True else 1)
"; then
  fail "settings.local.json re-enables enableAllProjectMcpServers and overrides settings.json"
else
  pass "settings.local.json does not re-enable MCP auto-approval"
fi

# --- MCP servers are pinned to exact versions -------------------------------
# @latest resolves an unreviewed version on every start. ADR 0004 pins npm
# dependencies exactly; servers that execute locally are held to the same bar.
if [ ! -f "$MCP" ]; then
  fail ".mcp.json not found at $MCP"
elif grep -q '@latest' "$MCP"; then
  fail ".mcp.json pins a server to @latest — use an exact version"
else
  pass "no @latest in .mcp.json"
fi

# --- file permissions (advisory, never fails) -------------------------------
# CLAUDE.md is injected into every prompt as system instructions, and the hooks
# execute on every Bash tool call. Group-writable versions of either are an
# injection surface for any other account in the owner's group.
#
# This is advisory, not an assertion: git records only the executable bit, so a
# fresh clone always materialises these at the umask default. Failing here would
# make the suite red on every clone for something git cannot carry. See
# docs/security/agent-config-audit.md for the command that reapplies them.
LOOSE=""
for f in "$ROOT/CLAUDE.md" "$ROOT/.mcp.json" "$SHARED" "$LOCAL"; do
  [ -f "$f" ] || continue
  case "$(stat -c '%a' "$f" 2>/dev/null)" in
    600 | 400) ;;
    *) LOOSE="$LOOSE $(basename "$f")" ;;
  esac
done
for f in "$ROOT"/.claude/hooks/*.sh "$ROOT"/.husky/pre-commit "$ROOT"/.husky/pre-push; do
  [ -f "$f" ] || continue
  case "$(stat -c '%a' "$f" 2>/dev/null)" in
    700 | 500) ;;
    *) LOOSE="$LOOSE $(basename "$f")" ;;
  esac
done

if [ -n "$LOOSE" ]; then
  echo "note: group- or world-accessible (advisory, not a failure):$LOOSE"
  echo "      reapply: see docs/security/agent-config-audit.md"
else
  pass "config and hook file permissions are owner-only"
fi

echo
if [ "$FAILURES" -eq 0 ]; then
  echo "settings hardening: all checks passed"
  exit 0
fi
echo "settings hardening: $FAILURES check(s) failed"
exit 1
