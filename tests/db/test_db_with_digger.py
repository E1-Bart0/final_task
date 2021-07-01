from src.db.models import Book
from src.db.services import create_books_and_authors


def test_create_books_and_authors__is_ok(db_session):
    data = [
        {
            "name": "Test",
            "year": 1,
            "author_first_name": "John",
            "author_last_name": "Doe",
        },
        {
            "name": "Test1",
            "year": 2,
            "author_first_name": "Jaine",
            "author_last_name": "Doe",
        },
    ]
    create_books_and_authors(db_session, data, False)
    books = db_session.query(Book).all()
    assert [b.as_dict for b in books] == [
        {
            "name": "Test",
            "year": 1,
            "author": {"first_name": "John", "last_name": "Doe"},
        },
        {
            "name": "Test1",
            "year": 2,
            "author": {"first_name": "Jaine", "last_name": "Doe"},
        },
    ]


def test_create_books_and_authors__but_author_is_none(db_session):
    data = [
        {
            "name": "Test",
            "year": 1,
            "author_first_name": None,
            "author_last_name": None,
        },
        {
            "name": "Test1",
            "year": 2,
            "author_first_name": "Jaine",
            "author_last_name": "Doe",
        },
    ]
    create_books_and_authors(db_session, data, False)
    books = db_session.query(Book).all()
    assert [b.as_dict for b in books] == [
        {"name": "Test", "year": 1, "author": None},
        {
            "name": "Test1",
            "year": 2,
            "author": {"first_name": "Jaine", "last_name": "Doe"},
        },
    ]


def test_create_books_and_authors__but_author_already_exists(db_session):
    data = [
        {
            "name": "Test",
            "year": 1,
            "author_first_name": "Jaine",
            "author_last_name": "Doe",
        },
        {
            "name": "Test1",
            "year": 2,
            "author_first_name": "Jaine",
            "author_last_name": "Doe",
        },
    ]
    create_books_and_authors(db_session, data, False)
    books = db_session.query(Book).all()
    assert [b.as_dict for b in books] == [
        {
            "name": "Test",
            "year": 1,
            "author": {"first_name": "Jaine", "last_name": "Doe"},
        },
        {
            "name": "Test1",
            "year": 2,
            "author": {"first_name": "Jaine", "last_name": "Doe"},
        },
    ]


def test_create_books_and_authors__but_book_already_exists(db_session):
    data = [
        {
            "name": "Test",
            "year": 1,
            "author_first_name": "Jaine",
            "author_last_name": "Doe",
        },
        {
            "name": "Test",
            "year": 1,
            "author_first_name": "Jaine",
            "author_last_name": "Doe",
        },
    ]
    create_books_and_authors(db_session, data, False)
    books = db_session.query(Book).all()
    assert [b.as_dict for b in books] == [
        {
            "name": "Test",
            "year": 1,
            "author": {"first_name": "Jaine", "last_name": "Doe"},
        }
    ]


def test_create_books_and_authors__with_update_flag_but_book_already_exists(db_session):
    data = [
        {
            "name": "Test",
            "year": 1,
            "author_first_name": "Jaine",
            "author_last_name": "Doe",
        },
        {
            "name": "Test",
            "year": 1,
            "author_first_name": "Jaine",
            "author_last_name": "Doe",
        },
    ]
    create_books_and_authors(db_session, data, True)
    books = db_session.query(Book).all()
    assert [b.as_dict for b in books] == [
        {
            "name": "Test",
            "year": 1,
            "author": {"first_name": "Jaine", "last_name": "Doe"},
        }
    ]
