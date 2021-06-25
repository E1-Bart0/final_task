import argparse
import os
import sys
from pathlib import Path

FILE_EXTENSIONS = ["", ".fb2", ".gz", ".zip"]


def parse_args(_args):
    """Create parser with args (-s, -a, -u) and parse args with the created parser"""
    parser = argparse.ArgumentParser(description="Save books in db")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s",
        type=dir_path,
        dest="dir_path",
        help="path to the folder with the catalog of books in the fb2, or fb2.zip, or fb2.gz format ",
    )
    group.add_argument(
        "-a",
        type=file_path,
        dest="book_path",
        help="path to one book in fb2, or fb2.zip, or fb2.gz format",
    )
    parser.add_argument(
        "-u",
        dest="flag",
        action="store_true",
        help="In case there is already a book in DataBase.\n"
        "If the -u flag is given, then we update the information about the book.\n"
        "If the -u flag is absent, then the information is not updated ",
    )
    return parser.parse_args(_args)


def dir_path(path):
    """Validate if path to directory exists"""
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"`{path}` is not a valid path for directory")


def file_path(path):
    if os.path.isfile(path):
        file_extension = Path(path).suffix
        if file_extension in FILE_EXTENSIONS:
            return path
        raise argparse.ArgumentTypeError(f"`{path}` is not a valid file extension")
    else:
        raise argparse.ArgumentTypeError(f"`{path}` is not a valid path to file")


def main():
    args = parse_args(sys.argv[1:])


if __name__ == "__main__":
    main()
