from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from services.file_extraction import get_files_from_dir


@pytest.fixture()
def get_dir_with_files():
    directory = TemporaryDirectory()
    files = []

    def create_files_in_dir(extensions):
        for extension in extensions:
            _file = NamedTemporaryFile(dir=directory.name, suffix=extension)
            files.append(_file)
        return directory.name

    yield create_files_in_dir
    for file in files:
        file.close()
    directory.cleanup()


def test_get_files_from_dir__but_dir_do_not_exists():
    dir_path = "/not/exists/"
    assert not list(get_files_from_dir(dir_path))


def test_get_files_from_dir__returns_only_one_file_because_of_extension(
    get_dir_with_files,
):
    extensions = [".fb2", ".exe", ".jpg"]
    dir_path = get_dir_with_files(extensions)
    result = list(get_files_from_dir(dir_path))
    assert len(result) == 1
    assert result[0].endswith(".fb2")


def test_get_files_from_dir__returns_all_needed_extensions(get_dir_with_files):
    extensions = [".fb2", ".gz", ".zip", ""]
    dir_path = get_dir_with_files(extensions)
    result = list(get_files_from_dir(dir_path))
    assert len(result) == 4


def test_get_files_from_dir__but_there_is_no_file_with_needed_extension(
    get_dir_with_files,
):
    extensions = [".py", ".exe", ".jpg"]
    dir_path = get_dir_with_files(extensions)
    assert not list(get_files_from_dir(dir_path))
