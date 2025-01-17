import pytest

from module_name.resolve import get_module_name


def test_get_module_name():
    from module_name import cli
    name = get_module_name(cli.__file__)
    assert name == "module_name.cli"

    empty = get_module_name("module_name.not_here")
    assert empty is None
