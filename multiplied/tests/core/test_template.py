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
    shape:
        whether to test shape
    rand:
        generate patters with random arithmetic unit distribution
"""
TEST_PATTERN_INSTANCE = [
    # TC(name, input, expected_output, metadata)
    TestCase("pattern_instance", REFERENCE["pattern"], mp.Pattern, {"all": True}),
    TestCase("pattern_random", None, mp.Pattern, {"all": True, "rand": True}),
]

TEST_TEMPLATE_INSTANCE = [
    # TC(name, input, expected_output, metadata)
    TestCase("template_shape", None, None,  {"all": True, "shape": True}),
    TestCase("template_instance", None, mp.Template, {"all": True}),
    TestCase("template_random", None, None, {"all": True, "rand": True}),
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


def test_pattern_instance(pattern_instance):
    """Generic test for all 4-bit scenarios"""
    result = process_pattern(pattern_instance.input_value, pattern_instance.metadata)
    if pattern_instance.metadata.get("ne", False):
        assert result != pattern_instance.expected_output
    if pattern_instance.metadata.get("res", False):
        assert isinstance(result, mp.Pattern)
    else:
        assert result == pattern_instance.expected_output


def test_template_instance(template_instance):
    """Generic test for all 8-bit scenarios"""
    result = process_template(template_instance.input_value, template_instance.metadata)
    if template_instance.metadata.get("ne", False):
        assert result != template_instance.expected_output
    else:
        assert result == template_instance.expected_output


def process_pattern(value, metadata):
    if value is None:
        if metadata.get("rand", False):
            # random templates
            return None
    ...

def process_template(value, metadata):

    ...

# -- pattern resolution tests ---------------------------------------

@pytest.fixture(params=reference_resolved_pattern())
def resolved_pattern_instance(request):
    return request.param

def test_resolve_pattern(resolved_pattern_instance):
    assert isinstance(resolved_pattern_instance, mp.Pattern)
