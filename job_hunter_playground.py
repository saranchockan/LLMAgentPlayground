import asyncio
import os
from enum import Enum
from time import sleep
from typing import Dict, List, TypedDict

from playwright.async_api import ElementHandle, Playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from job_hunter_llm_utils import (
    determine_if_web_page_is_software_role_application,
    get_job_search_element,
    is_web_element_related_to_career_exploration,
)
from job_hunter_tools import (
    fetch_web_element_metadata,
    is_web_element_related_to_software_engineering_role,
    search_software_roles,
    take_full_page_screenshots,
)
from perplexity_utils import SONAR_SMALL_ONLINE_MODEL, call_perpexity_llm
from prompts import (
    COMPANY_NAME,
    EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT,
    EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT,
)
from utils import (
    print_web_element,
    print_web_element_list,
    print_with_newline,
)
from web_element import WebElement, WebElementType, order_web_elements_by_regex


async def run_job_hunter(playwright: Playwright):

    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    page.set_default_timeout(100000)

    print_with_newline(
        f"✨✨✨ Extracting software engineering positions from {COMPANY_NAME} ✨✨✨"
    )
    """
    ASK perplexity for company's official career page url.
    """

    # TODO: Add error handling
    # TODO: Add career url validation
    # TODO: LLM DB Cache: if perplexity has previously
    # give us this company's career page URL, extract
    # URL from DB
    company_career_page_url = call_perpexity_llm(
        EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT,
        EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT,
        model=SONAR_SMALL_ONLINE_MODEL,
    )

    print_with_newline(f"{COMPANY_NAME} Career Page URL: {company_career_page_url}")

    await page.goto(company_career_page_url)

    """
    SEARCH for software engineer roles in the 
    company's career page.
    """

    try:
        await search_software_roles(page=page)
    except:
        print("Search failed!")
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
    anchor_web_elements: List[WebElement] = await fetch_web_element_metadata(
        page, WebElementType.ANCHOR
    )

    button_web_elements: List[WebElement] = await fetch_web_element_metadata(
        page, WebElementType.BUTTON
    )

    interactable_web_elements = order_web_elements_by_regex(
        anchor_web_elements + button_web_elements
    )

    """
    TODO: Keywords to regex
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

    print_web_element_list(interactable_web_elements)

    # for web_element in interactable_web_elements:
    #     if web_element["url"] not in company_career_page_url:
    #         if is_web_element_related_to_career_exploration(web_element=web_element):
    #             print_web_element(web_element)
    #     ...

    input("Press Enter to close the browser...")
    await browser.close()


SCREENSHOT_URL = os.getenv("SCREENSHOT_URL", "")


async def run_software_job_app_web_page_detection_script():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        page = await browser.new_page()
        await page.goto(SCREENSHOT_URL)

        # Take a full page screenshot
        num_of_screenshots = await take_full_page_screenshots(
            page=page, output_prefix="full_page_screenshot"
        )
        determine_if_web_page_is_software_role_application(num_of_screenshots)

        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run_job_hunter(playwright)
        # await run_software_job_app_web_page_detection_script()


asyncio.run(main=main())
