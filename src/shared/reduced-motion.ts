/**
 * The one shared reduced-motion check (T001 d6). Every animation the game adds asks this, and each phase's plan says
 * what "reduced" means for its own animations. E1 (owner, 2026-10-07): the book zoom is an instant cut and the puzzle
 * overlay appears in one frame.
 *
 * Read on every call, not cached: the player can flip the system setting while the game is open.
 */

const QUERY = '(prefers-reduced-motion: reduce)';

export function prefersReducedMotion(host: Pick<Window, 'matchMedia'> = window): boolean {
  try {
    if (typeof host.matchMedia !== 'function') return false;
    return host.matchMedia(QUERY).matches;
  } catch {
    // A blocked or broken matchMedia is "no preference", never a crash.
    return false;
  }
}
