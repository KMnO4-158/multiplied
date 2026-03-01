############################
# Map Bits Inside A Matrix #
############################

import multiplied as mp
from typing import Any, Iterator


class Map:
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
        mp.validate_bitwidth(self.bits)

        # -- handle bit defined maps --------------------------------
        if isinstance(map, int):
            self.map = self.build_zero_map(self.bits)
            self.rmap = ["00"] * self.bits
            return None

        # -- handle standard maps -------------------------------
        self.map = map
        if isinstance(self.map[0], list):
            self.rmap = []
            return None

        # -- handle row maps ----------------------------------------
        # TODO: refactor -> coordinate based mapping
        # TODO: calculate when map results in out-of-bound mapping(s)
        checksum = [0] * self.bits
        for i, x in enumerate(map):
            if 2 != len(x) or not (0 <= int(x, 16) <= 255):
                raise TypeError(
                    f"Expected hex value in range '00' to 'FF', got mapping {x}"
                )
            checksum[i] = 1 if x != "00" else 0

        self.checksum = checksum
        self.map = self.build_map(map)
        self.rmap = map
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

        mp.validate_bitwidth(n := len(rmap))
        map = []
        for i in range(n):
            if len(rmap[i]) != 2 and not (isinstance(rmap[i], str)):
                raise ValueError(f"Invalid row map element {rmap[i]}")
            map.append([rmap[i] for _ in range(n * 2)])
        return map

    def build_zero_map(self, bits: int) -> list[list[str]]:
        """Build a zero map of the specified size."""
        return [["00"] * (self.bits << 1) for _ in range(self.bits)]

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __str__(self) -> str:
        return mp.pretty(self.map)

    def __iter__(self) -> Iterator[list[str]]:
        return iter(self.map)

    def __next__(self) -> list[str]:
        if self._index >= self.bits:
            raise StopIteration
        self._index += 1
        return self.map[self._index - 1]


def empty_map(bits: int) -> Map:
    """Return empty Multiplied Map object"""
    mp.validate_bitwidth(bits)
    return Map(["00"] * bits)


def build_dadda_map(bits: int) -> Map:
    """Return map representing the starting point of Dadda tree algorithm."""
    mp.validate_bitwidth(bits)
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
