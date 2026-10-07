import { prefersReducedMotion } from './reduced-motion';

import type { Scene } from 'phaser';

/**
 * The storybook page-zoom: a page grows until it fills the screen, then the
 * level scene starts. Reversed on the way back out.
 *
 * Placeholder look — the real one needs the painted page art. Reduced motion
 * (owner, 2026-10-07) is an instant cut: no pan, no zoom, no timer.
 */

export interface ZoomTarget {
  readonly x: number;
  readonly y: number;
}

const EASE = 'Cubic.easeInOut';
const PAGE_ZOOM = 4;

export function zoomIntoPage(
  scene: Scene,
  target: ZoomTarget,
  onComplete: () => void,
  durationMs = 700,
  reduced = prefersReducedMotion(),
): void {
  if (reduced) {
    onComplete();
    return;
  }
  scene.cameras.main.pan(target.x, target.y, durationMs, EASE);
  scene.cameras.main.zoomTo(PAGE_ZOOM, durationMs, EASE);
  scene.time.delayedCall(durationMs, onComplete);
}

/**
 * Called from the book's `create` on the way back from a level: start magnified on the page the child left, then pan
 * home while zooming out, so the book ends centred (`zoomTo(1)` alone would leave it offset on that page).
 */
export function zoomOutToBook(
  scene: Scene,
  from: ZoomTarget,
  home: ZoomTarget,
  onComplete: () => void,
  durationMs = 500,
  reduced = prefersReducedMotion(),
): void {
  const camera = scene.cameras.main;
  if (reduced) {
    camera.setZoom(1);
    camera.centerOn(home.x, home.y);
    onComplete();
    return;
  }
  camera.setZoom(PAGE_ZOOM);
  camera.centerOn(from.x, from.y);
  camera.pan(home.x, home.y, durationMs, EASE);
  camera.zoomTo(1, durationMs, EASE);
  scene.time.delayedCall(durationMs, onComplete);
}
