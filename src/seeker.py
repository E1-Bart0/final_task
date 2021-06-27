import sys
from argparse import ArgumentParser

from .db.core import session_scope
from .db.services import get_books_from_db


def parse_args(_args):
    """Create parser with args (-a, -n, -y -s) and parse args with the created parser"""
    parser = ArgumentParser(description="Find books in db")
    parser.add_argument(
        "-n", type=str, dest="book_name", required=True, help="Book name", nargs="+"
    )
    parser.add_argument(
        "-a",
        type=str,
        dest="author",
        required=False,
        help="Book author full name",
        nargs=2,
    )
    parser.add_argument(
        "-y",
        type=int,
        dest="year",
        required=False,
        help="year of publication of the book ",
    )
    parser.add_argument(
        "-s",
        dest="primary_key_flag",
        action="store_true",
        help="In case there is already a book in DataBase.\n"
        "If the -s flag is given, then we return book primary key"
        "If the -s flag is absent, then we return book",
    )
    return parser.parse_args(_args)


def main():
    args = parse_args(sys.argv[1:])

    book_name = " ".join(args.book_name)
    author_first_name, author_last_name = None, None
    if args.author is not None:
        author_first_name, author_last_name = args.author

    with session_scope() as session:
        books = get_books_from_db(
            session,
            book_name,
            author_first_name,
            author_last_name,
            args.year,
            args.primary_key_flag,
        )
        for book in books:
            sys.stdout.write(book)


if __name__ == "__main__":
    main()
