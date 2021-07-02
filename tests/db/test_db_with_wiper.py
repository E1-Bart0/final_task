from src.db.models import Author, Book
from src.db.services import delete_book_or_all_db
from tests.db.test_db import create_book_with_author


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
