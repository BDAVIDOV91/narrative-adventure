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
