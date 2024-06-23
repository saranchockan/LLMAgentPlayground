from enum import Enum
from typing import DefaultDict, Dict, List, TypedDict, Union
import re

from utils import get_first_or_raise, group_by


class WebElementType(Enum):
    ANCHOR = "a"
    BUTTON = "button"
    INPUT = "input"


class WebElement(TypedDict):
    # element_type: WebElementType
    label: str
    url: str
    description: str


def coalesce_web_elements(web_elements: List[WebElement]) -> List[WebElement]:
    """Coalesces a list of web elements by grouping them based on their URL and combining their descriptions and labels.

    Args:
        web_elements (List[WebElement]): A list of WebElement objects to be coalesced.

    Returns:
        List[WebElement]: A list of coalesced WebElement objects.
    """
    coalesced_web_elements: List[WebElement] = []
    web_element_by_url: Dict[str, List[WebElement]] = group_by(
        web_elements, lambda w: w["url"]
    )

    for url, web_elements in web_element_by_url.items():
        coalesced_web_elements.append(
            WebElement(
                # element_type=get_first_or_raise(web_elements)["element_type"],
                description=" ".join(
                    web_element["description"] for web_element in web_elements
                ),
                url=url,
                label=" ".join(web_element["label"] for web_element in web_elements),
            )
        )
    return coalesced_web_elements


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
    # TODO: Modularize this regex fn to add words
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


def print_web_element_list(metadata_list: List[WebElement]) -> None:
    """
    Prints a list of WebElement objects in a readable format with spacing.

    Args:
        metadata_list (List[Metadata]): A list of Metadata objects.

    Returns:
        None
    """
    print("[")
    for i, metadata in enumerate(metadata_list):
        print("   {")
        for j, (key, value) in enumerate(metadata.items()):
            print(f'      {key}: "{value}",', end="")
            if j < len(metadata) - 1:
                print()
        print("\n   }", end="")
        if i < len(metadata_list) - 1:
            print(",")
        print()
    print("]")


def print_web_element(web_element: WebElement) -> None:
    """
    Prints a list of WebElement objects in a readable format with spacing.

    Args:
        web_element (List[Metadata]): A list of Metadata objects.

    Returns:
        None
    """
    print("   {")
    for j, (key, value) in enumerate(web_element.items()):
        print(f'      {key}: "{value}",', end="")
        if j < len(web_element) - 1:
            print()
    print("\n   }", end="")
    print()
