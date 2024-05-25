from enum import Enum
from typing import TypedDict


class WebElementType(Enum):
    ANCHOR = "a"
    BUTTON = "button"
    INPUT = "input"


class WebElement(TypedDict):
    label: str
    url: str
    description: str
    element_type: WebElementType
