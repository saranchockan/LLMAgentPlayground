import base64
from cProfile import label
from typing import List, Union

from anthropic import Anthropic
from anthropic.types import Message

from anthropic_utils import extract_text_from_anthropic_message
from openai_utils import extract_message_from_openai_message
from perplexity_utils import MIXTRAL_8X7B_INSTRUCT_MODEL, call_perpexity_llm
from prompts import (
    DETERMINE_WEB_PAGE_IS_SOFTWARE_APPLICATION_PROMPT,
    IS_WEB_ELEMENT_RELATED_TO_CAREER_EXPLORATION_PROMPT,
    SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT,
)
from utils import print_with_newline, str_to_bool
from web_element import WebElement
import os

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
        html_input_elements (List[str]): _description_

    Returns:
        str: _description_
    """

    # TODO: OpenAI, Anthropic Chat completion wrappers

    completion = openAIClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT.format(
                    HTML_INPUT_ELEMENTS=html_input_elements
                ),
            },
        ],
    )
    return extract_message_from_openai_message(completion)

    # message: Message = anthropicClient.messages.create(
    #     model="claude-3-opus-20240229",
    #     max_tokens=1024,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT.format(
    #                 HTML_INPUT_ELEMENTS=html_input_elements
    #             ),
    #         },
    #     ],
    # )
    # return extract_text_from_anthropic_message(message)


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


def determine_if_web_page_is_software_role_application(num_of_web_page_images: int):
    """
    https://docs.anthropic.com/en/docs/vision
    """

    """
    TODO: if the url has 
    greehouse, lever -> we should skip vision...

    Learn from vision ML 
    if career puck websites are software role applications, 
    then we shouldn't repeatedly call vision   ! ! ! !


    If a url is career application page, we tell that to 
    LLM and then determine if other URLs follow the same
    pattern !!!!


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
            "text": DETERMINE_WEB_PAGE_IS_SOFTWARE_APPLICATION_PROMPT,
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
    print(extract_text_from_anthropic_message(message=message))
