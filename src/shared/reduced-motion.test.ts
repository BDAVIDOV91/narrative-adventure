import { describe, expect, it } from 'vitest';

import { prefersReducedMotion } from './reduced-motion';

type MatchMediaHost = Parameters<typeof prefersReducedMotion>[0];

function host(matchMedia: unknown): MatchMediaHost {
  return { matchMedia } as unknown as MatchMediaHost;
}

describe('prefersReducedMotion', () => {
  it('is true when the player asked the system for reduced motion', () => {
    const query: string[] = [];
    const reduced = prefersReducedMotion(
      host((q: string) => {
        query.push(q);
        return { matches: true };
      }),
    );
    expect(reduced).toBe(true);
    expect(query).toEqual(['(prefers-reduced-motion: reduce)']);
  });

  it('is false when they did not', () => {
    expect(prefersReducedMotion(host(() => ({ matches: false })))).toBe(false);
  });

  it('is false when matchMedia does not exist', () => {
    expect(prefersReducedMotion(host(undefined))).toBe(false);
  });

  it('is false when matchMedia throws', () => {
    expect(
      prefersReducedMotion(
        host(() => {
          throw new Error('blocked');
        }),
      ),
    ).toBe(false);
  });
});
