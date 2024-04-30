from typing import Dict

from playwright.sync_api import ElementHandle, Playwright, sync_playwright

from job_search_element_picker import get_job_search_element
from perplexity_playground import call_perpexity_llm
from prompts import (
    COMPANY_NAME,
    EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT,
    EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT,
)


def run(playwright: Playwright):

    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    print(
        f"✨✨✨ Extracting software engineering positions from {COMPANY_NAME} ✨✨✨"
    )
    """
    ASK perplexity for company's official career page url.
    """

    # TODO: Add error handling
    # TODO: LLM DB Cache: if perplexity has previously
    # give us this company's career page URL, extract
    # URL from DB
    company_career_page_url = call_perpexity_llm(
        EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT,
        EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT,
    )

    print(f"{COMPANY_NAME} Career Page URL: {company_career_page_url}")

    page.goto(company_career_page_url)

    """
    SEARCH for software engineer roles in the 
    company's career page.
    """
    page.wait_for_selector("input", timeout=10000)

    search_elements = page.query_selector_all("input")
    search_elements_map: Dict[str, ElementHandle] = {}
    for search_element in search_elements:
        search_element_html_str = str(search_element.get_property("outerHTML"))
        search_elements_map[search_element_html_str] = search_element

    print(list(search_elements_map.keys()))
    job_search_element_key = get_job_search_element(list(search_elements_map.keys()))
    job_search_element = search_elements_map[job_search_element_key]

    job_search_element.type("Software")
    job_search_element.press("Enter")

    input("Press Enter to close the browser...")
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
