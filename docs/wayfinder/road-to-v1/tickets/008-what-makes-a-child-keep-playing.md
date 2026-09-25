---
id: "008"
title: What makes a child want to keep playing
type: grilling
status: open
assignee: ""
blocked_by: []
---

## Question

Beyond the next page and the fact strings, what reward loop makes an 11–12 year old *want* to keep playing, and
what does each beat hand out?

The owner raised this on 2026-09-25, while ticket 003 was being resolved. Settled inputs, not to be re-asked:

- **The kind of pull:** curiosity and collection, like a sky album the child fills, noticed things kept, hidden
  optional finds, and the book's pages coming alive. **No compulsion mechanics:** no streaks, no daily-login
  pressure, no timers, no random loot, and nothing that punishes stopping (UK Children's Code, EU DSA dark patterns;
  CLAUDE.md rule 8).
- **The owner's own idea to grill:** achievements that also *help*. Gathering enough of them earns hints to spend on
  a later level when the child is stuck. Grill it or a similar idea.

Decide:

- what counts as an achievement (a solved optional beat, a hidden find, a noticed thing), and where it is shown;
- whether and how achievements convert to hints, and what a hint is (it must not give the answer away, or it
  becomes a lock with a key rather than a lesson);
- how the collection is shown without a number or counter (rule 2 applies to any display a child reads as a score);
- how it interacts with the gate: hints must never let a child skip a **required** marker's lesson, and optional
  markers still never carry a level on their own;
- storage: `localStorage` only, nothing leaves the device (rule 8);
- content: every string through `content/bg/` (rule 3).

Consult `puzzle-pedagogy-reviewer` on the hint design. It likely touches the book's through-line fog patch ("The
book's through-line, ending and navigation"); say so if the answer settles part of it.
