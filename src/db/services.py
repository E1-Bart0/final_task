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
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance


def create_books_and_authors(session: Session, data: Sequence[dict], flag: bool):
    pass


def find_books_and_authors(
    session: Session,
    book_name: str,
    author_fullname: Optional[str],
    book_year: Optional[int],
):
    pass
