import pytest
import multiplied as mp


@pytest.mark.parametrize("size", mp.SUPPORTED_BITWIDTHS)
class TestMapInstance:
    def test_map_instance(self, size):
        assert mp.Map(size) is not None

    def test_zero_map(self, size):
        zero_map = mp.Map(size)
        assert isinstance(zero_map, mp.Map)

    def test_zero_row_map(self, size):
        zero_row_map = mp.Map(["00"] * size)
        assert isinstance(zero_row_map, mp.Map)

    def test_row_map(self, size):
        row_map = mp.Map([f"{(255 - j):02X}"[-2:] for j in range(size - 1, -1, -1)])
        assert isinstance(row_map, mp.Map)

    # ! NOT IMPLEMENTED
    # def test_out_of_bound_row_map(self, size):
    #     with pytest.raises(ValueError):
    #         mp.Map((["FF"] + ["00"] * (size-1)))  # out_of_bound_row_map
    #         mp.Map((["7F"] * (size)))             # out_of_bound_row_map
    #         mp.Map((["00"] * (size-1) + ["01"]))  # out_of_bound_row_map
    #         mp.Map((["80"] * (size)))             # out_of_bound_row_map

    def test_row_map_type(self, size):
        print(size)
        with pytest.raises(ValueError):
            mp.Map(["0"] * size)  # Not 2-bit hex
            mp.Map(["F"] * size)  # Not 2-bit hex


def test_dadda_map_instance(dadda_map):
    assert isinstance(dadda_map, mp.Map)
    print(dadda_map)
    # -- validate dadda shape ---------------------------------------
    assert len(dadda_map.map) == dadda_map.bits
    if dadda_map.rmap != []:
        assert len(dadda_map.rmap) == (dadda_map.bits)


def test_dadda_map_mapping(dadda_map, reference_dadda_map):
    # -- validate dadda mapping -------------------------------------
    if dadda_map.bits == reference_dadda_map.bits:
        for i in range(dadda_map.bits):
            assert dadda_map.map[i] == reference_dadda_map.map[i]
    else:
        with pytest.raises(AssertionError):
            for i in range(dadda_map.bits):
                assert dadda_map.map[i] == reference_dadda_map.map[i]
