import base64
from typing import List

from anthropic import Anthropic
from anthropic.types import Message

from anthropic_utils import extract_text_from_message
from perplexity_utils import MIXTRAL_8X7B_INSTRUCT_MODEL, call_perpexity_llm
from prompts import (
    DETERMINE_WEB_PAGE_IS_SOFTWARE_APPLICATION_PROMPT,
    SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT,
)

ANTHROPIC_API_KEY = "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"
client = Anthropic(
    # This is the default and can be omitted
    api_key=ANTHROPIC_API_KEY,
)


def get_job_search_element(html_input_elements: List[str]) -> str:
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

    message: Message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT.format(
                    HTML_INPUT_ELEMENTS=html_input_elements
                ),
            },
        ],
    )
    return extract_text_from_message(message)


def determine_if_web_page_is_software_role_application(num_of_web_page_images: int):
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
            "text": DETERMINE_WEB_PAGE_IS_SOFTWARE_APPLICATION_PROMPT,
        },
    ]

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
    print(extract_text_from_message(message=message))
