from pathlib import Path
from typing import Optional, Sequence, Union

from src.services.fb2_parser import FB2Parser
from src.services.file_extraction import (
    get_files_from_dir,
    gzip_extraction,
    zip_extraction,
)

FILE_EXTENSIONS = ["", ".fb2", ".gz", ".zip"]


def find_books(
    dir_path: Optional[Union[str, Path]] = None,
    book_path: Optional[Union[str, Path]] = None,
) -> Sequence[dict]:
    """
    Parse file or directory and returns info about book

    :return [{'name': str, 'author_first_name': str,'author_last_name': str, 'year': int}, ...]
    """
    return (
        get_books_from_directory(dir_path)
        if dir_path is not None
        else get_books_from_file(book_path)
    )


def get_books_from_file(file: Optional[Union[str, Path]]) -> Sequence[dict]:
    """
    Find info about book in file

    :return [{'name': str, 'author_first_name': str,'author_last_name': str, 'year': int}, ...]
    """
    extension = Path(file).suffix
    if extension == ".gz":
        return [FB2Parser(text=gzip_extraction(file)).as_dict]
    elif extension == ".zip":
        return [
            FB2Parser(text=file_content).as_dict
            for file_content in zip_extraction(file)
        ]
    return [FB2Parser(filename=file).as_dict]


def get_books_from_directory(dir_path: Optional[Union[str, Path]]) -> Sequence[dict]:
    """
    Find info about books in all files in the specified directory

    :return [{'name': str, 'author_first_name': str,'author_last_name': str, 'year': int}, ...]
    """
    books = []
    for file in get_files_from_dir(dir_path):
        books += get_books_from_file(file)
    return books
