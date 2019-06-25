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

import docopt


def main():
    """Read input arguments."""
    docopt.docopt(__doc__, version="0.1.0a1")


if __name__ == "__main__":
    main()
