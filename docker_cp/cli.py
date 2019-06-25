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

import docker
import docopt


class CopyCommand(object):
    """Copy file from or to a Docker container.

    Attributes:
        version: A string with the command version.
        args: A dictionary containing the command arguments.
        client: A Docker client instance.
        buffer_length: An integer for the file transfer buffer size.
    """

    version = "0.1.0a1"

    def __init__(self, args):
        """Initialize copy command.

        Parameters:
            args: A dictionary with command arguments and options.
        """
        self.args = args
        self.client = docker.from_env()
        self.buffer_length = docker.constants.DEFAULT_DATA_CHUNK_SIZE

    def copy(self):
        """Perform a copy operation."""
        pass

    @classmethod
    def run(cls, args):
        """Run a file copy with the given arguments.

        Parameters:
            args: A dictionary with command arguments and options.
        """
        cmd = cls(args)
        cmd.copy()


def main():
    """Read input arguments and run copy command."""
    args = docopt.docopt(__doc__, version=CopyCommand.version)
    CopyCommand.run(args)


if __name__ == "__main__":
    main()
