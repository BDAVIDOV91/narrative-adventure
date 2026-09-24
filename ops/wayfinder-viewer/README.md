# Read-only wayfinder viewer

A visual view (Graph / Board / Fog / Map doc) of the decision maps in `docs/wayfinder/`. The viewer is the mentor's
Node app. It is third-party code and lives OUTSIDE this repo, in `~/tools/wayfinder-viewer/`.
`wayfinder-view.mjs` is our front for it and the only way we run it. Ported from `pdf_data_extractor_v2`
(`ops/wayfinder-viewer/kna-view.mjs`) on 2026-09-24.

This is local dev tooling. It lives outside `src/`, Vite never bundles it, and the game still makes zero network
requests (CLAUDE.md rule 8).

## Run it (owner, in your own terminal)

```bash
npm run wayfinder                                    # http://127.0.0.1:7777 (steps up if busy)
node ops/wayfinder-viewer/wayfinder-view.mjs --port 7800
xdg-open http://127.0.0.1:7777
```

Stop it with Ctrl-C or `kill <pid>` (the pid is printed). Never `pkill -f` from the Bash tool: it kills its own shell.

## What the wrapper guarantees (each line has a test in `wayfinder-view.test.mjs`)

- Every non-GET/HEAD request answers **405** before the viewer's code runs. The launch buttons still render; they
  show "The wayfinder viewer is read-only". Launching a session from the page would start a second session on the
  one working tree, which the RAM budget cannot hold.
- Websocket upgrades are destroyed. The viewer's terminal gateway is removed.
- Pages carry a CSP without inline script. The viewer puts a ticket's `type` into `innerHTML` unescaped, and research
  tickets are written by agents that read external text.
- It binds `127.0.0.1` only. `--host` and `--root` are refused: the viewer's websocket is a shell.
- Nothing is written to `$HOME` or `$TMPDIR`.

## Test

```bash
npm run test:ops     # node --test on the FILE: `node --test <dir>` runs zero tests and exits 0
```

The test **never skips**: on a machine without `~/tools/wayfinder-viewer` (or `$WAYFINDER_VIEWER_DIR`) it fails, and
so does any commit that stages `ops/` (`.husky/pre-commit` runs it). Install the viewer first.

## Install or reinstall

The installed copy at `~/tools/wayfinder-viewer/` was reviewed and installed for `pdf_data_extractor_v2` on
2026-09-17 and is shared by both repos. Its procedure lives in that repo's `ops/wayfinder-viewer/README.md`
("Install or reinstall"): copy only `server.mjs`, `README.md`, `lib/`, `public/` from the mentor's drop
(`~/Desktop/hope_for_win/viewer/.viewer/`), hand-write a `package.json` whose single dependency is `"ws": "8.21.2"`,
`npm ci --ignore-scripts`, and verify `public/vendor/` against the official xterm tarballs. Never copy its
`node_modules`, `package.json` (it declares `node-pty` and a `postinstall`) or `scripts/`.
