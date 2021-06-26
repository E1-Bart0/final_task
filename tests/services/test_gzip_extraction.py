import gzip
from tempfile import TemporaryDirectory

import pytest

from src.services.file_extraction import gzip_extraction


@pytest.fixture()
def create_gzip_file():
    directory = TemporaryDirectory()
    file_name = f"{directory.name}/test.gz"

    def create_gzip_file(text):
        with gzip.open(file_name, mode="w") as gzip_file:
            gzip_file.write(text.encode())
        return file_name

    yield create_gzip_file
    directory.cleanup()


def test_gzip_extraction__but_file_path_not_exists():
    file_path = "/not_exists.gz"
    with pytest.raises(FileNotFoundError, match="No such file or directory:"):
        list(gzip_extraction(file_path))


def test_gzip_extraction__works(create_gzip_file):
    data = "text"
    zip_file = create_gzip_file(data)
    assert gzip_extraction(zip_file) == "text"
