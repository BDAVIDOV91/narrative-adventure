#!/usr/bin/env bash
# PreToolUse(Bash): on `git commit`, inject the PER FIX test checklist.
# Non-blocking — surfaces a reminder, never stops the commit.
input="$(cat)"
cmd="$(printf '%s' "$input" | python3 -c "import sys,json;
try: print(json.load(sys.stdin).get('tool_input',{}).get('command',''))
except Exception: print('')" 2>/dev/null)"
case "$cmd" in
  *"git commit"*)
    python3 - <<'PY'
import json
msg = ("PRE-COMMIT CHECK (CLAUDE.md PER FIX rule) — before this commit lands: "
       "1) If this fixes a bug, did you write a regression test for it? "
       "2) Did that test fail RED on the old code, then pass GREEN on the fix? "
       "3) Is the full suite still green (nothing else broke)? "
       "If yes to all -> commit. If not -> stop and write the test first. "
       "No fix ships without its own regression test; if it shipped untested, "
       "it isn't done.")
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": msg}}))
PY
    ;;
esac
exit 0
