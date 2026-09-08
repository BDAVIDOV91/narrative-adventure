import facts from '@content/bg/facts.json';
import levels from '@content/bg/levels.json';
import puzzles from '@content/bg/puzzles.json';
import ui from '@content/bg/ui.json';

/**
 * Bulgarian is the only shipped locale in v1. This module is the single seam
 * where that could later become a choice — every player-facing string in the
 * game resolves through `t()`, so no Cyrillic literal ever lives in a scene.
 *
 * Keys stay ASCII so code and grep stay readable; values are Cyrillic.
 */

const bundles = { ...ui, ...levels, ...puzzles, ...facts };

export type ContentKey = keyof typeof bundles;

const strings: Record<string, string | undefined> = bundles;

/** Resolve a content key to its Bulgarian string. */
export function t(key: ContentKey): string {
  const value = strings[key];
  if (value === undefined) {
    // Returning the key rather than throwing keeps a missing string from
    // taking down a level mid-play; it shows up loudly on screen instead.
    console.error(`[content] missing key: ${key}`);
    return key;
  }
  return value;
}

/** Every key that exists, for the build-time completeness check. */
export function allKeys(): readonly string[] {
  return Object.keys(bundles);
}
