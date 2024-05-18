import asyncio
from typing import Dict

from playwright.async_api import async_playwright
from playwright.async_api import ElementHandle, Playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from job_search_element_picker import get_job_search_element
from perplexity_playground import SONAR_SMALL_ONLINE_MODEL, call_perpexity_llm
from playwright_utils import extract_anchor_elements
from prompts import (
    COMPANY_NAME,
    EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT,
    EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT,
)


async def run(playwright: Playwright):

    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    page.set_default_timeout(10000)

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

    # TODO: Error handle cases where
    # there are no search inputs. Eg - Notion!
    await page.wait_for_selector("input", timeout=10000)

    search_elements = page.query_selector_all("input")
    search_elements_map: Dict[str, ElementHandle] = {}
    for search_element in await search_elements:
        search_element_html_str = str(await search_element.get_property("outerHTML"))
        search_elements_map[search_element_html_str] = search_element

    print(search_elements_map)
    # TODO: Prompt the LLM to return empty output if none of the
    # input elements are relevant for job search
    job_search_element_key = get_job_search_element(list(search_elements_map.keys()))
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

    print("Job Search Element Key:", job_search_element_key)

    job_search_element = search_elements_map[job_search_element_key]

    await job_search_element.type("Software")
    await job_search_element.press("Enter")

    """
    At this stage, the state of the world can be N scenarios
    a) <a> hyerplinks to software positions (Lyft)
    b) <button> to software positions (Benchling)
    ...
    n) ...


    Extrack links to software engineer roles
    """

    try:
        links = page.locator("a")
        link_texts = [await link.text_content() for link in await links.all()]
        link_urls = [await link.get_attribute("href") for link in await links.all()]

        # Print the link texts and URLs
        for text, url in zip(link_texts, link_urls):
            print(f"Link text: {text}, URL: {url}")
    except PlaywrightTimeoutError:
        print("Timeout! Page does not have links")

    try:
        # Get all the buttons on the page
        buttons = page.locator("button")
        button_texts = [await button.text_content() for button in await buttons.all()]
        # Print the button texts
        for text in button_texts:
            print(f"Button text: {text}")
    except PlaywrightTimeoutError:
        print("Timeout! Page does not have buttons")

    await extract_anchor_elements(page)

    input("Press Enter to close the browser...")
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main=main())
