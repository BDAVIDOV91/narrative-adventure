import { defineConfig, devices } from '@playwright/test';

/**
 * The E1 suite (T004, T006 d4-d6): the production build under `vite preview`, one worker, the headless shell.
 * It runs on the M2 at every phase exit; on M1 only behind mem-guard with the dev server stopped (T006 d6).
 *
 * 127.0.0.1, not localhost: Node 22 may resolve localhost to ::1 only, and the zero-network test compares
 * every request against this one exact origin (CF B8).
 */
export const PREVIEW_ORIGIN = 'http://127.0.0.1:4173';

export default defineConfig({
  testDir: './e2e',
  workers: 1,
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  // No HTML report: nothing to serve, nothing to open (CF privacy).
  reporter: 'list',
  use: {
    baseURL: PREVIEW_ORIGIN,
    serviceWorkers: 'block',
    trace: 'off',
  },
  // No `channel`: headless chromium is the headless shell from `playwright install --only-shell chromium`.
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: 'npm run build && npx vite preview --host 127.0.0.1 --strictPort --port 4173',
    url: PREVIEW_ORIGIN,
    reuseExistingServer: false,
    // tsc + the Phaser chunk can take over a minute on the M1 APU.
    timeout: 180_000,
  },
});
