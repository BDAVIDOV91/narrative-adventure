---
id: "005"
title: Where imagery and reference-data work sits
type: grilling
status: closed
assignee: owner
blocked_by: ["003"]
---

## Question

Where do the asset and data rows handed over by road-to-v1's struck "Imagery and data per level" patch
(`road-to-v1/MAP.md:106-137`, v1-spec §6) sit among the phases?

- **Imagery:**
  - the NASA textures (Earth first);
  - per-marker page art;
  - the M9, R3, PIA19400, J1, J7, Ganymede, Mercury and J4 frames;
  - PIA06230 and PIA20016;
  - Earth's telescope-Saturn art;
  - the back-cover vignettes and ribbon;
  - the five Сияна vignettes.
- **Reference data:**
  - the radius rows;
  - the Galilean periods and orbit radii;
  - the rotation rows;
  - the ring radii;
  - `saturn-ring-geometry.json` and its render test;
  - the `surface-gravity.json` trim or re-document.
- **Sources:** each image's `docs/sources.md` imagery entry.

Decide:

- whether each item rides in its level's phase, or batches into asset phases;
- which items need the owner's hands (downloads, licensing, hand-drawing), as checklists;
- where placeholder art is allowed, and the phase by which it is replaced. Placeholder art is allowed at the finish bar;
  AI-generated astronomy never is.

Ticket 003's Resolution (decision 8) lists each reference row's first-needing phase; this ticket decides where each is
built. The phase list after Earth is the shell, grid + ribbon, Moon A/B, Mars A/B, Jupiter A/B1/B2, Saturn A/B, back
cover.

## Resolution

Grilled with the owner on 2026-09-27 in two rounds, then challenged by two `challenger`s (both revise). Seven challenger
findings went back to the owner. Every answer took the recommended option.

Facts checked first:

- `assets/images/{nasa,nasa/raw,generated}` are empty; `data/reference/` holds only `day-length-sofia.json` and
  `surface-gravity.json`.
- `process-textures.py` only downscales to ≤2048px WebP (`data/scripts/process-textures.py:36-53`), and writes every raw
  file's stem into `assets/images/nasa/` (:49).
- `surface-gravity.json`'s `_readme` says it "feeds the gravity-drop beat" (:6-8); `tests/test_reference_data.py:91-106`
  pins that beat's Moon < Mars < Earth < Jupiter order; E0 deletes the beat (v1-spec :51, :291). Road-to-v1 T005 keeps
  the entries live (`road-to-v1/tickets/005-adr-0006-verdict.md:113`).
- `earth-telescope-focus` rewards `fact.telescope-saturn` (`src/scenes/earth/earth-data.json:148-159`). The 2026–27
  opening is VERIFIED twice: `docs/sources.md:345-350` and the monthly south-face table, claim 4 (:1725), −6.1° to
  −14.4°, negative on every day of the window.
- `docs/sources.md:977-996` says the Sun and Moon look "almost" the same size, with no ratio.
- `docs/sources.md` has no imagery-entry format yet; the only mention is "still needs an imagery entry" (:735).

### Decisions

1. **Reference rows: the first needer builds them.** Each row, its `test_reference_data.py` test and its `sources.md`
   check land in the first-needing phase. Ticket 003 decision 8's table stands, amended:

   | Row                                              | Built in                   |
   | ------------------------------------------------ | -------------------------- |
   | Sun radius, Moon radius (eclipse, M5 annular)    | Moon B (was: Moon in Mars B) |
   | Mars radius                                      | Mars B (R2)                |
   | Galilean periods and orbit radii; Jupiter radius | Jupiter A (J2)             |
   | Jupiter and Earth rotation periods               | Jupiter B1 (J7)            |
   | Ganymede and Mercury radii                       | Jupiter B2 (J3)            |
   | C, B, A ring radii; `saturn-ring-geometry.json`  | Saturn A (S1, S4)          |
   | Titan radius                                     | Saturn B (S3)              |
   | Telescope-Saturn ring angle (decision 9)         | E6                         |
   | `surface-gravity.json` re-document (decision 2)  | E0                         |

   The eclipse and annular discs are sized from radius over the ephemeris `distanceAu` (a Sun distance row only if the
   ephemeris lacks one). Mars B reuses the Moon radius.
2. **`surface-gravity.json` is re-documented in E0, not trimmed.** The prune rewrites the `_readme`: the file backs
   Jupiter's completion line (a content key, not a code reader) and the Moon's hammer-and-feather line. It re-scopes
   test :91's name and docstring. All four rows, the `dropComparison` key and every guard (:109, :125) stay. Any row
   deletion waits for Jupiter B2's plan.
3. **Imagery rides with its first shower; no asset phases.** Each image, its `process-textures.py` run and its
   `sources.md` imagery entry land in the phase whose beat or element first shows it.

   | Image                                  | Phase                                   |
   | -------------------------------------- | --------------------------------------- |
   | NASA Earth texture                     | E2 (ticket 001)                         |
   | Earth's telescope-Saturn picture       | E6, drawn in code (decision 9)          |
   | Per-marker page art                    | E7 (Earth), then each level's B         |
   | Сияна vignettes                        | with each level's memory (E7, each B)   |
   | M5 discs                               | Moon B, drawn from data; a face texture only if M5's plan asks, then a real photo |
   | M9 frames                              | Moon B                                  |
   | R3 disc, PIA19400                      | Mars B                                  |
   | J1 rung-3 frames                       | Jupiter A                               |
   | J7 close-up                            | Jupiter B1                              |
   | Ganymede and Mercury discs; J4 frame   | Jupiter B2                              |
   | PIA06230, PIA20016                     | Saturn B                                |
   | Back-cover vignettes                   | Back cover (the ribbon itself: grid + ribbon) |

4. **Placeholder policy.**
   - Photos are never placeholders: they are real at their phase exit.
   - Drawn art (page elements, Сияна and back-cover vignettes) may ship as a textless, content-free placeholder (a plain
     shape or colour block, no astronomy) until the owner replaces it. Replacement is not a phase exit, and v1 may ship
     with it.
   - Drawn art that shows astronomy is either hand-drawn from a cited reference with an imagery entry, or content-free.
     AI-generated astronomy never.
   - Memory and back-cover text never refers to what a placeholder picture would show.
   - Placeholder back-cover blocks, like real ones, render only for completed worlds. Ticket 009's "no dim placeholder"
     (no picture for an uncompleted world) is a different rule and still holds.
   - A replacement commit adds that picture's `docs/sources.md` imagery entry, copying its guard list (e.g.
     `road-to-v1/tickets/012-companion-story.md:87-95`), so the commit routes to `astronomy-report`.
5. **Owner hands: a checklist one phase early.** Each photo phase's checklist (image, source URL, licence/credit line,
   drop path `assets/images/nasa/raw/`) is handed over in the previous phase's plan, so the files arrive before they're
   needed. E2's stays at E2 entry. Only a phase's exit waits on its files.
6. **Credits.** Images before Saturn B are public-domain NASA/JPL, with the credit in `sources.md` only. A frame whose
   licence needs visible attribution pulls the on-screen credit display forward to its phase, as a named amendment to
   tickets 002 and 003.
7. **Imagery entries and the degrade recipe.**
   - E2, the first image phase, defines the `sources.md` imagery-entry format: one stable id per committed file.
   - Moon B, with M9, adds a degrade mode to `process-textures.py`: a committed per-image recipe (source, blur/resolution,
     output name). A raw file with a recipe row is processed only by its recipe, so no full-resolution twin lands.
   - Moon B's pytest checks that every committed WebP under `assets/images/` has an imagery entry, without needing the
     gitignored `raw/`.
   - Mars B (R3) and Jupiter A (J1) add recipe rows only. If M9 needs no degrade (real amateur photos), the mode moves
     to Mars B.
8. **Placeholder tracking is data.** Page-element, vignette and back-cover entries map to an image through data, with
   `placeholder: true`. A test asserts:
   - nothing under `assets/images/nasa/` is a placeholder;
   - every flagged entry is on the list `qa-report` prints at each milestone;
   - no flagged entry has an imagery entry.

   The owner swaps a placeholder by editing data, not code.
9. **Telescope-Saturn is drawn in code in E6** (amends ticket 001's E6).
   - A 2D ball and ring ellipse, south face, blurred and sharpened by the `telescope-focus` engine.
   - Its angle is a `data/reference/` row: the cited window (claim 4, `docs/sources.md:1725`) and the angle drawn. A
     pytest checks the angle is negative (south face) and inside the window.
   - E6's plan states the orientation convention (north up or telescope-inverted) and which ring arc crosses in front
     of the globe, checked against a cited reference image.
   - The drawing is rendered to a runtime texture, so the engine takes a texture key per rung from E6 on; J1, M9 and R3
     add bitmap rungs without reshaping it.
   - Saturn A reuses the row, not the drawing (S1 is a model, not a telescope view). Its exit adds a test that
     `saturn-ring-geometry.json` agrees with the row.
   - No bitmap, no placeholder, no owner hands.

Handed on:

- **Ticket 006**: `qa-report` prints the `placeholder: true` list at every milestone; the placeholder test and the
  imagery-entry test run with the suite from the phase that adds them.
- **Ticket 008** folds in:
  - `surface-gravity.json` re-documented in E0 (amends ticket 001's E0 and ticket 003 decision 8);
  - the ring-angle row and the code-drawn Saturn in E6 (amends ticket 001's E6);
  - Sun and Moon radii in Moon B (amends ticket 003 decision 8);
  - the imagery-entry format in E2;
  - the degrade recipe and the imagery test in Moon B;
  - photo checklists one phase early;
  - public-domain-only images before Saturn B.
