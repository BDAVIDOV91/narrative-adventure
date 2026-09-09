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


# The hook degrades gracefully when the venv is missing ("skipped: venv not
# found") so a stale interpreter path does NOT fail a commit — it silently stops
# running every Python check while commits keep succeeding. That happened when
# .venv/ was renamed to venv/. These assertions make the path a tested fact.
echo ""
echo "interpreter paths:"

for path in $(grep -oE '(^|[[:space:]])[.a-zA-Z0-9_/-]*venv/bin/[a-z0-9]+' .husky/pre-commit | tr -d ' ' | sort -u); do
  if [ -x "$path" ]; then
    echo "  ok   exists and is executable: $path"
  else
    echo "  FAIL pre-commit references a missing interpreter: $path"
    echo "         the hook would silently SKIP its Python checks"
    FAILURES=$((FAILURES + 1))
  fi
done

# The setup command in the hook's own skip message must create the path the
# hook then looks for. These drifted apart once already.
SETUP_VENV="$(grep -oE 'uv venv [.a-zA-Z0-9_/-]+' .husky/pre-commit | head -1 | awk '{print $3}')"
HOOK_VENV="$(grep -oE '[.a-zA-Z0-9_/-]*venv/bin/python' .husky/pre-commit | head -1 | sed 's|/bin/python||')"
if [ "$SETUP_VENV" = "$HOOK_VENV" ]; then
  echo "  ok   skip-message setup path matches the checked path: $HOOK_VENV"
else
  echo "  FAIL skip message says 'uv venv $SETUP_VENV' but the hook checks $HOOK_VENV"
  FAILURES=$((FAILURES + 1))
fi

# What the hook actually runs, not just which branch it picks. The scoping
# assertions above prove ts=1, but a branch that type-checks and never runs a
# test is a gate with a hole in it — and that hole is invisible from the plan
# output.
echo ""
echo "what each branch runs:"

if grep -q 'vitest' .husky/pre-commit; then
  echo "  ok   the typescript branch runs vitest"
else
  echo "  FAIL the typescript branch never runs vitest"
  echo "         src/ has no test runner in the commit gate, so CLAUDE.md rule 5"
  echo "         (no fix ships without its own regression test) cannot be enforced"
  FAILURES=$((FAILURES + 1))
fi

# A commit-time gate must not fetch a moving version. Everything else in this
# repo is pinned exactly (save-exact=true, ADR-0004); the hook must match.
UNPINNED="$(grep -n '@latest' .husky/pre-commit || true)"
if [ -z "$UNPINNED" ]; then
  echo "  ok   no unpinned @latest fetch in the hook"
else
  echo "  FAIL the hook fetches an unpinned version at commit time:"
  printf '         %s\n' "$UNPINNED"
  FAILURES=$((FAILURES + 1))
fi

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "pre-commit scoping: all checks passed"
  exit 0
fi
echo "pre-commit scoping: $FAILURES failure(s)"
exit 1
