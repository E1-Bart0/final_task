import argparse
from tempfile import gettempdir, NamedTemporaryFile
from unittest.mock import patch

import pytest

from src.digger import validate_dir_path, validate_file_path, parse_args


def test_dir_path__if_dir_do_not_exists():
    path_to_directory = "/not_exists/"
    with pytest.raises(
        argparse.ArgumentTypeError, match="is not a valid path for directory"
    ):
        validate_dir_path(path_to_directory)


def test_dir_path__if_path_leads_to_file():
    path_to_file = NamedTemporaryFile().name
    with pytest.raises(
        argparse.ArgumentTypeError, match="is not a valid path for directory"
    ):
        validate_dir_path(path_to_file)


def test_dir_path__return_path():
    path_to_directory = gettempdir()
    assert validate_dir_path(path_to_directory) == path_to_directory


def test_file_path__if_file_do_not_exists():
    path_to_file = "/not_exists"
    with pytest.raises(argparse.ArgumentTypeError, match="is not a valid path to file"):
        validate_file_path(path_to_file)


def test_file_path__if_path_leads_to_directory():
    path_to_directory = gettempdir()
    with pytest.raises(argparse.ArgumentTypeError, match="is not a valid path to file"):
        validate_file_path(path_to_directory)


@pytest.mark.parametrize("extension", [".exe", ".doc", ".rar"])
def test_file_path__if_file_with_bad_extensions(extension):
    file = NamedTemporaryFile(suffix=extension)
    with pytest.raises(
        argparse.ArgumentTypeError, match="is not a valid file extension"
    ):
        validate_file_path(file.name)


@pytest.mark.parametrize("extension", [".gz", ".zip", "", ".fb2"])
def test_file_path__return_path(extension):
    file = NamedTemporaryFile(suffix=extension)
    assert validate_file_path(file.name) == file.name


def test_parse_args__without_args():
    with pytest.raises(SystemExit):
        parse_args([])


@patch("src.digger.validate_dir_path", side_effect=lambda x: x)
@patch("src.digger.validate_file_path", side_effect=lambda x: x)
def test_parse_args__with_a_and_s_args(mock_file_path, mock_dir_path):
    with pytest.raises(SystemExit):
        parse_args(["-a", "/path/to/file", "-s", "/path/to/dir"])


@patch("src.digger.validate_file_path", side_effect=lambda x: x)
def test_parse_args__a__without_path(mock_file_path):
    with pytest.raises(SystemExit):
        parse_args(["-a"])


@patch("src.digger.validate_dir_path", side_effect=lambda x: x)
def test_parse_args__s__without_path(mock_dir_path):
    with pytest.raises(SystemExit):
        parse_args(["-s"])


@patch("src.digger.validate_dir_path", side_effect=lambda x: x)
def test_parse_args__s__and__u(mock_dir_path):
    args = parse_args(["-s", "/path/to/dir/", "-u"])
    assert args.dir_path == "/path/to/dir/"
    assert args.book_path is None
    assert args.flag


@patch("src.digger.validate_dir_path", side_effect=lambda x: x)
def test_parse_args__s(mock_dir_path):
    args = parse_args(["-s", "/path/to/dir/"])
    assert args.dir_path == "/path/to/dir/"
    assert args.book_path is None
    assert not args.flag


@patch("src.digger.validate_file_path", side_effect=lambda x: x)
def test_parse_args__a__and__u(mock_file_path):
    args = parse_args(["-a", "/path/to/file", "-u"])
    assert args.dir_path is None
    assert args.book_path == "/path/to/file"
    assert args.flag


@patch("src.digger.validate_file_path", side_effect=lambda x: x)
def test_parse_args__a(mock_file_path):
    args = parse_args(["-a", "/path/to/file"])
    assert args.dir_path is None
    assert args.book_path == "/path/to/file"
    assert not args.flag
