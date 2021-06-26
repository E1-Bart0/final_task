import pytest

from src.wiper import parse_args


def test_parse_args__without_args():
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args__with__n__and__a__args():
    with pytest.raises(SystemExit):
        parse_args(["-n", "123", "-a"])


def test_parse_args__n__arg():
    args = parse_args(["-n", "123"])
    assert args.number == 123
    assert not args.all


def test_parse_args__a__arg():
    args = parse_args(["-a"])
    assert args.number is None
    assert args.all
