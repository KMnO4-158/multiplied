from multiplied.tests import REFERENCE, TestCase
import pytest
import multiplied as mp
# block ruff format:
# fmt: off


# -- test data generation -------------------------------------------
"""
metadata:
    type:
        sha: shallow truth table
    all:
        test all supported bits

"""
TEST_TRUTH_TABLES = [
    # TC(name, input, expected_output, metadata)
    TestCase("shallow_small_scope", REFERENCE["small_scope"], None, {"type": "sha", "all": True}),
    TestCase("shallow_medium_scope", REFERENCE["medium_scope"], None, {"type": "sha", "all": True}),
    TestCase("table_small_scope", REFERENCE["small_scope"], None, {"all": True}),
    TestCase("table_medium_scope", REFERENCE["medium_scope"], None, {"all": True}),
]

# -- test scope generation ------------------------------------------
"""
metadata:
    None
"""
TEST_SCOPE = [
    # TC(name, input, expected_output, metadata)
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

# -- parameterise ---------------------------------------------------

@pytest.fixture(params=TEST_TRUTH_TABLES, ids=lambda tc: tc.name)
def truth_table_cases(request):
    """Parameterized fixture truth table scenarios"""
    return request.param

@pytest.fixture(params=TEST_SCOPE, ids=lambda tc: tc.name)
def truth_scope_cases(request):
    """Parameterized fixture for truth scopes"""
    return request.param

# -- truth table tests ----------------------------------------------
@pytest.mark.parametrize("bits", mp.SUPPORTED_BITWIDTHS)
def test_truth_table_scenarios(truth_table_cases, bits):
    """Generic test for all 4-bit scenarios"""
    result = process_table(truth_table_cases.input_value, truth_table_cases.metadata, bits)
    if truth_table_cases.metadata.get("ne", False):
        assert result != truth_table_cases.expected_output
    else:
        assert result == truth_table_cases.expected_output


def process_table(value, metadata, bits):
    if metadata.get("shallow", False):
        return validate_shallow_table(value, bits)
    else:
        return validate_table(value, bits)


def validate_shallow_table(scope, bits):
    alg = mp.Algorithm(bits)
    alg.auto_resolve_stage()
    table = mp.shallow_truth_table(scope, mp.Algorithm(bits))
    try:
        if all([isinstance(t, mp.Matrix) for t in table]):
            return None
        else:
            return TypeError
    except TypeError:
        return TypeError
    except ValueError:
        return ValueError
    except Exception:
        return Exception

def validate_table(scope, bits):
    alg = mp.Algorithm(bits)
    alg.auto_resolve_stage()
    table = mp.truth_table(scope, alg)
    try:
        for d in table:
            for k, v in d.items():
                if not isinstance(v, mp.Matrix):
                    return TypeError
    except TypeError:
        return TypeError
    except ValueError:
        return ValueError
    except Exception:
        return Exception


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
