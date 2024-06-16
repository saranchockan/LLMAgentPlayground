from enum import Enum
from typing import List, TypedDict
import re


class WebElementType(Enum):
    ANCHOR = "a"
    BUTTON = "button"
    INPUT = "input"


class WebElement(TypedDict):
    element_type: WebElementType
    label: str
    url: str
    description: str


def order_web_elements_by_regex(dicts: List[WebElement]) -> List[WebElement]:
    """
    Orders a list of typed dictionaries based on the best match of a regular expression search
    through all their elements.

    Args:
        dicts (List[MyTypedDict]): A list of typed dictionaries.
        regex (str): The regular expression pattern to search for.

    Returns:
        List[MyTypedDict]: The ordered list of typed dictionaries.
    """
    job_related_keywords_regex = (
        r"(?:job|software|engineer|apply|lever|greenhouse|career)"
    )
    # Create a list of tuples with the dictionary and its match score
    scored_dicts = []
    for d in dicts:
        match_score = sum(
            len(re.findall(job_related_keywords_regex, str(v), re.IGNORECASE))
            for v in d.values()
        )
        scored_dicts.append((d, match_score))

    # Sort the list of tuples based on the match score in descending order
    sorted_scored_dicts = sorted(scored_dicts, key=lambda x: x[1], reverse=True)

    # Extract the ordered dictionaries from the sorted list of tuples
    ordered_dicts = [d[0] for d in sorted_scored_dicts]

    return ordered_dicts
