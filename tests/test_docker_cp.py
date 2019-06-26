import sys
import tempfile
from unittest import mock

import docker
import pytest
import schema

from docker_cp import cli


def test_main(args):
    argv = ["docker_cp.cli", args["FILE"], args["TARGET"]]
    with mock.patch.object(sys, "argv", argv):
        with mock.patch("docker_cp.cli.CopyCommand") as m_cp:
            try:
                cli.main()
                assert m_cp.run.called
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


def test_CopyDirection_enum_flag():
    _from = cli.CopyDirection.FROM
    _to = cli.CopyDirection.TO
    _across = cli.CopyDirection.ACROSS
    assert _from != _to
    assert _from != _across
    assert _to != _across
    assert _from | _to == _across


def test_docker_server_connection_fail(args):
    expected = "Could not connect to Docker"
    with mock.patch("docker_cp.cli.docker") as m_docker:
        m_cli = mock.Mock()
        m_cli.containers.get.side_effect = ConnectionError(expected)
        m_docker.from_env.return_value = m_cli
        with pytest.raises(SystemExit) as error:
            cli.CopyCommand.run(args)
        assert str(error.value.code) == expected


def test_container_not_found(args):
    expected = "Container not found"
    with mock.patch("docker_cp.cli.docker") as m_docker:
        m_cli = mock.Mock()
        m_cli.containers.get.side_effect = docker.errors.NotFound(expected)
        m_docker.from_env.return_value = m_cli
        with pytest.raises(SystemExit) as error:
            cli.CopyCommand.run(args)
        assert str(error.value.code) == expected


def test_copy_between_containers_unsupported(args):
    args["TARGET"] = "other:/tmp"
    expected = "Copying between containers is not supported"
    with mock.patch("docker_cp.cli.docker"):
        with pytest.raises(SystemExit) as error:
            cli.CopyCommand.run(args)
        assert str(error.value.code) == expected


def test_copy_needs_container(args):
    args["FILE"] = "file"
    expected = "At least one container must be specified"
    with mock.patch("docker_cp.cli.docker"):
        with pytest.raises(SystemExit) as error:
            cli.CopyCommand.run(args)
        assert str(error.value.code) == expected


def test_copy_from_container_to_invalid_path(args):
    args["TARGET"] = "/foo_/bar_"
    expected = "Invalid output path"
    with mock.patch("docker_cp.cli.docker"):
        with pytest.raises(SystemExit) as error:
            cli.CopyCommand.run(args)
        assert str(error.value.code) == expected


def test_copy_from_container(args, response):
    with mock.patch("docker_cp.cli.docker") as m_docker:
        m_container = mock.Mock()
        m_container.get_archive.return_value = response
        m_cli = mock.Mock()
        m_cli.containers.get.return_value = m_container
        m_docker.from_env.return_value = m_cli
        with mock.patch(
            "builtins.open", new_callable=mock.mock_open()
        ) as m_open:
            cmd = cli.CopyCommand(args)
            cmd.copy()
            assert m_open.called
            assert m_container.get_archive.called


def test_copy_to_container_from_invalid_path(args):
    args["FILE"] = "/foo_/bar_"
    args["TARGET"] = "test:/tmp"
    expected = "Invalid source file"
    with mock.patch("docker_cp.cli.docker"):
        with pytest.raises(SystemExit) as error:
            cli.CopyCommand.run(args)
        assert str(error.value.code) == expected


def test_copy_to_container(args):
    with mock.patch("docker_cp.cli.docker") as m_docker:
        m_container = mock.Mock()
        m_cli = mock.Mock()
        m_cli.containers.get.return_value = m_container
        m_docker.from_env.return_value = m_cli
        with tempfile.NamedTemporaryFile() as tmpf:
            tmpf.write(b"It's a secret to everybody.\n")
            args["FILE"] = tmpf.name
            args["TARGET"] = "test:/tmp"
            try:
                cli.CopyCommand.run(args)
                assert m_container.put_archive.called
            except SystemExit:
                assert not "Should not be raised"
