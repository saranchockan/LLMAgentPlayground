import os
from enum import Enum
from re import L
from time import sleep
from typing import Any, Callable, Dict, List, Optional, TypedDict, Union
from urllib.parse import urljoin, urlparse

from playwright.async_api import BrowserContext, ElementHandle, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from job_hunter_utils import get_job_search_element
from perplexity import SONAR_SMALL_ONLINE_MODEL, call_perpexity_llm
from playwright_utils import (
    click_and_retrieve_new_tab_url,
    fetch_elements_description_and_url,
    fetch_neighboring_elements,
    get_absolute_url,
    get_all_child_elements,
    get_element_inner_text,
    get_element_tag_name,
    get_element_url,
)
from prompts import (
    EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT,
    EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT,
)
from utils import (
    is_truthy,
    none_to_str,
    print_var_name_value,
    print_with_newline,
    remove_newlines,
    remove_special_chars,
)
from web_element import (
    WebElement,
    WebElementType,
    coalesce_web_elements,
    order_web_elements_by_regex,
)


def get_company_page_career_url(company_name: str) -> str:
    """Gets the career page url of the company
    from an online LLM model.

    Args:
        company_name (str): name of the company

    Returns:
        str: URL of the company name's career page url
    """
    # TODO: Add error handling
    # TODO: Add career url validation
    # TODO: LLM DB Cache: if perplexity has previously
    # give us this company's career page URL, extract
    # URL from DB
    return call_perpexity_llm(
        EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT,
        EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT.format(COMPANY_NAME=company_name),
        model=SONAR_SMALL_ONLINE_MODEL,
    )


async def fetch_job_search_element(page: Page) -> Union[ElementHandle, None]:
    """Fetches the job search element in the web page

    Args:
        page (Page): web page to retrieve
    """
    try:
        await page.wait_for_selector(WebElementType.INPUT.value, timeout=10000)
        search_elements = await page.query_selector_all(WebElementType.INPUT.value)
    except Exception as e:
        print("Web page does not have search.")
        raise e

    search_elements_map: Dict[str, ElementHandle] = {}
    for search_element in search_elements:
        """
        Removing special chars because
        LLM can re-format special chars that
        affect str comparison ' -> \'
        """
        search_element_html_str = remove_special_chars(
            str(await search_element.get_property("outerHTML"))
        )
        search_elements_map[search_element_html_str] = search_element

    job_search_element_key = get_job_search_element(list(search_elements_map.keys()))
    """
    TODO: Prompt the LLM to return empty output if none of the
    input elements are relevant for job search
    TODO: Add error handling
    Case 1: Hallucination: If the LLM returns a job_search_element_key
    that is not in the search_elements_map, teach the LLM that it is hallucinating
    and tell it to pick an input element from the provided list
    Case 2: Misdirection: LLM picks an input element from the examples. Tell the
    LLM that it picked an input element from the list and tell it to pick
    an input element from the user provided list.
    Case 3: LLM determines that none of the search input
    are for searching software roles

    TODO: Memory
    How can the LLM learn to pick search elements better by relying
    on past examples?

    TODO: Collect examples
    As the LLM performs this task, collect a list of input elements
    and output. This will be useful for fine tune data modelling

    TODO: Use Langchain Prompt Template (Few Shot)
    and Output parsing for greater control
    """

    try:
        if job_search_element_key:
            return search_elements_map[job_search_element_key]
    except KeyError as k:
        raise k
    return None


async def search_software_roles(
    page: Page, job_search_element: Optional[ElementHandle] = None
) -> Union[ElementHandle, None]:
    """SEARCH for software engineer roles in the
    the web page.

    Args:
        page (Page): web page to search for software roles
    """
    if not is_truthy(job_search_element):
        job_search_element = await fetch_job_search_element(page)
    try:
        """
        TODO: Instead of naively typing in 'Software', we should check
        if the search input has options. For example, https://www.anthropic.com/jobs
        """
        if is_truthy(job_search_element):
            await job_search_element.type("Software")  # type: ignore
            await job_search_element.press("Enter")  # type: ignore
            return job_search_element
    except Exception as e:
        print(e)
    print_with_newline("Unable to search for software roles!")


async def get_interactable_career_web_elements(
    page: Page, restore_page_initial_dom_state: Callable
) -> List[WebElement]:
    """_summary_

    Args:
        page (Page): _description_

    Returns:
        List[WebElement]: _description_
    """
    interactable_web_elements = order_web_elements_by_regex(
        coalesce_web_elements(
            await fetch_interactable_web_elements(page, restore_page_initial_dom_state)
        )
    )
    return interactable_web_elements


# TODO: shift this to webelement module
async def fetch_interactable_web_elements(
    page: Page, restore_page_initial_dom_state: Callable
) -> List[WebElement]:
    """Extracts metadata of web elements (eg - anchor (<element> </element>))
    from the page.

    Args:
        page (Page):
            page to extract anchor elements.
    """

    """
    Retrieving elements from <main> lets us
    chase to relevent elements (<footer> elements are definitively not relevant) and reduce calls
    to LLMs to determine career relevancy
    """
    main_element = await page.query_selector("main")

    if main_element:
        # elements = await main_element.query_selector_all(selector.value)
        elements = await main_element.query_selector_all("button")
    else:
        elements = await page.query_selector_all("button")

    interactable_web_elements: List[WebElement] = []
    for element in elements:
        label = remove_special_chars(remove_newlines(await element.inner_text()))
        description = none_to_str(await get_element_inner_text(element=element))

        tag_name = await get_element_tag_name(element=element)

        print_var_name_value(label)
        print_var_name_value(description)
        print_var_name_value(tag_name)
        print()
        url = await get_element_url(
            page=page,
            element=element,
            restore_page_initial_dom_state=restore_page_initial_dom_state,
        )
        """
        Extract metadata of neighboring elements
        This is useful when we have an <a>'s description
        in a adjacent div or h2.
        For eg - https://www.anthropic.com/jobs
        """
        (
            neighbor_elements_descriptions,
            neighbor_elements_urls,
        ) = await fetch_elements_description_and_url(
            page=page,
            elements=await fetch_neighboring_elements(
                element=element, element_filter=tag_name
            ),
            fetch_urls=not is_truthy(url),
            filter_element_tag_name=tag_name,
        )
        description += remove_special_chars(
            remove_newlines(
                " ".join(description for description in neighbor_elements_descriptions)
            )
        )

        if is_truthy(url):
            interactable_web_elements.append(
                WebElement(
                    label=label,
                    url=url,  # type: ignore
                    description=description,
                )
            )
        elif is_truthy(neighbor_elements_urls):
            interactable_web_elements += [
                WebElement(
                    label=label,
                    url=url,
                    description=description,
                )
                for url in neighbor_elements_urls
            ]

    return interactable_web_elements
