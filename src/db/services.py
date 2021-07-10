import logging
from typing import Iterable, Optional, Sequence

from .core import Base, Session
from .models import Author, Book


def delete_book_or_all_db(
    session: Session,
    primary_key: Optional[int] = None,
    all_flag: Optional[bool] = False,
) -> int:
    """Delete a book in a database if not all_flag else Flush whole db"""

    counter = 0
    if not all_flag:
        logging.debug("Searching book in db")
        book = session.query(Book).filter(Book.id == primary_key).first()

        if book is None:
            logging.info("Book Not Found")
            return counter

        logging.debug(f"Deleting book: {book.as_dict}")
        session.delete(book)
        counter += 1
    else:
        logging.debug("Deleting all books")
        counter += session.query(Book).delete()

        logging.debug("Deleting all authors")
        counter += session.query(Author).delete()
    session.commit()
    return counter


def get_or_create(session: Session, model: Base, **kwargs) -> (Base, bool):
    """Find instance with such kwarg in db or Create if not exists"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, True
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance, False


def find_books_and_authors(
    session: Session,
    book_name: str,
    author_first_name: Optional[str],
    author_last_name: Optional[str],
    book_year: Optional[int],
) -> (Sequence[Book], Optional[Author]):
    """Find Books and Author of books in DB"""
    query_param = [
        Book.name == book_name,
        (Book.year == book_year) if book_year is not None else None,
        Book.author.has(
            Author.first_name == author_first_name
            and Author.last_name == author_last_name
        )
        if author_first_name is not None and author_last_name is not None
        else None,
    ]
    query_param = filter(lambda x: x is not None, query_param)
    return session.query(Book).filter(*query_param).all()


def get_books_from_db(
    session: Session,
    book_name: str,
    author_first_name: Optional[str],
    author_last_name: Optional[str],
    book_year: Optional[int],
    primary_key: bool,
):
    """Find Books in DB and convert it into dict"""

    logging.debug("Searching book in db")
    books = find_books_and_authors(
        session, book_name, author_first_name, author_last_name, book_year
    )
    if primary_key:
        return [book.id for book in books]
    return [book.as_dict for book in books]


def create_books_and_authors(session: Session, data: Sequence[dict], update_flag: bool):
    """Creating Books and Authors if they do not exists in DB"""

    authors = create_all_authors(session, data)
    create_all_books(session, data, authors, update_flag)


def create_all_authors(
    session: Session, data: Sequence[dict]
) -> Iterable[Optional[Author]]:
    """Creating Authors if they do not exists in DB"""

    def get_author(book_info):
        if book_info["author_first_name"] is None:
            return None
        kwargs = {
            "first_name": book_info["author_first_name"],
            "last_name": book_info["author_last_name"],
        }
        return get_or_create(session, Author, **kwargs)[0]

    return map(get_author, data)


def create_all_books(
    session: Session,
    data: Sequence[dict],
    authors: Iterable[Optional[Author]],
    update_flag: bool,
):
    """Creating Books if they do not exists in DB else update it, if update_flag is True"""
    cr, up = 0, 0

    for book_data, author in zip(data, authors):
        book_kwargs = {
            "name": book_data["name"],
            "year": book_data["year"],
            "author_id": author.id if author is not None else None,
        }
        book, not_created = get_or_create(session, Book, **book_kwargs)
        if not_created:
            up += update_if_update_flag(session, book, book_data, update_flag)
        else:
            cr += 1
            logging.debug(f"Saving info about book: {book.as_dict}")
    logging.info(f"Created: {cr} books AND Updated: {up} books")


def update_if_update_flag(
    session: Session, book: Book, book_data: dict, update_flag: bool
) -> bool:
    """Update Book if update_flag is True"""

    logging.debug(f"Book already exists: {book.as_dict}")
    if update_flag:
        logging.debug(f"Updating info about book: {book.as_dict}")
        book.name = book_data["name"]
        book.year = book_data["year"]
        session.commit()
        return True
    return False
