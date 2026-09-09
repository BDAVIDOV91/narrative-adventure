# 0003 — Bulgarian is the only locale in v1, but nothing is hardcoded

- **Status**: accepted
- **Date**: 2026-09-08
- **Amended**: 2026-09-09 — see "What does not translate" below

## Context

The game is for Bulgarian children. The brief also wants it "culturally
reskinnable for other countries later." Those pull in opposite directions: the
first says ship one language, the second says do not paint yourself in.

## Decision

Bulgarian is the only locale that exists. There is no language switcher and no
English UI. But **no player-facing string lives in a `.ts` file** — everything
resolves through `src/shared/content.ts` to `content/bg/*.json`.

Content **keys** stay ASCII (`puzzle.earth.sundial.label`) so code and grep stay
readable. **Values** are Cyrillic.

## Why

Retrofitting i18n means touching every scene. Doing it now costs one indirection
and buys the reskin the brief asks for. Shipping two languages in v1 costs
translation effort with no user.

## Consequences

- `schemas/level-data.schema.json` enforces an ASCII pattern on content keys, so
  a Cyrillic literal in level data fails validation. There is a test for this.
- **Fonts must cover Cyrillic.** Many stylized storybook display fonts are
  Latin-only and render every string as blank boxes. Verify coverage — including
  Bulgarian glyph forms, since some Cyrillic fonts default to Russian shapes —
  before adopting a font. If bitmap fonts are used, the atlas needs the Cyrillic
  block baked in. Current stack is verified present on the dev machine
  (`fc-list :lang=bg`).
- **Never bake text into generated art.** Image generators mangle Cyrillic.
  Generate art without text; render strings at runtime.
- Bulgarian runs longer than English. UI containers wrap and grow; no
  fixed-width text boxes.
- Astronomy terms use standard Bulgarian forms, not literal translations. See
  [`sources.md`](../sources.md).

## Amendment, 2026-09-09 — what does not translate

The owner confirmed the intent behind the brief's "reskinnable later": once the
game is finished, **add English and make it a worldwide education game.** That
does not change v1 — Bulgarian-only still ships, with no switcher — but it settles
that this ADR records **scope, not permanent architecture**. A future locale is a
new directory under `content/`, not a refactor, which is what the indirection
above was bought for.

The part that does **not** survive translation is the folklore.

Зорница/Вечерница, Квачката, Ралица, Колата and Лъжи керван carry the astronomy
precisely because a Bulgarian child already half-knows them. Зорница works
because the folk belief in two sister stars _is_ the misconception the orbit then
resolves — that is why it passes [ADR 0005](0005-folklore-must-carry-astronomy.md)
where Кумова слама failed. Rendered in English for a child who has never heard of
Зорница, the beat carries no prior belief to overturn, and becomes a decorative
anecdote — exactly what ADR 0005 exists to reject.

So a worldwide version **rewrites those specific puzzles around its own culture's
sky stories**; it does not translate ours. The astronomy underneath is universal
and reskins cleanly. The folklore layer is the seam that has to be re-cut.

This is also why folklore is a **bonus layer and never the driver**: the goal is
Bulgarian children getting interested in astronomy and physics, and a design that
leans on folklore is a design that has to be rebuilt for every new audience.
