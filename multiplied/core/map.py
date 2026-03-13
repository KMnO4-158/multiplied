############################
# Map Bits Inside A Matrix #
############################


from typing import Any, Iterator

from .dtypes.base import MultipliedMeta
from .utils.bool import ishex2, validate_bitwidth
from .utils.pretty import pretty


class Map(MultipliedMeta):
    """Generates Map object from row map or standard map.

    Each Mapping is defined by a 2-bit hexadecimal value. Positive
    mappings move bits downwards, negative mappings move bits upwards.

    Parameters
    ----------
    map : list[Any]
        Simplified row map or 2D matrix.

    Examples
    --------
    >>> rmap = [00, FF, FF, 00]
    >>> Map(rmap)
    [[00,00,00,00,00,00,00,00],
     [FF,FF,FF,FF,FF,FF,FF,FF],
     [FF,FF,FF,FF,FF,FF,FF,FF],
     [00,00,00,00,00,00,00,00]]

    """

    def __init__(self, map: list[Any] | int, *, dadda: bool = False) -> None:
        if not isinstance(map, (list, int)):
            raise TypeError(f"Map must be type list or int got {type(map)}")
        self.bits = map if isinstance(map, int) else len(map)
        validate_bitwidth(self.bits)

        # -- handle bit defined maps --------------------------------
        if isinstance(map, int):
            self.map = self.build_zero_map(self.bits)
            self.rmap = ["00"] * self.bits
            return None

        # -- handle complex maps ------------------------------------
        self.map = map
        if isinstance(self.map[0], list):
            self.rmap = []

            # -- sanity check ---------------------------------------
            # ! Can be parallelised
            for y in map:
                for x in y:
                    if not ishex2(x):
                        raise ValueError(f"Invalid row map element {x}")
            return None

        self.map = self.build_map(map)
        self.rmap = map

        self._soft_type = list()
        self._dtype = "Map"
        return None

    def build_map(self, rmap: list[str]) -> list[list[str]]:
        """Use row map to generate standard map. Each element of simple map
        is a 2-bit, signed hex value. +ve = up, -ve = down.

        Parameters
        ----------
        rmap : list[str]
            Row map of the multiplied matrix.

        Returns
        -------
        list[list[str]]
            Standard map of the multiplied matrix.
        """

        validate_bitwidth(n := len(rmap))
        map = []
        for i in range(n):
            if not ishex2(rmap[i]):
                raise ValueError(f"Invalid row map element {rmap[i]}")
            map.append([rmap[i] for _ in range(n * 2)])
        return map

    def build_zero_map(self, bits: int) -> list[list[str]]:
        """Build a zero map of the specified size."""
        return [["00"] * (self.bits << 1) for _ in range(self.bits)]

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __str__(self) -> str:
        return pretty(self.map)

    def __iter__(self) -> Iterator[list[str]]:
        return iter(self.map)

    def __next__(self) -> list[str]:
        if self._index >= self.bits:
            raise StopIteration
        self._index += 1
        return self.map[self._index - 1]


def empty_map(bits: int) -> Map:
    """Return empty Multiplied Map object"""
    validate_bitwidth(bits)
    return Map(["00"] * bits)


def build_dadda_map(bits: int) -> Map:
    """Return map representing the starting point of Dadda tree algorithm."""
    validate_bitwidth(bits)
    return Map(raw_dadda_map(bits))


def raw_zero_map(bits: int) -> list[list[str]]:
    """Returns a zero-filled map of size `bits`."""
    matrix = []
    for i in range(bits):
        row = ["00"] * (bits << 1)
        matrix.append(row)
    return matrix


def raw_dadda_map(bits: int) -> list[list[str]]:
    """Returns a Dadda map of size `bits`."""
    matrix = []
    for i in range(bits):
        # generate 2-bit hex values which result in "V" shape partial product tree
        dadda = [f"{(255 - j):02X}"[-2:] for j in range(i - 1, -1, -1)]
        row = (["00"] * (bits - i)) + dadda + (["00"] * bits)
        matrix.append(row)
    return matrix

def unify_bounds(bounds: dict) -> dict:
    """Returns a simplified bound for non empty characters

    Parameters
    ----------
    bounds : dict
        Bounding box for each arithmetic unit in Template object

    Returns
    -------
    dict
        Unified bounds where  {y : [x0, x1]}

    See Also
    --------
    :func:`update_bounding_box`
    """
    if not isinstance(bounds, dict):
        raise TypeError(f"Expected dict got {type(bounds)}")
    if bounds.get("_") is None:
        raise ValueError("Bounds must have a `_` key")

    unified_row_bounds = {}
    for k, unit_bounds in bounds.items():
        if k == "_":
            continue
        for item, row in unit_bounds:
            if unified_row_bounds.get(row) is None:
                unified_row_bounds[row] = []
            unified_row_bounds[row].append(item)

    return unified_row_bounds


def apply_complex_map(matrix: list[list[str]], map: Map, bounds: dict) -> None:
    """Applies a complex mapping to source Matrix

    Parameters
    ----------
    matrix : mp.Matrix
        Matrix to apply mapping to

    map : mp.Map
        Multiplied Map object to apply mapping from

    bounds : dict[str: list[int]]
        Unified bounds for all arithmetic units
    """
    if not all([isinstance(r, int) for r in bounds]):
        raise TypeError("Expected all row bounds to be integers")

    for row in sorted(bounds.keys()):
        if not isinstance(bounds[row], list):
            raise TypeError("Expected row bounds to be a list")

        for col in range(bounds[row][0], bounds[row][1] + 1):
            if map.map[row][col] == "00":
                continue
            if (offset := int(map.map[row][col], 16)) & 128:
                offset = (~offset + 1) & 255  # 2s complement

            matrix[row - offset][col] = matrix[row][col]
            matrix[row][col] = "_"

    return None
