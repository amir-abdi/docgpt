from pydoc_gpt import main
import os


def test_get_target():
    source_path = "/path/to/sample.py"
    assert (
        main.get_target(source_path=source_path, target=None, overwrite=False)
        == f"/path/to/sample_{main.DEFAULT_TARGET_APPEND}"
    )

    assert (
        main.get_target(source_path=source_path, target=None, overwrite=False)
        == f"/path/to/sample_{main.DEFAULT_TARGET_APPEND}"
    )

    assert main.get_target(source_path=source_path, target=None, overwrite=True) == source_path


def test_get_source_code():
    source_code, source_path = main.get_source_code(
        source=os.path.join(os.curdir, "pydoc_gpt/main.py")
    )
    assert len(source_code) > 100
    assert source_path == "./pydoc_gpt/main.py"


def test_estimate_tokens():
    # this, ' ', is, /, a, +, 4
    assert main.estimate_num_tokens("this is/a+4") == int(7 * main.TOKEN_ESTIMATE_COEFF)
