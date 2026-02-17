import pytest
from multiplied.core.utils.char import (
    chargen,
    chartff,
    allchars,
)


@pytest.fixture
def char_fixture():
    return [chr(i) for i in range(65, 65 + 26)]


def test_chargen(char_fixture):
    chars = chargen()
    for _ in range(52):
        assert next(chars) in char_fixture


def test_chartff():
    chars = chartff("A")
    assert [next(chars) for _ in range(4)] == ["A", "a", "A", "a"]
    chars = chartff("a")
    assert [next(chars) for _ in range(4)] == ["a", "A", "a", "A"]


def test_allchars():
    arr_2d = [
        ["_", "_", "_", "_", "a", "A", "a", "A"],
        ["_", "_", "_", "A", "a", "A", "a", "_"],
        ["_", "_", "a", "A", "a", "A", "_", "_"],
        ["_", "b", "B", "b", "B", "_", "_", "_"],
    ]
    assert allchars(arr_2d) == {"A", "B"}
