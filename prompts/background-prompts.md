# Background, Storybook Page & UI Prompts

Covers the storybook page art (the level-select book), level backgrounds, and UI
elements. Generator: **Nano Banana Pro**

## Consistency requirement

The book is the spine of the whole game — every page must look like it came from
the same volume. Record the shared style anchor here once and reuse the exact
wording in every page prompt rather than re-describing the style each time.

> _(style anchor to be written after the first approved page render)_

## Cyrillic warning

Any generated art containing **text** is a trap: image generators reliably
mangle Cyrillic. Generate art *without* text and render all Bulgarian strings at
runtime from `content/bg/` in a Cyrillic-capable font. Never bake a word into an
image.

## Format

```
### <scene or element>
- **File**: assets/images/generated/<file>.webp
- **Date**: YYYY-MM-DD
- **Prompt**: <exact prompt string>
- **Notes**: <retries, what to avoid>
```

## Entries

_(none yet)_
