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
        print(f"{prefix}{combined_string}{suffix}")


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


from typing import List

from playwright_data_interface import WebElement


def print_metadata_list(metadata_list: List[WebElement.Metadata]) -> None:
    """
    Prints a list of Metadata objects in a readable format with spacing.

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
