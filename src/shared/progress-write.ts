import {
  loadProgress,
  meetsThreshold,
  saveProgress,
  type GameProgress,
  type ThresholdMarker,
} from './game-state';

/**
 * The progress write (latent bug 4: `saveProgress` had no caller). A solved puzzle lands here and nowhere else.
 *
 * `recordSolve` also sets `completed` once the level's threshold is met. That is ticket 002 d7's level-complete hook,
 * landed early in E1 (owner, 2026-10-07); E4 proves it in play ("Earth is completable").
 */

/** Pure: the progress after `markerId` is solved. Idempotent, and a completed level stays completed. */
export function recordSolve(
  progress: GameProgress,
  levelId: string,
  markerId: string,
  markers: readonly ThresholdMarker[],
  threshold: number,
): GameProgress {
  const level = progress.levels[levelId] ?? { solved: [], completed: false };
  const solved = level.solved.includes(markerId) ? level.solved : [...level.solved, markerId];
  const withSolve: GameProgress = {
    ...progress,
    levels: { ...progress.levels, [levelId]: { solved, completed: level.completed } },
  };
  const completed = level.completed || meetsThreshold(withSolve, levelId, markers, threshold);
  return { ...progress, levels: { ...progress.levels, [levelId]: { solved, completed } } };
}

/**
 * Load, record, save. Returns the new progress even when storage refuses the write (`saveProgress` swallows that),
 * so the session plays on and only persistence is lost.
 */
export function commitSolve(
  levelId: string,
  markerId: string,
  markers: readonly ThresholdMarker[],
  threshold: number,
): GameProgress {
  const next = recordSolve(loadProgress(), levelId, markerId, markers, threshold);
  saveProgress(next);
  return next;
}
