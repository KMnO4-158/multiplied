from multiplied.tests import (
    TestCase,
    REFERENCE,
    reference_resolved_pattern
)
import multiplied as mp
import pytest


"""
metadata:
    all:
        whether to test all attributes
    bits:
        input.bits
    len:
        input.__len__()
    rand:
        generate patters with random arithmetic unit distribution
"""
TEST_PATTERN_INSTANCE = [
    # TC(name, input, expected_output, metadata)
    TestCase("pattern_instance", REFERENCE["pattern"], mp.Pattern, {"all": True}),
    TestCase("pattern_bits", REFERENCE["pattern"], None, {"bits": True, "all": True}),
    TestCase("pattern_len", REFERENCE["pattern"], None, {"len": True, "all": True}),

    # TestCase("pattern_random", None, mp.Pattern, {"all": True, "rand": True}), # TODO
]

TEST_TEMPLATE_INSTANCE = [
    # TC(name, input, expected_output, metadata)
    TestCase("template_instance", REFERENCE["template"], mp.Template, {"all": True}),
    TestCase("template_bits", REFERENCE["template"], None,  {"bits": True, "all": True}),
    TestCase("template_len", REFERENCE["template"], None,  {"len": True, "all": True}),

    # TestCase("template_random", None, None, {"all": True, "rand": True}), # TODO
]

# --
TEST_BOOLEAN = []

TEST_ITER = []

TEST_ERROR = []


@pytest.fixture(params=TEST_PATTERN_INSTANCE, ids=lambda tc: tc.name)
def pattern_instance(request):
    """Parameterized fixture for 4-bit truth table scenarios"""
    return request.param


@pytest.fixture(params=TEST_TEMPLATE_INSTANCE, ids=lambda tc: tc.name)
def template_instance(request):
    """Parameterized fixture for 8-bit truth table scenarios"""
    return request.param



def test_pattern_instance(pattern_instance, supported_bitwidths):
    """Generic test for all 4-bit scenarios"""
    bits = supported_bitwidths
    result = process_value(pattern_instance.input_value, pattern_instance.metadata, supported_bitwidths)
    if pattern_instance.metadata.get("ne", False):
        assert not isinstance(result, pattern_instance.expected_output)
    elif pattern_instance.metadata.get("bits", False):
        assert result == bits
    elif pattern_instance.metadata.get("len", False):
        assert result == bits
    else:
        assert isinstance(result, pattern_instance.expected_output)


def test_template_instance(template_instance, supported_bitwidths):
    """Generic test for all 8-bit scenarios"""
    bits = supported_bitwidths
    result = process_value(template_instance.input_value, template_instance.metadata, supported_bitwidths)
    if template_instance.metadata.get("ne", False):
        assert not isinstance(result, template_instance.expected_output)
    elif template_instance.metadata.get("bits", False):
        assert result == bits
    elif template_instance.metadata.get("len", False):
        assert result == bits
    else:
        assert isinstance(result, template_instance.expected_output)

def process_value(value, metadata, supported_bitwidths):
    bits = supported_bitwidths
    if isinstance(value[bits][0], str):
        print(f"pattern:: bits: {bits}, value: {value[bits]}")
        data = mp.Pattern(value[bits])
    elif isinstance(value[bits][0], list):
        print(f"template:: bits: {bits}, value: {value[bits]}")
        data = mp.Template(value[bits])
    else:
        raise TypeError(f"Expected raw template or pattern got {value}")

    if metadata.get("rand", False):
        raise NotImplementedError("Random data not implmented")
    elif metadata.get("bits", False):
        return data.bits
    elif metadata.get("len", False):
        return data.__len__()
    else:
        return data

# -- pattern resolution tests ---------------------------------------

@pytest.fixture(params=reference_resolved_pattern())
def resolved_pattern_instance(request):
    return request.param

def test_resolve_pattern(resolved_pattern_instance):
    assert isinstance(resolved_pattern_instance, mp.Pattern)
