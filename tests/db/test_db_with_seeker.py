from src.db.models import Book
from src.db.services import find_books_and_authors, get_books_from_db
from tests.db.test_db import create_book_with_author


def test_find_books_and_authors__search_with_author(db_session):
    book = create_book_with_author(
        db_session, book_name="Book", book_year=1, author_f_n="John", author_l_n="Doe"
    )

    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name="John",
        author_last_name="Doe",
        book_year=1,
    )
    assert result == [book]


def test_find_books_and_authors__search_with_author_but_there_not_such_author(
    db_session,
):
    create_book_with_author(
        db_session, book_name="Book", book_year=1, author_f_n="Jaine", author_l_n="Doe"
    )
    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name="John",
        author_last_name="Doe",
        book_year=1,
    )
    assert result == []


def test_find_books_and_authors__search_without_author_but_book_has_author(db_session):
    book = create_book_with_author(
        db_session, book_name="Book", book_year=1, author_f_n="John", author_l_n="Doe"
    )
    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name=None,
        author_last_name=None,
        book_year=1,
    )
    assert result == [book]


def test_find_books_and_authors__search_without_author_and_book_has_no_author(
    db_session,
):
    book = Book(name="Book", year=1, author_id=None)
    db_session.add(book)
    db_session.commit()

    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name=None,
        author_last_name=None,
        book_year=1,
    )
    assert result == [book]


def test_find_books_and_authors__search_without_year__book_has_no_author(db_session):
    book = Book(name="Book", year=1, author_id=None)
    db_session.add(book)
    db_session.commit()

    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name=None,
        author_last_name=None,
        book_year=None,
    )
    assert result == [book]


def test_find_books_and_authors__search_without_year__book_has_author(db_session):
    book = create_book_with_author(
        db_session, book_year=1, book_name="Book", author_l_n="Doe", author_f_n="John"
    )
    result = find_books_and_authors(
        db_session,
        book_name="Book",
        author_first_name=None,
        author_last_name=None,
        book_year=None,
    )
    assert result == [book]


def test_get_books_from_db__with_author__without_primary_key(db_session):
    create_book_with_author(
        db_session, book_year=1, book_name="Test", author_l_n="Doe", author_f_n="John"
    )
    result = get_books_from_db(db_session, "Test", "John", "Doe", 1, False)
    assert list(result) == [
        {
            "name": "Test",
            "year": 1,
            "author": {"first_name": "John", "last_name": "Doe"},
        }
    ]


def test_get_books_from_db__with_author__with_primary_key(db_session):
    book = create_book_with_author(
        db_session, book_year=1, book_name="Test", author_l_n="Doe", author_f_n="John"
    )
    result = get_books_from_db(db_session, "Test", "John", "Doe", 1, True)
    assert list(result) == [book.id]


def test_get_books_from_db__without_author__with_primary_key(db_session):
    book = Book(name="Test", year=1, author_id=None)
    db_session.add(book)
    db_session.commit()

    result = get_books_from_db(db_session, "Test", None, None, 1, True)
    assert list(result) == [book.id]


def test_get_books_from_db__without_author__without_primary_key(db_session):
    book = Book(name="Test", year=1, author_id=None)
    db_session.add(book)
    db_session.commit()

    result = get_books_from_db(db_session, "Test", None, None, 1, False)
    assert list(result) == [{"name": "Test", "year": 1, "author": None}]
