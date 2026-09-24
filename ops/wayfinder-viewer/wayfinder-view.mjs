#!/usr/bin/env node
/**
 * Read-only front for the mentor's wayfinder viewer (owner decision 2026-09-17).
 *
 * Ported from pdf_data_extractor_v2 (2026-09-24). The viewer is third-party code kept OUTSIDE
 * this repo, in ~/tools/wayfinder-viewer (override: WAYFINDER_VIEWER_DIR). We want its Graph /
 * Board / Fog / Map views over docs/wayfinder/, and none of its side effects: its launch routes
 * type commands into terminals, its websocket is a shell, and a session it started would be a
 * second session on the one working tree.
 *
 * Nothing in the viewer's own files is edited. This wrapper imports its server and:
 *   1. answers 405 to every non-GET/HEAD request BEFORE third-party code runs. The effect stubs
 *      below are not enough on their own: a chart launch writes a note into $TMPDIR, and a
 *      session close clears state, before the stubbed effect is ever reached;
 *   2. destroys every websocket upgrade (the viewer's own gateway is removed);
 *   3. adds a CSP without inline script to every page. The viewer puts a ticket's `type` into
 *      innerHTML unescaped, and research tickets are written by agents that read external text.
 *      /raw responses keep the stricter CSP the viewer sets itself;
 *   4. binds 127.0.0.1 only and refuses --host and --root: the websocket is a shell;
 *   5. never writes ~/.wayfinder-viewer.json (the viewer's main() is never called).
 *
 * Usage: npm run wayfinder  (or: node ops/wayfinder-viewer/wayfinder-view.mjs [--port 7777])
 * Stop it with Ctrl-C, or `kill <pid>`. Never `pkill -f`: from the Bash tool that kills its own shell.
 * Regression test: node --test ops/wayfinder-viewer/wayfinder-view.test.mjs
 */
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(HERE, '..', '..');
const DEFAULT_ROOT = path.join(REPO_ROOT, 'docs', 'wayfinder');
const HOST = '127.0.0.1';
const DEFAULT_PORT = 7777;
const READ_METHODS = new Set(['GET', 'HEAD']);

export const resolveViewerDir = () =>
  process.env.WAYFINDER_VIEWER_DIR || path.join(os.homedir(), 'tools', 'wayfinder-viewer');

const refuse = (name) => async () => {
  throw new Error(`${name} refused: the wayfinder viewer is read-only`);
};

/** Defence in depth behind the 405 gate: every effect that opens, attaches or kills a shell refuses. */
export const REFUSING_EFFECTS = Object.freeze({
  hasTmux: async () => false,
  openSession: refuse('openSession'),
  openTerminal: refuse('openTerminal'),
  attachTerminal: refuse('attachTerminal'),
  closeSession: refuse('closeSession'),
});

/** sha256 sources for the inline scripts in the viewer's shell page, so the CSP can name them. */
function inlineScriptHashes(viewerDir) {
  const html = fs.readFileSync(path.join(viewerDir, 'public', 'index.html'), 'utf8');
  return Array.from(
    html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi),
    (match) => `'sha256-${createHash('sha256').update(match[1], 'utf8').digest('base64')}'`,
  );
}

function contentSecurityPolicy(viewerDir) {
  return [
    "default-src 'self'",
    `script-src ${["'self'", ...inlineScriptHashes(viewerDir)].join(' ')}`,
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data:",
    "connect-src 'self'",
    "object-src 'none'",
    "base-uri 'none'",
    "form-action 'none'",
    "frame-ancestors 'none'",
  ].join('; ');
}

/**
 * The viewer's server with the read-only gate in front of it. Not yet listening: the caller binds
 * it, and must bind 127.0.0.1.
 */
export async function createReadOnlyViewer({
  root = DEFAULT_ROOT,
  viewerDir = resolveViewerDir(),
} = {}) {
  const entry = path.join(viewerDir, 'server.mjs');
  if (!fs.existsSync(entry)) {
    throw new Error(
      `the wayfinder viewer is missing at ${viewerDir} (set WAYFINDER_VIEWER_DIR). ` +
        'Install steps: ops/wayfinder-viewer/README.md',
    );
  }
  const { createViewerServer } = await import(pathToFileURL(entry).href);
  const server = createViewerServer({
    host: HOST,
    port: 0,
    root: path.resolve(root),
    effects: REFUSING_EFFECTS,
  });

  const inner = server.listeners('request');
  server.removeAllListeners('request');
  server.removeAllListeners('upgrade');
  server.on('upgrade', (_req, socket) => socket.destroy());

  const csp = contentSecurityPolicy(viewerDir);
  server.on('request', (req, res) => {
    if (!READ_METHODS.has(req.method)) {
      req.resume();
      const body = JSON.stringify({ error: 'The wayfinder viewer is read-only' });
      res.writeHead(405, {
        allow: 'GET, HEAD',
        'content-type': 'application/json; charset=utf-8',
        'content-length': Buffer.byteLength(body),
        'cache-control': 'no-store',
      });
      res.end(body);
      return;
    }
    /** Defaults only: headers the viewer passes to writeHead (the /raw CSP) win over these. */
    res.setHeader('content-security-policy', csp);
    res.setHeader('x-content-type-options', 'nosniff');
    res.setHeader('referrer-policy', 'no-referrer');
    for (const listener of inner) listener.call(server, req, res);
  });
  return server;
}

function parseCli(argv) {
  let port = DEFAULT_PORT;
  for (let i = 0; i < argv.length; i += 1) {
    const [flag, inline] = argv[i].split(/=(.*)/s, 2);
    if (flag === '--port') {
      port = Number(inline ?? argv[(i += 1)]);
      if (!Number.isSafeInteger(port) || port < 1024 || port > 65535)
        throw new Error('--port must be 1024-65535');
    } else if (flag === '--host' || flag === '--root') {
      throw new Error(
        `${flag} is not allowed: the viewer binds ${HOST} and reads docs/wayfinder only`,
      );
    } else {
      throw new Error(`unknown argument: ${argv[i]}`);
    }
  }
  return { port };
}

function listen(server, port, attemptsLeft = 20) {
  return new Promise((resolve, reject) => {
    const onError = (error) => {
      server.off('listening', onListening);
      if (error.code === 'EADDRINUSE' && attemptsLeft > 0)
        resolve(listen(server, port + 1, attemptsLeft - 1));
      else reject(error);
    };
    const onListening = () => {
      server.off('error', onError);
      resolve(port);
    };
    server.once('error', onError);
    server.once('listening', onListening);
    server.listen(port, HOST);
  });
}

async function main() {
  const { port: wanted } = parseCli(process.argv.slice(2));
  const server = await createReadOnlyViewer();
  const port = await listen(server, wanted);
  console.log(`Wayfinder viewer (read-only)  http://${HOST}:${port}`);
  console.log(`  root ${DEFAULT_ROOT}`);
  console.log(`  pid  ${process.pid}  (stop: Ctrl-C or kill ${process.pid})`);
  for (const signal of ['SIGINT', 'SIGTERM', 'SIGHUP']) {
    process.once(signal, () => {
      server.closeAllConnections?.();
      server.close(() => process.exit(0));
    });
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    await main();
  } catch (error) {
    console.error(`wayfinder-view: ${error?.message || error}`);
    process.exit(2);
  }
}
