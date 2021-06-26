import sys
from argparse import ArgumentParser


def parse_args(_args):
    """Create parser with args (-a, -n, -y -s) and parse args with the created parser"""
    parser = ArgumentParser(description="Find books in db")
    parser.add_argument(
        "-n", type=str, dest="book_name", required=True, help="Book name"
    )
    parser.add_argument(
        "-a", type=str, dest="author", required=False, help="Book author full name"
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


if __name__ == "__main__":
    main()
