from typing import List

from perplexity_utils import MIXTRAL_8X7B_INSTRUCT_MODEL, call_perpexity_llm
from prompts import (
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
