import { describe, expect, it } from 'vitest';

/**
 * Tripwires for latent bugs that were "functions with no caller" (2026-09-09 handoff, bugs 4 and 5). The behaviour
 * lives in Phaser scenes, which vitest does not boot (vitest.config.ts), so this guards the wiring at the source
 * level and the dev walk carries the behaviour. Deleting a call site turns this RED.
 */
const sources = import.meta.glob<string>('../scenes/**/*.ts', {
  eager: true,
  query: '?raw',
  import: 'default',
});

function source(path: string): string {
  const text = sources[`../scenes/${path}`];
  if (text === undefined) throw new Error(`no scene source at ${path}`);
  return text;
}

/** A call, not an import or a mention in a comment. */
function calls(text: string, fn: string): boolean {
  return new RegExp(String.raw`(?<![\w.])${fn}\(`).test(
    text.replaceAll(/\/\/.*$/gm, '').replaceAll(/\/\*[\s\S]*?\*\//g, ''),
  );
}

describe('bug 4: progress has a writer', () => {
  it('a level scene commits a solve through the progress write', () => {
    // commitSolve (progress-write.ts) is the one function that calls saveProgress; its own behaviour is unit-tested.
    // This guards the other half: that a scene reaches it at all.
    const scenes = Object.keys(sources).filter((path) => calls(sources[path] ?? '', 'commitSolve'));
    expect(scenes).not.toEqual([]);
  });
});

describe('bug 5: the book zoom has call sites', () => {
  it('a page tap zooms into the page', () => {
    expect(calls(source('storybook-scene.ts'), 'zoomIntoPage')).toBe(true);
  });

  it('returning to the book zooms back out', () => {
    expect(calls(source('storybook-scene.ts'), 'zoomOutToBook')).toBe(true);
  });

  it("Earth's way back tells the book which page it came from", () => {
    expect(source('earth/earth-scene.ts')).toMatch(/returnFrom/);
  });
});
