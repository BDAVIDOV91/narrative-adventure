import { isContentKey, type ContentKey } from './content';

/**
 * The companion's tiers per puzzle (earth-level-brief.md:154, v1-spec :27-29). The count is level data
 * (`companionTiers` in the level JSON), never a branch in code. Earth: arrival (naming the goal, when the puzzle
 * opens), nudge (on a stall), fact (on success). Every later level: nudge and fact.
 */

export type CompanionTiers = 2 | 3;
export type CompanionStage = 'arrival' | 'nudge' | 'fact';

export function companionStages(tiers: CompanionTiers): readonly CompanionStage[] {
  return tiers === 3 ? ['arrival', 'nudge', 'fact'] : ['nudge', 'fact'];
}

/**
 * The arrival line for a marker, or undefined when the level has no arrival tier or the line is not written yet
 * (E1 authors the four required Earth markers; the rest arrive with their engines, owner 2026-10-07).
 */
export function arrivalKey(tiers: CompanionTiers, markerId: string): ContentKey | undefined {
  if (!companionStages(tiers).includes('arrival')) return undefined;
  const key = `companion.${markerId}.arrival`;
  return isContentKey(key) ? key : undefined;
}
