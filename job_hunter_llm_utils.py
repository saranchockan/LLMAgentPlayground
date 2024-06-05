import base64
from typing import List

from anthropic import Anthropic

from perplexity_utils import MIXTRAL_8X7B_INSTRUCT_MODEL, call_perpexity_llm
from prompts import (
    DETERMINE_WEB_PAGE_IS_SOFTWARE_APPLICATION_PROMPT,
    SEARCH_FOR_SOFTWARE_ROLES_SYS_PROMPT,
    SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT,
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
    return call_perpexity_llm(
        sys_prompt=SEARCH_FOR_SOFTWARE_ROLES_SYS_PROMPT,
        user_prompt=str(
            SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT.format(
                HTML_INPUT_ELEMENTS=html_input_elements
            )
        ),
        model=MIXTRAL_8X7B_INSTRUCT_MODEL,
    )


def determine_if_web_page_is_software_role_application():
    """
    https://docs.anthropic.com/en/docs/vision
    """
    ANTHROPIC_API_KEY = "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"
    client = Anthropic(
        # This is the default and can be omitted
        api_key=ANTHROPIC_API_KEY,
    )

    # Get image binary data from screenshots/
    images_content = []
    base64_images = []
    for i in range(7):
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
    print(message)
