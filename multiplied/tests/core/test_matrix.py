from typing import Any
from multiplied.tests import REFERENCE, TestCase
import pytest
import warnings
import multiplied as mp

# block ruff format:
# fmt: off

# -- test instance --------------------------------------------------
# ! make bit widths programmatic
"""
metadata:
    raw:
        convert input to list[list[str]]
    empty:
        convert input to 'empty' matrix filled with underscores ['_']
    dadda:
        map input to dadda shape
    bits:
        input.bits
    len:
        input.__len__()

"""
TEST_4_BIT_INSTANCE = [
    # TC(name, input, expected_output, metadata)
    TestCase("4_bit_matrix",4, REFERENCE["dummy_matrix"][4], {"raw": True, "ne": True}),
    TestCase("4_bit_zero_matrix",4, REFERENCE["zero_matrix"][4], {"raw": True}),
    TestCase("4_bit_empty_matrix",4, REFERENCE["empty_matrix"][4], {"empty": True}),
    TestCase("4_bit_dadda_matrix",4, REFERENCE["dadda_matrix"][4], {"dadda": True, "raw": True}),
    TestCase("4_bit_matrix_bits",4, 4, {"bits": True}),
    TestCase("4_bit_matrix_len",4, 4, {"len": True}),

]

TEST_8_BIT_INSTANCE = [
    # TC(name, input, expected_output, metadata)
    TestCase("8_bit_matrix", 8, REFERENCE["dummy_matrix"][8], {"raw": True, "ne": True}),
    TestCase("8_bit_zero_matrix", 8, REFERENCE["zero_matrix"][8], {"raw": True}),
    TestCase("8_bit_empty_matrix", 8, REFERENCE["empty_matrix"][8], {"empty": True}),
    TestCase("8_bit_dadda_matrix", 8, REFERENCE["dadda_matrix"][8], {"dadda": True, "raw": True}),
    TestCase("8_bit_matrix_bits",8, 8, {"bits": True}),
    TestCase("8_bit_matrix_len",8, 8, {"len": True}),
]


# -------------------------------------------------------------------
""""""
TEST_BOOLEAN = [
    # TC(name, input, expected_output, metadata)
]


TEST_ITER = [
    # TC(name, input, expected_output, metadata)
]

TEST_MATRIX_MERGE = [
    # TC(name, input, expected_output, metadata)
]

TEST_ERROR = [
    # TC(name, input, expected_output, metadata)
]
# fmt: on


@pytest.fixture(params=TEST_4_BIT_INSTANCE, ids=lambda tc: tc.name)
def matrix_cases_4(request):
    """Parameterized fixture for 4-bit test matrix instances"""
    return request.param


@pytest.fixture(params=TEST_8_BIT_INSTANCE, ids=lambda tc: tc.name)
def matrix_cases_8(request):
    """Parameterized fixture for 8-bit test matrix instances"""
    return request.param


def test_4_bit_instance(matrix_cases_4):
    """Generic test for all 4-bit scenarios"""
    result = process_value(matrix_cases_4.input_value, matrix_cases_4.metadata)
    if matrix_cases_4.metadata.get("ne", False):
        assert result != matrix_cases_4.expected_output
    else:
        assert result == matrix_cases_4.expected_output


def test_8_bit_instance(matrix_cases_8):
    """Generic test for all 8-bit scenarios"""
    result = process_value(matrix_cases_8.input_value, matrix_cases_8.metadata)
    if matrix_cases_8.metadata.get("ne", False):
        assert result != matrix_cases_8.expected_output
    else:
        assert result == matrix_cases_8.expected_output


def process_value(value, metadata):

    matrix: list[Any] | mp.Matrix

    # -- generate input ---------------------------------------------
    if metadata.get("dadda", False):
        matrix = mp.Matrix(value)
        mp.hoist(matrix)
    elif metadata.get("empty", False):
        matrix = mp.raw_empty_matrix(value)
    else:
        matrix = mp.Matrix(value)

    # -- conditional conversion -------------------------------------
    if metadata.get("raw", False):
        if isinstance(matrix, mp.Matrix):
            matrix = matrix.matrix
        else:
            warnings.warn("Cannot convert non-matrix object to raw matrix")

    # -- process matrix ---------------------------------------------
    if isinstance(matrix, mp.Matrix):
        if metadata.get("bits", False):
            result = matrix.bits
            return result
        elif metadata.get("len", False):
            result = matrix.__len__()
            return result

    elif isinstance(matrix, list):
        if metadata.get("bits", False):
            raise AttributeError("List object has no attribute 'bits'")
        elif metadata.get("len", False):
            result = matrix.__len__()
            return result

    return matrix
