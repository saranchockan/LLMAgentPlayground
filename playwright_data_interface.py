from enum import Enum
from typing import TypedDict


class WebElement:
    class HTMLElement(Enum):
        ANCHOR = "a"
        BUTTON = "button"
        INPUT = "input"

    class Metadata(TypedDict):
        label: str
        url: str
        description: str
        element_type: "WebElement.HTMLElement"
