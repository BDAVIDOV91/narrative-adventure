import { describe, expect, it } from 'vitest';

import { allKeys, t, type ContentKey } from '@/shared/content';

/**
 * Every Bulgarian bundle on disk, discovered rather than listed. `content.ts`
 * hardcodes its imports, so a new file under `content/bg/` is seen by
 * `validate-levels.py` — which globs the directory — and invisible to `t()`.
 * That split passes Python and fails in a child's browser, showing the raw
 * ASCII key on screen. This test is the tripwire.
 */
const bundles = import.meta.glob<Record<string, string>>('../../content/bg/*.json', {
  eager: true,
  import: 'default',
});

describe('content bundles', () => {
  it('finds the bundles on disk at all', () => {
    expect(Object.keys(bundles).length).toBeGreaterThan(0);
  });

  it('exposes every key of every content/bg/*.json through t()', () => {
    const reachable = new Set(allKeys());
    const unreachable: string[] = [];

    for (const [path, bundle] of Object.entries(bundles)) {
      for (const key of Object.keys(bundle)) {
        if (!reachable.has(key)) unreachable.push(`${path} -> ${key}`);
      }
    }

    // A failure here almost always means content.ts needs the new file added
    // to its import list, not that the key is wrong.
    expect(unreachable).toEqual([]);
  });

  it('resolves a key to its Bulgarian string, not to the key', () => {
    const key = allKeys()[0] as ContentKey;
    expect(t(key)).not.toBe(key);
  });

  it('keeps content keys ASCII so code and grep stay readable', () => {
    // ADR 0003: keys ASCII, values Cyrillic. The schema enforces this for keys
    // referenced from level data; this covers the bundles themselves.
    const nonAscii = allKeys().filter((key) => !/^[ -~]+$/.test(key));
    expect(nonAscii).toEqual([]);
  });
});
