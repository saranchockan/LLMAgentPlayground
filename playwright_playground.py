import os
from typing import List

from playwright.sync_api import Page, Playwright, sync_playwright

from perplexity_playground import call_perpexity_llm


COMPANY_NAME = os.getenv("COMPANY_NAME")
EXTRACT_COMPANY_CAREER_PAGE_URL_PROMPT = f"""Can you output the URL that is the 
official careers page for a tech company called {COMPANY_NAME}? 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE."""


def run(playwright: Playwright):

    print(f"### Extracting software engineering positions from {COMPANY_NAME} ###")

    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    # TODO: add error handling
    company_career_page_url = call_perpexity_llm(EXTRACT_COMPANY_CAREER_PAGE_URL_PROMPT)

    print(company_career_page_url)

    page.goto(company_career_page_url)

    input("Press Enter to close the browser...")

    browser.close()


with sync_playwright() as playwright:
    run(playwright)


"""
    Navigate to Careers page from an company's official 
    website.

    ```
    page = browser.new_page()
    page.goto("https://www.notion.so/careers")
    hyperlink_titles = get_page_hyperlink_titles(page=page)

    print("Navigating to Notion Careers...")
    page.get_by_text("Careers").click()
    ```
"""


def get_page_hyperlink_titles(page: Page) -> List[str]:
    ret = []
    # Get all the hyperlinks on the page
    links = page.query_selector_all("a")
    # Print the title of each link
    for link in links:
        title = link.get_attribute("title")
        title = title if title else link.text_content()
        ret.append(title)
    return ret
