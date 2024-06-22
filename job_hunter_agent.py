import asyncio
from time import sleep
from typing import List

from playwright.async_api import ElementHandle, Playwright

from job_hunter_llm_utils import (
    is_job_application_web_page_a_software_role,
    is_web_page_a_software_role_application,
    is_web_element_related_to_career_exploration,
)
from job_hunter_playground import is_url_software_role_application
from job_hunter_tools import (
    fetch_web_element_metadata,
    get_company_page_career_url,
    search_software_roles,
)
from prompts import COMPANY_NAME
from utils import (
    are_urls_similar,
    get_first_or_raise,
    print_var_name_value,
    print_with_newline,
)
from web_element import (
    WebElement,
    WebElementType,
    coalesce_web_elements,
    order_web_elements_by_regex,
    print_web_element,
    print_web_element_list,
)

from playwright.async_api import async_playwright


async def run_job_hunter_agent(playwright: Playwright):
    print_with_newline(
        f"✨✨✨ Extracting software engineering positions from {COMPANY_NAME} ✨✨✨"
    )
    company_career_page_url = await get_company_page_career_url()
    ...

    print_with_newline(f"{COMPANY_NAME} Career Page URL: {company_career_page_url}")

    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    context = await browser.new_context()
    page = await browser.new_page()
    page.set_default_timeout(100000)

    software_role_app_urls: List[WebElement] = [
        WebElement(
            description="",
            label="",
            url="https://boards.greenhouse.io/anthropic/jobs/4035354008",
            element_type=WebElementType.ANCHOR,
        )
    ]

    async def software_role_app_web_crawler(
        url: str, software_role_app_urls: List[WebElement]
    ):
        if len(software_role_app_urls) != 1:
            return
        # Navigate to URL in browser
        await page.goto(url)

        """
        SEARCH for software engineer roles in the 
        current page.
        """

        try:
            await search_software_roles(page=page)
        except Exception as e:
            print("Search failed!")
            print("Exception:", e)

        sleep(5)
        anchor_web_elements: List[WebElement] = await fetch_web_element_metadata(
            context, page, WebElementType.ANCHOR
        )
        button_web_elements: List[WebElement] = await fetch_web_element_metadata(
            context, page, WebElementType.BUTTON
        )
        interactable_web_elements = order_web_elements_by_regex(
            coalesce_web_elements((anchor_web_elements + button_web_elements))
        )

        for web_element in interactable_web_elements:
            if is_web_element_related_to_career_exploration(web_element=web_element):
                try:
                    software_role_url = get_first_or_raise(software_role_app_urls)

                    if are_urls_similar(software_role_url["url"], web_element["url"]):
                        if await is_job_application_web_page_a_software_role(
                            web_element["url"]
                        ):
                            print("Found software engineering role w/o vision!")
                            print_web_element(web_element=web_element)
                            software_role_app_urls.append(web_element)
                            continue
                        print("Not a software engineering application role!")
                        print_web_element(web_element=web_element)
                        continue
                except Exception as e:
                    print(e)
                print("Running vision !! !!")
                if await is_url_software_role_application(url=web_element["url"]):
                    print("Found software engineering role w/ vision!")
                    print_web_element(web_element=web_element)
                    software_role_app_urls.append(web_element)
                    continue

                await software_role_app_web_crawler(
                    url=web_element["url"],
                    software_role_app_urls=software_role_app_urls,
                )

        ...

    await software_role_app_web_crawler(
        url=company_career_page_url, software_role_app_urls=software_role_app_urls
    )

    print("Software engineering web app elements")
    print_web_element_list(software_role_app_urls)


async def main():
    async with async_playwright() as playwright:
        await run_job_hunter_agent(playwright)


asyncio.run(main=main())
