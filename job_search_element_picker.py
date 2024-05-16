"""
A company's official career website can have multiple 
search HTML elements. An LLM can pick the
search element that is most relevant to searching
for job openings in the company in the career website.  
"""

from typing import List
from perplexity_playground import MIXTRAL_8X7B_INSTRUCT_MODEL, call_perpexity_llm
from prompts import (
    SEARCH_FOR_SOFTWARE_ROLES_SYS_PROMPT,
    SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT,
)

HTML_INPUT_ELEMENT = [
    '<input type="text" class="" style="label:input;color:inherit;background:0;opacity:1;width:100%;grid-area:1 / 2;font:inherit;min-width:2px;border:0;margin:0;outline:0;padding:0" autocapitalize="none" autocomplete="off" autocorrect="off" id="Department-2Zcdjo2u4l73wlxSlEDdS-input" spellcheck="false" tabindex="0" value="" aria-autocomplete="list" aria-expanded="false" aria-haspopup="true" role="combobox">',
    '<input type="hidden" name="department" value="all-departments">',
    '<input type="text" class="BaseInput-module_input__At1nr BaseInput-module_size48__OHWCP" name="role" value="" id="role-_-YMMqB9RCnoPEWa5Ya2C" spellcheck="false">',
    '<input type="text" class="" style="label:input;color:inherit;background:0;opacity:1;width:100%;grid-area:1 / 2;font:inherit;min-width:2px;border:0;margin:0;outline:0;padding:0" autocapitalize="none" autocomplete="off" autocorrect="off" id="Location-73nDeDPvU9NVMGS9nA7MY-input" spellcheck="false" tabindex="0" value="" aria-autocomplete="list" aria-expanded="false" aria-haspopup="true" role="combobox">',
    '<input type="hidden" name="location" value="all-locations">',
]


def get_job_search_element(html_input_elements: List[str]) -> str:
    return call_perpexity_llm(
        sys_prompt=SEARCH_FOR_SOFTWARE_ROLES_SYS_PROMPT,
        user_prompt=str(
            SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT.format(
                HTML_INPUT_ELEMENTS=html_input_elements
            )
        ),
        model=MIXTRAL_8X7B_INSTRUCT_MODEL,
    )
