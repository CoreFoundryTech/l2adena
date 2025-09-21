import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/L2 Adena/);
});

test('navigation to listings', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Listings');
  await expect(page).toHaveURL(/listings/);
});