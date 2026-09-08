# 0003 — Bulgarian is the only locale in v1, but nothing is hardcoded

- **Status**: accepted
- **Date**: 2026-09-08

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
