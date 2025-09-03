import { chromium } from "playwright";

import type { Browser } from "playwright";

let browser: Browser | null = null;

const getBrowser = async (): Promise<Browser> =>
  browser ?? (browser = await chromium.launch());

const closeBrowser = async (): Promise<void> => await browser?.close();

export { getBrowser, closeBrowser };
