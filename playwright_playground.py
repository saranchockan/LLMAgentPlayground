import os
from typing import List

from playwright.sync_api import Page, Playwright, sync_playwright

from perplexity_playground import call_perpexity_llm


COMPANY_NAME = os.getenv("COMPANY_NAME")
EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT = """You are a website crawler. You will be given the name of a company. 
You should output the URL of the company's career page. 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE"""
EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT = f"""Can you output the URL that is the 
official careers page for a tech company called {COMPANY_NAME}? 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE."""

SEARCH_FOR_SOFTWARE_ROLES_SYS_PROMPT = """You are an AI Job Hunter Web Agent who is an expert
in search for software engineer roles on company career websites. 

You will be given {HTML_INPUT_ELEMENTS}. Each input element in {HTML_INPUT_ELEMENTS} is an   
You should pick one input element that is prompting the user to search for specific job openings in the company. 

HTML_INPUT_ELEMENTS = [
"<input data-testid="SearchInput" color="pink80" name="search" placeholder="Openings" class="sc-bc6dc228-2 hQcbLS" value="">"
"<input data-testid="core-ui-dropdown" name="categoryFiter" role="combobox" aria-expanded="false" aria-autocomplete="none" aria-readonly="false" aria-describedby="core-ui-id-8154769791-description" aria-invalid="false" id="core-ui-id-8154769791" readonly="" class="sc-1v6kknp-5 hsPasW">"
"<input data-testid="core-ui-dropdown" name="locationFilter" role="combobox" aria-expanded="false" aria-autocomplete="none" aria-readonly="false" aria-describedby="core-ui-id-4236106179-description" aria-invalid="false" id="core-ui-id-4236106179" readonly="" class="sc-1v6kknp-5 hsPasW">"
]

Pick an input element from HTML_INPUT_ELEMENTS. Remember, YOUR OUTPUT SHOULD ONLY BE THE INPUT ELEMENT and NOTHING ELSE.

"""


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
    for input_element in input_elements:
        print(input_element.get_property("outerHTML"))

    input("Press Enter to close the browser...")
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
