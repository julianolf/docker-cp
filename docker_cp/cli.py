"""Copy file from or to a Docker container.

Usage:
    docker-cp [--buffer-length=<bytes>] FILE TARGET
    docker-cp (-h | --help)
    docker-cp --version

Arguments:
    FILE    Source file. e.g. mycontainer:/proc/version
    TARGET  Destination directory. e.g. .

Options:
    --buffer-length=<bytes>  Buffer size in bytes.
"""

import enum
import io
import os
import sys
import tarfile

import docker
import docopt
import schema


class CopyDirection(enum.Flag):
    """The direction of the copy relative to the container.

    Attributes:
        FROM: A flag indicating copy from the container to the host.
        TO: A flag indicating copy from the host to the container.
        ACROSS: A flag indicating copy between containers.
    """

    FROM = enum.auto()
    TO = enum.auto()
    ACROSS = FROM | TO


class CopyCommand(object):
    """Copy file from or to a Docker container.

    Attributes:
        version: A string with the command version.
        args: A dictionary containing the command arguments.
        client: A Docker client instance.
        direction: A copy direction (from/to/across a container).
        buffer_length: An integer for the file transfer buffer size.
        container: A Docker container to copy a file from/to.
        source: A string with the source file.
        destination: A string with the destination file path.
    """

    version = "0.1.0a1"

    def __init__(self, args):
        """Initialize copy command.

        Parameters:
            args: A dictionary with command arguments and options.

        Raises:
            SchemaError: If any argument value is invalid.
        """
        self.args = self.validate(args)
        self.client = docker.from_env()
        self.direction = CopyDirection.FROM & CopyDirection.TO
        self.buffer_length = docker.constants.DEFAULT_DATA_CHUNK_SIZE

    def validate(self, data):
        """Validate command arguments.

        Parameters:
            data: A dictionary with command arguments and options.

        Returns:
            A dictionary containing the validated command arguments.

        Raises:
            SchemaError: If any argument value is invalid.
        """
        validator = schema.Schema(
            {
                "FILE": schema.And(str, len, error="Invalid input file"),
                "TARGET": schema.And(
                    str, len, error="Invalid destination directory"
                ),
                schema.Optional("--buffer-length"): schema.Or(
                    None,
                    schema.And(
                        schema.Use(int),
                        lambda n: n > 0,
                        error=(
                            "Buffer length must be "
                            "an integer greater than 0"
                        ),
                    ),
                ),
                schema.Optional("--help"): schema.Use(bool),
                schema.Optional("-h"): schema.Use(bool),
                schema.Optional("--version"): schema.Use(bool),
            }
        )

        return validator.validate(data)

    def split_arg(self, arg):
        """Split an argument into container name and file path.

        Parameters:
            arg: A string argument representing a file input or target.

        Returns:
            A tuple of strings with a container name and a file path.

            e.g.

            'test:/proc/version' becomes ('test', '/proc/version')
            './file' becomes ('', './file')
        """
        if os.path.isdir(arg):
            return "", arg

        parts = arg.split(":", 1)
        if len(parts) == 1 or parts[0].startswith("."):
            return "", arg

        return parts[0], parts[1]

    def copy_from(self):
        """Copy file from a container to the host.

        Raises:
            APIError: If Docker server returns an error.
            ValueError: If destination path is invalid.
        """
        directory = os.path.abspath(self.destination)
        if not os.path.isdir(directory):
            directory = os.path.dirname(directory)
        if not os.path.exists(directory):
            raise ValueError("Invalid output path")

        data, stat = self.container.get_archive(
            self.source, chunk_size=self.buffer_length
        )

        stream = io.BytesIO()
        for chunk in data:
            stream.write(chunk)
        stream.seek(0)

        with tarfile.open(fileobj=stream) as tar:
            with tar.extractfile(stat["name"]) as f:
                content = f.read()
                output = os.path.join(directory, stat["name"])
                with open(output, "wb") as out:
                    out.write(content)

    def copy_to(self):
        """Copy file from the host to a container.

        Raises:
            APIError: If Docker server returns an error.
            ValueError: If source file doesn't exist or can't be read.
        """
        filepath = os.path.abspath(self.source)
        if not os.path.exists(filepath):
            raise ValueError("Invalid source file")

        filename = os.path.basename(filepath)
        stream = io.BytesIO()
        with open(filepath, "rb") as f:
            with tarfile.open(fileobj=stream, mode="w") as tar:
                stat = os.fstat(f.fileno())
                info = tarfile.TarInfo(name=filename)
                info.size = stat.st_size
                info.mode = stat.st_mode
                info.mtime = stat.st_mtime
                tar.addfile(info, fileobj=f)
        stream.seek(0)

        self.container.put_archive(self.destination, stream)

    def copy(self):
        """Perform a copy operation.

        Raises:
            APIError: If the Docker server returned an error.
            NotFound: If the given container is not found.
            ValueError: If the copy operation is invalid.
        """
        src_container, self.source = self.split_arg(self.args["FILE"])
        dst_container, self.destination = self.split_arg(self.args["TARGET"])

        if src_container:
            self.direction |= CopyDirection.FROM
            self.container = self.client.containers.get(src_container)
        if dst_container:
            self.direction |= CopyDirection.TO
            self.container = self.client.containers.get(dst_container)

        if self.args.get("--buffer-length", None):
            self.buffer_length = self.args["--buffer-length"]

        if self.direction == CopyDirection.FROM:
            self.copy_from()
        elif self.direction == CopyDirection.TO:
            self.copy_to()
        elif self.direction == CopyDirection.ACROSS:
            raise ValueError("Copying between containers is not supported")
        else:
            raise ValueError("At least one container must be specified")

    @classmethod
    def run(cls, args):
        """Run a file copy with the given arguments.

        Parameters:
            args: A dictionary with command arguments and options.
        """
        try:
            cmd = cls(args)
            cmd.copy()
        except ConnectionError:
            sys.exit("Could not connect to Docker")
        except Exception as err:
            sys.exit(err)


def main():
    """Read input arguments and run copy command."""
    args = docopt.docopt(__doc__, version=CopyCommand.version)
    CopyCommand.run(args)


if __name__ == "__main__":
    main()
