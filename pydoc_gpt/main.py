import fileinput
import logging
import os
import re
import sys
from textwrap import dedent
from typing import Optional

import openai
from jsonargparse import CLI

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# path constants
DEFAULT_TARGET_APPEND = "pydoced.py"
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".docgpt")
KEY_FILE_PATH = os.path.join(CONFIG_DIR, "OAI_KEY")

# prompt constants
S_TAG = "<script>"
ENDS_TAG = "</script>"
MIN_SOURCE_LENGTH = 40
MAX_PROMPT_LENGTH_THRESHOLD = 1800
TOKEN_ESTIMATE_COEFF = 1.27

# Model constants
MAX_CONTEXT_LENGTH = 4097
MODEL = "text-davinci-003"


def get_api_key(input_api_key: Optional[str]) -> str:
    if input_api_key:
        return input_api_key

    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]

    if KEY_FILE_PATH:
        with open(KEY_FILE_PATH, mode="r", encoding="utf-8") as file:
            api_key = file.read()
            if api_key:
                return api_key

    print_error(
        "OpenAI API Key as not found. Please set the 'OPENAI_API_KEY' environment variable",
    )
    return ""


def get_user_yes_no_input() -> bool:
    user_input = input()
    if user_input.lower() not in ("y", "yes", None, "", " "):
        return True
    return False


def cache_api_key(key_to_cache: str):
    if not key_to_cache:
        return

    if os.path.exists(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, mode="r", encoding="utf-8") as file:
            old_key = file.read()
        if old_key == key_to_cache:
            return

        print("Do you want to replace the cached OpenAI API Key? ([Y]es/[N]o) [Yes]")
        if get_user_yes_no_input():
            return

    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(KEY_FILE_PATH, mode="w", encoding="utf-8") as file:
        file.write(key_to_cache)


def get_prompt(source_code: str):
    return dedent(
        f'''
    Please add comments and one-liner docstrings to the following Python script to help explain
    what each line of code is doing and how it contributes to the overall function of the program.

    {S_TAG}
    def permute_batch(z):
        assert z.dim() == 2
        B, _ = z.size()

        perm_idx = torch.randperm(B)
        permuted_z = z[perm_idx, :]

        return permuted_z, perm_idx
    {ENDS_TAG}

    The updated script is:
    {S_TAG}
    def permute_batch(z):
        """Permute the samples in the given batch across the first dimension."""
        assert z.dim() == 2
        B, _ = z.size()

        # Randomly permute z
        perm_idx = torch.randperm(B)
        permuted_z = z[perm_idx, :]

        # return the permuted tensor and the permutation index
        return permuted_z, perm_idx
    {ENDS_TAG}

    {S_TAG}
    {source_code}
    {ENDS_TAG}

    The updated script is:
    {S_TAG}

    '''
    )


def estimate_num_tokens(prompt: str) -> int:
    tokens = re.split(r"([\W_]+)", prompt)
    return int(len(tokens) * TOKEN_ESTIMATE_COEFF)


def get_source_code(source: Optional[str]) -> tuple[str, str]:
    if source is not None:

        # source = path to file
        if source.endswith(".py"):
            if not os.path.exists(source):
                print_error(f"Source file does not exist at '{source}'")
                return "", ""

            if os.path.isdir(source):
                print_warning(
                    "Current version of DocGPT does not support directory inputs. "
                    "If you need the feature to recursively convert all python files in a "
                    "directory, please submit an issue: "
                    "https://github.com/amir-abdi/DocGPT/issues"
                )
                return "", ""

            with open(source, mode="r", encoding="utf-8") as file:
                return file.read().strip(), source

    # try piped input
    if not sys.stdin.isatty():
        source_code = ""
        with fileinput.input() as lines:
            for line in lines:
                source_code += f"{line}"

        if len(source_code) < MIN_SOURCE_LENGTH:
            print_error("The source code you passed is too small:\n")
            print(source_code)
            return "", ""

        return source_code, os.path.curdir

    print_error("No source provided.")
    print_warning(
        "You can pass the source code in 3 ways:\n"
        ">> docgpt --source <file.py>\n"
        ">> cat <file.py> | docgpt",
    )
    return "", ""


def code_to_chars(code):
    csi = "\033["
    return csi + str(code) + "m"


def print_warning(msg: str):
    yellow = code_to_chars(33)
    reset = code_to_chars(0)
    print(f"{yellow}{msg}{reset}")


def print_error(msg: str):
    red = code_to_chars(31)
    reset = code_to_chars(0)
    print(f"{red}{msg}{reset}")


def get_target(source_path: str, overwrite: bool, target: Optional[str]):
    # overwrite the source file
    if overwrite:
        return source_path

    # Get `target_path` from the `source_path`
    if not target:
        target_path = f"{os.path.splitext(source_path)[0]}_{DEFAULT_TARGET_APPEND}"

    # `target_path` is given by the user
    else:
        target_path = target

    if not target_path.endswith(".py"):
        target_path += ".py"

    return target_path


def validate_args(source, target, overwrite) -> bool:
    if overwrite and source is None:
        print_error("The '--source' flag is required when '--overwrite' flag is used.")
        return False

    if source is None and target is None:
        print_error(
            "In absence of '--source', please specify where you wish to export via '--target' flag."
        )
        return False

    return True


def invoke_oai_model(prompt: str, estimated_tokens: int):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=MAX_CONTEXT_LENGTH - estimated_tokens,
        temperature=0.0,
        top_p=0.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=ENDS_TAG,
    )

    completed_text = completions.choices[0].text
    if completions.usage.total_tokens > MAX_CONTEXT_LENGTH - 10:
        print_warning(
            "Model ran out of token space (reached max Context Length). "
            "The output file is probably missing some lines. "
            "Please chunk the source code into multiple files and retry ach separately."
        )

    logger.debug(completions.choices[0].text)
    logger.debug(completed_text)

    # Cleanup completion and add blank line end of file
    completed_text = completed_text.strip()
    completed_text += "\n"

    return completed_text


def validate_prompt_length(estimated_tokens: int) -> bool:
    if estimated_tokens > MAX_PROMPT_LENGTH_THRESHOLD:
        print_warning(
            (
                f"Your file is too big. It contains around {estimated_tokens} which is more than "
                f"half the model's context length ({MAX_CONTEXT_LENGTH}). "
                f"Not enough context space left for completion (adding docstrings and comments). "
                f"Please partition the file into smaller chunks and try each separately."
            ),
        )
        return False
    return True

def main(
        source: Optional[str] = None,
        target: Optional[str] = None,
        api_key: Optional[str] = None,
        overwrite: bool = False,
) -> int:
    """DocGPT is a CLI tool to automatically document Python source code.

    Args:
        source: source code or path to source file.
        target: path to where the output file will be stored.
        api_key: OpenAI API key.
        overwrite: whether to overwrite the source file.
    """
    # Set API Key
    api_key = get_api_key(api_key)
    if not api_key:
        return 1
    cache_api_key(api_key)
    openai.api_key = api_key

    if not validate_args(source, target, overwrite):
        return 1

    source_code, source_path = get_source_code(source)
    if not source_code:
        return 1
    target_path = get_target(source_path=source_path, overwrite=overwrite, target=target)

    prompt = get_prompt(source_code)
    estimated_tokens = estimate_num_tokens(prompt)
    if not validate_prompt_length(estimated_tokens):
        return 1

    print("Waiting for GPT3 to respond...")
    completed_text = invoke_oai_model(prompt, estimated_tokens)

    with open(target_path, mode="w", encoding="utf-8") as file:
        file.write(completed_text)
    print(f"Commented script exported: {target_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if not sys.argv[1].startswith("--"):
            new_argv = ["--source"] + sys.argv[1:]
            sys.exit(CLI(main, args=new_argv))

    sys.exit(CLI(main))
