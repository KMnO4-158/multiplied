import pytest
from multiplied.core.utils.char import (
    chargen,
    chartff,
    allchars,
)

TYPE_ERROR_RAISERS = [None, "", "string", [1, 2, 3], {"key": "value"}]


def test_chargen():
    target = [chr(i) for i in range(65, 65 + 26)]
    chars = chargen()
    for ch in target:
        assert next(chars) == ch
    for ch in target:
        assert next(chars) == ch


def test_chartff():
    with pytest.raises(TypeError):
        for x in TYPE_ERROR_RAISERS:
            next(chartff(x))

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

    with pytest.raises(TypeError):
        for x in TYPE_ERROR_RAISERS:
            allchars(x)

    with pytest.raises(ValueError):
        allchars(arr_2d, hash=[1])

    assert allchars(arr_2d) == {"A", "B"}
