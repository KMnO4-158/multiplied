from dataclasses import dataclass
from typing import Any
from multiplied.tests import REFERENCE
import pytest
import warnings
import multiplied as mp

@dataclass
class TestCase:
    """Describes a single test scenario

    assert metadata(input_value) -> expected_output
    """
    name: str
    input_value: Any
    expected_output: Any
    metadata: dict
    __test__ = False


# block ruff format:
# fmt: off
TEST_4_BIT_INSTANCE = [
    # TestCase("", mp.Matrix(4), REFERENCE[""], {}),  # template
    TestCase("4_bit_matrix",4, REFERENCE["dummy_matrix"][4], {"raw": True, "ne": True}),
    TestCase("4_bit_zero_matrix",4, REFERENCE["zero_matrix"][4], {"raw": True}),
    TestCase("4_bit_empty_matrix",4, REFERENCE["empty_matrix"][4], {"empty": True}),
    TestCase("4_bit_dadda_matrix",4, REFERENCE["dadda_matrix"][4], {"dadda": True, "raw": True}),
    TestCase("4_bit_matrix_bits",4, 4, {"bits": True}),
    TestCase("4_bit_matrix_len",4, 4, {"len": True}),

]

TEST_8_BIT_INSTANCE = [
    # TestCase("", mp.Matrix(8), REFERENCE[""], {}),  # template
    TestCase("8_bit_matrix", 8, REFERENCE["dummy_matrix"][8], {"raw": True, "ne": True}),
    TestCase("8_bit_zero_matrix", 8, REFERENCE["zero_matrix"][8], {"raw": True}),
    TestCase("8_bit_empty_matrix", 8, REFERENCE["empty_matrix"][8], {"empty": True}),
    TestCase("8_bit_dadda_matrix", 8, REFERENCE["dadda_matrix"][8], {"dadda": True, "raw": True}),
    TestCase("8_bit_matrix_bits",8, 8, {"bits": True}),
    TestCase("8_bit_matrix_len",8, 8, {"len": True}),
]


TEST_BOOLEAN = [

]


TEST_ITER = [

]

TEST_MATRIX_MERGE = [

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

def test_4_bit_scenarios(matrix_cases_4):
    """Generic test for all 4-bit scenarios"""
    print(matrix_cases_4.input_value)
    result = process_value(matrix_cases_4.input_value, matrix_cases_4.metadata)
    if matrix_cases_4.metadata.get("ne", False):
        assert result != matrix_cases_4.expected_output
    else:
        assert result == matrix_cases_4.expected_output


def test_8_bit_scenarios(matrix_cases_8):
    """Generic test for all 8-bit scenarios"""
    print(matrix_cases_8.input_value)

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
