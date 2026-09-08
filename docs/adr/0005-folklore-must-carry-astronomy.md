# 0005 — Astrophysics is the lesson; folklore is a bonus that must carry it

- **Status**: accepted
- **Date**: 2026-09-08

## Context

The brief weaves Bulgarian folklore through the game as "flavor, not core
mechanics". Two folklore beats were named: Зорница/Вечерница for Venus, and
Кумова слама for the Milky Way.

Verifying them against real ethnography turned up something more useful than a
pair of corrections. **Both claims in the brief were factually wrong** — the
Зорница kinship detail is unattested, and "кум" was mistranslated as "groom"
(it is the godfather) with the tale's central theft omitted entirely. But the
two beats also failed in different ways, and the difference is the decision
worth recording.

## Decision

**The astronomy and astrophysics are the lesson. Folklore is a bonus layer.**

A folklore beat earns its place only when **learning the folklore and learning
the astronomy are the same act.** If the story can be removed without the
astronomy lesson changing, it is decoration — keep it as texture if it is
charming, but it must not occupy a puzzle.

## Why

Apply the test to the two beats the brief named:

**Зорница / Вечерница passes.** Folk tradition treats them as two different
stars. They are one planet. The folklore _creates_ the misconception and the
astronomy _resolves_ it — the child cannot learn the story without confronting
the science. This is the model.

**Кумова слама fails.** The tale is about a man stealing straw from his
кръстник and being cursed for it. It is authentic, it is well attested, and
children like it — but a child who learns it has learned nothing about the Milky
Way. The story and the science sit side by side without touching.

No Bulgarian variant fixes this. Попова слама, Пато and the
milk-of-the-moon version all fail the same test. **The fix is not folklore, it is
Galileo**: the eye says a smear, the telescope says stars.

Two more beats were found that pass the test:

- **Лъжи керван** (Sirius) — the Зорница pattern running backwards. There the
  folklore splits one object into two; here it fuses two into one. Same physics
  resolves both, and a child who solved the Venus puzzle already owns the tool.
- **Квачката** (the Pleiades) — the folk name is a hen with 6–7 chicks, so it
  _encodes the naked-eye count_. Nobody has to be told the number; the name is
  the number, and the telescope then breaks it open into dozens.

## Consequences

- `docs/sources.md` gains a status vocabulary entry, **NOT ATTESTED**, for claims
  investigated and found unsupported — so a rejected idea is not re-proposed by
  the next person who finds it appealing. Two entries already use it: "Косери"
  for Orion, and **Стожер** for the Pole Star.
- Кумова слама is removed from the game. The name and the corrected tale stay
  recorded in `sources.md` so the research is not lost.
- The kinship detail is **not told at all**. Two authoritative sources conflict
  (ИЕФЕМ–БАН says both are the Sun's sisters; Георгиева says Зорница accompanies
  the Sun and Вечерница the Moon, hedged as "според някои вярвания"). The game
  says only that folk tradition calls them sisters, which both support.
- Folklore content is written **attached to a lesson**, never as a standalone
  fact string.

## The trap this guards against

An appealing folk metaphor that turns out not to exist. **Стожер** — the pole at
the centre of a threshing floor that everything turns around — would be a
beautiful and astronomically apt folk name for the celestial pole. It was
proposed during design with real confidence.

It is not attested. Речник на българския език (ИБЕ–БАН) records no astronomical
sense for the word, and **стожари** is attested for the _Pleiades_ — the opposite
slot. No Bulgarian folk name for Polaris was found in any source consulted.

The metaphor may still be used as _the game's own picture_ ("небето се върти като
харман около кол"). It must never be presented as a folk name. A wrong folk name
in a Bulgarian children's game is precisely the error this audience will catch.

## When to revisit

If a folklore beat is proposed that passes the test above and is traceable to a
named ethnographic source, it belongs in the game. The bar is the test, not a
fixed list.

Acquiring ИЕФЕМ–БАН's _Звездното небе: митология и наука_ (2026) would settle the
Зорница kinship conflict and the Mizar/Alcor "влахче" question. Deferred — the
beats currently in the game are all citable without it.
