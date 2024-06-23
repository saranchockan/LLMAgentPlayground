import re
from collections import defaultdict
from difflib import SequenceMatcher
from typing import (
    Any,
    Callable,
    DefaultDict,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    TypedDict,
    TypeVar,
    Union,
)


def similarity_ratio(str1: str, str2: str) -> float:
    """
    Calculate the similarity ratio between two strings.

    Parameters:
    str1 (str): The first string.
    str2 (str): The second string.

    Returns:
    float: The similarity ratio between the two strings.
    """
    return SequenceMatcher(None, str1, str2).ratio()


def are_urls_similar(url1: str, url2: str, threshold: float = 0.9) -> bool:
    """
    Determine if two URLs are similar based on a given threshold.

    Parameters:
    url1 (str): The first URL.
    url2 (str): The second URL.
    threshold (float): The similarity ratio threshold. Default is 0.9.

    Returns:
    bool: True if the similarity ratio is above the threshold, False otherwise.
    """
    ratio = similarity_ratio(url1, url2)
    return ratio >= threshold


def get_first_or_raise(lst):
    """
    Returns the first element of a list or raises a ValueError if the list is empty.

    Args:
        lst (list): The input list.

    Returns:
        The first element of the list.

    Raises:
        ValueError: If the input list is empty.
    """
    if not lst:
        raise ValueError("The input list is empty.")

    return lst[0]


T = TypeVar("T")
K = TypeVar("K")


def group_by(items: Iterable[T], key: Callable[[T], K]) -> DefaultDict[K, list[T]]:
    """
    Group a collection of items by a key function.

    Args:
        items (Iterable[T]): The collection of items to be grouped.
        key (Callable[[T], K]): A function that takes an item and returns a key to group by.

    Returns:
        DefaultDict[K, list[T]]: A dictionary-like object where the keys are the unique values
            returned by the key function, and the values are lists of items that share that key.

    Example:
        >>> people = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
        >>> grouped_by_age = group_by(people, lambda p: p["age"])
        >>> grouped_by_age
        defaultdict(<class 'list'>, {25: [{'name': 'Alice', 'age': 25}], 30: [{'name': 'Bob', 'age': 30}]})
    """
    result: DefaultDict[K, list[T]] = defaultdict(list)
    for item in items:
        key_value = key(item)
        result[key_value].append(item)
    return result


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
            print(f"{name} = {value}")
            break


def print_with_newline(value: Any, end: str = "\n\n") -> None:
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


def remove_newlines(text):
    """
    Removes newline characters (\n) from a given string.

    Args:
        text (str): The input string.

    Returns:
        str: The string with newline characters removed.
    """
    return text.replace("\n", "")


def str_to_bool(string):
    """
    Convert a string to a boolean value.

    Args:
        string (str): The input string to be converted. The function expects
            the string to be either "True" or "False" (case-insensitive).

    Returns:
        bool: The boolean value corresponding to the input string.

    Raises:
        ValueError: If the input string is not "True" or "False" (case-insensitive).

    Examples:
        >>> str_to_bool("True")
        True
        >>> str_to_bool("FALSE")
        False
        >>> str_to_bool("hello")
        Traceback (most recent call last):
            ...
        ValueError: Invalid input: hello. Expected 'True' or 'False'.
    """
    string = string.lower()
    if string == "true":
        return True
    elif string == "false":
        return False
    else:
        raise ValueError(f"Invalid input: {string}. Expected 'True' or 'False'.")


def is_truthy(value) -> bool:
    """
    Determine if a value is truthy according to Python's truthiness rules.

    This function returns False for None and all falsy values, and True otherwise.

    Falsy values in Python include:
    - None
    - False
    - Zero of any numeric type (0, 0.0, 0j)
    - Empty sequences and collections ('', (), [], {}, set(), range(0))

    Parameters:
    value (any): The value to be evaluated for truthiness.

    Returns:
    bool: False if the value is None or falsy, True otherwise.

    Examples:
    >>> is_truthy(None)
    False
    >>> is_truthy(0)
    False
    >>> is_truthy('')
    False
    >>> is_truthy([])
    False
    >>> is_truthy(1)
    True
    >>> is_truthy('Hello')
    True
    >>> is_truthy([1, 2, 3])
    True
    """
    return bool(value)


def none_to_str(value: Union[str, None]) -> str:
    """
    Convert None to an empty string.

    Args:
        value (str): The input string or None.

    Returns:
        str: The original string if not None, otherwise an empty string.
    """
    return "" if value is None else value
