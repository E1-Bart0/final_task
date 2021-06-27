from typing import Optional, Sequence

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
        book = session.query(Book).filter(Book.id == primary_key).first()
        if book is None:
            return counter
        session.delete(book)
        counter += 1
    else:
        counter += session.query(Book).delete()
        counter += session.query(Author).delete()
    session.commit()
    return counter


def get_or_create(session: Session, model: Base, **kwargs):
    """Find instance with such kwarg in db or Create if not exists"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance


def find_author_by_name(session: Session, first_name: str, last_name: str):
    return (
        session.query(Author)
        .filter_by(first_name=first_name, last_name=last_name)
        .first()
    )


def find_books(session: Session, **kwargs):
    return session.query(Book).filter_by(**kwargs).all()


def find_books_and_authors(
    session: Session,
    book_name: str,
    author_first_name: Optional[str],
    author_last_name: Optional[str],
    book_year: Optional[int],
):
    author, author_id = None, None
    if author_first_name is not None and author_last_name is not None:
        author = find_author_by_name(session, author_first_name, author_last_name)
        author_id = author.id
    return (
        find_books(session, name=book_name, author_id=author_id, year=book_year),
        author,
    )


def get_books_from_db(
    session: Session,
    book_name: str,
    author_first_name: Optional[str],
    author_last_name: Optional[str],
    book_year: Optional[int],
    primary_key: bool,
):
    books, author = find_books_and_authors(
        session, book_name, author_first_name, author_last_name, book_year
    )
    if primary_key:
        return (book.id for book in books)
    if author is None:
        return (book.as_dict for book in books)
    return ({**book.as_dict, "author": author.as_dict} for book in books)


def create_books_and_authors(session: Session, data: Sequence[dict], flag: bool):
    pass
