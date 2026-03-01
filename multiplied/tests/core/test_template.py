from dataclasses import dataclass
from typing import Any
from multiplied.tests import REFERENCE, TestCase
import pytest
# import warnings
import multiplied as mp

TEST_4_BIT_SCENARIOS = [
    # TC(name, [domain, range], error, metadata)
]

TEST_8_BIT_SCENARIOS = [

]

TEST_BOOLEAN = [

]

TEST_ITER = [

]

TEST_MATRIX_MERGE = [

]

@pytest.fixture(params=TEST_4_BIT_SCENARIOS, ids=lambda tc: tc.name)
def truth_cases_4(request):
    """Parameterized fixture for 4-bit truth table scenarios"""
    return request.param


@pytest.fixture(params=TEST_8_BIT_SCENARIOS, ids=lambda tc: tc.name)
def truth_cases_8(request):
    """Parameterized fixture for 8-bit truth table scenarios"""
    return request.param

def test_4_bit_scenarios(truth_cases_4):
    """Generic test for all 4-bit scenarios"""
    result = process_value(truth_cases_4.input_value, truth_cases_4.metadata)
    if truth_cases_4.metadata.get("ne", False):
        assert result != truth_cases_4.expected_output
    else:
        assert result == truth_cases_4.expected_output

def test_8_bit_scenarios(truth_cases_8):
    """Generic test for all 8-bit scenarios"""
    result = process_value(truth_cases_8.input_value, truth_cases_8.metadata)
    if truth_cases_8.metadata.get("ne", False):
        assert result != truth_cases_8.expected_output
    else:
        assert result == truth_cases_8.expected_output


def process_value(value, metadata):
    ...
