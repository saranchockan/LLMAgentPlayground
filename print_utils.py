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
