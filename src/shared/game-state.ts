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

/**
 * How many markers the player has solved in a level, required or not.
 *
 * Display only — "you have found 3 things here". It is deliberately NOT the
 * threshold numerator: pairing this count with a required-only denominator is
 * the arithmetic hole `meetsThreshold` exists to close.
 */
export function solvedCount(progress: GameProgress, levelId: string): number {
  return progress.levels[levelId]?.solved.length ?? 0;
}

/** The shape `meetsThreshold` needs from a level's marker list. */
export interface ThresholdMarker {
  readonly id: string;
  readonly required?: boolean;
}

/**
 * Markers that count toward the unlock threshold.
 *
 * `required` defaults to true: an author who says nothing gets the safe
 * reading, not a level that unlocks itself.
 */
export function requiredMarkerIds(markers: readonly ThresholdMarker[]): readonly string[] {
  return markers.filter((marker) => marker.required !== false).map((marker) => marker.id);
}

/**
 * The brief's forgiving gate: a level unlocks the next one at `threshold`
 * (0.7 for open levels, 1.0 for the two guided ones). Kept as data, not code,
 * so both level kinds run through this one function.
 *
 * The fraction is over the REQUIRED markers, and the numerator is `solved`
 * intersected with `required`. Counting every solved marker against a
 * required-only denominator would let a child unlock a guided level by
 * finishing optional puzzles and never touching the causal spine — which
 * dissolves "guided" entirely.
 *
 * This mirrors `meets_threshold` in `data/scripts/validate-levels.py`, which is
 * the canonical definition. The two must not drift.
 */
export function meetsThreshold(
  progress: GameProgress,
  levelId: string,
  markers: readonly ThresholdMarker[],
  threshold: number,
): boolean {
  const required = requiredMarkerIds(markers);
  if (required.length === 0) return false;
  const solved = new Set(progress.levels[levelId]?.solved);
  const met = required.filter((id) => solved.has(id)).length;
  return met / required.length >= threshold;
}
