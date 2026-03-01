from multiplied.tests import TestCase
import pytest
import multiplied as mp

TEST_4_BIT_SCENARIOS = [
    # truth table / truth dataframe
]

TEST_8_BIT_SCENARIOS = [

    # truth table / truth dataframe
]

# TC(name, [domain, range], error, metadata)
TEST_SCOPE = [
    TestCase("4_bit_truth_scope", [(1, 15), (1, 255)], None, {}),
    TestCase("8_bit_truth_scope", [(1, 255), (1, 65535)], None, {}),
    TestCase("tr_scope_all_one", [(1, 1), (1, 1)], None, {}),
    TestCase("tr_sc_max_in_lt_min_out", [(1, 15), (150, 255)], None, {}),
    TestCase("tr_scope_min_cross", [(2, 15), (1, 255)], Warning, {}),
    TestCase("tr_scope_max_cross", [(2, 15), (2, 14)], Warning, {}),
    TestCase("tr_scope_str_tup", ["ab", ("cd")], TypeError, {}),
    TestCase("tr_scope_str_str", ["ab", "cd"], TypeError, {}),
    TestCase("tr_scope_str_int", ["ab", 255], TypeError, {}),
    TestCase("tr_scope_int_int", [15, 255], TypeError, {}),
    TestCase("tr_scope_tup_str_int", [("f", 15), ("ff", 255)], TypeError, {}),
    TestCase("tr_scope_zero", [(0, 255), (150, 255)], ValueError, {}),
    TestCase("tr_scope_zero", [(0, 255), (150, 255)], ValueError, {}),

]


@pytest.fixture(params=TEST_4_BIT_SCENARIOS, ids=lambda tc: tc.name)
def truth_cases_4(request):
    """Parameterized fixture for 4-bit truth table scenarios"""
    return request.param


@pytest.fixture(params=TEST_8_BIT_SCENARIOS, ids=lambda tc: tc.name)
def truth_cases_8(request):
    """Parameterized fixture for 8-bit truth table scenarios"""
    return request.param

@pytest.fixture(params=TEST_SCOPE, ids=lambda tc: tc.name)
def truth_scope_cases(request):
    """Parameterized fixture for truth scopes"""
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

# -- truth scope tests ----------------------------------------------

def test_truth_scope(truth_scope_cases):
    """Generic test for truth scopes"""

    domain_, range_ = truth_scope_cases.input_value

    if (err := truth_scope_cases.expected_output) is None:
        assert mp.truth_scope(range_, domain_) is not None
    elif err is Warning:
        with pytest.warns(UserWarning):
            next(mp.truth_scope(domain_, range_))

    else:
        with pytest.raises(err):
            next(mp.truth_scope(domain_, range_))
