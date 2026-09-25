#!/usr/bin/env bash
# PreToolUse(Bash): on `git commit`, route to the domain report skills that the
# staged files actually call for. Non-blocking.
input="$(cat)"
cmd="$(printf '%s' "$input" | python3 -c "import sys,json;
try: print(json.load(sys.stdin).get('tool_input',{}).get('command',''))
except Exception: print('')" 2>/dev/null)"

case "$cmd" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac

STAGED="${PRECOMMIT_STAGED:-$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null)}"
[ -z "$STAGED" ] && exit 0

NEEDED=""
printf '%s\n' "$STAGED" | grep -qE '^content/|^data/generated/|^docs/sources\.md$' \
  && NEEDED="$NEEDED astronomy-report"
printf '%s\n' "$STAGED" | grep -qE '^src/puzzles/|^content/bg/' \
  && NEEDED="$NEEDED pedagogy-report"
printf '%s\n' "$STAGED" | grep -qE '^assets/|planet-render\.ts$|^package\.json$' \
  && NEEDED="$NEEDED perf-report"
printf '%s\n' "$STAGED" | grep -qE '^package\.json$|^requirements\.txt$|^index\.html$|^src/' \
  && NEEDED="$NEEDED privacy-guard"
# A dependency change is the one event that actually moves this game's attack
# surface. privacy-guard audits the tree for network calls; supply chain is a
# different question and is section 1 of security-audit.
printf '%s\n' "$STAGED" | grep -qE '^package(-lock)?\.json$|^requirements\.txt$' \
  && NEEDED="$NEEDED security-audit"

[ -z "$NEEDED" ] && exit 0

NEEDED="$NEEDED" python3 - <<'PY'
import json, os
needed = os.environ["NEEDED"].split()
msg = (
    "PRE-COMMIT DOMAIN CHECKS. The staged files call for: "
    + ", ".join(needed)
    + ". Run each relevant skill and report its findings before committing. "
    "These are non-blocking — they report, the user decides. "
    "Ground every finding in the actual diff and cite file:line; "
    "'no issues' is only valid after the checklist was actually walked."
)
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": msg}}))
PY
exit 0
