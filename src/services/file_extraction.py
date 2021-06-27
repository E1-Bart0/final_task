import gzip
import logging
import os
from pathlib import Path
from typing import Generator, Union
from zipfile import ZipFile


def zip_extraction(zip_file: Union[str, Path]) -> Generator[str, None, None]:
    """Extracts and reads file from zip-archive"""
    with ZipFile(zip_file, "r") as zip_obj:
        for file in zip_obj.namelist():
            logging.debug(f"Unzipping file: {file} from {zip_file}")
            yield zip_obj.read(file).decode()


def gzip_extraction(gzip_file: Union[str, Path]) -> str:
    """Extracts and reads file from zip-archive"""
    with gzip.open(gzip_file, "r") as file:
        logging.debug(f"Extracts gzip file: {file} from {gzip_file}")
        return file.read().decode()


def get_files_from_dir(dir_path: Union[str, Path]) -> Generator[str, None, None]:
    """Yields files with correct extension from directory"""
    from services.parse_book_from_file import FILE_EXTENSIONS

    logging.debug(f"Scanning directory for file: {dir_path}")
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_extension = Path(file).suffix
            if file_extension in FILE_EXTENSIONS:
                yield os.path.join(root, file)
