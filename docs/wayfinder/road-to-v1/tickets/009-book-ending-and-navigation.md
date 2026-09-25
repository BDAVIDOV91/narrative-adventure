---
id: "009"
title: The book's ending and navigation
type: grilling
status: open
assignee: ""
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
