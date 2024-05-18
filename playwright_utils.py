from enum import Enum
from typing import List, TypedDict, Union
from urllib.parse import urljoin, urlparse

from playwright.async_api import ElementHandle, Page

from print_utils import print_if_not_empty


class WebElement:
    class Selector(Enum):
        ANCHOR = "a"
        BUTTON = "button"

    class Metadata(TypedDict):
        label: str
        url: str
        description: str


async def fetch_web_element_metadata(page: Page, selector: WebElement.Selector):
    """Extracts metadata of anchor (<element> </element>) elements
    from the web page

    Args:
        page (Page):
            page to extract anchor elements.
    """
    elements: List[ElementHandle] = await page.query_selector_all(selector.value)
    for element in elements:
        label = await element.inner_text()
        href = await element.get_attribute("href")
        url = get_absolute_url(page, href)
        print_if_not_empty(
            label,
            url,
        )
        sub_elements = await element.query_selector_all(":scope > *")
        for sub_element in sub_elements:
            try:
                t = await sub_element.inner_text()
                if t is not "":
                    print_if_not_empty(t)
            except:
                ...


def get_absolute_url(page: Page, url: Union[str, None]) -> str:
    """Gets the absolute url relative to the page

    Args:
        page (Page): page
        relative_url (_type_): _description_

    Returns:
        str: absolute url
    """
    if url == None:
        return ""

    def is_absolute_url(url) -> bool:
        """Checks if the url is absolute

        Args:
            url (str): url

        Returns:
            bool: if url is absolute
        """
        return bool(urlparse(url).netloc)

    if is_absolute_url(url):
        return url

    return urljoin(page.url, url)
