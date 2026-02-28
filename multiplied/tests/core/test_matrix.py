import pytest
import multiplied as mp

@pytest.mark.parametrize("size", mp.SUPPORTED_BITWIDTHS)
class TestSliceInstance():
    ...

@pytest.mark.parametrize("size", mp.SUPPORTED_BITWIDTHS)
class TestMatrixInstance():

    def test_matrix_instance(self, size):
        assert mp.Matrix(size) is not None

    def test_zero_matrix(self, size):
        zero_matrix = mp.Matrix(size)
        assert isinstance(zero_matrix, mp.Matrix)

        row = ["0"] * size
        for i in range(size):
            assert zero_matrix.matrix[i] == ["_"] * (size - i) + row + ["_"] * i

    def test_empty_matrix(self, size):
        empty_matrix = mp.Matrix(mp.raw_empty_matrix(size))
        assert isinstance(empty_matrix, mp.Matrix)
        for i in range(size):
            assert empty_matrix.matrix[i] == ["_"] * (size << 1)

    def test_resolve_rmap(size): ...

    def test_apply_map(size): ...


def test_raw_empty_matrix(size): ...
def test_raw_zero_matrix(size): ...
def test_matrix_merge(size): ...
