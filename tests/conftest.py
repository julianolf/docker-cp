import pytest


@pytest.fixture
def args():
    return {
        "--buffer-length": "4",
        "--help": False,
        "--version": False,
        "-h": False,
        "FILE": "test:/proc/version",
        "TARGET": ".",
    }
