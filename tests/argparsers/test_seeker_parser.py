import pytest

from src.seeker import parse_args


def test_parse_args__without_args():
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args__n__arg():
    args = parse_args(["-n", "Book", "Name"])
    assert args.book_name == ["Book", "Name"]
    assert args.author is None
    assert args.year is None
    assert not args.primary_key_flag


def test_parse_args__n__and__a__args():
    args = parse_args(["-n", "book_name", "-a", "author", "name"])
    assert args.book_name == ["book_name"]
    assert args.author == ["author", "name"]
    assert args.year is None
    assert not args.primary_key_flag


def test_parse_args__n__a__y__args():
    args = parse_args(["-n", "book_name", "-a", "author", "name", "-y", "1234"])
    assert args.book_name == ["book_name"]
    assert args.author == ["author", "name"]
    assert args.year == 1234
    assert not args.primary_key_flag


def test_parse_args__n__a__y__s__args():
    args = parse_args(["-n", "book_name", "-a", "author", "name", "-y", "1234", "-s"])
    assert args.book_name == ["book_name"]
    assert args.author == ["author", "name"]
    assert args.year == 1234
    assert args.primary_key_flag


def test_parse_args__n__but_without_text():
    with pytest.raises(SystemExit):
        parse_args(["-n"])


def test_parse_args__a__but_with_three_args():
    with pytest.raises(SystemExit):
        parse_args(["-n", "book", "-a", "first", "second", "fulle"])


def test_parse_args__a__but_with_one_args():
    with pytest.raises(SystemExit):
        parse_args(["-n", "book", "-a", "first"])
