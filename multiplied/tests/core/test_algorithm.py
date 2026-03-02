from multiplied.tests import (
    TestCase,
    REFERENCE,
    reference_resolved_pattern
)
import multiplied as mp
import pytest


"""
metadata:
    all: # ignored for now
        whether to test all bitwidths
    bits:
        input.bits
    len:
        input.__len__()
"""
TEST_ALGORITHM_INSTANCE = [
    # TC(name, input, expected_output, metadata)
    TestCase("auto_alg_len", None, None, {"len": True, "all": True}),
    TestCase("auto_alg_bits", None, None, {"bits": True, "all": True}),
    TestCase("auto_alg", None, mp.Algorithm, {"all": True}),
    TestCase("auto_alg_pattern", REFERENCE["pattern"], mp.Algorithm, {"all": True}),
    TestCase("auto_alg_template", REFERENCE["template"], mp.Algorithm, {"all": True}),

]

TEST_ALGORITHM_EXECUTION = [
    TestCase("alg_exec", None, mp.Matrix, {"all": True, "exec": True}),
    TestCase("alg_step_one", 1, mp.Matrix, {"all": True, "step":True}),
    TestCase("alg_step_all", 0, mp.Matrix, {"all": True, "step":True}),
]

# --
TEST_BOOLEAN = []

TEST_ITER = []

TEST_ERROR = []


@pytest.fixture(params=TEST_ALGORITHM_INSTANCE, ids=lambda tc: tc.name)
def algorithm_instance(request):
    """Parameterized fixture for Algorithm instances"""
    return request.param


@pytest.fixture(params=TEST_ALGORITHM_EXECUTION, ids=lambda tc: tc.name)
def algorithm_execution(request):
    """Parameterized fixture for Algorithm execution scenarios"""
    return request.param



def test_algorithm_instance(algorithm_instance, supported_bitwidths):
    """Generic test for all Algorithm instance scenarios"""
    bits = supported_bitwidths
    result = process_value(algorithm_instance.input_value, algorithm_instance.metadata, supported_bitwidths)
    if algorithm_instance.metadata.get("ne"):
        assert not isinstance(result, algorithm_instance.expected_output)
    elif algorithm_instance.metadata.get("bits"):
        assert result == bits
    elif algorithm_instance.metadata.get("len"):
        assert isinstance(result, int) and 1 < result
    else:
        assert isinstance(result, algorithm_instance.expected_output)

def test_algorithm_execution(algorithm_execution, supported_bitwidths):
    """Generic test for all Algorithm execution scenarios"""
    result = process_value(algorithm_execution.input_value, algorithm_execution.metadata, supported_bitwidths)
    if not isinstance(result, dict):
        raise TypeError(f"Expected [dict] got {type(result)}")
    if algorithm_execution.metadata.get("ne"):
        assert not isinstance(result, algorithm_execution.expected_output)
    else:
        assert all([isinstance(r, algorithm_execution.expected_output) for r in result.values()])

def process_value(value, metadata, supported_bitwidths):

    # -- instantiate ------------------------------------------------

    bits = supported_bitwidths
    if value is not None and not isinstance(value, int):
        alg = mp.Algorithm(bits)
        if isinstance(value.get(bits), list):
            pattern = mp.Pattern(value[bits])
            alg.push(pattern)
        elif isinstance(value[bits]["T"][0], list):
            template = mp.Template(value[bits]["T"], result=value[bits]["R"])
            alg.push(template)
        else:
            raise TypeError(f"Expected raw template or pattern got {value}")

        alg.auto_resolve_stage()
    else:
        alg = mp.Algorithm(bits)
        alg.auto_resolve_stage()


    # -- apply function ---------------------------------------------

    if metadata.get("bits"):
        return alg.bits

    elif metadata.get("len"):
        return alg.__len__()

    elif metadata.get("step"):
        matrix = mp.Matrix(bits, a=((2**bits)-1), b=((2**bits)-1))
        alg.reset(matrix)
        if value < 1:
            data = alg.step()
            return {1: data}

        data = {}
        for i in range(value):
            data[i] = alg.step()
        return data

    elif metadata.get("exec"):
        data = alg.exec(((2**bits)-1), ((2**bits)-1))
        return data

    else:
        return alg
