import re
from typing import Any, List

from web_element import WebElement


def remove_special_chars(input_str):
    """
    Removes all special characters (including apostrophes) from a string.

    Args:
        input_str (str): The input string.

    Returns:
        str: The input string with all special characters removed.
    """
    # Define a regular expression pattern to match special characters
    pattern = r"[^a-zA-Z0-9\s]"

    # Use the re.sub() function to replace all matches with an empty string
    cleaned_str = re.sub(pattern, "", input_str)

    return cleaned_str


def print_if_not_empty(*strings, sep=" ", prefix="", suffix=""):
    """
    Prints the given strings if their concatenation is not empty.

    Args:
        *strings: One or more strings to concatenate and print.
        sep (str, optional): The separator to use when concatenating the strings. Default is a space.
        prefix (str, optional): A prefix to add before the concatenated string. Default is an empty string.
        suffix (str, optional): A suffix to add after the concatenated string. Default is an empty string.
    """
    combined_string = sep.join(str(s) for s in strings)
    if combined_string:
        print(f"{prefix}{combined_string}{suffix}", end="\n")


def print_var_name_value(var):
    """
    Prints the name and value of a variable.

    Args:
        var: Any variable or object.
    """
    import inspect

    caller_frame = inspect.currentframe().f_back
    caller_vars = caller_frame.f_locals

    for name, value in caller_vars.items():
        if value is var:
            print(f"{name} = {value}", end="\n")
            break


def print_with_newline(value: Any, end: str = "\n") -> None:
    """
    Prints the given value to the console, followed by a newline character.

    Args:
        value (Any): The value to be printed.
        end (str, optional): The string to be printed at the end of the value.
                             Defaults to a newline character ('\n').

    Returns:
        None

    Example:
        >>> print_with_newline("Hello, World!")
        Hello, World!

        >>> print_with_newline(42, end='--')
        42--

    """
    print(value, end=end)


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


def remove_newlines(text):
    """
    Removes newline characters (\n) from a given string.

    Args:
        text (str): The input string.

    Returns:
        str: The string with newline characters removed.
    """
    return text.replace("\n", "")
