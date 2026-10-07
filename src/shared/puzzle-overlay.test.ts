import { describe, expect, it, vi } from 'vitest';

import { openPuzzleOverlay } from './puzzle-overlay';

import type { Scene } from 'phaser';

/** Any Phaser game object: every method chains, and the few fields the layout reads exist. */
function fakeObject(): unknown {
  const target = { height: 20, input: { hitArea: { setTo: vi.fn() } } };
  const proxy: unknown = new Proxy(target, {
    get: (object, key): unknown =>
      Reflect.has(object, key) ? (Reflect.get(object, key) as unknown) : () => proxy,
  });
  return proxy;
}

function stubScene() {
  const shutdown: (() => void)[] = [];
  const scale = { width: 1280, height: 720, on: vi.fn(), off: vi.fn() };
  const tweens = { add: vi.fn() }; // never completes: as if the scene stopped mid-fade
  const events = {
    once: vi.fn((name: string, handler: () => void) => {
      if (name === 'shutdown') shutdown.push(handler);
    }),
    off: vi.fn(),
  };
  const add = { rectangle: fakeObject, text: fakeObject };
  const scene = { add, scale, tweens, events } as unknown as Scene;
  const stop = (): void => {
    for (const handler of shutdown) handler();
  };
  return { scene, scale, stop };
}

const CONTENT = { title: 'T', body: 'B', closeLabel: 'C' };

describe('puzzle overlay cleanup', () => {
  it('a scene that stops mid fade-out still takes the resize listener with it (perf-report, 2026-10-07)', () => {
    const { scene, scale, stop } = stubScene();
    const callbacks = { onSolved: vi.fn(), onClosed: vi.fn() };
    const overlay = openPuzzleOverlay(scene, CONTENT, callbacks, false);
    const layout = scale.on.mock.calls[0]?.[1] as unknown;
    expect(scale.on).toHaveBeenCalledWith('resize', layout);

    overlay.close(); // starts the 200 ms fade, whose onComplete never runs
    stop(); // the scene shuts down mid-fade

    expect(scale.off).toHaveBeenCalledWith('resize', layout);
  });

  it('reduced motion closes at once and removes the listener exactly once', () => {
    const { scene, scale, stop } = stubScene();
    const callbacks = { onSolved: vi.fn(), onClosed: vi.fn() };
    openPuzzleOverlay(scene, CONTENT, callbacks, true).close();
    stop();
    expect(scale.off).toHaveBeenCalledTimes(1);
    expect(callbacks.onClosed).toHaveBeenCalledOnce();
  });
});
