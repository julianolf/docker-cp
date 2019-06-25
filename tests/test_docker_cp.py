import sys
from unittest import mock

import pytest

from docker_cp import cli


def test_main(args):
    argv = ["docker_cp.cli", args["FILE"], args["TARGET"]]
    with mock.patch.object(sys, "argv", argv):
        try:
            cli.main()
        except SystemExit:
            assert not "Should not be raised"


def test_main_missing_required_argument(args):
    argv = ["docker_cp.cli", args["FILE"]]
    with mock.patch.object(sys, "argv", argv):
        with pytest.raises(SystemExit):
            cli.main()
