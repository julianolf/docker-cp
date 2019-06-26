import io
import tarfile

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


@pytest.fixture
def response():
    data = io.BytesIO(b"It's dangerous to go alone! Take this.\n")
    info = {
        "name": "oldman.txt",
        "size": 39,
        "mode": 33188,
        "mtime": 1561398395,
    }
    tarinfo = tarfile.TarInfo()
    for k, v in info.items():
        setattr(tarinfo, k, v)
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as tar:
        tar.addfile(tarinfo, data)
    return (stream.getvalue() for __ in range(1)), info
