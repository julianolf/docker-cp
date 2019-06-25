import sys
from unittest import mock

import pytest
import schema

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


@pytest.mark.parametrize(
    "arg,exp",
    [
        (
            {"--buffer-length": "4.5"},
            "Buffer length must be an integer greater than 0",
        ),
        ({"FILE": ""}, "Invalid input file"),
        ({"TARGET": ""}, "Invalid destination directory"),
    ],
)
def test_validate_raises_exception(arg, exp, args):
    cmd = cli.CopyCommand(args)
    args.update(arg)
    with pytest.raises(schema.SchemaError) as error:
        cmd.validate(args)
    assert str(error.value) == exp


@pytest.mark.parametrize(
    "arg,exp",
    [
        ("", ("", "")),
        ("./", ("", "./")),
        ("test:/proc/version", ("test", "/proc/version")),
    ],
)
def test_split_arg_properly(arg, exp, args):
    cmd = cli.CopyCommand(args)
    assert cmd.split_arg(arg) == exp
