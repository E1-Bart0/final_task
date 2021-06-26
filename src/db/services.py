from typing import Optional, Sequence, Union

from .core import session_scope
from .models import Book, Author


def find_book(name: str, author: Optional[str], year: Optional[int]) -> Optional[Book]:
    """Get a book with such name, author, year from a database or returns None if there is no such book"""
    with session_scope() as session:
        book = session.query(Book).filter(
            Book.author.full_name == author, Book.name == name, Book.year == year
        )
        return book


def create_new_books(data: Sequence[Sequence[Union[str, int, None]]], update: bool) -> Sequence[Book]:
    """Create a new book in a database"""
    with session_scope() as session:
        objects = [Book(name=name, year=year) for name, author, year in data]
        # return session.bulk_save_objects(objects)


def create_author(author: str) -> Author:
    """Create a new author in a database or do nothing if author already exists"""
    with session_scope() as session:
        author = session.create_or_update(Author)
        return author


def delete_book(primary_key: Optional[str]) -> None:
    """Delete a book in a database"""
    with session_scope() as session:
        book = session.query(Book).filter(Book.id == primary_key)
        return book
