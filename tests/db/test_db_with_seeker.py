from unittest.mock import patch

import pytest

from src.db.models import Author, Book
from src.db.services import (
    find_author_by_name,
    find_books,
    find_books_and_authors,
    get_books_from_db,
)
from tests.db.test_db import create_book_with_author


def test_find_author_by_name_is_ok(db_session):
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
def test_find_books_and_authors__search_with_author(find_book, find_author, db_session):
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
    assert result == ("book_obj", author)


@patch("src.db.services.find_author_by_name")
def test_find_books_and_authors__search_with_author_but_there_not_such_author(
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
def test_find_books_and_authors__search_without_author(find_book, db_session):
    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name=None,
        author_last_name=None,
        book_year=1,
    )
    find_book.assert_called_once_with(db_session, name="Book", author_id=None, year=1)
    assert result == ("book_obj", None)


@patch("src.db.services.find_books_and_authors")
def test_get_books_from_db__with_author__without_primary_key(
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
def test_get_books_from_db__with_author__with_primary_key(
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
def test_get_books_from_db__without_author__with_primary_key(
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
def test_get_books_from_db__without_author__without_primary_key(
    find_book_and_author, db_session
):
    book = Book(name="Test", year=1, author_id=None)
    db_session.add(book)
    db_session.commit()

    find_book_and_author.return_value = [book], None
    result = get_books_from_db(db_session, "Test", None, None, 1, False)
    find_book_and_author.assert_called_once_with(db_session, "Test", None, None, 1)
    assert list(result) == [{"name": "Test", "year": 1, "author": None}]
