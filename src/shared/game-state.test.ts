import { beforeEach, describe, expect, it, vi } from 'vitest';

import {
  loadProgress,
  meetsThreshold,
  requiredMarkerIds,
  saveProgress,
  solvedCount,
  type GameProgress,
  type ThresholdMarker,
} from '@/shared/game-state';

/**
 * The Earth spine, shortened. Four required markers, two optional — the same
 * shape as `src/scenes/earth/earth-data.json`, which is what makes the hole
 * these tests close reachable in the shipping level.
 */
const EARTH_MARKERS: readonly ThresholdMarker[] = [
  { id: 'earth-sundial', required: true },
  { id: 'earth-day-night-spin', required: true },
  { id: 'earth-seasons-globe', required: true },
  { id: 'earth-day-length', required: true },
  { id: 'earth-moon-phase', required: false },
  { id: 'earth-gravity-drop', required: false },
];

function progressWith(solved: readonly string[]): GameProgress {
  return { version: 1, levels: { earth: { solved, completed: false } } };
}

describe('requiredMarkerIds', () => {
  it('treats a marker with no `required` key as required', () => {
    // The safe reading: an author who says nothing does not get a level that
    // unlocks itself. Matches validate-levels.py:required_marker_ids.
    expect(requiredMarkerIds([{ id: 'a' }, { id: 'b', required: false }])).toEqual(['a']);
  });

  it('keeps only the required markers, in level order', () => {
    expect(requiredMarkerIds(EARTH_MARKERS)).toEqual([
      'earth-sundial',
      'earth-day-night-spin',
      'earth-seasons-globe',
      'earth-day-length',
    ]);
  });
});

describe('meetsThreshold', () => {
  it('unlocks a guided level when every required marker is solved', () => {
    const progress = progressWith([
      'earth-sundial',
      'earth-day-night-spin',
      'earth-seasons-globe',
      'earth-day-length',
    ]);
    expect(meetsThreshold(progress, 'earth', EARTH_MARKERS, 1)).toBe(true);
  });

  it('does NOT unlock a guided level from optional markers alone', () => {
    // The arithmetic hole this function exists to close: counting every solved
    // marker against a required-only denominator lets a child finish the two
    // optional puzzles, never touch the causal spine, and still pass a 1.0
    // gate. The numerator is `solved` INTERSECTED WITH `required`.
    const progress = progressWith(['earth-moon-phase', 'earth-gravity-drop']);
    expect(meetsThreshold(progress, 'earth', EARTH_MARKERS, 1)).toBe(false);
  });

  it('does not let optional markers pad a partial spine over an open gate', () => {
    // Two of four required solved is 0.5, under the 0.7 open-level gate. The
    // two optional solves must not carry it over the line.
    const progress = progressWith([
      'earth-sundial',
      'earth-day-night-spin',
      'earth-moon-phase',
      'earth-gravity-drop',
    ]);
    expect(meetsThreshold(progress, 'earth', EARTH_MARKERS, 0.7)).toBe(false);
  });

  it('ignores a solved id that names no marker in this level', () => {
    const progress = progressWith(['earth-sundial', 'moon-crater-walk']);
    expect(meetsThreshold(progress, 'earth', EARTH_MARKERS, 0.25)).toBe(true);
    expect(meetsThreshold(progress, 'earth', EARTH_MARKERS, 0.5)).toBe(false);
  });

  it('is false for a level with no required markers rather than dividing by zero', () => {
    // validate-levels.py rejects such a level at build time; the runtime still
    // must not answer `true` if one ever reaches a browser.
    const progress = progressWith(['earth-moon-phase']);
    expect(
      meetsThreshold(progress, 'earth', [{ id: 'earth-moon-phase', required: false }], 1),
    ).toBe(false);
  });

  it('is false for a level the player has never opened', () => {
    expect(meetsThreshold({ version: 1, levels: {} }, 'earth', EARTH_MARKERS, 1)).toBe(false);
  });
});

describe('solvedCount', () => {
  it('counts every solved marker, required or not', () => {
    // Display only — "you have found 3 things here". Never a threshold
    // numerator; that is what meetsThreshold is for.
    expect(solvedCount(progressWith(['earth-sundial', 'earth-moon-phase']), 'earth')).toBe(2);
    expect(solvedCount(progressWith([]), 'moon')).toBe(0);
  });
});

describe('storage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('round-trips progress through localStorage', () => {
    const progress = progressWith(['earth-sundial']);
    saveProgress(progress);
    expect(loadProgress()).toEqual(progress);
  });

  it('returns empty progress rather than throwing when storage is unavailable', () => {
    // Private browsing modes make localStorage throw on access. A child's
    // browser doing that must not take the game down.
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('SecurityError');
    });
    expect(loadProgress()).toEqual({ version: 1, levels: {} });
  });

  it('discards stored data that is not this schema version', () => {
    localStorage.setItem('narrative-adventure:progress:v1', JSON.stringify({ version: 99 }));
    expect(loadProgress()).toEqual({ version: 1, levels: {} });
  });
});

function store(value: unknown): void {
  localStorage.setItem('narrative-adventure:progress:v1', JSON.stringify(value));
}

describe('hand-edited storage', () => {
  // The only untrusted input this game has: its own localStorage, which a
  // curious child with devtools can rewrite. Cheating themselves through a
  // level is harmless in an offline single-player game. Crashing the game to a
  // blank page is not — and `version: 1` plus a cast is all that stood between
  // a mistyped value and `undefined.length`.
  beforeEach(() => {
    localStorage.clear();
  });

  it('drops a level whose solved list is not an array', () => {
    store({ version: 1, levels: { earth: { solved: 5, completed: false } } });
    expect(loadProgress()).toEqual({ version: 1, levels: {} });
  });

  it('drops a level whose solved array holds things that are not marker ids', () => {
    store({ version: 1, levels: { earth: { solved: ['earth-sundial', 7], completed: false } } });
    expect(loadProgress()).toEqual({ version: 1, levels: {} });
  });

  it('drops a level with no completed flag but keeps the levels beside it', () => {
    store({
      version: 1,
      levels: {
        earth: { solved: ['earth-sundial'], completed: true },
        moon: { solved: [] },
      },
    });
    expect(loadProgress()).toEqual({
      version: 1,
      levels: { earth: { solved: ['earth-sundial'], completed: true } },
    });
  });

  it('survives `levels` being something other than an object', () => {
    store({ version: 1, levels: 'nope' });
    expect(loadProgress()).toEqual({ version: 1, levels: {} });
  });

  it('leaves the readers unable to throw on anything it lets through', () => {
    store({ version: 1, levels: { earth: { solved: 3, completed: false } } });
    const progress = loadProgress();
    expect(() => solvedCount(progress, 'earth')).not.toThrow();
    expect(() => meetsThreshold(progress, 'earth', EARTH_MARKERS, 1)).not.toThrow();
    expect(meetsThreshold(progress, 'earth', EARTH_MARKERS, 1)).toBe(false);
  });
});
