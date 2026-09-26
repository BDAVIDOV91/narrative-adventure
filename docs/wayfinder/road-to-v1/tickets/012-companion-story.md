---
id: "012"
title: The companion's story
type: grilling
status: closed
assignee: owner
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

## Resolution

Grilled with the owner on 2026-09-26 (Q1–Q23). `astronomy-consultant` proposed the candidate facts
([research 012](../research/012-companion-memories.md)). Two `challenger` agents both returned "revise" with wording
fixes, folded in below, and the owner answered Q20–Q23. `astronomy-accuracy-checker` VERIFIED all five memory facts
from full page reads. `puzzle-pedagogy-reviewer` passed the framing with changes, and its must-fixes are applied in
`docs/sources.md`. Reasoning and rejected options: [ADR 0008](../../../adr/0008-companion-story-replaces-dimming-star.md).

**The story.**

- The tiny AI stays in the old telescope, which belonged to **Сияна**. She is a fictional amateur astronomer with a
  first name only, who watched from her yard in Bulgaria. Her memories are undated, and no real observatory appears.
- The partner is an astronomer, not an astronaut, so there is no near-future fiction and no mission history.
- They were **separated**, and v1 never says why. Nothing reads as death, and nothing promises a reunion.
- The lost-memory story **replaces the dimming-star mystery**, which was interstellar (rule 6) and never designed.

**Tense and voice.**

- Memory lines are past, undated recollections in the companion's first person.
- The companion's own forms are gender-neutral: present tense, the first-person-singular aorist, and every „ние" form.
- Сияна is gendered feminine, and she is quoted in the present tense.
- Lines addressed to the child avoid gendered forms.
- The companion is never called „спътник".

**Where it lives** (nothing new is stored):

- **Intro:** one or two lines on the storybook, shown while
  `Object.values(progress.levels).every(l => l.solved.length === 0)`. The companion remembers only Сияна's name and her
  telescope. It must not repeat Earth's tier-1 arrival line.
- **One memory per world, five in all.** Each is its own element inside the page art. It lights up when the world is
  `completed`, the same flag as the unlock (`src/scenes/storybook-scene.ts:80`), and tapping it opens a card: a textless
  vignette of Сияна at the eyepiece, plus one line of at most two short sentences. Memories never gate and never add
  companion speech inside a level.
- **Back cover:** one companion line quoting Сияна: the sky is best when you show it to someone. Ticket 009's role-flip
  lines follow it. It is not a memory and carries no astronomy of its own; it frames back-cover claims 1–4.

**The five memories.** Each brings a fact its level does not already teach, VERIFIED in `docs/sources.md` under
"Companion memories (ticket 012)":

| World | Memory | Guard |
| ----- | ------ | ----- |
| Earth | After sunset, facing east: a dark blue-grey band with a pink glow above it, Earth's own shadow | never "Belt of Venus"; no Moon in the vignette; the shadow stays low in the east; "on clear evenings", never "every evening" |
| Moon | Beside a bright star, the Moon crept closer over the evening: it moves east among the stars, so it rises later each night | always „спрямо звездите"; no duration; the star is drawn on the Moon's east side |
| Mars | Mars brightened week after week, then faded, as it came closer and then moved away | „седмица след седмица", never "night after night"; „избледня", never „угасна"; no oval orbit; no magnitudes; not "brighter than Jupiter"; the cause reuses R1a |
| Jupiter | A tiny black dot crawled across Jupiter: a moon's shadow, a solar eclipse as seen from Jupiter's clouds | the dot is the shadow; "in the clouds", never "on the surface"; "this telescope", never "small" |
| Saturn | With the rings wide open, a thin dark line through them, with fewer pieces there | „по-малко на брой", never a bare „по-малко"; never "empty" (NOT ATTESTED); "this telescope", never "small"; undated |

On Mars, the owner answered "pick the previous recommended option", read as the brightening only. The dust storm stays
in the research file as the runner-up.

**Sourcing** (`docs/sources.md`):

- "Companion memories (ticket 012)" holds claims 1–5 as VERIFIED, and claim 6, "the Cassini Division is empty", as
  NOT ATTESTED.
- "Story lines — fiction, not claims" says Сияна and the companion are invented. Each line points at the VERIFIED row
  its astronomy rests on, and the section carries the pedagogy wording rules.
- The RETIRED status joins the vocabulary, as ticket 005 defined it.
- The "how far people have travelled" anchor is RETIRED (Q22), because no astronaut appears.

**Vignettes:** the astronomy in each is hand-drawn from a cited reference image, or is real processed photography,
never AI-generated, and each gets an imagery entry. See the map's "Imagery and data" fog.

**Map changes:**

- The finish bar gains the story's acceptance lines.
- The build notes gain the story follow-ups.
- The #25 fog patch is cleared: no post-Earth level needs per-latitude constellation visibility (Q23; checked against
  tickets 004, 006 and 011).
- The finale input now says it means finding Сияна.
- The README premise is rewritten, which also drops Кумова слама, cut by ADR 0005.

