# 0008 — The companion's lost memory of an astronomer replaces the dimming-star mystery

- **Status**: accepted
- **Date**: 2026-09-26
- **Supersedes**: the dimming-star premise in `README.md` and the 09-08 handoff
  ("The dimming-star mystery is flavour only", round 1, item 3)

## Context

The game's pitch has a tiny AI companion inside an old telescope, and "something is
dimming a star". The star was never designed. It would also be interstellar,
which rule 6 keeps out of v1. Ticket 009 (Q13) gave the owner's seed for a story
instead: the companion lost its partner, lost its memory in the grief, and
remembers again as the child explores. Wayfinder ticket 012 had to turn that seed
into a story. Four things pulled against it:

- the fiction wall: no child may take the story for history;
- rule 1: a memory must carry astronomy (in the spirit of ADR 0005);
- the 09-09 companion tiers, and ADR 0007's rule of no counters and no new state;
- ticket 009's rules: the back cover is not tappable, and nothing teases an unbuilt
  world.

## Decision

- The tiny AI stays in the old telescope. The telescope belonged to **Сияна**, a
  fictional amateur astronomer who watched the sky from her yard in Bulgaria.
  She has a first name only.
- They were **separated**. v1 never says why.
- **One memory per world**, five in all. A memory returns when that world is
  `completed`, the same flag that unlocks the next page. It lives in its own lit
  element inside the page art, and tapping the element opens a card: a textless
  vignette of Сияна at the eyepiece, with one memory line. Each memory brings one
  new fact that is VERIFIED in `docs/sources.md`:
  - Earth's shadow rising at dusk;
  - the Moon walking east among the stars;
  - Mars brightening week after week;
  - a moon's shadow crossing Jupiter;
  - the thin dark line in Saturn's rings.
- Memory lines are past, undated recollections in the companion's first person.
  The companion's own forms stay gender-neutral, and lines addressed to the child
  avoid gendered forms.
- A storybook **intro** shows only while no level has a solved marker: the
  companion remembers only her name and her telescope.
- The **back cover** carries one companion line, with Сияна quoted in the present
  tense (the past would read as a eulogy): the sky is best when you show it to someone. Ticket 009's role flip follows, and the child shows
  the companion the real sky. The v1 story ends complete there.

The lasting rules:

- Story lines are fiction. They are listed in `docs/sources.md` under "Story lines",
  and each one points at the VERIFIED row its astronomy rests on.
- Memories never gate, never add companion speech inside a level, and add no stored
  state.
- The astronomy in a vignette is hand-drawn from a cited reference image, or is real
  processed photography, never AI-generated.

## Why

- **Astronomer, not astronaut.** An astronaut needs near-future fiction (a first
  crewed Mars mission) that a child could take as history, and a date-sensitive
  anchor ("no one past the Moon"). An astronomer's memories are real observing
  nights a child can repeat from Bulgaria. That fits the back cover's
  "go and look yourself". The anchor is now RETIRED.
- **Separation, not death.** Death is heavy for a learning game, and a post-v1 "help
  the companion" finale makes little sense with it. Separation leaves the finale
  something to find. Leaving the separation unstated forever was rejected: the
  finale would have nothing to resolve.
- **Memories carry new facts rather than repeating the level.** This was the owner's
  pick over a reuse-only set. It costs verification, and that has been paid: all
  five facts are VERIFIED.
- **The back-cover line is not a sixth memory.** It carries no astronomy, and the
  back cover cannot be tapped (ticket 009). As a framing line it introduces claims
  that are already VERIFIED.
- **An open hook on the back cover was rejected.** It would tease unbuilt content,
  which ticket 009 Q7 forbids.
- **A real observatory or a dated event was rejected.** The first invents a staff
  member at a real institution; the second puts a date in front of the player
  (rule 2) and goes stale.

## Consequences

- Each world page gains one element and one vignette, inside the page art, so
  ticket 009's 360px no-scroll layout still holds. There is one intro key, one
  back-cover line and five memory keys, probably in a new content bundle. That
  bundle needs its import in `src/shared/content.ts`.
- The memory element, the next page's unlock and the back cover all read the one
  `completed` flag. It is written once, when `meetsThreshold` first holds, and
  never cleared.
- Each vignette needs an imagery entry in `docs/sources.md`. The Earth vignette shows
  no Moon, which keeps it away from the phases-by-shadow misconception.
- The README premise is rewritten, and the dimming star is gone.
- The post-v1 finale (finding Сияна, and why they parted) belongs to the
  whole-solar-system map. v1 does not tease it.

## When to revisit

- Play-testing shows that children never open a memory, or read the separation as a
  death and are upset by it.
- The post-v1 map designs the finale, and it needs the separation's cause to be
  seeded earlier.
- The worldwide English version: Сияна's name and the Bulgarian setting get swapped,
  not translated (ADR 0003 amendment).
