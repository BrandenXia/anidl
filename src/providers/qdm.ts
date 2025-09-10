import { getBrowser } from "@/lib/browser";

import type { Browser, Page } from "playwright";
import type { Provider, SResultsSub } from "./base";

const QDM_BASE_URL = "https://qdm.plus";

const animePageId = "anime" as const;
const epPageId = "ep" as const;
type QdmSearchId = { text: string } & (
  | { page: typeof animePageId; link: string }
  | { page: typeof epPageId; link: string }
);

const findAnimes = async (page: Page) => {
  const locator = page.locator("xpath=//*[@id='searchList']/li/div/h4/a");
  const elements = await locator.elementHandles();
  const items = await Promise.all(
    elements.map(async (handle) => ({
      text: await handle.textContent(),
      link: await handle.getAttribute("href"),
    })),
  );
  return items
    .filter(({ text, link }) => text && link)
    .map(({ text, link }) => ({
      text: text?.trim() ?? "",
      page: animePageId,
      link: link?.trim() ?? "",
    }));
};

const findAnimesResult = async (
  browser: Browser,
  page: Page,
): Promise<SResultsSub<QdmSearchId>> => {
  const animes = await findAnimes(page);

  const nextBtn = page.locator("xpath=/html/body/div[1]/div/div/ul/li[6]/a");
  const hasNext = (await nextBtn.count()) > 0;

  return {
    page: "sub",
    results: animes,
    hasNext,
    next: hasNext
      ? await (async () => {
          const link = await nextBtn.getAttribute("href");
          return async () => {
            const newPage = await browser.newPage();
            await newPage.goto(link!);
            return findAnimesResult(browser, newPage);
          };
        })()
      : undefined,
  };
};

export const QdmProvider: Provider<{
  searchId: QdmSearchId;
}> = {
  search: async (query) => {
    const browser = await getBrowser();
    const page = await browser.newPage();
    await page.goto(QDM_BASE_URL);

    const searchBox = page.locator("#wd");
    await searchBox.fill(query);
    await searchBox.press("Enter");

    return findAnimesResult(browser, page);
  },
  query: async (query) => {},
};
