import { describe, expect, it } from 'vitest';

import { arrivalKey, companionStages } from './companion-tiers';

describe('companionStages', () => {
  it('Earth speaks in three tiers: arrival, nudge, fact', () => {
    expect(companionStages(3)).toEqual(['arrival', 'nudge', 'fact']);
  });

  it('every later level drops the arrival line and keeps nudge and fact', () => {
    expect(companionStages(2)).toEqual(['nudge', 'fact']);
  });
});

describe('arrivalKey', () => {
  it("names a marker's arrival line when the level speaks one and the line exists", () => {
    expect(arrivalKey(3, 'earth-sundial')).toBe('companion.earth-sundial.arrival');
  });

  it('is undefined on a two-tier level, even if a line were authored', () => {
    expect(arrivalKey(2, 'earth-sundial')).toBeUndefined();
  });

  it('is undefined for a marker whose line arrives with its engine', () => {
    expect(arrivalKey(3, 'earth-telescope-focus')).toBeUndefined();
  });
});
