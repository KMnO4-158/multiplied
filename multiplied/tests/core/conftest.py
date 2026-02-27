import pytest
import multiplied as mp

# -- algorithm ------------------------------------------------------

@pytest.fixture(params=mp.SUPPORTED_BITWIDTHS)
def supported_algorithms(request):
    bit_width = request.param

    alg = mp.Algorithm(bit_width)
    alg.auto_resolve_stage(recursive=True)

    return alg

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

# -- map ------------------------------------------------------------


@pytest.fixture(params=mp.SUPPORTED_BITWIDTHS)
def reference_dadda_map(request):
    dadda_map = {
        4: [
            ["00", "00", "00", "00"] + ["00"] * 4,
            ["00", "00", "00", "FF"] + ["00"] * 4,
            ["00", "00", "FE", "FF"] + ["00"] * 4,
            ["00", "FD", "FE", "FF"] + ["00"] * 4,
        ],
        8: [
            ["00", "00", "00", "00", "00", "00", "00", "00"] + ["00"] * 8,
            ["00", "00", "00", "00", "00", "00", "00", "FF"] + ["00"] * 8,
            ["00", "00", "00", "00", "00", "00", "FE", "FF"] + ["00"] * 8,
            ["00", "00", "00", "00", "00", "FD", "FE", "FF"] + ["00"] * 8,
            ["00", "00", "00", "00", "FC", "FD", "FE", "FF"] + ["00"] * 8,
            ["00", "00", "00", "FB", "FC", "FD", "FE", "FF"] + ["00"] * 8,
            ["00", "00", "FA", "FB", "FC", "FD", "FE", "FF"] + ["00"] * 8,
            ["00", "F9", "FA", "FB", "FC", "FD", "FE", "FF"] + ["00"] * 8,
        ],
    }
    return mp.Map(dadda_map[request.param])


@pytest.fixture(params=mp.SUPPORTED_BITWIDTHS)
def supported_maps(request):
    return mp.Map(mp.raw_zero_map(request.param))

@pytest.fixture()
def raw_map_4_bit():
    matrix = mp.raw_zero_map(4)
    return matrix

@pytest.fixture()
def raw_map_8_bit():
    matrix = mp.raw_zero_map(8)
    return matrix

# -- matrix ---------------------------------------------------------

@pytest.fixture(params=[])
def supported_matrices():
    ...

@pytest.fixture()
def raw_zero_matrix_8_bit():
    matrix = mp.raw_zero_matrix(8)
    return matrix

@pytest.fixture(params=[raw_zero_matrix_8_bit, 8])
def zero_matrix_8_bit(request):
    return mp.Matrix(request.param)

@pytest.fixture()
def raw_zero_matrix_4_bit():
    matrix = mp.raw_zero_matrix(4)
    return matrix

@pytest.fixture(params=[raw_zero_matrix_4_bit, 4])
def zero_matrix_4_bit(request):
    return mp.Matrix(request.param)



# -- template -------------------------------------------------------

# @pytest.fixture()
# def ():
#     ...

# @pytest.fixture()
# def ():
#     ...

# @pytest.fixture()
# def ():
#     ...
