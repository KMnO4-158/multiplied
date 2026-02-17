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

    def __init__(self, map: list[Any]) -> None:
        if not(isinstance(map, list)):
            raise ValueError("Map must be type list")
        mp.validate_bitwidth(bits := len(map))
        self.bits = bits

        # -- handle standard maps -----------------------------------
        if isinstance(map[0], list):
            self.map  = map
            self.rmap = []
            return None

        # -- handle row maps ---------------------------------------
        checksum = [0]*bits
        for i, x in enumerate(map):
            if 2 < len(x) or not(0 <= int(x, 16) <= 255):
                raise ValueError(f"Expected hex value in range '00' to 'FF', got mapping {x}")
            checksum[i] = 1 if x != '00' else 0

        self.checksum =  checksum
        self.map  = self.build_map(map)
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
            if len(rmap[i]) != 2 and not(isinstance(rmap[i], str)):
                raise ValueError(f"Invalid row map element {rmap[i]}")
            map.append([rmap[i] for _ in range(n*2)])
        return map

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


def empty_map(bits: int)-> Map:
    """Return empty Multiplied Map object"""
    mp.validate_bitwidth(bits)
    return Map(["00"]*bits)


def build_dadda_map(bits: int) -> Map:
    """Return map representing the starting point of Dadda tree algorithm."""
    mp.validate_bitwidth(bits)

    # TODO: Use hoist() to generate dadda maps
    # -- Repulsive - Design algorithm for 16-bit+ ------------------------------ #
    dadda_map = {                                                                #
        4: [                                                                     #
            ['00','00','00','00'] + ['00']*4,                                    #
            ['00','00','00','FF'] + ['00']*4,                                    #
            ['00','00','FE','FF'] + ['00']*4,                                    #
            ['00','FD','FE','FF'] + ['00']*4                                     #
        ],                                                                       #
        8: [                                                                     #
            ['00','00','00','00','00','00','00','00'] + ['00']*8,                #
            ['00','00','00','00','00','00','00','FF'] + ['00']*8,                #
            ['00','00','00','00','00','00','FE','FF'] + ['00']*8,                #
            ['00','00','00','00','00','FD','FE','FF'] + ['00']*8,                #
            ['00','00','00','00','FC','FD','FE','FF'] + ['00']*8,                #
            ['00','00','00','FB','FC','FD','FE','FF'] + ['00']*8,                #
            ['00','00','FA','FB','FC','FD','FE','FF'] + ['00']*8,                #
            ['00','F9','FA','FB','FC','FD','FE','FF'] + ['00']*8                 #
        ]                                                                        #
    }                                                                            #
    # -------------------------------------------------------------------------- #

    return Map(dadda_map[bits])
