#!/usr/bin/env sh
# Regression test for .claude/hooks/precommit-checks-reminder.sh routing.
#
# The hook decides which domain report skills a commit calls for from the staged
# file list. Its failure mode is silent in both directions: a missing route means
# a domain check never runs and nobody notices, and a route that fires on
# everything trains the reader to skim past it. Neither shows up in a commit.
#
# Usage: sh .claude/hooks/test-precommit-checks-reminder.sh

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT" || exit 1

HOOK=".claude/hooks/precommit-checks-reminder.sh"
FAILURES=0

# Run the hook as Claude Code would: the tool call on stdin, the staged list
# overridden so the test does not depend on the working tree.
route() {
  printf '{"tool_input":{"command":"git commit -m \\"x\\""}}' \
    | PRECOMMIT_STAGED="$1" sh "$HOOK" 2>/dev/null
}

# Asserts the routed skill list is exactly $2 (order as the hook emits it).
expect_routes() {
  description="$1"
  staged="$2"
  want="$3"
  got="$(route "$staged" | python3 -c "import sys,json
try:
    msg = json.load(sys.stdin)['hookSpecificOutput']['additionalContext']
except Exception:
    print(''); raise SystemExit
head = msg.split('call for: ', 1)[1].split('.')[0]
print(' '.join(head.split(', ')))" 2>/dev/null)"
  if [ "$got" = "$want" ]; then
    echo "  ok   $description"
  else
    echo "  FAIL $description"
    echo "         staged: $staged"
    echo "         want:   ${want:-<no routing>}"
    echo "         got:    ${got:-<no routing>}"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "domain skill routing:"

# The four documented routes in the CLAUDE.md review-gates table.
expect_routes "sources routes astronomy"        "docs/sources.md"          "astronomy-report"
expect_routes "generated data routes astronomy" "data/generated/stars.json" "astronomy-report"
expect_routes "a puzzle routes pedagogy"        "src/puzzles/rotate-match/rotate-match.ts" \
  "pedagogy-report privacy-guard"
expect_routes "bulgarian content routes both"   "content/bg/facts.json" \
  "astronomy-report pedagogy-report"
expect_routes "a texture routes perf"           "assets/images/nasa/mars.webp" "perf-report"
expect_routes "the renderer routes perf"        "src/shared/planet-render.ts" \
  "perf-report privacy-guard"

# A dependency change is the one event that genuinely alters this game's attack
# surface, and supply chain is section 1 of the security-audit skill. privacy-guard
# audits the tree for network calls, which is a different question.
expect_routes "package.json routes security"    "package.json" \
  "perf-report privacy-guard security-audit"
expect_routes "requirements routes security"    "requirements.txt" \
  "privacy-guard security-audit"
expect_routes "the lockfile routes security"    "package-lock.json" "security-audit"

# Silence where silence is correct — a routing prompt on every commit is noise.
expect_routes "docs only routes nothing"        "docs/handoffs/2026-09-09.md" ""
expect_routes "a hook change routes nothing"    ".husky/pre-commit"           ""

echo ""
echo "non-commit commands:"

for cmd in "git status" "npm test" "git log --oneline"; do
  got="$(printf '{"tool_input":{"command":"%s"}}' "$cmd" \
    | PRECOMMIT_STAGED="package.json" sh "$HOOK" 2>/dev/null)"
  if [ -z "$got" ]; then
    echo "  ok   stays silent for: $cmd"
  else
    echo "  FAIL routed on a non-commit command: $cmd"
    echo "         got: $got"
    FAILURES=$((FAILURES + 1))
  fi
done

echo ""
echo "contract:"

# The hook must never block a commit — the gates report, the owner decides.
printf '{"tool_input":{"command":"git commit -m \\"x\\""}}' \
  | PRECOMMIT_STAGED="package.json" sh "$HOOK" >/dev/null 2>&1
if [ "$?" -eq 0 ]; then
  echo "  ok   exits 0 (non-blocking)"
else
  echo "  FAIL the hook exits non-zero and would block a commit"
  FAILURES=$((FAILURES + 1))
fi

# Every skill the hook can name must actually exist, or the routing prompt sends
# the reader after something that is not there.
for skill in $(grep -oE 'NEEDED [a-z-]+"' "$HOOK" | grep -oE '[a-z-]+"' | tr -d '"' | sort -u); do
  if [ -f ".claude/skills/$skill/SKILL.md" ]; then
    echo "  ok   routed skill exists: $skill"
  else
    echo "  FAIL the hook routes to a skill that does not exist: $skill"
    FAILURES=$((FAILURES + 1))
  fi
done

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "precommit-checks-reminder: all checks passed"
  exit 0
fi
echo "precommit-checks-reminder: $FAILURES failure(s)"
exit 1
