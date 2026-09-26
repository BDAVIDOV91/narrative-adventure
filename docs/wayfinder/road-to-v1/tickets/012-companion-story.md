---
id: "012"
title: The companion's story
type: grilling
status: open
assignee: ""
blocked_by: []
---

## Question

Who is the companion, and what is its story? The owner's seed from ticket 009 (Q13) is this:

- the companion lost its partner, an astronomer or an astronaut;
- it lost its memory in the grief;
- as the child explores, memories of their missions come back, page by page;
- what happens when the memory is whole is still open.

Decide:

- who the partner was, and how they parted: death or separation, a tone call for 11–12 year olds;
- which memory, if any, each page returns in v1, and where it lives;
- what full memory unlocks: a post-v1 "help the companion" finale, when the whole solar system is cleared;
- how the back cover's role-flipping line (the child shows the companion the real sky) fits the story.

Constraints, not to be re-asked:

- **Fiction wall (Q16).**
  - Near-future fiction is allowed but kept close: humanity's first crewed Mars mission or the asteroid belt, never
    the deep solar system.
  - It must be framed so a child cannot take it as history. Decide the tense ("one day…" vs a memory of a past event),
    and how story lines are recorded in `docs/sources.md`, before any memory line is written.
  - Two VERIFIED anchors are in `docs/sources.md` ("Back cover — seeing the worlds with your own eyes"):
    - no person has travelled farther than the Moon; the farthest trip, Artemis II (April 2026), looped around it;
    - the last people to walk on the Moon were the Apollo 17 crew (December 1972). This goes stale the day Artemis
      lands a crew, so re-check it before release.
  - "Apollo 17 was the last crewed lunar mission" is DISPUTED (Artemis II). Never write it.
  - `pedagogy-report` must pass the framing.
- **A memory earns its place by carrying astronomy** (the spirit of ADR 0005): it is never a moral tale.
- **The 09-09 tiers stand.** This ticket gates only story and memory lines. The companion's arrival, nudge and fact
  lines go ahead with the Earth build. Memories never add companion speech on later levels, which would undo the tier
  reduction; if they ship, they go on the page or album card.
- **No tease** of unbuilt worlds (ticket 009 Q7).
- **Privacy:** no stored state beyond what `solved[]` and `completed` already give.
