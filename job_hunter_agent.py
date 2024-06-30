import asyncio
import os
from time import sleep
from typing import List, Set

from playwright.async_api import ElementHandle, Page, Playwright, async_playwright

from job_hunter_tools import (
    get_company_page_career_url,
    get_interactable_web_elements,
    is_web_element_a_software_role_application,
    search_software_roles,
)
from job_hunter_utils import (
    is_job_application_web_page_a_software_role,
    is_web_element_related_to_career_exploration,
)
from utils import (
    are_urls_similar,
    debug_print,
    format_execution_time,
    get_first_or_raise,
    print_var_name_value,
    print_with_newline,
)
from web_element import (
    WebElement,
    WebElementType,
    coalesce_web_elements,
    order_web_elements_by_career_regex,
    print_web_element,
    print_web_element_list,
)

COMPANY_NAME = os.getenv("COMPANY_NAME", "")


async def software_role_app_web_crawler(
    page: Page,
    web_element: WebElement,
    software_role_app_web_elements: List[WebElement],
    visited_urls: Set[str] = set(),
):
    if web_element[
        "url"
    ] in visited_urls or not is_web_element_related_to_career_exploration(
        web_element=web_element
    ):
        return

    try:
        software_role_url = get_first_or_raise(software_role_app_web_elements)
    except ValueError as e:
        debug_print("No software roles have been found yet, attempting vision", e)
        if await is_web_element_a_software_role_application(web_element=web_element):
            debug_print("Found software engineering role using Claude Vision")
            print_web_element(web_element=web_element)
            software_role_app_web_elements.append(web_element)
            return
    else:
        if are_urls_similar(
            web_element["url"], software_role_url["url"], threshold=0.8
        ):
            # TODO: Wrap is_job_application_web_page_a_software_role
            # in try catch
            if await is_job_application_web_page_a_software_role(web_element["url"]):
                debug_print(
                    "Found software engineering role without without using Claude Vision!"
                )
                print_web_element(web_element=web_element)
                software_role_app_web_elements.append(web_element)
            else:
                debug_print(
                    "Found a job application, but it is not for a software engineering role"
                )
                print_web_element(web_element=web_element)
            return
        else:
            debug_print(
                "Web Page URL is not similar to software_role_app_web_elements urls",
                web_element["url"],
                software_role_url["url"],
            )

    debug_print("Go to URL:", web_element["url"])
    # Navigate to URL in browser
    await page.goto(web_element["url"])
    visited_urls.add(web_element["url"])
    try:
        job_search_element = await search_software_roles(page=page)
    except Exception as e:
        debug_print("Failed to search software roles", e)
    sleep(5)

    # TODO: Modularize this on wrapper
    # over page to avoid prop drilling
    async def restore_page_initial_dom_state():
        await search_software_roles(page=page, job_search_element=job_search_element)

    interactable_web_elements = order_web_elements_by_career_regex(
        await get_interactable_web_elements(
            page=page,
            restore_page_initial_dom_state=restore_page_initial_dom_state,
        )
    )
    print("interactable_web_elements")
    print_web_element_list(interactable_web_elements)

    for web_element in interactable_web_elements:
        await software_role_app_web_crawler(
            page=page,
            web_element=web_element,
            software_role_app_web_elements=software_role_app_web_elements,
        )


async def run_job_hunter_agent(playwright: Playwright):

    print_with_newline(
        f"✨✨✨ Extracting software engineering positions from {COMPANY_NAME} ✨✨✨"
    )
    company_career_page_url = get_company_page_career_url(COMPANY_NAME)
    ...

    print_with_newline(f"{COMPANY_NAME} Career Page URL: {company_career_page_url}")

    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    page.set_default_timeout(100000)

    caree_page_web_element: WebElement = WebElement(
        description=f"Career page of the company {COMPANY_NAME} that contains information about job opportunities",
        html="",
        url=company_career_page_url,
        label=f"{COMPANY_NAME} career page",
    )
    software_role_app_web_elements: List[WebElement] = []
    await software_role_app_web_crawler(
        page=page,
        web_element=caree_page_web_element,
        software_role_app_web_elements=software_role_app_web_elements,
    )

    print_web_element_list(software_role_app_web_elements)


async def main():
    async with async_playwright() as playwright:
        await run_job_hunter_agent(playwright)


import time

start_time = time.time()
asyncio.run(main=main())
end_time = time.time()

execution_time = end_time - start_time
print(f"Agent Hunt Execution time: {format_execution_time(execution_time)}")
