from tempfile import NamedTemporaryFile, TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from src.services.file_extraction import zip_extraction


@pytest.fixture()
def create_zip_dir_with_file():
    directory = TemporaryDirectory()
    file_name = f"{directory.name}/test.zip"

    def create_zip_file(data):
        with ZipFile(file_name, mode="w") as zip_obj:
            for text in data:
                file = NamedTemporaryFile(mode="w")
                file.write(text)
                file.seek(0)
                zip_obj.write(file.name, compress_type=ZIP_DEFLATED)
        return file_name

    yield create_zip_file
    directory.cleanup()


def test_zip_extraction__but_file_path_not_exists():
    file_path = "/not_exists.zip"
    with pytest.raises(FileNotFoundError, match="No such file or directory:"):
        list(zip_extraction(file_path))


def test_zip_extraction__zip_object_has_3_files_in_it(create_zip_dir_with_file):
    data = ["file1", "file2", "file3"]
    zip_file = create_zip_dir_with_file(data)
    assert list(zip_extraction(zip_file)) == ["file1", "file2", "file3"]


def test_zip_extraction__zip_object_has_1_files_in_it(create_zip_dir_with_file):
    data = ["file1"]
    zip_file = create_zip_dir_with_file(data)
    assert list(zip_extraction(zip_file)) == ["file1"]
