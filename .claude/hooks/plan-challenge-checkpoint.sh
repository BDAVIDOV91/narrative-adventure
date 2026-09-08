#!/usr/bin/env bash
# PostToolUse(ExitPlanMode): after a plan is approved, inject the standing
# "challenge or proceed?" checkpoint instruction.
#
# This hook does NOT spawn anything. It reliably reminds the main loop to run
# the user-gated challenger gate before any code is written. Transplanted from
# pdf_data_extractor_v2, with the plan-file glob corrected: plan files here do
# not contain "-agent-" in their names.
input="$(cat)"
tool="$(printf '%s' "$input" | python3 -c "import sys,json;
try: print(json.load(sys.stdin).get('tool_name',''))
except Exception: print('')" 2>/dev/null)"
case "$tool" in
  *ExitPlanMode*)
    python3 - <<'PY'
import json
msg = (
    "PLAN-CHALLENGE CHECKPOINT (project workflow). The plan is approved. "
    "BEFORE writing any implementation code, ask the user with AskUserQuestion: "
    "\"Challenge the plan or proceed?\" (options: Challenge / Proceed).\n"
    "- If Challenge: spawn TWO 'challenger' subagents IN PARALLEL (Agent tool, "
    "subagent_type: challenger), each given the plan file path (the newest "
    "~/.claude/plans/*.md). When BOTH return, post a combined summary of their "
    "findings plus both approve/revise verdicts, then MERGE the findings into the "
    "existing plan file: append a '## Challenger Findings' section and fold any "
    "accepted fixes inline where they apply (never overwrite or replace the "
    "original plan). Then proceed — the verdict reports, it does not block.\n"
    "- If Proceed: implement directly, no challenge."
)
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": msg}}))
PY
    ;;
esac
exit 0
