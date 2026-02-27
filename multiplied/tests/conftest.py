import pytest
import multiplied as mp

@pytest.fixture()
def supported_bitwidths():
    return mp.SUPPORTED_BITWIDTHS

@pytest.fixture(params=mp.SUPPORTED_BITWIDTHS)
def dadda_map(request):
    return mp.build_dadda_map(request.param)
