import logging
import os
import sys
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
from typing import Sequence, Union

from db.core import session_scope
from db.services import create_books_and_authors
from services.parse_book_from_file import FILE_EXTENSIONS, find_books


def parse_args(_args: Sequence[str]) -> ArgumentParser.__class__:
    """Create parser with args (-s, -a, -u) and parse args with the created parser"""
    parser = ArgumentParser(description="Save books in db")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s",
        type=validate_dir_path,
        dest="dir_path",
        help="path to the folder with the catalog of books in the fb2, or fb2.zip, or fb2.gz format ",
    )
    group.add_argument(
        "-a",
        type=validate_file_path,
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


def validate_dir_path(path: Union[str, Path]) -> Path:
    """Validate if path to directory exists"""
    if os.path.isdir(path):
        return path
    else:
        raise ArgumentTypeError(f"`{path}` is not a valid path for directory")


def validate_file_path(path: Union[str, Path]) -> Path:
    """Validate if path to file exists and file with correct extension"""
    if os.path.isfile(path):
        file_extension = Path(path).suffix
        if file_extension in FILE_EXTENSIONS:
            return path
        raise ArgumentTypeError(f"`{path}` is not a valid file extension")
    else:
        raise ArgumentTypeError(f"`{path}` is not a valid path to file")


def main():
    logging.debug(f"Called {sys.argv[0]} with {sys.argv[1:]}")
    args = parse_args(sys.argv[1:])
    books = find_books(args.dir_path, args.book_path)
    if books is None:
        logging.info("Book not Found")
        return
    logging.debug(f"Saving {len(books)} books")
    with session_scope() as session:
        create_books_and_authors(session, books, args.flag)


if __name__ == "__main__":
    main()
