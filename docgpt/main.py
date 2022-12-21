import fileinput
import os
import sys
from typing import Optional, Tuple

import openai
from jsonargparse import CLI

from docgpt import model
from docgpt.api_key import cache_api_key, get_api_key
from docgpt.io import print_error, print_warning, wlf

DEFAULT_TARGET_APPEND = "docgpt"
MIN_SOURCE_LENGTH = 40


def get_source_code(source: Optional[str]) -> Tuple[str, str]:
    """Get the source code from the given path or from stdin."""
    if source is not None:

        # source = path to file
        if not os.path.exists(source):
            print_error(f"Source file does not exist at '{source}'")
            return "", ""

        if os.path.isdir(source):
            print_warning(
                "Current version of DocGPT does not support directory inputs. "
                "If you need the feature to recursively convert all source files in a "
                "directory, please submit an issue: "
                "https://github.com/amir-abdi/docgpt/issues"
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

    print_error("No source provided.\n")
    print_warning(
        "Common use cases:\n"
        ">> docgpt --source <source> --target <target>\n"
        ">> docgpt --source <source> --overwrite\n"
        ">> docgpt --source <source>\n"
        ">> docgpt <source>\n"
        ">> cat <source> | docgpt",
    )
    return "", ""


def get_target(source_path: str, overwrite: bool, target: Optional[str]):
    """Get the target path for the documented source code."""
    # overwrite the source file
    if overwrite:
        return source_path

    # Get `target_path` from the `source_path`
    source_path_wo_ext, ext = os.path.splitext(source_path)
    if not target:
        target_path = f"{source_path_wo_ext}_{DEFAULT_TARGET_APPEND}{ext}"
        print_warning(f"No '--target' specified; will store the documented file at '{target_path}'")

    # `target_path` is given by the user
    else:
        target_path = target

    # Append extension to the target path if it is not already present
    if not target_path.endswith(ext):
        target_path += ext

    return target_path


def validate_args(source: Optional[str], target: Optional[str], overwrite: bool) -> bool:
    """Validate the given arguments."""
    # Check if overwrite flag is used and source is not specified
    if overwrite and source is None:
        print_error("The '--source' flag is required when '--overwrite' flag is used.")
        return False

    if overwrite and target is not None:
        print_error(
            "The '-overwrite' and '--target' flags are mutually exclusive, use either, not both."
        )
        return False

    # Check if source and target are not specified
    if source is None and target is None:
        print_error(
            "In absence of '--source', please specify where you wish to export via '--target' flag."
        )
        return False

    # Return true if all arguments are valid
    return True


def main(
    source: Optional[str] = None,
    target: Optional[str] = None,
    api_key: Optional[str] = None,
    overwrite: bool = False,
) -> int:
    """DocGPT is a CLI tool to automatically document source code.

    Args:
        source: source code or path to source file.
        target: path to where the output file will be stored.
        api_key: OpenAI API key.
        overwrite: whether to overwrite the source file.
    """
    print(wlf())

    # Set API Key
    api_key = get_api_key(api_key)
    if not api_key:
        return 1
    cache_api_key(api_key)
    openai.api_key = api_key

    source_code, source_path = get_source_code(source)
    if not source_code:
        return 1

    # Get prompt from source code
    prompt = model.get_prompt(source_code)
    estimated_tokens = model.estimate_num_tokens(prompt)
    if not model.validate_prompt_length(estimated_tokens):
        return 1

    if not validate_args(source, target, overwrite):
        return 1

    # Get target path for output
    target_path = get_target(source_path=source_path, overwrite=overwrite, target=target)

    print(f"source: {source_path}")
    print(f"target: {target_path}")

    # Invoke GPT-3 to generate documentation
    print("Waiting for GPT3 to respond...")
    completed_text = model.invoke(prompt, estimated_tokens)

    # Write output to target path
    with open(target_path, mode="w", encoding="utf-8") as file:
        file.write(completed_text)
    print(f"Documented source code exported: {target_path}")
    return 0


def cli():
    """Command line interface for docgpt."""
    if len(sys.argv) >= 2:

        # First arg as --source
        new_argv = sys.argv[1:]
        if not sys.argv[1].startswith("--"):
            new_argv = ["--source"] + sys.argv[1:]

        # --overwrite as store true
        if "--overwrite" in new_argv:
            overwrite_i = new_argv.index("--overwrite")
            if overwrite_i == len(new_argv) - 1 or new_argv[overwrite_i + 1].startswith("--"):
                new_argv.insert(overwrite_i + 1, "true")

        sys.exit(CLI(main, args=new_argv))

    sys.exit(CLI(main))


if __name__ == "__main__":
    cli()
