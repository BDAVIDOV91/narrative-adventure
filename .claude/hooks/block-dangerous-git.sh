#!/usr/bin/env bash
# PreToolUse(Bash): HARD BLOCK on git commands the owner reserves for themselves
# or that destroy work. Exit 2 + stderr is what stops the call.
#
# Transplanted from pdf_data_extractor_v2, with `git push` blocked for this
# project's own reason: the owner does every push themselves.
#
# Implemented with a real tokenizer rather than regex. Regex either missed
# `git -C /repo push` (an option that takes a separate value) and
# `bash -c "git push"` (preceded by a quote, not whitespace), or matched
# `git commit -m "fix push"` (the word inside a message). Parsing the tokens
# and reading the actual subcommand gets all four right.
#
# Over-blocking is deliberate: a false positive costs one message, a lost
# working tree costs the session.

input="$(cat)"
printf '%s' "$input" | python3 -c '
import json, shlex, sys

try:
    cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
except Exception:
    sys.exit(0)

if not cmd:
    sys.exit(0)

RULES = {
    ("git", "push"): "git push — the owner does every push themselves. Commit, then say it is ready to push.",
    ("gh", "pr", "create"): "gh pr create — the owner opens their own PRs.",
    ("gh", "release", "create"): "gh release create — the owner cuts their own releases.",
    ("git", "stash"): "git stash — sessions and subagents share one working tree; a stash can bury another one’s work. For a clean baseline read the committed version (git show HEAD:<path>) or use a git worktree.",
}

# git global options that consume the NEXT token as their value.
TAKES_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")", "{", "}"}
# Only these treat a following quoted string as a command to run. Recursing
# into every quoted token instead would block `echo "git push is blocked"`.
SHELLS = {"bash", "sh", "zsh", "dash", "ksh", "env"}


def tokenize(text):
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()


def segments(tokens):
    """Split a token stream on shell separators into individual commands."""
    current = []
    for token in tokens:
        if token in SEPARATORS:
            if current:
                yield current
            current = []
        else:
            current.append(token)
    if current:
        yield current


def check(tokens, depth=0):
    """Return a rule string if this token stream runs a blocked command."""
    if depth > 3:
        return None

    for segment in segments(tokens):
        if not segment:
            continue

        program = segment[0].rsplit("/", 1)[-1]

        # A shell invoked with -c runs its argument as a command: recurse into
        # it. Scoped to real shells so a quoted string elsewhere stays data.
        if program in SHELLS:
            for position, token in enumerate(segment):
                if token == "-c" and position + 1 < len(segment):
                    hit = check(tokenize(segment[position + 1]), depth + 1)
                    if hit:
                        return hit

        if program not in ("git", "gh"):
            continue

        # Walk past global options to reach the real subcommand.
        words = []
        index = 1
        while index < len(segment):
            token = segment[index]
            if token.startswith("-"):
                if token in TAKES_VALUE:
                    index += 2
                    continue
                index += 1
                continue
            words.append(token)
            index += 1

        for length in (3, 2, 1):
            key = (program, *words[:length])
            if key in RULES:
                return RULES[key]

        # Destructive forms that depend on a flag or path, not just the verb.
        if program == "git" and words:
            sub = words[0]
            rest = [t for t in segment[1:] if t != sub]
            if sub == "reset" and "--hard" in rest:
                return "git reset --hard — destroys uncommitted work irreversibly."
            if sub == "clean" and any(
                t.startswith("-") and "f" in t.lstrip("-") for t in rest
            ):
                return "git clean -f — deletes untracked files irreversibly."
            if sub == "branch" and "-D" in rest:
                return "git branch -D — force-deletes a branch and any commits only on it."
            if sub in ("checkout", "restore") and "." in words[1:]:
                return f"git {sub} . — discards every uncommitted change in the tree."
    return None


hit = check(tokenize(cmd))
if hit:
    print(f"BLOCKED: {hit}", file=sys.stderr)
    print("", file=sys.stderr)
    print("This is a standing CLAUDE.md rule enforced by a hook, not a permission", file=sys.stderr)
    print("prompt. Do not retry it, do not rephrase it, and do not edit the hook.", file=sys.stderr)
    print("If the owner genuinely wants this command, they run it themselves.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
'
