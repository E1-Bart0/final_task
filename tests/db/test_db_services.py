import random
import uuid
from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError

from src.db.models import Author, Book
from src.db.services import (
    delete_book_or_all_db,
    find_author_by_name,
    find_books,
    find_books_and_authors,
    get_books_from_db,
    get_or_create,
)


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


def test_find_author_by_name(db_session):
    author = Author(first_name="John", last_name="Doe")
    db_session.add(author)
    db_session.commit()

    result = find_author_by_name(db_session, first_name="John", last_name="Doe")
    assert result == author


def test_find_author_by_name__but_there_is_not_such_author(db_session):
    result = find_author_by_name(db_session, first_name="John", last_name="Doe")
    assert result is None


def test_find_books(db_session):
    book = create_book_with_author(db_session, book_name="Book")
    result = find_books(db_session, name="Book")
    assert result == [book]


def test_find_books__2_book_with_the_same_name(db_session):
    book1 = create_book_with_author(db_session, book_name="Book")
    book2 = create_book_with_author(db_session, book_name="Book")
    result = find_books(db_session, name="Book")
    assert result == [book1, book2]


def test_find_books__different_by_authors(db_session):
    book1 = create_book_with_author(db_session, book_name="Book", book_year=1)
    create_book_with_author(db_session, book_name="Book", book_year=2134)
    result = find_books(db_session, name="Book", year=1)
    assert result == [book1]


def test_find_books__with_none_in_search(db_session):
    book1 = Book(name="Test", year=None, author_id=None)
    db_session.add(book1)
    db_session.commit()
    result = find_books(db_session, name="Test", year=None)
    assert result == [book1]


def test_find_books__but_there_is_not_such_book(db_session):
    result = find_books(db_session, name="Test", year=None)
    assert result == []


@patch("src.db.services.find_author_by_name")
@patch("src.db.services.find_books", return_value="book_obj")
def test_find_books_and_authors__with_author(find_book, find_author, db_session):
    author = Author(first_name="John", last_name="Doe")
    db_session.add(author)
    db_session.commit()

    author_id = author.id
    find_author.return_value = author

    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name="John",
        author_last_name="Doe",
        book_year=1,
    )
    find_book.assert_called_once_with(
        db_session, name="Book", author_id=author_id, year=1
    )
    find_author.assert_called_once_with(db_session, "John", "Doe")
    assert result == "book_obj"


@patch("src.db.services.find_author_by_name")
def test_find_books_and_authors__with_author_but_there_not_such_author(
    find_author, db_session
):
    find_author.return_value = None

    with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'id'"):
        find_books_and_authors(
            db_session,
            book_name="Book",
            author_first_name="John",
            author_last_name="Doe",
            book_year=1,
        )
    find_author.assert_called_once_with(db_session, "John", "Doe")


@patch("src.db.services.find_books", return_value="book_obj")
def test_find_books_and_authors__without_author(find_book, db_session):
    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name=None,
        author_last_name=None,
        book_year=1,
    )
    find_book.assert_called_once_with(db_session, name="Book", author_id=None, year=1)
    assert result == "book_obj"


@patch("src.db.services.find_books_and_authors")
def test_get_books_from_db_with_author_without_primary_key(
    find_book_and_author, db_session
):
    book = create_book_with_author(
        db_session, book_year=1, book_name="Test", author_l_n="Doe", author_f_n="John"
    )
    author = db_session.query(Author).filter_by(id=book.author_id).first()
    find_book_and_author.return_value = [book], author
    result = get_books_from_db(db_session, "Test", "John", "Doe", 1, False)
    find_book_and_author.assert_called_once_with(db_session, "Test", "John", "Doe", 1)
    assert list(result) == [
        {
            "name": "Test",
            "year": 1,
            "author": {"first_name": "John", "last_name": "Doe"},
        }
    ]


@patch("src.db.services.find_books_and_authors")
def test_get_books_from_db_with_author_with_primary_key(
    find_book_and_author, db_session
):
    book = create_book_with_author(
        db_session, book_year=1, book_name="Test", author_l_n="Doe", author_f_n="John"
    )
    author = db_session.query(Author).filter_by(id=book.author_id).first()
    find_book_and_author.return_value = [book], author
    result = get_books_from_db(db_session, "Test", "John", "Doe", 1, True)
    find_book_and_author.assert_called_once_with(db_session, "Test", "John", "Doe", 1)
    assert list(result) == [book.id]


@patch("src.db.services.find_books_and_authors")
def test_get_books_from_db_without_author_with_primary_key(
    find_book_and_author, db_session
):
    book = Book(name="Test", year=None, author_id=None)
    db_session.add(book)
    db_session.commit()

    find_book_and_author.return_value = [book], None
    result = get_books_from_db(db_session, "Test", None, None, 1, True)
    find_book_and_author.assert_called_once_with(db_session, "Test", None, None, 1)
    assert list(result) == [book.id]


@patch("src.db.services.find_books_and_authors")
def test_get_books_from_db_without_author_without_primary_key(
    find_book_and_author, db_session
):
    book = Book(name="Test", year=1, author_id=None)
    db_session.add(book)
    db_session.commit()

    find_book_and_author.return_value = [book], None
    result = get_books_from_db(db_session, "Test", None, None, 1, False)
    find_book_and_author.assert_called_once_with(db_session, "Test", None, None, 1)
    assert list(result) == [{"name": "Test", "year": 1, "author": None}]
