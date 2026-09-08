# 0004 — Exact dependency pins, and the constraints that chose them

- **Status**: accepted
- **Date**: 2026-09-08

## Context

`.npmrc` sets `save-exact=true` and `engine-strict=true`, so every dependency is
pinned exactly. Several pins are _not_ the latest version, and the reasons are
not obvious from reading the manifest.

## Decision

Record the constraint next to each non-obvious pin, here and in
`requirements.txt`. A pin without a recorded reason gets "helpfully" bumped by a
future reader and breaks something.

## The pins that are not simply "latest"

| Package                  | Pinned | Latest at the time | Constraint                                                                                                                                      |
| ------------------------ | ------ | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `typescript`             | 5.9.3  | 7.0.2              | `typescript-eslint@8.70.0` declares peer `typescript: ">=4.8.4 <6.1.0"`. TS 7 breaks linting outright.                                          |
| `lint-staged`            | 16.2.7 | 17.5.0             | 17.x requires Node `>=22.22.1`; this machine runs 22.17.0. `engine-strict` caught it at install. Also the version `pdf_data_extractor_v2` uses. |
| `phaser`                 | 3.90.0 | 4.2.1              | See [0002](0002-phaser-3-over-phaser-4.md).                                                                                                     |
| `eslint-plugin-import-x` | 4.17.1 | —                  | Replaces `eslint-plugin-import`, which caps at ESLint 9 and cannot load under ESLint 10. Same `import/order` rules under a different prefix.    |

## Consequences

- Bumping TypeScript past 6.1 requires a `typescript-eslint` major first.
- Bumping `lint-staged` requires upgrading Node first.
- `engine-strict=true` stays on. It turned a silent runtime break into an
  install-time error, which is the whole point.

## Python

Pins live in `requirements.txt`, each with its reason inline — the convention
carried over from `pdf_data_extractor_v2`, where every non-obvious pin carries a
comment describing the incident that caused it.
