import pytest
import multiplied as mp
import pandas as pd


@pytest.fixture(params=mp.SUPPORTED_BITWIDTHS)
def supported_bitwidths(request):
    bit = request.param
    return bit


@pytest.fixture(params=mp.SUPPORTED_BITWIDTHS)
def dadda_map(request, ids=lambda tc: f"{tc}-bit"):
    map = mp.build_dadda_map(request.param)
    return map


@pytest.fixture(params=mp.SUPPORTED_BITWIDTHS)
def sample_dataframe(request, ids=lambda tc: f"{tc}-bit"):
    """
    PURPOSE:
        Creates a small DataFrame with proper column format for heatmap testing.
        This is the most basic fixture - use when you just need some valid data.

    EXAMPLE OUTPUT:
        Index  s0_p0_b0  s0_p0_b1  s0_p1_b0  ... s1_p1_b7
        0           0         1         0   ...        1
        1           1         0         1   ...        0
        2           0         1         0   ...        1
        3           1         0         1   ...        0
        4           1         1         0   ...        1

    """
    column_data = {}
    bits = request.params
    stages = bits >> 1  # Number of stages in algorithm
    num_rows = 5  # Number of test data rows
    ppm_bits = bits << 1  # Bit width
    ppms = bits  # PPMs per stage

    # Create columns in format: s{stage}_p{ppm}_b{bit}
    for stage in range(stages):
        for ppm in range(ppms):
            for bit in range(ppm_bits):
                col_name = f"s{stage}_p{ppm}_b{bit}"
                # Fill with alternating 0/1 values
                column_data[col_name] = [i % 2 for i in range(num_rows)]

    return pd.DataFrame(column_data)


@pytest.fixture()
def algorithm_4_bit():
    alg = mp.Algorithm(4)
    alg.auto_resolve_stage(recursive=True)
    return alg


@pytest.fixture()
def algorithm_8_bit():
    alg = mp.Algorithm(8)
    alg.auto_resolve_stage(recursive=True)
    return alg
