# Settled — do not re-research

Each was resolved against a real source and recorded in `docs/sources.md`.
Re-running these costs time and proves nothing new.

## Resolved, with the answer

- **Orion's Belt — the brief was exactly inverted.** Alnilam is the brightest AND
  the only single star; Mintaka is faintest with five components.
  Oplištilová et al., A&A 704, A204 (2025).
- **Mizar/Alcor is the `zoom-split-star` target**, not a belt star — Ursa Major is
  circumpolar from Bulgaria, Orion is winter-only. Separation recomputed
  independently: **708.6″ = 11.81′**.
- **Pleiades naked-eye count** reproduced from catalogue data: 6 at V ≤ 5.0, 7
  with Pleione at 5.05. Квачката's folk number is the naked-eye limit.
- **Star catalogue provenance**: HYG v4.4 (CC BY-SA 4.0, Codeberg — the GitHub
  repo is archived with NOASSERTION), 2,851 stars at mag ≤ 5.5, plus Stellarium
  `modern_iau` figures. Every position verified against Hipparcos-2 at build time,
  build fails over 30″.

## Rejected, with the reason

- **IAU/WGSN Naked Eye Catalog is corrupt** — 15 stars with wrong RA, including
  **Mizar off by 3.2°**. It passes every bounds check, which is why the generator
  now verifies against Hipparcos-2 instead.
- **Albireo is DISPUTED — do not use.**
- **Alioth is brightest in UMa but must never become a player task** — the margin
  over Dubhe is 0.05 mag, invisible.
- **Кумова слама was cut** — a moral tale about theft that teaches nothing about
  the Milky Way (ADR 0005). Also "кум" is the godfather, not the groom.

## NOT ATTESTED — never re-propose

- **"Косери"** for Orion.
- **"Стожер"** for the Pole Star — appealing metaphor, but ИБЕ–БАН records no
  astronomical sense for the word.
- **"вълк" = η UMa** — see [[bulgarian-folk-figures]].

## Still open, non-blocking

- **Galilean moon periods from JPL** — the last NEEDS SOURCE. Task #20, not on the
  critical path.
