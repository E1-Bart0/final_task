from tempfile import NamedTemporaryFile

import pytest

from services.fb2_parser import FB2Parser


@pytest.fixture()
def get_file_path():
    file = NamedTemporaryFile(mode="w", suffix=".fb2")

    def write_to_file(text):
        file.write(text)
        file.seek(0)
        return file.name

    yield write_to_file
    file.close()


def test_fb2_parser__works_with_file(get_file_path):
    text = """<?xml version="1.0" encoding="UTF-8"?>
<FictionBook xmlns="URL">
    <description>
        <title-info>
            <author><first-name>John</first-name><last-name>Doe</last-name></author>
            <book-title>Test Book</book-title>
        </title-info>
        <publish-info>
            <publisher>SelfPub</publisher>
            <year>2021</year>
        </publish-info>
    </description>
</FictionBook>"""
    file = get_file_path(text)
    book = FB2Parser(filename=file)
    assert book.as_dict == {
        "name": "Test Book",
        "author_first_name": "John",
        "author_last_name": "Doe",
        "year": 2021,
    }


def test_fb2_parser__as_file__if_not_author__book(get_file_path):
    text = """<?xml version="1.0" encoding="UTF-8"?>
<FictionBook xmlns="URL">
    <description>
        <title-info>
            <book-title>Test Book</book-title>
        </title-info>
        <publish-info>
            <publisher>SelfPub</publisher>
            <year>2021</year>
        </publish-info>
    </description>
</FictionBook>"""
    file = get_file_path(text)
    book = FB2Parser(filename=file)
    assert book.as_dict == {
        "name": "Test Book",
        "author_first_name": None,
        "author_last_name": None,
        "year": 2021,
    }


def test_fb2_parser__as_file__if_not_year_and_not_author(get_file_path):
    text = """<?xml version="1.0" encoding="UTF-8"?>
<FictionBook xmlns="URL">
    <description>
        <title-info>
            <book-title>Test Book</book-title>
        </title-info>
    </description>
</FictionBook>"""
    file = get_file_path(text)
    book = FB2Parser(filename=file)
    assert book.as_dict == {
        "name": "Test Book",
        "author_first_name": None,
        "author_last_name": None,
        "year": None,
    }


def test_fb2_parser__as_file__if_not_book_name(get_file_path):
    text = """<?xml version="1.0" encoding="UTF-8"?>
<FictionBook xmlns="URL">
</FictionBook>"""
    file = get_file_path(text)
    book = FB2Parser(filename=file)
    with pytest.raises(AttributeError, match="object has no attribute 'text'"):
        _ = book.name


def test_fb2_parser__works_with_text(get_file_path):
    text = """<?xml version="1.0" encoding="UTF-8"?>
<FictionBook xmlns="URL">
    <description>
        <title-info>
            <author><first-name>John</first-name><last-name>Doe</last-name></author>
            <book-title>Test Book</book-title>
        </title-info>
        <publish-info>
            <publisher>SelfPub</publisher>
            <year>2021</year>
        </publish-info>
    </description>
</FictionBook>"""
    book = FB2Parser(text=text)
    assert book.as_dict == {
        "name": "Test Book",
        "author_first_name": "John",
        "author_last_name": "Doe",
        "year": 2021,
    }
