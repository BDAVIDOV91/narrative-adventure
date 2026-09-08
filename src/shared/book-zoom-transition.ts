import type { Scene } from 'phaser';

/**
 * The storybook page-zoom: a page grows until it fills the screen, then the
 * level scene starts. Reversed on the way back out.
 *
 * Placeholder implementation — the real one needs the painted page art. The
 * signature is settled so scenes can already call it.
 */

export interface ZoomTarget {
  readonly x: number;
  readonly y: number;
}

export function zoomIntoPage(
  scene: Scene,
  target: ZoomTarget,
  onComplete: () => void,
  durationMs = 700,
): void {
  scene.cameras.main.pan(target.x, target.y, durationMs, 'Cubic.easeInOut');
  scene.cameras.main.zoomTo(4, durationMs, 'Cubic.easeInOut');
  scene.time.delayedCall(durationMs, onComplete);
}

export function zoomOutToBook(scene: Scene, onComplete: () => void, durationMs = 500): void {
  scene.cameras.main.zoomTo(1, durationMs, 'Cubic.easeInOut');
  scene.time.delayedCall(durationMs, onComplete);
}
