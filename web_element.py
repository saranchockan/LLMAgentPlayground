from enum import Enum
from typing import TypedDict


class WebElementType(Enum):
    ANCHOR = "a"
    BUTTON = "button"
    INPUT = "input"


class WebElement(TypedDict):
    element_type: WebElementType
    label: str
    url: str
    description: str
