import os
from typing import Optional

from docgpt.io import print_error, print_warning, get_user_yes_no_input

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".docgpt")
KEY_FILE_PATH = os.path.join(CONFIG_DIR, "oai_key")


def get_api_key(input_api_key: Optional[str]) -> str:
    """Retrieve the OpenAI API key from the given input, environment variable, or cached file."""
    if input_api_key:
        return input_api_key

    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]

    if KEY_FILE_PATH:
        with open(KEY_FILE_PATH, mode="r", encoding="utf-8") as file:
            api_key = file.read()
            if api_key:
                return api_key

    print_warning("OpenAI API Key: ", end="")
    user_api_key: str = input()
    if user_api_key:
        return user_api_key

    print_error(
        "OpenAI API Key as not found.\n"
        "Get API Key from OpenAI here: https://openai.com/api/\n"
        "and set the 'OPENAI_API_KEY' environment variable or use the '--api_key' flag.",
    )
    return ""


def cache_api_key(key_to_cache: str):
    """Cache the given OpenAI API key in a file."""
    if not key_to_cache:
        return

    if os.path.exists(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, mode="r", encoding="utf-8") as file:
            old_key = file.read()
        if old_key == key_to_cache:
            return

        # Prompt user to replace cached API key
        print("Do you want to replace the cached OpenAI API Key? ([Y]es/[N]o) [Yes]")
        if get_user_yes_no_input():
            return

    # Create directory and cache API key
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(KEY_FILE_PATH, mode="w", encoding="utf-8") as file:
        file.write(key_to_cache)
