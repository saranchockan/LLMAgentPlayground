from typing import List
from urllib.parse import urljoin, urlparse

from playwright.async_api import ElementHandle, Page


def is_absolute_url(url):
    return bool(urlparse(url).netloc)


def get_absolute_url(page: Page, relative_url):
    return urljoin(page.url, relative_url)


async def extract_anchor_elements(page: Page):
    links: List[ElementHandle] = await page.query_selector_all("a")
    for link in links:
        label = await link.inner_text()
        href = await link.get_attribute("href")
        url = href if is_absolute_url(href) else get_absolute_url(page, href)
        print(label, url)
