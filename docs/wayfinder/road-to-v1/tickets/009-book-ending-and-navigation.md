---
id: "009"
title: The book's ending and navigation
type: grilling
status: closed
assignee: owner
blocked_by: []
---

## Question

What does the storybook do when the last roster page (Jupiter) is completed, and how does the book lay out its four
pages at narrow and tablet widths?

Settled inputs, not to be re-asked:

- **Page display:** a page comes alive as its markers are solved. Each solved marker lights an element of that page, and
  there is no counter (ticket 008, ADR 0007).
- **Current layout:** a one-row, 200px-per-page layout (`src/scenes/storybook-scene.ts:71-80`). It fits only at about
  900px or wider, and the canvas is `Scale.RESIZE` (`src/main.ts:12`).

Decide:

- the final page or ending, and what it hands the child. It must stay inside rule 6 and point at nothing unbuilt: no
  coming-soon marker;
- the layout below about 900px (wrap, scroll, or page-turn);
- how a returning child sees which pages are open, without a number.

## Resolution

Grilled with the owner on 2026-09-26 (Q1–Q18). Two `challenger` agents both returned "revise" with doc-wording fixes,
folded in below, and the owner answered Q17–Q18. `astronomy-accuracy-checker` verified the back-cover claims.

**The ending is a back cover.**

- **What it is:** a gameplay-free final page, always the book's last. It is **not tappable**: the page itself is the
  ending, and nothing zooms in. Future worlds' pages insert before it.
- **When it opens:** when the last world page is `completed`, the ordinary 0.7 gate. Every optional marker is not
  required: that would be a hidden checklist, a counter by another name (ADR 0007).
- **Stored state:** it is derived from the final world's `completed` flag. In v1 that flag is never written false, so
  the back cover never re-locks, and there is **no new `localStorage` field**. The post-v1 map that inserts worlds
  decides how it stays open.
- **Its art:**
  - textless storybook vignettes, drawn only for completed worlds, with no dim placeholder;
  - they are pictures, not the naked-eye view;
  - a closed back cover is a plain dim cover with no text.
- **No tease:** nothing anywhere points at an unbuilt world.
- **Its companion lines flip roles.** The companion asks the child to show it these worlds in the real sky, ideally
  going out with someone from home. It is 2–3 short lines, reviewed by `puzzle-pedagogy-reviewer` at build. The lines
  name the worlds and use no count word; they never say "tonight". Claims (`docs/sources.md`, "Back cover — seeing
  the worlds with your own eyes"):

| Idea | Status | Wording guard |
| ---- | ------ | ------------- |
| The Moon, Mars, Jupiter and Saturn are naked-eye objects, not every night and not always together | VERIFIED | Saturn is a point of light; its rings only in a telescope frame; never "bright" |
| Away from lights, the eyes adapt and see many more stars | VERIFIED (search excerpt; read Webvision before any duration is used) | no duration shown |
| The planets are always **near** the path the Sun and Moon cross | VERIFIED | "near", never "on"; the art shows a soft band; the word "ecliptic" never shown |
| Planets usually shine more steadily than stars | VERIFIED | „обикновено" must stay |
| "Planets don't twinkle" | NOT ATTESTED | never state it |

**Navigation:**

- **Layout:**
  - Pages wrap into a grid. The column count comes from both width and height, and the header is part of the fit.
    The whole book fits with **no scrolling**, down to **360px portrait**.
  - Tile geometry scales, but text keeps a floor (names about 16px). A tile drops its blurb when the blurb cannot fit
    at its floor.
  - The layout re-runs on Phaser's `resize` event (`Scale.RESIZE`, `src/main.ts:12`).
- **A returning child sees:**
  - open pages bright, with their lit elements (ticket 008);
  - a **bookmark ribbon** on the newest open page (on the back cover once it is open);
  - closed pages dim, showing only the world's name. „Заключено" is dropped. No number anywhere.

**The destination grew: Saturn joins v1** as page 5 at 0.7 (Q5, Q8).

- Ticket 001 is amended.
- Saturn designs on the five kept types only; a revival would reopen 005 in ADR 0006.
- **Saturn is conditional (Q17):** [What Saturn can teach, deep](010-what-saturn-can-teach.md) must find three honest
  required beats, or Saturn returns to post-v1.
- [Saturn level design](011-saturn-level-design.md) is blocked by 010.

**Post-v1 inputs (map Out of scope):**

- **Pluto:** an optional bonus page near Sun + Mercury, outside the unlock chain. It needs a rule 6 amendment first
  (Q6, Q11).
- **The companion finale:** "help the companion", unlocked when the whole solar system is cleared (Q13).

**New ticket:** [The companion's story](012-companion-story.md) (Q13, Q15, Q16). It gates only story and memory lines,
not the 09-09 tier lines. It carries the near-future fiction wall and the VERIFIED anchors. My first anchor, "Apollo
17 was the last crewed lunar mission", was false (Artemis II, April 2026) and is recorded as DISPUTED.

**Build follow-ups, beside the map:**

- Replace the one-row layout (`src/scenes/storybook-scene.ts:71-80`) with the grid above.
- Drop `ui.book.locked` (`content/bg/ui.json:5`).
- Add content keys for the back-cover lines and any bookmark label.
- Keep `level.saturn.name`.
- The back cover is not a level: it has no `-data.json` and no `sceneKey`.
