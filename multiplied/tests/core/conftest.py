import pytest
import multiplied as mp

# -- algorithm ------------------------------------------------------

@pytest.fixture(params=[4, 8])
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
def raw_zero_map(bits):
    matrix = []
    for i in range(bits):
        row = ["00"] * (bits << 1)
        matrix.append(row)
    return matrix

@pytest.fixture(params=[4, 8])
def supported_maps(request):
    bits = request.param
    return mp.Map(raw_zero_map(bits))

@pytest.fixture()
def raw_map_4_bit():
    matrix = raw_zero_map(4)
    return matrix

@pytest.fixture()
def raw_map_8_bit():
    matrix = raw_zero_map(8)
    return matrix

# -- matrix ---------------------------------------------------------

def raw_empty_matrix(bits):
    matrix = []
    for i in range(bits):
        row = ["_" for _ in range(bits << 1)]
        matrix.append(row)
    return matrix

def raw_zero_matrix(bits):
    matrix = []
    zero = ["0"] * bits
    for i in range(bits):
        row = (["_"] * ((bits << 1) - bits - i)) + zero + (["_"] * i)
        matrix.append(row)
    return matrix

@pytest.fixture(params=[])
def supported_matrices():
    ...

@pytest.fixture()
def raw_zero_matrix_8_bit():
    matrix = raw_zero_matrix(8)
    return matrix

@pytest.fixture(params=[raw_zero_matrix_8_bit, 8])
def zero_matrix_8_bit(request):
    return mp.Matrix(request.param)

@pytest.fixture()
def raw_zero_matrix_4_bit():
    matrix = [
        ["_", "_", "_", "_", "0", "0", "0", "0"],
        ["_", "_", "_", "0", "0", "0", "0", "_"],
        ["_", "_", "0", "0", "0", "0", "_", "_"],
        ["_", "0", "0", "0", "0", "_", "_", "_"]
    ]
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
