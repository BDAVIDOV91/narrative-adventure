/**
 * Progress lives in localStorage only — no account, no server, no sync.
 * Every access is wrapped: localStorage throws outright in some privacy modes,
 * and a child's browser clearing site data must not crash the game.
 */

const STORAGE_KEY = 'narrative-adventure:progress:v1';

export interface LevelProgress {
  /** Marker ids the player has solved. */
  readonly solved: readonly string[];
  readonly completed: boolean;
}

export interface GameProgress {
  readonly version: 1;
  readonly levels: Readonly<Record<string, LevelProgress>>;
}

const EMPTY: GameProgress = { version: 1, levels: {} };

export function loadProgress(): GameProgress {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw === null) return EMPTY;
    const parsed: unknown = JSON.parse(raw);
    if (
      typeof parsed === 'object' &&
      parsed !== null &&
      'version' in parsed &&
      parsed.version === 1
    ) {
      return parsed as GameProgress;
    }
    return EMPTY;
  } catch {
    return EMPTY;
  }
}

export function saveProgress(progress: GameProgress): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  } catch {
    // Storage full or blocked. The session still plays; progress just is not kept.
    console.warn('[game-state] progress could not be saved');
  }
}

export function solvedCount(progress: GameProgress, levelId: string): number {
  return progress.levels[levelId]?.solved.length ?? 0;
}

/**
 * The brief's forgiving gate: a level unlocks the next one at `threshold`
 * (0.7 for open levels, 1.0 for the two guided ones). Kept as data, not code,
 * so both level kinds run through this one function.
 */
export function meetsThreshold(solved: number, total: number, threshold: number): boolean {
  if (total <= 0) return false;
  return solved / total >= threshold;
}
