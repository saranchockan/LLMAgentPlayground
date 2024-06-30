import os
from time import sleep
from typing import List
import asyncio

from playwright.async_api import Playwright, async_playwright

from job_hunter_tools import (
    fetch_interactable_web_elements,
    get_company_page_career_url,
    search_software_roles,
)
from job_hunter_utils import (
    is_job_application_web_page_a_software_role,
    is_web_page_a_software_role_application,
)
from playwright_utils import take_full_page_screenshots
from utils import print_with_newline
from web_element import (
    WebElement,
    WebElementType,
    coalesce_web_elements,
    order_web_elements_by_career_regex,
    print_web_element_list,
)

COMPANY_NAME = os.environ["COMPANY_NAME"]


async def run_job_hunter(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    context = await browser.new_context()
    page = await browser.new_page()
    page.set_default_timeout(100000)

    print_with_newline(
        f"✨✨✨ Extracting software engineering positions from {COMPANY_NAME} ✨✨✨"
    )
    """
    ASK perplexity for company's official career page url.
    """

    company_career_page_url = get_company_page_career_url(COMPANY_NAME)

    print_with_newline(f"{COMPANY_NAME} Career Page URL: {company_career_page_url}")

    await page.goto(company_career_page_url)

    """
    SEARCH for software engineer roles in the
    company's career page.
    """

    try:
        await search_software_roles(page=page)
    except Exception as e:
        print("Search failed!")
        print("Exception:", e)
        ...

    """
    At this stage, the state of the world can be N scenarios
    a) <a> hyerplinks to software positions (Lyft)
    b) <button> to software positions (Benchling)
    ...
    n) ...

    Agent needs to be able to identify which page it is on
    A) List of job roles
        Search for software (Lyft)
        Click on Engineering button (Anthropic)
    B) A software role page
        At this point of time, AgentHunt is done. AgentApply
        should take over to deem role fit and apply

    Extrack links to software engineer roles
    """
    sleep(5)
    anchor_web_elements: List[WebElement] = await fetch_interactable_web_elements(page)

    """
    We search of buttons b/c some websites
    don't expose <a> hrefs For eg - Benchling

    There could be anchors and buttons that represent the same
    thing and we should coalesce them.

    Buttons that don't have URLs are compeletly valid
    and should be clicked

    """
    button_web_elements: List[WebElement] = await fetch_interactable_web_elements(page)

    """
    Keywords to regex
    "job" "software" "engineer "apply" "lever" "greenhouse" "career"...

    Push prioritized web elements to the top of the list,
    run through is_web_element_related_to_career_exploration,
    run the process in DFS, put a condition
    to stop checking web elemenst after n jobs have been extracted
    The objective here is to reduce the calls to LLMs. (Or maybe
    this doesn't matter to scale since we are still developing MVP)

    AND

    do we get web elements in order? If so, we can deduct that
    starting set of elements are in header and the ending set of
    elements are in footer. So, we start DFS in elements in the middle
    set.

    """
    interactable_web_elements = order_web_elements_by_career_regex(
        coalesce_web_elements((anchor_web_elements + button_web_elements))
    )

    print_web_element_list(interactable_web_elements)

    input("Press Enter to close the browser...")
    await browser.close()


SCREENSHOT_URL = os.getenv("SCREENSHOT_URL", "")


async def main():
    async with async_playwright() as playwright:
        await run_job_hunter(playwright)


print(
    asyncio.run(
        main=is_job_application_web_page_a_software_role(
            "https://boards.greenhouse.io/anthropic/jobs/4020295008"
        )
    )
)
