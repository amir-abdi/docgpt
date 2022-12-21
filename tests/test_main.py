import os

from docgpt import main


def test_get_target():
    source_path = "/path/to/sample"

    assert (
        main.get_target(source_path=source_path, target=None, overwrite=False)
        == f"/path/to/sample_{main.DEFAULT_TARGET_APPEND}"
    )

    assert (
        main.get_target(source_path=f"{source_path}.py", target=None, overwrite=False)
        == f"/path/to/sample_{main.DEFAULT_TARGET_APPEND}.py"
    )

    # new_target with cpp extension
    assert (
        main.get_target(source_path=f"{source_path}.cpp", target="new_target", overwrite=False)
        == f"new_target.cpp"
    )

    # mixed extension (impossible case)
    assert (
        main.get_target(source_path=f"{source_path}.cpp", target="new_target.py", overwrite=False)
        == f"new_target.py.cpp"
    )

    assert main.get_target(source_path=source_path, target=None, overwrite=True) == source_path


def test_get_source_code():
    source_code, source_path = main.get_source_code(
        source=os.path.join(os.curdir, "docgpt/main.py")
    )
    assert len(source_code) > 100
    assert source_path == "./docgpt/main.py"
