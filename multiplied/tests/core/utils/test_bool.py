import pytest
from multiplied.core.utils.bool import (
    isint,
    ishex2,
    ischar,
    isalpha,
    validate_bitwidth,
)


TYPE_ERROR_RAISERS = [
    None, "", "string", [1, 2, 3], {"key": "value"}
]
SUPPORTED_BITWIDTHS = [4, 8]

def test_validate_bitwidth():
    for x in SUPPORTED_BITWIDTHS:
        assert validate_bitwidth(x) is None
    with pytest.raises(ValueError):
        for x in [0, 16, 32, None ,""]:
            validate_bitwidth(x)
    with pytest.raises(TypeError):
        for x in TYPE_ERROR_RAISERS:
            validate_bitwidth(x)


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, True),
        ("0", True),
        ("_", False),
        ("A", False),
    ],
)
def test_isint(val, expected):
    assert isint(val) == expected

    for x in TYPE_ERROR_RAISERS:
        assert isint(x) is False

    with pytest.raises(ValueError):
        for x in [0, 16, 32]:
            validate_bitwidth(x)


@pytest.mark.parametrize(
    "val, expected",
    [
        ("a1", True),
        ("AJ", False),
        ("1", False),
        ("__", False),
        (1, False),
    ],
)
def test_ishex2(val, expected):
    assert ishex2(val) == expected

    for x in TYPE_ERROR_RAISERS:
        assert ishex2(x) is False


@pytest.mark.parametrize(
    "val, expected",
    [
        ("0", True),
        (1, False),
        ("_", True),
        ("a1", False),
        (" ", True)
    ],
)
def test_ischar(val, expected):
    assert ischar(val) == expected

    for x in TYPE_ERROR_RAISERS:
        assert ischar(x) is False


@pytest.mark.parametrize(
    "val, expected",
    [
        ("A", True),
        ("a", True),
        (1, False),
        ("1", False),
        ("_", False),
    ],
)
def test_isalpha(val, expected):
    assert isalpha(val) == expected

    for x in TYPE_ERROR_RAISERS:
        assert isint(x) is False
