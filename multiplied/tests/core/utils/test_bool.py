import pytest
from multiplied.core.utils.bool import (
    isint,
    ishex2,
    ischar,
    isalpha,
    validate_bitwidth,
)



def test_validate_bitwidth():
    with pytest.raises(ValueError):
        validate_bitwidth(0)
        validate_bitwidth(16)
        validate_bitwidth(32)
    assert validate_bitwidth(4) is None
    assert validate_bitwidth(8) is None

@pytest.mark.parametrize("val, expected", [
    (1, True), ("0", True), ("_", False), ("A", False),
])
def test_isint(val, expected):
    assert isint(val) == expected

@pytest.mark.parametrize("val, expected", [
    ("a1", True), ("AJ", False), ("1", False), ("__", False), (1, False),
])
def test_ishex2(val, expected):
    assert ishex2(val) == expected

@pytest.mark.parametrize("val, expected", [
    ("0", True), (1, False), ("_", True), ("a1", False),
])
def test_ischar(val, expected):
    assert ischar(val) == expected

@pytest.mark.parametrize("val, expected", [
    ("A", True), ("a", True), (1, False), ("1", False), ("_", False),
])
def test_isalpha(val, expected):
    assert isalpha(val) == expected
