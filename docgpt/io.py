# pylint: disable=W,C
from textwrap import dedent
from typing import Optional


def reset():
    """Reset the terminal color to default."""
    return code_to_chars(0)


def code_to_chars(code):
    """Convert a color code to a terminal color character."""
    csi = "\033["
    return csi + str(code) + "m"


def print_warning(msg: str, end: Optional[str] = None):
    """Print a warning message in yellow."""
    yellow = code_to_chars(33)
    print(f"{yellow}{msg}{reset()}", end=end)


def print_error(msg: str, end: Optional[str] = None):
    """Print an error message in red."""
    red = code_to_chars(31)
    print(f"{red}{msg}{reset()}", end=end)


def wlf():
    """Print the 'Woman Life Freedom' message in cyan."""
    cyan = code_to_chars(36)
    yellow = code_to_chars(33)
    return dedent(
        f"""{cyan}
        ███████████████████████████████████████████████████████████████████████████████████████████████████████████
        █▄─█▀▀▀█─▄█─▄▄─█▄─▀█▀─▄██▀▄─██▄─▀█▄─▄███▄─▄███▄─▄█▄─▄▄─█▄─▄▄─███▄─▄▄─█▄─▄▄▀█▄─▄▄─█▄─▄▄─█▄─▄▄▀█─▄▄─█▄─▀█▀─▄█
        ██─█─█─█─██─██─██─█▄█─███─▀─███─█▄▀─█████─██▀██─███─▄████─▄█▀████─▄████─▄─▄██─▄█▀██─▄█▀██─██─█─██─██─█▄█─██
        ▀▀▄▄▄▀▄▄▄▀▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▀▀▄▄▄▄▄▀▄▄▄▀▄▄▄▀▀▀▄▄▄▄▄▀▀▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▀▄▄▄▄▀▄▄▄▀▄▄▄▀
    Global action in solidarity with {yellow}Courageous People of Iran{cyan} who are demonstrating peacefully for their human rights.

        Timeline of Events:\t\thttps://irantimelines.com/
        #MahsaAmini on Twitter:\t\thttps://twitter.com/search/?q=MahsaAmini
        Song (Baraye by Shervin):\thttps://www.youtube.com/watch?v=BGesf7QcREk
    {reset()}
    """
    )


def get_user_yes_no_input() -> bool:
    """Get user input and return a boolean value based on the input."""
    user_input = input()
    if user_input.lower() not in ("y", "yes", None, "", " "):
        return True
    return False
