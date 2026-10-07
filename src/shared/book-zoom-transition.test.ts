import { describe, expect, it, vi } from 'vitest';

import { zoomIntoPage, zoomOutToBook } from './book-zoom-transition';

import type { Scene } from 'phaser';

/** Only the camera and the clock: the two things the zoom touches. */
function stubScene() {
  const camera = {
    pan: vi.fn(),
    zoomTo: vi.fn(),
    setZoom: vi.fn(),
    centerOn: vi.fn(),
  };
  const time = { delayedCall: vi.fn() };
  const scene = { cameras: { main: camera }, time } as unknown as Scene;
  return { scene, camera, time };
}

const PAGE = { x: 150, y: 320 };
const HOME = { x: 512, y: 384 };

describe('zoomIntoPage', () => {
  it('pans and zooms onto the page, then continues after the duration', () => {
    const { scene, camera, time } = stubScene();
    const done = vi.fn();
    zoomIntoPage(scene, PAGE, done, 700, false);
    expect(camera.pan).toHaveBeenCalledWith(150, 320, 700, 'Cubic.easeInOut');
    expect(camera.zoomTo).toHaveBeenCalledWith(4, 700, 'Cubic.easeInOut');
    expect(time.delayedCall).toHaveBeenCalledWith(700, done);
    expect(done).not.toHaveBeenCalled();
  });

  it('reduced motion: an instant cut, with no tween and no timer', () => {
    const { scene, camera, time } = stubScene();
    const done = vi.fn();
    zoomIntoPage(scene, PAGE, done, 700, true);
    expect(done).toHaveBeenCalledOnce();
    expect(camera.pan).not.toHaveBeenCalled();
    expect(camera.zoomTo).not.toHaveBeenCalled();
    expect(time.delayedCall).not.toHaveBeenCalled();
  });
});

describe('zoomOutToBook', () => {
  it('starts magnified on the page it came from, then pans home while zooming out', () => {
    const { scene, camera, time } = stubScene();
    const done = vi.fn();
    zoomOutToBook(scene, PAGE, HOME, done, 500, false);
    expect(camera.setZoom).toHaveBeenCalledWith(4);
    expect(camera.centerOn).toHaveBeenCalledWith(150, 320);
    // Recentres on the book, not just zoomTo(1): otherwise the book ends off-centre (CF A1/B3).
    expect(camera.pan).toHaveBeenCalledWith(512, 384, 500, 'Cubic.easeInOut');
    expect(camera.zoomTo).toHaveBeenCalledWith(1, 500, 'Cubic.easeInOut');
    expect(time.delayedCall).toHaveBeenCalledWith(500, done);
  });

  it('reduced motion: the book at zoom 1, centred, at once, with no tween and no timer', () => {
    const { scene, camera, time } = stubScene();
    const done = vi.fn();
    zoomOutToBook(scene, PAGE, HOME, done, 500, true);
    expect(camera.setZoom).toHaveBeenLastCalledWith(1);
    expect(camera.centerOn).toHaveBeenLastCalledWith(512, 384);
    expect(done).toHaveBeenCalledOnce();
    expect(camera.pan).not.toHaveBeenCalled();
    expect(camera.zoomTo).not.toHaveBeenCalled();
    expect(time.delayedCall).not.toHaveBeenCalled();
  });
});
