#!/usr/bin/env sh
# Regression test for .claude/hooks/block-dangerous-git.sh
#
# Both directions matter. A missed block lets work get destroyed or pushed
# without the owner; a false positive blocks ordinary commits and makes the
# hook something to disable. The two cases at the bottom of the ALLOW list are
# the ones an earlier regex version got wrong.
#
# Usage: sh .claude/hooks/test-block-dangerous-git.sh

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT" || exit 1
HOOK=".claude/hooks/block-dangerous-git.sh"
FAILURES=0

run() {
  python3 -c "import json,sys; print(json.dumps({'tool_input':{'command':sys.argv[1]}}))" "$1" \
    | bash "$HOOK" >/dev/null 2>&1
  echo $?
}

blocks() {
  code="$(run "$1")"
  if [ "$code" = "2" ]; then
    echo "  ok   blocks: $1"
  else
    echo "  FAIL should block (exit=$code): $1"
    FAILURES=$((FAILURES + 1))
  fi
}

allows() {
  code="$(run "$1")"
  if [ "$code" = "0" ]; then
    echo "  ok   allows: $1"
  else
    echo "  FAIL should allow (exit=$code): $1"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "block-dangerous-git:"

# The owner does every push and opens every PR themselves.
blocks "git push"
blocks "git push origin development"
blocks "git push --force"
blocks "git -C /repo push"
blocks "git --git-dir=/x/.git push"
blocks "/usr/bin/git push"
blocks "npm test && git push"
blocks "bash -c \"git push\""
blocks "gh pr create --fill"
blocks "gh release create v1"

# Destroys shared working-tree state.
blocks "git stash"
blocks "git stash push -m wip"
blocks "sh -c 'git stash'"

# Destroys uncommitted work.
blocks "git reset --hard HEAD"
blocks "git clean -fd"
blocks "git clean -f"
blocks "git branch -D old"
blocks "git checkout ."
blocks "git restore ."

# Ordinary work must stay unblocked.
allows "git status"
allows "git add -A"
allows "git log --oneline -5"
allows "git diff --cached"
allows "git checkout development"
allows "git checkout -b feat/moon-level"
allows "git restore --staged file.ts"
allows "git branch -d merged-branch"
allows "git reset HEAD~1"
allows "git clean -n"
allows "git show HEAD:src/main.ts"
allows "npm run build"

# The word appearing inside a commit message or a search is not a command.
allows "git commit -m \"fix push handling\""
allows "git commit -m \"add stash support to the editor\""
allows "echo \"git push is blocked\""
allows "grep -rn \"git push\" docs/"

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "block-dangerous-git: all checks passed"
  exit 0
fi
echo "block-dangerous-git: $FAILURES failure(s)"
exit 1
