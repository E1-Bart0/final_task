import random
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from src.db.models import Author, Book
from src.db.services import get_or_create


def create_book_with_author(
    session,
    author_f_n=None,
    author_l_n=None,
    book_name=None,
    book_year=None,
):
    author_l_n = author_l_n or str(uuid.uuid4())
    author_f_n = author_f_n or str(uuid.uuid4())
    book_name = book_name or str(uuid.uuid4())
    book_year = book_year or random.randint(0, 10000)

    author = Author(first_name=author_f_n, last_name=author_l_n)
    session.add(author)
    session.commit()
    book = Book(name=book_name, year=book_year, author_id=author.id)
    session.add(book)
    session.commit()
    return book


def test_get_or_create__creating_new_instance(db_session):
    data = {"name": "Book1", "author_id": None, "year": 1234}
    get_or_create(db_session, Book, **data)
    book = db_session.query(Book).first()
    assert book.name == "Book1"
    assert book.author_id is None
    assert book.year == 1234


def test_get_or_create__get_already_exists_instance(db_session):
    data = {"name": "Book1", "author_id": None, "year": 1234}
    book = Book(**data)
    db_session.add(book)
    db_session.commit()
    assert len(db_session.query(Book).all()) == 1
    result = get_or_create(db_session, Book, **data)
    assert result == (book, True)
    assert len(db_session.query(Book).all()) == 1


def test_create_author__but_such_author_already_exists(db_session):
    data = {"first_name": "John", "last_name": "Doe"}
    author = Author(**data)
    db_session.add(author)
    db_session.commit()
    assert len(db_session.query(Author).all()) == 1
    author = Author(**data)
    db_session.add(author)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_create_book__but_such_book_already_exists(db_session):
    data = {"name": "Book1", "author_id": None, "year": 1234}
    book = Book(**data)
    db_session.add(book)
    db_session.commit()
    assert len(db_session.query(Book).all()) == 1
    db_session.add(book)
    db_session.commit()
    assert len(db_session.query(Book).all()) == 1
