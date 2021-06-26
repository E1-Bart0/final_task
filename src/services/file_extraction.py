import gzip
import os
from pathlib import Path
from typing import Union, Generator
from zipfile import ZipFile


def zip_extraction(zip_file: Union[str, Path]) -> Generator[str, None, None]:
    """Extracts and reads file from zip-archive"""
    with ZipFile(zip_file, "r") as zip_obj:
        for file in zip_obj.namelist():
            yield zip_obj.read(file).decode()


def gzip_extraction(gzip_file: Union[str, Path]) -> str:
    """Extracts and reads file from zip-archive"""
    with gzip.open(gzip_file, "r") as file:
        return file.read().decode()


def get_files_from_dir(dir_path: Union[str, Path]) -> Generator[str, None, None]:
    """Yields files with correct extension from directory"""
    from src.services.parse_book_from_file import FILE_EXTENSIONS

    for root, _, files in os.walk(dir_path):
        for file in files:
            file_extension = Path(file).suffix
            if file_extension in FILE_EXTENSIONS:
                yield os.path.join(root, file)
