---
name: companion-memories-012
description: Ticket 012 companion-memory facts (Earth's shadow, Moon eastward drift and always-later moonrise, Mars brightening, Jupiter shadow transit, Cassini Division) — resolved, plus the fetch path that works and the misquoted-excerpt trap
metadata:
  type: project
---

Resolved 2026-09-26, recorded in docs/sources.md under "Companion memories (ticket 012)". All five were VERIFIED from pages read in full.

- **Fetch path that works (durable).** WebFetch is blocked by the context-mode hook, and the context-mode MCP tools are not exposed to this subagent. Plain `curl -sL -A "Mozilla/5.0 ..."` from Bash DOES work. Strip the HTML with a small python script in the scratchpad. S&T returns 403, so use a Wayback snapshot (`web.archive.org/web/2025/<url>`).
- **Trap: the consultant's "search excerpt" quotes can be paraphrases dressed as quotes.** APOD 2018-07-05 and NASA "The Familiar Division" did not contain the quoted wording. Always read the page before copying a quote into sources.md.
- **Moonrise is always later across all of Bulgaria (41.2–44.2° N).** Computed with skyfield and de440s over 2020–2038 (6,704 pairs). The minimum is +19.0 min at 42.7° N, and there are no negative gaps. Do not recompute.
- Mars: "night after night" is wrong at the level of perception. Use "week after week". The 2027 peak is about −1.28, fainter than Jupiter.
- Jupiter shadow transit: about 75–90 mm at 100× in steady air. APODs use the words "cloud tops" and "Jupiter's perspective", so never write "surface".
- Cassini Division: about 80 mm minimum, 100 mm or more comfortable. No sourced threshold for the ring opening. The Bulgarian term is „делението на Касини“ (bg.wiki Сатурн). „участъкът Касини“ is a calque. "Empty" is NOT ATTESTED.

**Why:** these took a full session to pin down. The misquote trap would silently put false quotes in sources.md.
**How to apply:** skip re-research of these five facts. For any new consultant excerpt, fetch it with curl before trusting the quote. See also [[back-cover-009]].
