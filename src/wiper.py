import logging
import sys
from argparse import ArgumentParser

from db.core import session_scope
from db.services import delete_book_or_all_db


def parse_args(_args):
    """Create parser with args (-n, -a) and parse args with the created parser"""
    parser = ArgumentParser(description="Delete books in db")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-n", type=int, dest="number", required=False, help="Primary key of book"
    )
    group.add_argument("-a", dest="all", action="store_true", help="Flush DB")
    return parser.parse_args(_args)


def main():
    logging.debug(f"Called {sys.argv[0]} with {sys.argv[1:]}")

    args = parse_args(sys.argv[1:])
    with session_scope() as session:
        row_deleted = delete_book_or_all_db(session, args.number, args.all)
        logging.info(f"Deleted rows: {row_deleted}")


if __name__ == "__main__":
    main()
