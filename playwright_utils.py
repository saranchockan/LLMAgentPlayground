from typing import Any, List, Union, Tuple
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext, ElementHandle, Page, async_playwright

from utils import is_truthy, print_var_name_value


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


def get_absolute_url(page: Page, url: Union[str, None]) -> Union[str, None]:
    """Gets the absolute url relative to the page

    Args:
        page (Page): page
        relative_url (_type_): _description_

    Returns:
        str: absolute url
    """
    if url == None:
        return None

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


async def extract_all_text_from_web_page(url: str) -> str:
    """
    Asynchronously extracts all text content from a given web page using Playwright and BeautifulSoup.

    Parameters:
    url (str): The URL of the web page from which to extract text.

    Returns:
    str: A single string containing all the text content from the web page, with spaces as separators.

    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Get the full HTML content
        html_content = await page.content()

        # Parse HTML and extract text
        soup = BeautifulSoup(html_content, "html.parser")
        all_text = soup.get_text(separator=" ", strip=True)

        await browser.close()
        return all_text


async def click_and_retrieve_new_tab_url(
    page: Page, element: ElementHandle
) -> Union[str, None]:
    """
    Clicks on a given element while holding the Meta key (Command key on macOS) to open it in a new tab,
    retrieves the URL of the newly opened tab, and then closes the new tab.

    Args:
        page (Page): The current Playwright page object.
        element (ElementHandle): The element handle to be clicked.

    Returns:
        str: The URL of the newly opened tab.

    Raises:
        Exception: If any error occurs during the process, it will be printed to the console.
    """
    try:
        # Expect a new page to be opened
        async with page.context.expect_page(timeout=500) as new_page_info:
            # Click the element with Meta key (Command key on macOS)
            print("Attempting to button")
            await element.click(button="left", modifiers=["Meta"], timeout=1)
            print("Clicked button")

            # Get the new page object
            new_page = await new_page_info.value

            print("Got new page")

            # Get the URL of the new page
            new_tab_url = new_page.url

            print("Got new_tab_url", new_tab_url)

            # Close the new page
            await new_page.close()

            print("Closed new page")

            return new_tab_url
    except Exception as e:
        print(e)


async def get_all_child_elements(
    element: ElementHandle, element_filter: Any
) -> List[ElementHandle]:
    """
    Recursively retrieves all child elements of a given element, excluding elements with a specific tag name.

    This function uses a depth-first search approach to traverse the DOM tree and collect all child elements. It filters out elements with a tag name matching the `element_filter` to avoid collecting potentially
    irrelevant metadata.

    Args:
        element (ElementHandle): The parent element to start the search from.
        element_filter (Any): The tag name to filter out during the search.

    Returns:
        List[ElementHandle]: A list of all child elements found, excluding those with the filtered tag name.
    """
    all_child_elements: List[ElementHandle] = []

    async def helper(
        curr_element: Union[ElementHandle, None],
        all_child_elements: List[ElementHandle],
    ):
        """
        Recursive helper function to traverse the DOM tree and collect child elements.

        Args:
            curr_element (Union[ElementHandle, None]): The current element being processed.
            all_child_elements (List[ElementHandle]): The list to store all found child elements.
        """
        if not curr_element:
            return

        # Query all immediate child elements of the current element
        child_elements: List[ElementHandle] = await curr_element.query_selector_all(
            ":scope > *"
        )

        # Add the found child elements to the list
        all_child_elements += child_elements

        for child_element in child_elements:
            # Get the tag name of the child element
            tag_name = await child_element.get_property("tagName")
            tag_name_value = await tag_name.json_value()

            # Recursively process child elements that don't match the filter
            if tag_name_value != element_filter:
                await helper(child_element, all_child_elements)

    # Start the recursive process from the initia[] element
    await helper(element, all_child_elements)

    return all_child_elements


from typing import Any, List
from playwright.async_api import ElementHandle


async def fetch_neighboring_elements(
    element: ElementHandle, element_filter: Any
) -> List[ElementHandle]:
    """
    Fetches neighboring elements of a given element that match a specified filter.

    This function retrieves all child elements of the parent of the given element
    that match the provided filter, as well as all child elements of the given element
    itself that match the filter.

    Args:
        element (ElementHandle): The reference element whose neighboring elements are to be fetched.
        element_filter (Any): A filter to apply when selecting child elements.

    Returns:
        List[ElementHandle]: A list of ElementHandle objects representing the neighboring elements that match the specified filter.

    """
    parent_element = await element.query_selector("..")
    return (
        await get_all_child_elements(
            element=parent_element, element_filter=element_filter
        )
        if parent_element
        else []
    ) + await get_all_child_elements(element=element, element_filter=element_filter)


async def fetch_elements_description_and_url(
    page: Page,
    elements: List[ElementHandle],
    fetch_urls: bool,
    filter_element_tag_name: Any,
) -> Tuple[List[str], List[str]]:
    """
    Fetches the descriptions and URLs of the given elements on a web page.

    Args:
        page (Page): The Playwright Page object representing the web page.
        elements (List[ElementHandle]): A list of ElementHandle objects representing the elements to process.
        fetch_urls (bool): A flag indicating whether to fetch URLs from the elements.
        filter_element_tag_name (Any): A filter object used to exclude certain elements based on their tag name.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing two lists:
            - descriptions: A list of inner text descriptions of the elements.
            - urls: A list of URLs extracted from the elements' href attributes.

    Description:
        This function iterates over the provided list of elements and performs the following actions:
        1. Retrieves the tag name of each element.
        2. If the tag name does not match the specified filter, it attempts to:
            a. Append the inner text of the element to the descriptions list.
            b. If fetch_urls is True, append the absolute URL (if any) from the element's href attribute to the urls list.
        3. Handles exceptions gracefully by printing error messages if retrieving inner text or href fails.

    """
    print_var_name_value(fetch_urls)
    descriptions: List[str] = []
    urls: List[str] = []

    for element in elements:
        element_tag_name = await (await element.get_property("tagName")).json_value()

        if element_tag_name.lower() != filter_element_tag_name.lower():
            try:
                descriptions.append(await element.inner_text())
            except Exception as e:
                print("Failed to retrieve neighboring element inner text", e)
            try:
                href = await element.get_attribute("href")
                if fetch_urls:
                    url = get_absolute_url(page, href)
                    if is_truthy(url):
                        urls.append(url)  # type: ignore
            except Exception as e:
                print("Failed to retrieve neighboring element href", e)

    return (descriptions, urls)


async def get_element_inner_text(element: ElementHandle) -> Union[str, None]:
    try:
        return await element.inner_text()
    except Exception as e:
        print("Failed to get inner text of element", e)
        return None


async def get_element_url(page: Page, element: ElementHandle) -> Union[str, None]:
    href = await element.get_attribute("href")
    url = get_absolute_url(page, href)
    if is_truthy(url):
        return url
    print("click_and_retrieve_new_tab_url()")
    return await click_and_retrieve_new_tab_url(page=page, element=element)


async def get_element_tag_name(element: ElementHandle) -> Union[str, None]:
    return await (await element.get_property("tagName")).json_value()
