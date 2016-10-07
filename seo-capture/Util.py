import typing

def find_value(arg: str, string: str) -> str:
    """ Searches for "arg=X" in the string and returns X
    as a string
    """
    for s in string.split():
        if s[0:len(arg)+1] == arg+"=":
            return s[len(arg)+1:]

    return ""

