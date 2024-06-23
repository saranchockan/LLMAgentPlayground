import base64
from typing import List, Union

from anthropic import Anthropic
from anthropic.types import Message

from anthropic_utils import extract_text_from_anthropic_message
from openai_utils import extract_message_from_openai_message
from playwright_utils import extract_all_text_from_web_page
from prompts import (
    IS_JOB_APP_WEB_PAGE_FOR_SOFTWARE_PROMPT,
    IS_WEB_ELEMENT_RELATED_TO_CAREER_EXPLORATION_PROMPT,
    IS_WEB_PAGE_A_SOFTWARE_APPLICATION_PROMPT,
    SEARCH_FOR_SOFTWARE_ROLES_PROMPT,
)
from utils import str_to_bool
from web_element import WebElement

ANTHROPIC_API_KEY = "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"
anthropicClient = Anthropic(
    # This is the default and can be omitted
    api_key=ANTHROPIC_API_KEY,
)

from openai import OpenAI

openAIClient = OpenAI()


def get_job_search_element(html_input_elements: List[str]) -> Union[str, None]:
    """Gets the search element related to searching for
    job openings. A company's official career website can have multiple
    search HTML elements. An LLM can pick the
    search element that is most relevant to searching
    for job openings in the company in the career website.

    Args:
        html_input_elements (List[str]): list of html of input elements in web page

    Returns:
        str: html of input element for searching job roles
    """

    completion = openAIClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": SEARCH_FOR_SOFTWARE_ROLES_PROMPT.format(
                    HTML_INPUT_ELEMENTS=html_input_elements
                ),
            },
        ],
    )
    return extract_message_from_openai_message(completion)


def is_web_element_related_to_career_exploration(web_element: WebElement) -> bool:
    web_element_str = web_element.__str__()
    message: Message = anthropicClient.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": IS_WEB_ELEMENT_RELATED_TO_CAREER_EXPLORATION_PROMPT.format(
                    WEB_ELEMENT_METADATA=web_element_str
                ),
            },
        ],
    )
    return str_to_bool(extract_text_from_anthropic_message(message))


def is_web_page_a_software_role_application(
    num_of_web_page_images: int,
) -> bool:
    """
    https://docs.anthropic.com/en/docs/vision
    """
    # Get image binary data from screenshots/
    images_content = []
    base64_images = []
    for i in range(num_of_web_page_images):
        with open(f"screenshots/full_page_screenshot_{i}.png", "rb") as image_file:
            # Read the image data
            b = base64.b64encode(image_file.read()).decode("utf-8")
            base64_images.append(b)
            images_content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": b,
                    },
                }
            )

    content = images_content + [
        {
            "type": "text",
            "text": IS_WEB_PAGE_A_SOFTWARE_APPLICATION_PROMPT,
        },
    ]

    message = anthropicClient.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
    return str_to_bool((extract_text_from_anthropic_message(message=message)))


async def is_job_application_web_page_a_software_role(job_app_url: str) -> bool:

    completion = openAIClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": IS_JOB_APP_WEB_PAGE_FOR_SOFTWARE_PROMPT.format(
                    WEB_PAGE_TEXT=await extract_all_text_from_web_page(job_app_url)
                ),
            },
        ],
    )
    ret = str_to_bool(extract_message_from_openai_message(completion))
    return ret
