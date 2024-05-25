import asyncio
from enum import Enum
from time import sleep
from typing import Dict, TypedDict

from playwright.async_api import ElementHandle, Playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from job_hunter_llm_utils import get_job_search_element
from job_hunter_tools import (
    fetch_web_element_metadata,
    search_software_roles,
    take_screenshot,
)
from playwright_data_interface import WebElementType
from perplexity_utils import SONAR_SMALL_ONLINE_MODEL, call_perpexity_llm
from utils import print_metadata_list
from prompts import (
    COMPANY_NAME,
    EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT,
    EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT,
)


async def run_job_hunter(playwright: Playwright):

    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    page.set_default_timeout(100000)

    print(
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

    print(f"{COMPANY_NAME} Career Page URL: {company_career_page_url}")

    await page.goto(company_career_page_url)

    """
    SEARCH for software engineer roles in the 
    company's career page.
    """

    await search_software_roles(page=page)

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
    print("<a> Elements")
    print_metadata_list(await fetch_web_element_metadata(page, WebElementType.ANCHOR))

    print("<button> Elements")
    print_metadata_list(await fetch_web_element_metadata(page, WebElementType.BUTTON))

    input("Press Enter to close the browser...")
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run_job_hunter(playwright)


asyncio.run(main=main())


async def run_screen_shot_script():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.palantir.com/careers")

        # Take a full page screenshot
        await take_screenshot(page, "screenshots/palantir.png", full_page=True)

        await browser.close()
