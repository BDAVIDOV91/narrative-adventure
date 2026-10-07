import { beforeEach, describe, expect, it, vi } from 'vitest';

import { loadProgress, type GameProgress } from './game-state';
import { commitSolve, recordSolve } from './progress-write';

const MARKERS = [
  { id: 'earth-sundial', required: true },
  { id: 'earth-day-night-spin', required: true },
  { id: 'earth-orbit-year', required: false },
];
const EMPTY: GameProgress = { version: 1, levels: {} };

describe('recordSolve', () => {
  it('adds the marker to the level without touching the input', () => {
    const next = recordSolve(EMPTY, 'earth', 'earth-sundial', MARKERS, 1);
    expect(next.levels['earth']).toEqual({ solved: ['earth-sundial'], completed: false });
    expect(EMPTY.levels).toEqual({});
  });

  it('is idempotent: solving the same marker twice records it once', () => {
    const once = recordSolve(EMPTY, 'earth', 'earth-sundial', MARKERS, 1);
    const twice = recordSolve(once, 'earth', 'earth-sundial', MARKERS, 1);
    expect(twice.levels['earth']?.solved).toEqual(['earth-sundial']);
  });

  it('completes the level once the required markers meet the threshold', () => {
    let progress = recordSolve(EMPTY, 'earth', 'earth-sundial', MARKERS, 1);
    progress = recordSolve(progress, 'earth', 'earth-day-night-spin', MARKERS, 1);
    expect(progress.levels['earth']?.completed).toBe(true);
  });

  it('never completes a guided level on an optional marker alone', () => {
    const progress = recordSolve(EMPTY, 'earth', 'earth-orbit-year', MARKERS, 1);
    expect(progress.levels['earth']?.completed).toBe(false);
  });

  it('never un-completes a level', () => {
    const done: GameProgress = {
      version: 1,
      levels: { earth: { solved: ['earth-sundial', 'earth-day-night-spin'], completed: true } },
    };
    // A later edit to the level's markers must not take a finished page away from a child.
    const next = recordSolve(done, 'earth', 'earth-orbit-year', [...MARKERS, { id: 'new-one' }], 1);
    expect(next.levels['earth']?.completed).toBe(true);
  });

  it('leaves other levels alone', () => {
    const other: GameProgress = {
      version: 1,
      levels: { moon: { solved: ['m1'], completed: false } },
    };
    const next = recordSolve(other, 'earth', 'earth-sundial', MARKERS, 1);
    expect(next.levels['moon']).toEqual({ solved: ['m1'], completed: false });
  });
});

describe('commitSolve: bug 4, progress is actually written', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('a solve survives a fresh load from storage', () => {
    commitSolve('earth', 'earth-sundial', MARKERS, 1);
    expect(loadProgress().levels['earth']?.solved).toEqual(['earth-sundial']);
  });

  it('builds on what is already stored', () => {
    commitSolve('earth', 'earth-sundial', MARKERS, 1);
    const after = commitSolve('earth', 'earth-day-night-spin', MARKERS, 1);
    expect(after.levels['earth']?.completed).toBe(true);
    expect(loadProgress().levels['earth']?.completed).toBe(true);
  });

  it('still returns the new progress when storage throws, so the session plays on', () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('quota');
    });
    vi.spyOn(console, 'warn').mockImplementation(() => {});
    const after = commitSolve('earth', 'earth-sundial', MARKERS, 1);
    expect(after.levels['earth']?.solved).toEqual(['earth-sundial']);
  });
});
