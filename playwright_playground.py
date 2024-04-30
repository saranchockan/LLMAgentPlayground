from playwright.sync_api import Playwright, sync_playwright

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

    input_elements = page.query_selector_all("input")
    input_elements_html_str_arr = []
    for input_element in input_elements:
        print(input_element.get_property("outerHTML"))
        input_elements_html_str_arr.append(str(input_element.get_property("outerHTML")))

    print(str(input_elements_html_str_arr))

    input("Press Enter to close the browser...")
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
