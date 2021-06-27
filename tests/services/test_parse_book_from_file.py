from unittest.mock import call, patch

from src.services.parse_book_from_file import (
    find_books,
    get_books_from_directory,
    get_books_from_file,
)


@patch(
    "src.services.parse_book_from_file.get_books_from_directory",
    return_value=[{"name": "Book1"}],
)
def test_find_books__dir_path(mock):
    dir_path = "/path/to/dir/"
    result = find_books(dir_path=dir_path)
    mock.assert_called_once_with(dir_path)
    assert result == [{"name": "Book1"}]


@patch(
    "src.services.parse_book_from_file.get_books_from_file",
    return_value=[{"name": "Book1"}],
)
def test_find_books__book_path(mock):
    book_path = "/path/to/file"
    result = find_books(book_path=book_path)
    mock.assert_called_once_with(book_path)
    assert result == [{"name": "Book1"}]


@patch("src.services.parse_book_from_file.FB2Parser")
def test_get_books_from_file__without_extension(mock_parser):
    mock_parser.return_value.as_dict = {"name": "Book1"}
    book_path = "/path/to/file"
    result = get_books_from_file(book_path)
    mock_parser.assert_called_once_with(filename=book_path)
    assert result == [{"name": "Book1"}]


@patch("src.services.parse_book_from_file.FB2Parser")
@patch("src.services.parse_book_from_file.gzip_extraction", return_value="file_content")
def test_get_books_from_file__with_extension_gz(mock_gzip, mock_parser):
    mock_parser.return_value.as_dict = {"name": "Book1"}
    book_path = "/path/to/file.gz"
    result = get_books_from_file(book_path)
    mock_parser.assert_called_once_with(text="file_content")
    assert result == [{"name": "Book1"}]


@patch("src.services.parse_book_from_file.FB2Parser")
@patch(
    "src.services.parse_book_from_file.zip_extraction", return_value=["file_content"]
)
def test_get_books_from_file__with_extension_zip(mock_zip, mock_parser):
    mock_parser.return_value.as_dict = {"name": "Book1"}
    book_path = "/path/to/file.zip"
    result = get_books_from_file(book_path)
    mock_parser.assert_called_once_with(text="file_content")
    assert result == [{"name": "Book1"}]


@patch("src.services.parse_book_from_file.FB2Parser")
@patch(
    "src.services.parse_book_from_file.zip_extraction",
    return_value=["file_content1", "file_content2"],
)
def test_get_books_from_file__with_extension_zip_returns_2_file_in_zip(
    mock_zip, mock_parser
):
    mock_parser.return_value.as_dict = {"name": "Book1"}
    book_path = "/path/to/file.zip"
    result = get_books_from_file(book_path)
    calls = mock_parser.call_args_list
    assert calls == [call(text="file_content1"), call(text="file_content2")]
    assert result == [{"name": "Book1"}, {"name": "Book1"}]


@patch(
    "src.services.parse_book_from_file.get_books_from_file",
    return_value=[{"name": "Book1"}],
)
@patch("src.services.parse_book_from_file.get_files_from_dir", return_value=["/file/1"])
def test_get_books_from_directory__works(mock_dir, mock_books_from_file):
    dir_path = "/path/to/dir/"
    result = get_books_from_directory(dir_path)
    calls = mock_books_from_file.call_args_list
    assert calls == [call("/file/1")]
    assert result == [{"name": "Book1"}]


@patch(
    "src.services.parse_book_from_file.get_books_from_file",
    return_value=[{"name": "Book1"}],
)
@patch(
    "src.services.parse_book_from_file.get_files_from_dir",
    return_value=["/file/1", "/file/2"],
)
def test_get_books_from_directory__works_with_2_file(mock_dir, mock_books_from_file):
    dir_path = "/path/to/dir/"
    result = get_books_from_directory(dir_path)
    calls = mock_books_from_file.call_args_list
    assert calls == [call("/file/1"), call("/file/2")]
    assert result == [{"name": "Book1"}, {"name": "Book1"}]


@patch(
    "src.services.parse_book_from_file.get_books_from_file",
    return_value=[{"name": "Book1"}, {"name": "Book1"}],
)
@patch("src.services.parse_book_from_file.get_files_from_dir", return_value=["/file/1"])
def test_get_books_from_directory__works_if_get_books_from_file_return_2_books(
    mock_dir, mock_books_from_file
):
    dir_path = "/path/to/dir/"
    result = get_books_from_directory(dir_path)
    calls = mock_books_from_file.call_args_list
    assert calls == [call("/file/1")]
    assert result == [{"name": "Book1"}, {"name": "Book1"}]
