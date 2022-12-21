import logging
import re
from textwrap import dedent

import openai

from docgpt.io import print_warning

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# prompt constants
S_TAG = "<script>"
ENDS_TAG = "</script>"
MAX_PROMPT_LENGTH_THRESHOLD = 1800
TOKEN_ESTIMATE_COEFF = 1.28


# Model constants
MAX_CONTEXT_LENGTH = 4097
OAI_MODEL = "text-davinci-003"


def get_prompt(source_code: str):  # pragma: no cover
    """Generate a prompt for the given source code."""
    return dedent(
        f'''
    Add comments and one-liner docstrings to the following source code to help explain
    what each line of code is doing and how it contributes to the overall function of the program.

    {S_TAG}
    def permute_batch(z):
        assert z.dim() == 2
        B, _ = z.size()

        perm_idx = torch.randperm(B)
        permuted_z = z[perm_idx, :]

        return permuted_z, perm_idx
    {ENDS_TAG}

    The documented script is:
    {S_TAG}
    def permute_batch(z):
        """Permute the samples in the given batch across the first dimension."""
        # Assert dimension is 2
        assert z.dim() == 2

        # Get shape of tensor
        B, _ = z.size()

        # Randomly permute z
        perm_idx = torch.randperm(B)
        permuted_z = z[perm_idx, :]

        # return the permuted tensor and the permutation index
        return permuted_z, perm_idx
    {ENDS_TAG}

    {S_TAG}
    #include <iostream>
    #include <vector>

    using namespace std;

    void quicksort(vector<int> &arr, int left, int right) {{
      if (left >= right) return;

      int pivot = arr[(left + right) / 2];
      swap(arr[left], arr[(left + right) / 2]);
      int i = left + 1;
      int j = right;

      while (i <= j) {{
        while (i <= j && arr[i] < pivot) i++;
        while (i <= j && arr[j] >= pivot) j--;
        if (i < j) swap(arr[i++], arr[j--]);
      }}

      swap(arr[left], arr[j]);

      quicksort(arr, left, j - 1);
      quicksort(arr, j + 1, right);
    }}
    {ENDS_TAG}

    The documented script is:
    {S_TAG}
    #include <iostream>
    #include <vector>

    using namespace std;

    void quicksort(vector<int> &arr, int left, int right) {{
      // base case: if the subarray has fewer than 2 elements, it's already sorted
      if (left >= right) return;

      // choose a pivot element and move it to the front of the subarray
      int pivot = arr[(left + right) / 2];
      swap(arr[left], arr[(left + right) / 2]);
      int i = left + 1;
      int j = right;

      // partition the subarray around the pivot
      while (i <= j) {{
        // find the first element that is larger than the pivot
        while (i <= j && arr[i] < pivot) i++;
        // find the last element that is smaller than the pivot
        while (i <= j && arr[j] >= pivot) j--;
        // if i and j have not crossed, swap the elements and move on
        if (i < j) swap(arr[i++], arr[j--]);
      }}

      // move the pivot element to its final position
      swap(arr[left], arr[j]);

      // recursively sort the left and right subarrays
      quicksort(arr, left, j - 1);
      quicksort(arr, j + 1, right);
    }}
    {ENDS_TAG}

    {S_TAG}
    {source_code}
    {ENDS_TAG}

    The documented script is:
    {S_TAG}

    '''
    )


def invoke(prompt: str, estimated_tokens: int):
    completions = openai.Completion.create(
        engine=OAI_MODEL,
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


def estimate_num_tokens(prompt: str) -> int:
    """Estimate the number of tokens in the given prompt."""
    tokens = re.split(r"([\W_]+)", prompt)
    return int(len(tokens) * TOKEN_ESTIMATE_COEFF)


def validate_prompt_length(estimated_tokens: int) -> bool:
    """Validate the estimated number of tokens against the maximum prompt length threshold."""
    if estimated_tokens > MAX_PROMPT_LENGTH_THRESHOLD:
        print_warning(
            (
                f"Your file is too big. It contains around {estimated_tokens} which is more than "
                f"half the model's context length ({MAX_CONTEXT_LENGTH}). "
                f"Not enough context space left for auto-documentation. "
                f"Please partition the file into smaller chunks and try each separately."
            ),
        )
        return False
    return True
