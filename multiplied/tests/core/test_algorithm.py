from multiplied.tests import TestCase, REFERENCE
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
# block ruff format:
# fmt: off

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
    TestCase("alg_step_one", 1, mp.Matrix, {"all": True, "step": True}),
    TestCase("alg_step_all", 0, mp.Matrix, {"all": True, "step": True}),
    TestCase("alg_exec_complex", (REFERENCE["complex_template"][8]["T"], REFERENCE["complex_map"][8]), None, {"exec": True}),
]

# --
TEST_BOOLEAN = []

TEST_ITER = []

TEST_ERROR = []
# fmt: on


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
    result = process_value(
        algorithm_instance.input_value, algorithm_instance.metadata, supported_bitwidths
    )
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
    if algorithm_execution.metadata.get("all"):
        result = process_value(
            algorithm_execution.input_value,
            algorithm_execution.metadata,
            supported_bitwidths,
        )
        if not isinstance(result, dict):  # pragma: no cover
            raise TypeError(f"Expected [dict] got {type(result)}")
    else:
        result = process_algorithm(
            algorithm_execution.input_value,
            algorithm_execution.metadata,
        )

    if algorithm_execution.metadata.get("ne"):
        assert not isinstance(result, algorithm_execution.expected_output)
    elif algorithm_execution.metadata.get("all"):
        if not isinstance(result, dict):  # pragma: no cover
            raise TypeError(f"Expected [dict] got {type(result)}")
        assert all(
            [
                isinstance(r, algorithm_execution.expected_output)
                for r in result.values()
            ]
        )
    else:
        if not isinstance(result, tuple):  # pragma: no cover
            raise TypeError(f"Expected [tuple] got {type(result)}")
        assert result[0] == result[1]


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
        else:  # pragma: no cover
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
        matrix = mp.Matrix(bits, a=((2**bits) - 1), b=((2**bits) - 1))
        alg.reset(matrix)
        if value < 1:
            data = alg.step()
            return {1: data}

        data = {}
        for i in range(value):
            data[i] = alg.step()
        return data

    elif metadata.get("exec"):
        data = alg.exec(((2**bits) - 1), ((2**bits) - 1))
        return data

    else:
        return alg  # to assert instance


def process_algorithm(value: list | tuple, metadata):
    if isinstance(value, list):
        if not isinstance(value[0], list):
            raise TypeError(f"Expected [list[list]] got {type(value)}")
    elif isinstance(value, tuple):
        if not (isinstance(value[0], list) and isinstance(value[1], list)):
            raise TypeError(f"Expected tuple[list, list] got {type(value)}")
    else:
        raise TypeError("Unexpected TestCase values")

    match value:
        case list():
            bits = len(value)
            mp.validate_bitwidth(bits)
            map_ = None
            template = value
        case tuple():
            if len(value[0]) != len(value[1]):
                raise ValueError("Template bitwidth must match Map bitwidth")
            bits = len(value[0])
            template = value[0]
            map_ = value[1]
        case _:
            raise TypeError("Unexpected TestCase values")

    print(map_)
    alg = mp.Algorithm(bits)

    if map_ is not None:
        alg.push(mp.Template(template), mp.Map(map_))
    else:
        alg.push(mp.Template(template))

    alg.auto_resolve_stage()

    if metadata.get("exec"):
        output = alg.exec((2**bits) - 1, (2**bits) - 1)
        print(list(output.values())[-1][0][0])
        print(alg)
        for i in output.values():
            print(i)
        result = int("".join(list(output.values())[-1][0][0]), 2)
        product = ((2**bits) - 1) * ((2**bits) - 1)
        return (result, product)

    if metadata.get("step"):
        matrix = mp.Matrix(bits, a=((2**bits) - 1), b=((2**bits) - 1))
        alg.reset(matrix)
        output = [matrix]

        for _ in range(alg.__len__()):
            output.append(alg.step())
        print(output[-1][0][0])
        result = int("".join(output[-1][0][0]), 2)
        product = ((2**bits) - 1) * ((2**bits) - 1)
        return (result, product)
