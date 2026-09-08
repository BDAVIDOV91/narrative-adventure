#!/usr/bin/env sh
# Regression test for .husky/pre-commit scoping.
#
# The hook decides which checks to run from the staged file list. If that logic
# drifts, either commits get slow again (running everything) or checks silently
# stop running (running nothing) — and the second failure is invisible.
#
# Usage: sh .husky/test-pre-commit-scope.sh

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT" || exit 1

FAILURES=0

expect() {
  description="$1"
  staged="$2"
  want="$3"
  got="$(PRECOMMIT_STAGED="$staged" PRECOMMIT_DRY_RUN=1 sh .husky/pre-commit)"
  if [ "$got" = "$want" ]; then
    echo "  ok   $description"
  else
    echo "  FAIL $description"
    echo "         staged: $staged"
    echo "         want:   $want"
    echo "         got:    $got"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "pre-commit scoping:"

# A docs-only commit must cost nothing. This is the whole point of scoping.
expect "docs only runs nothing"          "docs/README.md"                    "plan: ts=0 py=0 levels=0"
expect "README only runs nothing"        "README.md"                         "plan: ts=0 py=0 levels=0"
expect "prompts only runs nothing"       "prompts/planet-prompts.md"         "plan: ts=0 py=0 levels=0"

expect "a scene runs ts"                 "src/scenes/earth/earth-scene.ts"   "plan: ts=1 py=0 levels=0"
expect "eslint config runs ts"           "eslint.config.mjs"                 "plan: ts=1 py=0 levels=0"
expect "tsconfig runs ts"                "tsconfig.json"                     "plan: ts=1 py=0 levels=0"

expect "a script runs python"            "data/scripts/validate-levels.py"   "plan: ts=0 py=1 levels=0"
expect "requirements runs python"        "requirements.txt"                  "plan: ts=0 py=1 levels=0"
expect "flake8 config runs python"       ".flake8"                           "plan: ts=0 py=1 levels=0"

expect "level data runs the validator"   "src/scenes/earth/earth-data.json"  "plan: ts=0 py=0 levels=1"
expect "the schema runs the validator"   "schemas/level-data.schema.json"    "plan: ts=0 py=0 levels=1"

# Content keys are typed, so a Bulgarian string change can break the build.
expect "content runs ts and validator"   "content/bg/ui.json"                "plan: ts=1 py=0 levels=1"

# Multiple kinds at once.
expect "a mixed commit runs everything" \
  "$(printf 'src/main.ts\ndata/scripts/orbital-positions.py\ncontent/bg/facts.json')" \
  "plan: ts=1 py=1 levels=1"

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "pre-commit scoping: all checks passed"
  exit 0
fi
echo "pre-commit scoping: $FAILURES failure(s)"
exit 1
