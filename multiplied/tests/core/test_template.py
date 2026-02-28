import pytest
import multiplied as mp


def test_build_adder():
    mp.build_adder

def test_build_csa():
    mp.build_csa

def test_build_noop():
    mp.build_noop

def test_build_empty_slice():
    mp.build_empty_slice



@pytest.mark.parametrize("size", mp.SUPPORTED_BITWIDTHS)
class TestPatternInstance():
    ...

@pytest.mark.parametrize("size", mp.SUPPORTED_BITWIDTHS)
class TestTemplateInstance():
    ...
