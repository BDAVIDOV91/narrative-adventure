import { expect, test, type Page } from '@playwright/test';

import { PREVIEW_ORIGIN } from '../playwright.config';

/**
 * The preview smoke (T006 d4): the production build boots with no failed request, no 4xx/5xx inside the preview
 * origin, and no uncaught page error. Each level phase extends it to open its own scene (T006 d5).
 */
function watchProblems(page: Page): string[] {
  const problems: string[] = [];
  page.on('requestfailed', (request) => {
    problems.push(`failed: ${request.url()} (${request.failure()?.errorText ?? '?'})`);
  });
  page.on('response', (response) => {
    if (response.url().startsWith(PREVIEW_ORIGIN) && response.status() >= 400) {
      problems.push(`${String(response.status())}: ${response.url()}`);
    }
  });
  page.on('pageerror', (error) => {
    problems.push(`pageerror: ${error.message}`);
  });
  return problems;
}

/*
 * The favicon. Full Chrome falls back to GET /favicon.ico (a 404 here: no public/ dir), but the headless shell never
 * fetches favicons, so a network check cannot see it (verified on the M2, 2026-10-07). The regression test is the
 * declared icon instead: a data: URI, so it costs zero requests (rule 8).
 */
test('the page declares an inline icon, so no browser asks for /favicon.ico', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('link[rel~="icon"]')).toHaveAttribute('href', /^data:image\/svg\+xml,/);
});

for (const reducedMotion of ['no-preference', 'reduce'] as const) {
  test(`the book boots clean (reduced motion: ${reducedMotion})`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion });
    const problems = watchProblems(page);

    await page.goto('/');
    await expect(page.locator('canvas')).toBeVisible();
    await page.waitForLoadState('networkidle');

    expect(problems).toEqual([]);
  });
}

/*
 * Into Earth and back, through the book zoom (CF A13). The canvas has no DOM to query, so this taps the Earth card
 * where the book lays it out (storybook-scene.ts: 3 pages, 200 px wide, 24 px apart, centred) and asserts the trip
 * raises no error. Level phases extend this to their own scenes (T006 d5).
 */
for (const reducedMotion of ['no-preference', 'reduce'] as const) {
  test(`into Earth and back to the book (reduced motion: ${reducedMotion})`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion });
    const problems = watchProblems(page);
    await page.goto('/');
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    const box = await canvas.boundingBox();
    if (box === null) throw new Error('no canvas box');

    const earthCard = { x: (box.width - 648) / 2 + 100, y: box.height / 2 };
    await canvas.click({ position: earthCard });
    await page.waitForTimeout(1200); // the 700 ms zoom, then Earth's create
    await canvas.click({ position: { x: 40, y: 24 } }); // Earth's back button, top left
    await page.waitForTimeout(900); // the 500 ms zoom out

    expect(problems).toEqual([]);
  });
}
