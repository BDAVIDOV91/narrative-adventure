import { expect, test } from '@playwright/test';

import { PREVIEW_ORIGIN } from '../playwright.config';

/**
 * Rule 8: the game makes zero network requests. Any request whose origin is not the preview server fails
 * the suite. `data:` and `blob:` are in-page, not network (Phaser's default textures are data URIs).
 */
test('the book loads without a single request outside the preview origin', async ({ page }) => {
  const outside: string[] = [];
  page.on('request', (request) => {
    const url = request.url();
    if (url.startsWith('data:') || url.startsWith('blob:')) return;
    if (new URL(url).origin !== PREVIEW_ORIGIN) outside.push(url);
  });

  await page.goto('/');
  await expect(page.locator('canvas')).toBeVisible();
  // Give the boot scene and the storybook a moment to request whatever they request.
  await page.waitForLoadState('networkidle');

  expect(outside).toEqual([]);
});
