from tempfile import NamedTemporaryFile

import pytest

from src.services.fb2_parser import FB2Parser


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
    assert book.name == "Test Book"
    assert book.author_full_name == "John Doe"
    assert book.published_year == 2021
    assert book.as_dict == {"name": "Test Book", "author": "John Doe", "year": 2021}


def test_fb2_parser__if_not_author__book_as_file(get_file_path):
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
    assert book.name == "Test Book"
    assert book.author_full_name is None
    assert book.published_year == 2021
    assert book.as_dict == {"name": "Test Book", "author": None, "year": 2021}


def test_fb2_parser__if_not_published_year_and_author__book_as_file(get_file_path):
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
    assert book.name == "Test Book"
    assert book.author_full_name is None
    assert book.published_year is None
    assert book.as_dict == {"name": "Test Book", "author": None, "year": None}


def test_fb2_parser__if_not_book_name__book_as_file(get_file_path):
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
    assert book.name == "Test Book"
    assert book.author_full_name == "John Doe"
    assert book.published_year == 2021
    assert book.as_dict == {"name": "Test Book", "author": "John Doe", "year": 2021}
