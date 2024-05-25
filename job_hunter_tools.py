import os
from enum import Enum
from re import L
from typing import Dict, List, TypedDict, Union
from urllib.parse import urljoin, urlparse

from playwright.async_api import ElementHandle, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from job_hunter_llm_utils import get_job_search_element
from print_utils import print_if_not_empty, print_var_name_value


class WebElement:
    class Selector(Enum):
        ANCHOR = "a"
        BUTTON = "button"
        INPUT = "input"

    class Metadata(TypedDict):
        label: str
        url: str
        description: str


async def search_software_roles(page: Page):
    """SEARCH for software engineer roles in the
    company's career page.

    Args:
        page (Page): _description_
    """
    # TODO: Error handle cases where
    # there are no search inputs. Eg - Notion!
    try:
        await page.wait_for_selector(WebElement.Selector.INPUT.value, timeout=10000)

        search_elements = await page.query_selector_all(WebElement.Selector.INPUT.value)

        print_var_name_value(search_elements)

        search_elements_map: Dict[str, ElementHandle] = {}
        for search_element in search_elements:
            search_element_html_str = str(
                await search_element.get_property("outerHTML")
            )
            search_elements_map[search_element_html_str] = search_element

        print_var_name_value(search_elements_map)
        # TODO: Prompt the LLM to return empty output if none of the
        # input elements are relevant for job search
        job_search_element_key = get_job_search_element(
            list(search_elements_map.keys())
        )
        # TODO: Add error handling
        # Case 1: Hallucination: If the LLM returns a job_search_element_key
        # that is not in the search_elements_map, teach the LLM that it is hallucinating
        # and tell it to pick an input element from the provided list
        # Case 2: Misdirection: LLM picks an input element from the examples. Tell the
        # LLM that it picked an input element from the list and tell it to pick
        # an input element from the user provided list.

        # TODO: Memory
        # How can the LLM learn to pick search elements better by relying
        # on past examples?

        # TODO: Collect examples
        # As the LLM performs this task, collect a list of input elements
        # and output. This will be useful for fine tune data modelling

        # TODO: Use Langchain Prompt Template (Few Shot)
        # and Output parsing for greater control

        print_var_name_value(job_search_element_key)

        job_search_element = search_elements_map[job_search_element_key]

        await job_search_element.type("Software")
        await job_search_element.press("Enter")
    except PlaywrightTimeoutError:
        print("Timeout! Page does not have search")


async def fetch_web_element_metadata(
    page: Page, selector: WebElement.Selector
) -> List[WebElement.Metadata]:
    """Extracts metadata of anchor (<element> </element>) elements
    from the web page

    Args:
        page (Page):
            page to extract anchor elements.
    """

    elements: List[ElementHandle] = await page.query_selector_all(selector.value)
    elementsMetadata: List[WebElement.Metadata] = []
    for element in elements:
        label = await element.inner_text()
        href = await element.get_attribute("href")
        url = get_absolute_url(page, href)

        sub_elements = await element.query_selector_all(":scope > *")
        description = ""
        for sub_element in sub_elements:
            try:
                description += await sub_element.inner_text()
            except:
                ...
        elementsMetadata.append(
            WebElement.Metadata(label=label, url=url, description=description)
        )
    return elementsMetadata


def is_web_element_related_to_software_engineering_role(
    web_element: WebElement,
) -> bool: ...


async def take_screenshot(page: Page, screenshot_path, full_page=False):
    """
    Takes a screenshot of the given Playwright page.

    Args:
        page (Page): The Playwright page object.
        screenshot_path (str): The path to save the screenshot file.
        full_page (bool, optional): Whether to capture the full scrollable page. Defaults to False.
        quality (int, optional): The quality of the screenshot (0-100). Defaults to 100.

    Returns:
        bool: True if the screenshot was taken successfully, False otherwise.
    """
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

        # Take the screenshot
        await page.screenshot(path=screenshot_path, full_page=full_page)
        print(f"Screenshot saved to: {screenshot_path}")
        return True
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return False


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
