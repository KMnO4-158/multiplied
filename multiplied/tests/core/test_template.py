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
    rand:
        generate patterns with random arithmetic unit distribution
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

# == test instance ==================================================

@pytest.fixture(params=TEST_PATTERN_INSTANCE, ids=lambda tc: tc.name)
def pattern_instance(request):
    """Parameterized fixture for Pattern instances"""
    return request.param


@pytest.fixture(params=TEST_TEMPLATE_INSTANCE, ids=lambda tc: tc.name)
def template_instance(request):
    """Parameterized fixture for Template instances"""
    return request.param



def test_pattern_instance(pattern_instance, supported_bitwidths):
    """Generic test for all Pattern instances scenarios"""
    bits = supported_bitwidths
    result = process_value(pattern_instance.input_value, pattern_instance.metadata, supported_bitwidths)
    if pattern_instance.metadata.get("ne"):
        assert not isinstance(result, pattern_instance.expected_output)
    elif pattern_instance.metadata.get("bits"):
        assert result == bits
    elif pattern_instance.metadata.get("len"):
        assert result == bits
    else:
        assert isinstance(result, pattern_instance.expected_output)


def test_template_instance(template_instance, supported_bitwidths):
    """Generic test for all Template instances scenarios"""
    bits = supported_bitwidths
    result = process_value(template_instance.input_value, template_instance.metadata, supported_bitwidths)
    if template_instance.metadata.get("ne"):
        assert not isinstance(result, template_instance.expected_output)
    elif template_instance.metadata.get("bits"):
        assert result == bits
    elif template_instance.metadata.get("len"):
        assert result == bits
    else:
        assert isinstance(result, template_instance.expected_output)

def process_value(value, metadata, supported_bitwidths):

    # -- instantiate ------------------------------------------------
    bits = supported_bitwidths
    if isinstance(value.get(bits), list): # REF pattern: list, REF dict:
        data = mp.Pattern(value[bits])
    elif isinstance(value[bits]["T"][0], list):
        data = mp.Template(value[bits]["T"])
    else: # pragma: no cover
        raise TypeError(f"Expected raw template or pattern got {value}")

    # -- apply function ---------------------------------------------
    if metadata.get("rand"): # pragma: no cover
        raise NotImplementedError("Random data not implemented") # pragma: no cover
    elif metadata.get("bits"):
        return data.bits
    elif metadata.get("len"):
        return data.__len__()
    else:
        return data

# == test pattern resolution ========================================

@pytest.fixture(params=reference_resolved_pattern())
def resolved_pattern_instance(request):
    return request.param

def test_resolve_pattern(resolved_pattern_instance):
    assert isinstance(resolved_pattern_instance, mp.Pattern)
