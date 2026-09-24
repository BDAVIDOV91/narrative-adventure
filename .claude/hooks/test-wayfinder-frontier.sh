#!/usr/bin/env bash
# Regression test for .claude/hooks/wayfinder-frontier.sh (SessionStart, 2026-09-18).
#
# The owner is new to wayfinder and asked to be guided. The skill is hidden from the per-turn skill list,
# so while a map has open tickets nothing tells a fresh session (or the owner) what is takeable. The hook
# prints the frontier and the exact line to type. It must mirror the read-only viewer's parser
# (~/tools/wayfinder-viewer/lib/parse.mjs, fog.mjs), or the hook and the viewer disagree about what is
# takeable: only `status: closed` closes, a non-empty assignee is a claim, a ticket is blocked while any
# blocked_by id is not a CLOSED ticket, and an unknown id blocks forever. The viewer shows no warning for
# that last case, so the hook must.
#
# Offline, builds its own fixtures, never touches docs/wayfinder/. Usage: test-wayfinder-frontier.sh [hook]
set -uo pipefail
HOOK="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/wayfinder-frontier.sh}"
pass=0; fail=0
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT

ok()   { printf '  ok    %s\n' "$1"; pass=$((pass+1)); }
bad()  { printf '  FAIL  %s\n' "$1"; [ -n "${2:-}" ] && printf '        %s\n' "$2"; fail=$((fail+1)); }
has()  { if grep -qF -- "$2" <<< "$OUT"; then ok "$1"; else bad "$1" "missing: $2"; fi; }
hasnt(){ if grep -qF -- "$2" <<< "$OUT"; then bad "$1" "unexpected: $2"; else ok "$1"; fi; }
run()  { OUT="$(bash "$HOOK" "$1" 2>&1)"; RC=$?; }

ticket() { # ticket <file> <id> <title> <type> <status> <assignee> <blocked_by line(s)>
  mkdir -p "$(dirname "$1")"
  printf -- '---\nid: "%s"\ntitle: %s\ntype: %s\nstatus: %s\nassignee: "%s"\n%s\n---\n\n## Question\n\nQ?\n' \
    "$2" "$3" "$4" "$5" "$6" "$7" > "$1"
}
map() { # map <dir> <fog bullets>
  mkdir -p "$1"
  printf '# %s\n\n<!-- wayfinder:map -->\n\n## Destination\n\nX.\n\n## Notes\n\n## Decisions so far\n\n## Not yet specified\n\n%s\n\n## Out of scope\n\n' \
    "$(basename "$1")" "$2" > "$1/MAP.md"
}

echo "wayfinder-frontier regression"

# 1. no docs/wayfinder at all
mkdir -p "$T/r1"; run "$T/r1"
[ "$RC" -eq 0 ] && [ -z "$OUT" ] && ok "no docs/wayfinder: silent, rc=0" || bad "no docs/wayfinder: silent, rc=0" "rc=$RC out=$OUT"

# 2. only a README, no map
mkdir -p "$T/r2/docs/wayfinder"; echo "# readme" > "$T/r2/docs/wayfinder/README.md"; run "$T/r2"
[ "$RC" -eq 0 ] && [ -z "$OUT" ] && ok "README only: silent" || bad "README only: silent" "rc=$RC out=$OUT"

# 3. a live map: closed / frontier / blocked / claimed, flow list with a trailing comment, block list
M="$T/r3/docs/wayfinder/demo-map"; map "$M" '- **Dim thing** — not sharp yet'
ticket "$M/tickets/001-a.md" 001 "Where it runs"      grilling closed owner 'blocked_by: []'
ticket "$M/tickets/002-b.md" 002 "What it emits"      research open   ""    'blocked_by: ["001"]   # closed'
ticket "$M/tickets/003-c.md" 003 "Who may delete"     grilling open   ""    $'blocked_by:\n  - "002"'
ticket "$M/tickets/004-d.md" 004 "Already taken"      task     open   owner 'blocked_by: []'
ticket "$M/tickets/005-e.md" 005 "Second takeable"    grilling OPEN   ""    'blocked_by: ["001"]'
run "$T/r3"
[ "$RC" -eq 0 ] && ok "live map: rc=0" || bad "live map: rc=0" "rc=$RC"
has   "names the map"                         "demo-map"
has   "counts takeable tickets"               "2 takeable"
has   "counts claimed"                        "1 claimed"
has   "counts blocked"                        "1 blocked"
has   "counts closed of total"                "1/5 closed"
has   "lists the first takeable ticket"       "002 What it emits (research)"
has   "lists the second takeable ticket"      "005 Second takeable (grilling)"
hasnt "a blocked ticket is not offered"       "003 Who may delete"
hasnt "a claimed ticket is not offered"       "004 Already taken"
has   "prints the exact line to type"         "/wayfinder docs/wayfinder/demo-map/MAP.md"
has   "says the OWNER types it"               "owner types"

# 4. an unknown / unpadded blocker id blocks forever and the viewer never warns: the hook must
M="$T/r4/docs/wayfinder/bad-ids"; map "$M" ''
ticket "$M/tickets/001-a.md" 001 "Fine"          grilling closed owner 'blocked_by: []'
ticket "$M/tickets/002-b.md" 002 "Stuck forever" grilling open   ""    'blocked_by: ["1"]'
run "$T/r4"
has   "warns about an unknown blocker id"     'ticket 002 is blocked by unknown id "1"'
has   "and counts it as blocked"              "1 blocked"

# 5. `Closed` in any case closes (the viewer lowercases); any other word is open
M="$T/r5/docs/wayfinder/case"; map "$M" ''
ticket "$M/tickets/001-a.md" 001 "Cap closed" grilling Closed owner 'blocked_by: []'
ticket "$M/tickets/002-b.md" 002 "Done word"  grilling done   ""    'blocked_by: ["001"]'
run "$T/r5"
has   "status: Closed closes its dependants"  "002 Done word"
has   "status: done is NOT closed"            "1/2 closed"

# 5b. 2026-09-18 (RED->GREEN): a flow list WRAPPED across lines was read as `[]`, so a blocked ticket was
# offered as takeable. Found by cross-checking the hook against the viewer on the viewer's own `live`
# fixture (viewer: 1 takeable / 4 blocked; hook: 2 / 3). My own fixtures had only one-line lists.
M="$T/r5b/docs/wayfinder/wrapped"; map "$M" ''
ticket "$M/tickets/001-a.md" 001 "Open blocker"   grilling open "" 'blocked_by: []'
ticket "$M/tickets/002-b.md" 002 "Wrapped list"   task     open "" $'blocked_by: [\n  "001",\n  "003"\n]'
ticket "$M/tickets/003-c.md" 003 "Other blocker"  grilling open "" 'blocked_by: ["001"]   # trailing comment'
run "$T/r5b"
hasnt "a wrapped flow list still blocks"      "002 Wrapped list"
has   "and only the real frontier is counted" "1 takeable, 0 claimed, 2 blocked"

# 6. every ticket closed, live fog left: the map has STALLED
M="$T/r6/docs/wayfinder/stalled"; map "$M" $'- **Still dim** — unknown\n- ~~**Graduated**~~ — graduated to ticket 001'
ticket "$M/tickets/001-a.md" 001 "Only one" grilling closed owner 'blocked_by: []'
run "$T/r6"
has   "stalled map is reported"               "stalled"
has   "counts only LIVE fog patches"          "1 fog patch"

# 7. every ticket closed, only struck fog: the way is clear, so stay silent (no nagging forever)
M="$T/r7/docs/wayfinder/clear"; map "$M" '- ~~**Graduated**~~ — graduated to ticket 001'
ticket "$M/tickets/001-a.md" 001 "Only one" grilling closed owner 'blocked_by: []'
run "$T/r7"
[ -z "$OUT" ] && ok "finished map: silent" || bad "finished map: silent" "out=$OUT"

# 8. titles reach the session context: control characters stripped, length capped
M="$T/r8/docs/wayfinder/hostile"; map "$M" ''
LONG="$(printf 'A%.0s' $(seq 1 300))"
ticket "$M/tickets/001-a.md" 001 "$LONG" grilling open "" 'blocked_by: []'
printf -- '---\nid: "002"\ntitle: Esc\033[31mRED\ntype: grilling\nstatus: open\nassignee: ""\nblocked_by: []\n---\n' > "$M/tickets/002-b.md"
run "$T/r8"
LINE="$(grep -F '001 ' <<< "$OUT" | head -n 1)"
# (non-vacuous: an empty LINE must fail, and the escaped ticket must still be listed)
[ -n "$LINE" ] && [ "${#LINE}" -le 140 ] && ok "a 300-char title is listed and capped" || bad "a 300-char title is listed and capped" "line length ${#LINE}"
has   "the ticket with an escape is still listed" "002 Esc"
if grep -q $'\033' <<< "$OUT"; then bad "escape characters are stripped"; else ok "escape characters are stripped"; fi

# 9. garbage never breaks session start
M="$T/r9/docs/wayfinder/garbage"; map "$M" ''
mkdir -p "$M/tickets"; head -c 2048 /dev/urandom > "$M/tickets/001-bin.md"; echo "no frontmatter here" > "$M/tickets/002-plain.md"
run "$T/r9"
[ "$RC" -eq 0 ] && ok "binary / frontmatter-less tickets: rc=0" || bad "binary / frontmatter-less tickets: rc=0" "rc=$RC"

# 10. a slug the viewer would refuse is ignored; a directory without MAP.md is not a map
mkdir -p "$T/r10/docs/wayfinder/-bad slug" "$T/r10/docs/wayfinder/nomap/tickets"
ticket "$T/r10/docs/wayfinder/nomap/tickets/001-a.md" 001 "Orphan" grilling open "" 'blocked_by: []'
run "$T/r10"
[ -z "$OUT" ] && ok "no MAP.md / bad slug: silent" || bad "no MAP.md / bad slug: silent" "out=$OUT"

# 11. the hook file exists and is executable (non-vacuity: every case above ran the real script)
[ -x "$HOOK" ] && ok "hook is executable" || bad "hook is executable" "$HOOK"

echo; echo "pass=$pass fail=$fail"; [ "$fail" -eq 0 ]
