/**
 * Regression test for the read-only wrapper around the mentor's wayfinder viewer.
 *
 * The viewer is third-party code that lives OUTSIDE this repo, in ~/tools/wayfinder-viewer
 * (override: WAYFINDER_VIEWER_DIR). Its launch routes type commands into terminals and its websocket
 * is a shell. We only want its read views, so the wrapper must make every side effect unreachable:
 *   - any non-GET/HEAD request answers 405 BEFORE third-party code runs (a stubbed effect alone is not
 *     enough: a chart launch writes a note into $TMPDIR before the effect is reached);
 *   - a websocket upgrade is destroyed;
 *   - pages carry a CSP without inline script, because the viewer puts a ticket's `type` into
 *     innerHTML unescaped and research tickets are written by agents that read external text;
 *   - the bind address cannot be changed from 127.0.0.1;
 *   - nothing is written to the home directory.
 *
 * This test guarantees its own environment: it builds its fixture map, and it FAILS LOUD when the
 * viewer directory is missing. It never skips. Run:
 *   node --test ops/wayfinder-viewer/wayfinder-view.test.mjs
 */
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { after, before, test } from 'node:test';
import { fileURLToPath } from 'node:url';

import { REFUSING_EFFECTS, createReadOnlyViewer, resolveViewerDir } from './wayfinder-view.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CLI = path.join(HERE, 'wayfinder-view.mjs');
const NOTES_DIR = path.join(os.tmpdir(), 'wayfinder-viewer-notes');
const RUNTIME_FILE = path.join(os.homedir(), '.wayfinder-viewer.json');
const HOSTILE_TYPE = 'x" onmouseover="alert(1)';

let root;
let server;
let port;
let runtimeFileExistedBefore;

const listNotes = () =>
  fs.existsSync(NOTES_DIR) ? fs.readdirSync(NOTES_DIR).toSorted((a, b) => a.localeCompare(b)) : [];

function request({ method = 'GET', pathname, body, headers = {} }) {
  return new Promise((resolve, reject) => {
    const payload = body === undefined ? null : Buffer.from(JSON.stringify(body));
    const req = http.request(
      {
        host: '127.0.0.1',
        port,
        method,
        path: pathname,
        headers: payload
          ? { 'content-type': 'application/json', 'content-length': payload.length, ...headers }
          : headers,
      },
      (res) => {
        const chunks = [];
        res.on('data', (chunk) => {
          chunks.push(chunk);
        });
        res.on('end', () =>
          resolve({
            status: res.statusCode,
            headers: res.headers,
            text: Buffer.concat(chunks).toString('utf8'),
          }),
        );
      },
    );
    req.on('error', reject);
    req.end(payload ?? undefined);
  });
}

const fixtureTicket = (id, type, blockedBy) =>
  [
    '---',
    `id: "${id}"`,
    `title: Ticket ${id}`,
    `type: ${type}`,
    'status: open',
    'assignee: ""',
    `blocked_by: ${JSON.stringify(blockedBy)}`,
    '---',
    '',
    '## Question',
    '',
    'A question?',
    '',
  ].join('\n');

function writeFixture(dir) {
  const map = path.join(dir, 'demo');
  fs.mkdirSync(path.join(map, 'tickets'), { recursive: true });
  fs.writeFileSync(
    path.join(map, 'MAP.md'),
    [
      '# Demo map',
      '',
      '<!-- wayfinder:map -->',
      '',
      '## Destination',
      '',
      'A fixture.',
      '',
      '## Notes',
      '',
      '## Decisions so far',
      '',
      '## Not yet specified',
      '',
      '- **Something dim** — not sharp yet',
      '',
      '## Out of scope',
      '',
    ].join('\n'),
  );
  fs.writeFileSync(path.join(map, 'tickets', '001-first.md'), fixtureTicket('001', 'grilling', []));
  fs.writeFileSync(
    path.join(map, 'tickets', '002-hostile.md'),
    fixtureTicket('002', HOSTILE_TYPE, ['001']),
  );
}

before(async () => {
  const viewerDir = resolveViewerDir();
  assert.ok(
    fs.existsSync(path.join(viewerDir, 'server.mjs')),
    `the wayfinder viewer is missing at ${viewerDir} (set WAYFINDER_VIEWER_DIR). ` +
      'This test never skips: see ops/wayfinder-viewer/README.md to install it.',
  );
  runtimeFileExistedBefore = fs.existsSync(RUNTIME_FILE);
  root = fs.mkdtempSync(path.join(os.tmpdir(), 'wayfinder-view-test-'));
  writeFixture(root);
  server = await createReadOnlyViewer({ root });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  port = server.address().port;
});

after(async () => {
  if (server) {
    server.closeAllConnections?.();
    await new Promise((resolve) => server.close(resolve));
  }
  if (root) fs.rmSync(root, { recursive: true, force: true });
});

test('the read views still work: the fixture map is listed and parsed', async () => {
  const index = await request({ pathname: '/api/maps' });
  assert.equal(index.status, 200);
  assert.deepEqual(
    JSON.parse(index.text).maps.map((map) => map.slug),
    ['demo'],
  );

  const map = JSON.parse((await request({ pathname: '/api/map/demo' })).text);
  assert.deepEqual(
    map.tickets.map((ticket) => [ticket.id, ticket.state]),
    [
      ['001', 'frontier'],
      ['002', 'blocked'],
    ],
  );
});

test('every POST route answers 405 before third-party code runs', async () => {
  const notesBefore = listNotes();
  const bodies = {
    '/api/open': { intent: 'chart', title: 'New map', idea: 'long idea '.repeat(200) },
    '/api/session': { slug: 'demo', ticketId: '001' },
    '/api/session/close': { session: 'wf-demo-001' },
    '/api/notify': { token: 'x', session: 'wf-demo-001', event: 'waiting' },
  };
  for (const [pathname, body] of Object.entries(bodies)) {
    const res = await request({ method: 'POST', pathname, body });
    assert.equal(res.status, 405, `${pathname} must be refused by the front gate`);
    assert.match(String(res.headers.allow), /GET/);
  }
  assert.deepEqual(
    listNotes(),
    notesBefore,
    'a refused chart launch must not write a note into $TMPDIR',
  );
});

test('PUT and DELETE are refused too', async () => {
  for (const method of ['PUT', 'DELETE', 'PATCH']) {
    assert.equal((await request({ method, pathname: '/api/maps' })).status, 405);
  }
});

test('a websocket upgrade is destroyed, never answered', async () => {
  const outcome = await new Promise((resolve) => {
    const req = http.request({
      host: '127.0.0.1',
      port,
      path: '/ws/term?session=wf-demo-001&token=x',
      headers: {
        connection: 'Upgrade',
        upgrade: 'websocket',
        'sec-websocket-key': 'dGhlIHNhbXBsZSBub25jZQ==',
        'sec-websocket-version': '13',
      },
    });
    req.on('upgrade', () => resolve('upgraded'));
    req.on('response', (res) => resolve(`answered ${res.statusCode}`));
    req.on('error', () => resolve('destroyed'));
    req.end();
  });
  assert.equal(outcome, 'destroyed');
});

test('pages carry a CSP with no inline script; the hostile ticket type stays inert', async () => {
  const page = await request({ pathname: '/' });
  assert.equal(page.status, 200);
  const csp = String(page.headers['content-security-policy']);
  const scriptSrc = /script-src ([^;]+)/.exec(csp)?.[1] ?? '';
  assert.match(scriptSrc, /'self'/);
  assert.match(
    scriptSrc,
    /'sha256-[A-Za-z0-9+/=]+'/,
    'the one inline theme script is allowed by hash',
  );
  assert.doesNotMatch(scriptSrc, /unsafe-inline|unsafe-eval|\*|https?:/);
  assert.match(csp, /default-src 'self'/);
  assert.equal(page.headers['x-content-type-options'], 'nosniff');

  /** The viewer does NOT sanitise `type`; that is exactly why the CSP above is load-bearing. */
  const map = JSON.parse((await request({ pathname: '/api/map/demo' })).text);
  assert.equal(map.tickets[1].type, HOSTILE_TYPE.toLowerCase());
});

test('/raw keeps the stricter CSP the viewer sets itself', async () => {
  const raw = await request({ pathname: '/raw/demo/MAP.md' });
  assert.equal(raw.status, 200);
  assert.match(String(raw.headers['content-security-policy']), /default-src 'none'/);
});

test('the effects stubs refuse on their own (defence in depth)', async () => {
  assert.equal(await REFUSING_EFFECTS.hasTmux(), false);
  for (const name of ['openSession', 'openTerminal', 'attachTerminal', 'closeSession']) {
    await assert.rejects(() => REFUSING_EFFECTS[name]({}), /read-only/);
  }
});

test('nothing is written to the home directory', () => {
  assert.equal(fs.existsSync(RUNTIME_FILE), runtimeFileExistedBefore);
});

test('the CLI refuses --host in both spellings, and unknown flags', () => {
  for (const args of [['--host', '0.0.0.0'], ['--host=0.0.0.0'], ['--root', '/tmp'], ['--bogus']]) {
    const run = spawnSync(process.execPath, [CLI, ...args], { encoding: 'utf8', timeout: 15000 });
    assert.notEqual(run.status, 0, `${args.join(' ')} must exit non-zero`);
    assert.match(run.stderr, /not allowed|unknown/i);
  }
});

test('the CLI fails loud when the viewer directory is missing', () => {
  const run = spawnSync(process.execPath, [CLI], {
    encoding: 'utf8',
    timeout: 15000,
    env: {
      ...process.env,
      WAYFINDER_VIEWER_DIR: path.join(os.tmpdir(), 'wayfinder-view-no-such-dir'),
    },
  });
  assert.notEqual(run.status, 0);
  assert.match(run.stderr, /viewer is missing/i);
});
