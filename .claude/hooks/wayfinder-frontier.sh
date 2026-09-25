#!/usr/bin/env bash
# SessionStart hook: while a wayfinder map has open work, say what is takeable and what to type (2026-09-18).
# The owner is new to wayfinder and asked to be guided; the skill is hidden from the per-turn skill list
# (`disable-model-invocation: true`), so without this nothing reminds a fresh session that a map is waiting.
#
# Silent when docs/wayfinder/ holds no map, or every map is finished (all tickets closed, no live fog).
# SessionStart stdout becomes context, so ticket titles are stripped of control characters and capped.
# Mirrors the read-only viewer's parser (lib/parse.mjs, lib/fog.mjs): only `status: closed` closes, a
# non-empty assignee is a claim, a ticket is blocked while any blocked_by id is not a CLOSED ticket. An
# unknown id therefore blocks forever, and the viewer shows no warning for it, so this hook does.
# Exit 0 always: a broken map must never break session start.
#
# Usage for the test: wayfinder-frontier.sh [repo-root]
# Test: bash .claude/hooks/test-wayfinder-frontier.sh
root="${1:-${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}}"
[ -d "$root/docs/wayfinder" ] || exit 0

python3 - "$root" <<'PY' 2>/dev/null || true
import os, re, sys

root = sys.argv[1]
base = os.path.join(root, "docs", "wayfinder")
SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ITEM = re.compile(r"^(?:[-*+]|\d{1,9}[.)])[ \t]+")
FENCE = re.compile(r"^\s*(?:`{3,}|~{3,})")
MAX_LISTED, TITLE_CAP = 3, 80


def clean(text, cap=TITLE_CAP):
    text = re.sub(r"\x1b\[[0-9;?]*[ -/]*[@-~]", "", str(text))   # whole ANSI sequences first
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= cap else text[: cap - 1] + "…"


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def frontmatter(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            text = handle.read(65536)
    except OSError:
        return {}
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    data, key, flow = {}, None, None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if flow is not None:            # inside a flow list wrapped across lines: `blocked_by: [` … `]`
            flow += " " + line
            if "]" in line:
                inner = flow[: flow.index("]")]
                data[key] = [unquote(part) for part in re.sub(r"#[^,\]]*", "", inner).split(",") if part.strip()]
                flow = None
            continue
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and key is not None and isinstance(data.get(key), list):
            data[key].append(unquote(re.sub(r"\s+#.*$", "", item.group(1))))
            continue
        pair = re.match(r"^([A-Za-z0-9_.-]+)[ \t]*:[ \t]*(.*)$", line)
        if not pair:
            continue
        key, raw = pair.group(1), pair.group(2).strip()
        if raw.startswith("[") and "]" not in raw:
            flow, data[key] = raw[1:], []
        elif raw.startswith("["):
            inner = raw[1:raw.index("]")]
            data[key] = [unquote(part) for part in inner.split(",") if part.strip()]
        elif raw == "":
            data[key] = []
        else:
            data[key] = unquote(re.sub(r"\s+#.*$", "", raw)) if not raw.startswith(("\"", "'")) else unquote(raw)
    if flow is not None:                # `[` never closed: fail closed (blocked + warned), never "takeable"
        data[key] = ["unterminated list"]
    return data


def as_list(value):
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    value = str(value or "").strip()
    return [value] if value and value != "[]" else []


def load_tickets(map_dir):
    tickets_dir = os.path.join(map_dir, "tickets")
    try:
        names = sorted(n for n in os.listdir(tickets_dir) if n.lower().endswith(".md"))
    except OSError:
        return []
    tickets = []
    for name in names:
        data = frontmatter(os.path.join(tickets_dir, name))
        if not data:
            continue
        number = re.match(r"^(\d+)", name)
        tickets.append({
            "id": str(data.get("id") or (number.group(1) if number else name[:-3])).strip(),
            "title": data.get("title") if isinstance(data.get("title"), str) and data.get("title") else name[:-3],
            "type": (data.get("type") if isinstance(data.get("type"), str) else "") or "task",
            "closed": str(data.get("status") if isinstance(data.get("status"), str) else "open").strip().lower() == "closed",
            "claimed": bool(str(data.get("assignee") if isinstance(data.get("assignee"), str) else "").strip()),
            "blocked_by": as_list(data.get("blocked_by")),
        })
    return tickets


def live_fog(map_path):
    try:
        with open(map_path, encoding="utf-8", errors="replace") as handle:
            lines = handle.read(262144).split("\n")
    except OSError:
        return 0
    live, inside, fenced, prose_seen, bullets = 0, False, False, False, 0
    for line in lines:
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        heading = re.match(r"^##[ \t]+(.*?)[ \t]*#*[ \t]*$", line)
        if heading:
            inside = heading.group(1).strip().lower() == "not yet specified"
            continue
        if not inside or not line.strip() or line.lstrip().startswith("<!--"):
            continue
        if ITEM.match(line):
            bullets += 1
            if not re.match(ITEM.pattern + "~~", line):
                live += 1
        elif bullets == 0 and not line.startswith((" ", "\t")) and not prose_seen:
            prose_seen = True          # prose before the first bullet counts as one live patch
            live += 1
    return live


def describe(slug, map_dir):
    tickets = load_tickets(map_dir)
    by_id = {t["id"]: t for t in tickets}
    warnings, frontier, claimed, blocked = [], [], 0, 0
    for t in tickets:
        if t["closed"]:
            continue
        unknown = [b for b in t["blocked_by"] if b not in by_id]
        for b in unknown:
            warnings.append(f'  WARNING: ticket {clean(t["id"], 12)} is blocked by unknown id "{clean(b, 12)}" — '
                            "it stays blocked forever and the viewer will not warn. Fix blocked_by (quoted, 3 digits).")
        is_blocked = any((b not in by_id) or (not by_id[b]["closed"]) for b in t["blocked_by"])
        if t["claimed"]:
            claimed += 1
        elif is_blocked:
            blocked += 1
        else:
            frontier.append(t)
    total, closed = len(tickets), sum(1 for t in tickets if t["closed"])
    fog = live_fog(os.path.join(map_dir, "MAP.md"))
    rel = f"docs/wayfinder/{slug}/MAP.md"

    if total and closed == total:
        if fog == 0:
            return []                   # the way is clear: finished maps stay silent
        return [f"WAYFINDER: {slug} has stalled — every ticket is closed but {fog} fog patch{'es' if fog != 1 else ''} "
                f"remain{'s' if fog == 1 else ''} in \"Not yet specified\". Next session: turn the fog into tickets or "
                f"rule it out of scope.", f"  The owner types: /wayfinder {rel}"]
    if not total:
        return []

    out = [f"WAYFINDER: {slug} — {len(frontier)} takeable, {claimed} claimed, {blocked} blocked, "
           f"{closed}/{total} closed, {fog} fog."]
    for t in frontier[:MAX_LISTED]:
        out.append(f"  next: {clean(t['id'], 12)} {clean(t['title'])} ({clean(t['type'], 12).lower()})")
    if len(frontier) > MAX_LISTED:
        out.append(f"  … and {len(frontier) - MAX_LISTED} more takeable.")
    out.extend(warnings)
    if frontier:
        out.append(f"  The owner types: /wayfinder {rel}   (one ticket per session)")
    elif claimed:
        out.append(f"  Nothing takeable: {claimed} ticket{'s are' if claimed != 1 else ' is'} claimed. Finish or "
                   f"release it: /wayfinder {rel}")
    else:
        out.append(f"  Nothing takeable and nothing claimed: check blocked_by in docs/wayfinder/{slug}/tickets/.")
    return out


try:
    slugs = sorted(d for d in os.listdir(base)
                   if SLUG.match(d) and os.path.isfile(os.path.join(base, d, "MAP.md")))
except OSError:
    slugs = []

report = []
for slug in slugs:
    try:
        report.extend(describe(slug, os.path.join(base, slug)))
    except Exception:                   # noqa: BLE001 — a broken map must not break session start
        continue
if report:
    report.append("  (Claude: the owner is new to wayfinder. If they state no task, offer the next ticket. "
                  "The skill is OWNER-typed: never start it yourself. Triggers: docs/wayfinder/QUICKSTART.md)")
    print("\n".join(report))
PY
exit 0
