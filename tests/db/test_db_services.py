import random
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from src.db.models import Author, Book
from src.db.services import delete_book_or_all_db, get_or_create


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


def test_get_or_create__create_new_instance(db_session):
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
    assert result == book
    assert len(db_session.query(Book).all()) == 1


def test_create_author__unique_constraints(db_session):
    data = {"first_name": "John", "last_name": "Doe"}
    author = Author(**data)
    db_session.add(author)
    db_session.commit()
    assert len(db_session.query(Author).all()) == 1
    author = Author(**data)
    db_session.add(author)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_create_book__unique_constraints(db_session):
    data = {"name": "Book1", "author_id": None, "year": 1234}
    book = Book(**data)
    db_session.add(book)
    db_session.commit()
    assert len(db_session.query(Book).all()) == 1
    db_session.add(book)
    db_session.commit()
    assert len(db_session.query(Book).all()) == 1


def test_delete_book_or_all_db__delete_one_book(db_session):
    book1 = create_book_with_author(db_session)
    book2 = create_book_with_author(db_session)
    assert len(db_session.query(Book).all()) == 2
    assert len(db_session.query(Author).all()) == 2
    result = delete_book_or_all_db(db_session, primary_key=book1.id)
    assert result == 1
    assert book2 in db_session.query(Book).all()
    assert book1 not in db_session.query(Book).all()
    assert len(db_session.query(Author).all()) == 2


def test_delete_book_or_all_db__but_pk_do_not_exists(db_session):
    create_book_with_author(db_session)
    assert len(db_session.query(Book).all()) == 1
    assert len(db_session.query(Author).all()) == 1
    result = delete_book_or_all_db(db_session, primary_key=21345678)
    assert not result
    assert len(db_session.query(Book).all()) == 1
    assert len(db_session.query(Author).all()) == 1


def test_delete_book_or_all_db__delete_all_db(db_session):
    create_book_with_author(db_session)
    create_book_with_author(db_session)
    assert len(db_session.query(Book).all()) == 2
    assert len(db_session.query(Author).all()) == 2
    result = delete_book_or_all_db(db_session, all_flag=True)
    assert result == 4
    assert not db_session.query(Book).all()
    assert not db_session.query(Author).all()
