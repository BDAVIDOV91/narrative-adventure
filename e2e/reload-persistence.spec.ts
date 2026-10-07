import { expect, test } from '@playwright/test';

/**
 * Progress survives a reload (T006 d4). E1 has no puzzle engine, so nothing can be solved in play yet: the test seeds
 * a finished Earth the way the progress write stores it, reloads, and proves the game reads it without clobbering it.
 * E3 extends this to a played solve (owner, 2026-10-07).
 */
const KEY = 'narrative-adventure:progress:v1';
const SEEDED = JSON.stringify({
  version: 1,
  levels: {
    earth: {
      solved: ['earth-sundial', 'earth-day-night-spin', 'earth-seasons-globe', 'earth-day-length'],
      completed: true,
    },
  },
});

test('a finished Earth is still there after a reload', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('canvas')).toBeVisible();
  // page.evaluate, not addInitScript: an init script would re-seed on every load and prove nothing.
  await page.evaluate(([key, value]) => localStorage.setItem(key, value), [KEY, SEEDED] as const);

  await page.reload();
  await expect(page.locator('canvas')).toBeVisible();

  // The book reads progress in its create(), a few frames after the canvas mounts: watch the key across that window.
  const stored: (string | null)[] = [];
  for (let sample = 0; sample < 6; sample += 1) {
    stored.push(await page.evaluate((key) => localStorage.getItem(key), KEY));
    await page.waitForTimeout(100);
  }
  expect(stored.every((value) => value === SEEDED)).toBe(true);
});
