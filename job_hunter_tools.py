import os
from enum import Enum
from re import L
from typing import Dict, List, TypedDict, Union
from urllib.parse import urljoin, urlparse

from playwright.async_api import ElementHandle, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from job_hunter_llm_utils import get_job_search_element
from web_element import WebElementType, WebElement
from utils import print_if_not_empty, print_var_name_value, remove_newlines


async def search_software_roles(page: Page):
    """SEARCH for software engineer roles in the
    company's career page.

    Args:
        page (Page): _description_
    """
    # TODO: Error handle cases where
    # there are no search inputs. Eg - Notion!
    try:
        await page.wait_for_selector(WebElementType.INPUT.value, timeout=10000)

        search_elements = await page.query_selector_all(WebElementType.INPUT.value)

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
        # Case 3: LLM determines that none of the search input
        # are for searching software roles

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

        # TODO: Instead of naively typing in 'Software', we should check
        # if the search input has options. For example, https://www.anthropic.com/jobs
        await job_search_element.type("Software")
        await job_search_element.press("Enter")
    except PlaywrightTimeoutError:
        print("Timeout! Page does not have search")


async def fetch_web_element_metadata(
    page: Page, selector: WebElementType
) -> List[WebElement]:
    """Extracts metadata of web elements (eg - anchor (<element> </element>))
    from the page.

    Args:
        page (Page):
            page to extract anchor elements.
    """

    elements: List[ElementHandle] = await page.query_selector_all(selector.value)
    elementsMetadata: List[WebElement] = []
    for element in elements:
        label = await element.inner_text()
        href = await element.get_attribute("href")
        url = get_absolute_url(page, href)

        # Extract metadata of adjacent elements
        # This is useful when we have an <a>'s description
        # in a adjacent div or h2 Eg - https://www.anthropic.com/jobs

        # Get parent element
        parent_element = await element.query_selector("..")

        # If parent exists, get all adjacent elements
        # of element
        adjacent_elements = (
            await parent_element.query_selector_all(":scope > *")
            if parent_element
            else []
        )

        # Extract metadata of sub elements
        child_elements = await element.query_selector_all(":scope > *")

        neighbor_elements = adjacent_elements + child_elements
        description = ""

        for neighbor_element in neighbor_elements:
            tag_name = await neighbor_element.get_property("tagName")
            tag_name_value = await tag_name.json_value()
            # Neighboring elements that are of the same
            # web element type of element is highly likely
            # to not contain useful metadata
            if tag_name_value.lower() != selector.value:
                try:
                    description += await neighbor_element.inner_text() + " "
                except:
                    ...

        elementsMetadata.append(
            WebElement(
                element_type=selector,
                label=remove_newlines(label),
                url=url,
                description=remove_newlines(description),
            )
        )
    return elementsMetadata


def is_web_element_related_to_software_engineering_role(
    web_element: WebElement,
) -> bool: ...


async def take_full_page_screenshots(
    page: Page,
    output_prefix: str,
    viewport_width: int = 1092,
    viewport_height: int = 1092,
):
    """
    Take multiple screenshots to cover the entire web page.

    Args:
        page (Page): The Playwright page object.
        output_prefix (str): The prefix for the screenshot file names.
        viewport_width (int, optional): The viewport width in pixels. Defaults to 1092.
        viewport_height (int, optional): The viewport height in pixels. Defaults to 11092080.
    """
    # Get the height of the rendered page
    height = await page.evaluate("() => document.body.scrollHeight")

    # Set the viewport size
    await page.set_viewport_size(
        viewport_size={"width": viewport_width, "height": viewport_height}
    )

    # Calculate the number of screenshots needed
    num_screenshots = (height // viewport_height) + 1

    # Scroll and capture screenshots
    for i in range(num_screenshots):
        # Scroll to the desired position
        scroll_position = i * viewport_height
        await page.evaluate(f"window.scrollTo(0, {scroll_position})")

        # Capture the screenshot
        screenshot_path = f"screenshots/{output_prefix}_{i}.png"
        await page.screenshot(path=screenshot_path)

    return num_screenshots


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
