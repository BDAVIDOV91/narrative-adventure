import { fileURLToPath, URL } from 'node:url';

import { defineConfig } from 'vitest/config';

/**
 * The TypeScript regression suite (CLAUDE.md rule 5). Python has pytest; this
 * is its counterpart, and until it existed rule 5 was unenforceable on any
 * `.ts` file.
 *
 * `happy-dom` rather than `jsdom`: the only browser surfaces this suite needs
 * are `localStorage`, `requestAnimationFrame` and `devicePixelRatio`, and
 * happy-dom supplies all three for 7 packages where jsdom costs ~30. On a
 * machine budgeted at ~1.9 GB free (rule 9) the lighter runner is the one that
 * still runs while a dev server and a browser are open.
 *
 * Consequence, accepted deliberately: **puzzle solve and tolerance logic lives
 * in pure modules importable without a Phaser `Scene`.** Phaser needs a real
 * canvas and a WebGL context, so anything that reaches into a Scene is not unit
 * testable here and gets verified by playing it instead. Keep the arithmetic
 * out of the Scene and this suite can guard it.
 */
export default defineConfig({
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('src', import.meta.url)),
      '@content': fileURLToPath(new URL('content', import.meta.url)),
    },
  },
  test: {
    environment: 'happy-dom',
    include: ['src/**/*.test.ts'],
    restoreMocks: true,
  },
});
