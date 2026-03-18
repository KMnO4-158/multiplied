################################################
# Classes to Represent And Manage Nested Lists #
################################################

from copy import deepcopy
from itertools import batched, pairwise
from typing import Any, Iterator

from .dtypes.base import MultipliedMeta
from .map import Map, apply_complex_map
from .utils.bool import ischar, ishex2, isint, isppm, validate_bitwidth
from .utils.pretty import pretty


# ! Review slices and their integration to the wider library
#
# IDEAS:
# - work exclusively with multiplied objects
# - Slice also slices metadata from source object
class Slice(MultipliedMeta):
    """Matrix slice which adheres to multiplied formatting rules.
    Retains metadata slice from source object:

    Parameters
    ----------
    matrix : list[Any]
        A slice from any Multiplied object.
    """

    # TODO
    """
    >>> Matrix[start:end]
    Slice(
        <Matrix.bits>,
        <Matrix.matrix[start:end]>,
        <Matrix.checksum[start:end]>,
        <Matrix.meta[start:end],
        ...
        )
    """

    def __init__(self, matrix: list[Any]):
        if isinstance(matrix[0], list):
            self.bits = len(matrix[0]) >> 1
        elif isinstance(matrix, list) and isinstance(matrix[0], str):
            self.bits = len(matrix) >> 1

        validate_bitwidth(self.bits)
        self.slice = matrix if isinstance(matrix[0], list) else [matrix]

        self._soft_type = list()
        return None

    # TODO:: look into overloads for accurate type usage
    #
    #  index: int -> T
    #  index: slice -> list[T]
    def __getitem__(self, index: int) -> list[Any]:
        slice = [self.slice] if len(self.slice[index]) == 1 else self.slice
        return slice[index]

    def __eq__(self, slice: Any, /) -> bool:
        if slice.bits != self.bits:
            return False
        for i in range(self.bits):
            if slice.slice[i] != self.slice[i]:
                return False
        return True

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __str__(self):
        return str(pretty(self.slice))

    def __len__(self) -> int:
        return len(self.slice)

    def __iter__(self) -> Iterator:
        return iter(self.slice)

    def __next__(self):
        if self.index >= len(self.slice):
            raise StopIteration
        self.index += 1
        return self.slice[self.index - 1]


# ! Matrix.x_checksum is only useful in the context of Algorithm.__reduce()
# - Maybe use bounds to create x_checksum within __reduce()'s unit collection
# - OR within, the same scope, use bounds to execute a given arithmetic unit
class Matrix(MultipliedMeta):
    """Partial Product Matrix

    Parameters
    ----------
    matrix : list[Any] | int
        A 2D nested list or an integer representing the bitwidth.
    a : int=0, optional
        First operand used in partial product generation(PPM)
    b : int=0, optional
        Second operand used in PPM
    """

    def __init__(
        self,
        source: list[Any] | int,
        *,
        a: int = 0,
        b: int = 0,
    ) -> None:
        # -- sanity check -------------------------------------------
        if isinstance(source, int):
            self.bits = source
            validate_bitwidth(self.bits)
            self.__build_matrix(a, b)
            return
        elif isinstance(source, list) and isinstance(source[0], list):
            if not isppm(source):
                raise TypeError(f"Expected partial product matrix, got {source}")
            self.bits = len(source)
            validate_bitwidth(self.bits)
        elif isinstance(source, Slice):
            # ! matrix scatter Slice -> list[list[str]]
            raise NotImplementedError("Slice initialization not supported")
        else:
            raise TypeError(f"Expected integer or nested list, got {type(source)}")

        self.matrix = source

        self._soft_type = list()
        return None

    def __zero_matrix(self, bits: int) -> None:
        """Build a wallace tree for a bitwidth of self.bits"""
        row = ["0"] * bits
        matrix = []
        for i in range(bits):
            matrix.append(["_"] * (bits - i) + row + ["_"] * i)
        self.matrix = matrix
        return None

    def __build_matrix(self, operand_a: int, operand_b: int) -> None:
        """Build Logical AND matrix using source operands and it's checksum."""

        validate_bitwidth((bits := self.bits))
        if (operand_a > ((2**bits) - 1)) or (operand_b > ((2**bits) - 1)):
            raise ValueError("Operand bit width exceeds matrix bit width")

        # -- catch multiply by zero ---------------------------------
        if operand_a == 0 or operand_b == 0:
            self.__zero_matrix(bits)
            return None

        # -- generate -----------------------------------------------
        # convert to binary, removing '0b' and padding with zeros
        a = bin(operand_a)[2:].zfill(bits)
        b = bin(operand_b)[2:].zfill(bits)
        matrix = []
        for i in range(bits - 1, -1, -1):
            if b[i] == "0":
                matrix.append(["_"] * (i + 1) + ["0"] * (bits) + ["_"] * (bits - i - 1))
            elif b[i] == "1":
                matrix.append(["_"] * (i + 1) + list(a) + ["_"] * (bits - i - 1))

        self.matrix = matrix
        return None

    def resolve_rmap(self, *, ignore_zeros: bool = True) -> Map:
        """Find empty rows, create simple map to efficiently pack rows

        Parameters
        ----------
        ignore_zeros : bool
            If True, ignore rows with only zeros

        Returns
        -------
        Map
            Map object containing the generated row mapping

        """

        option = "0" if ignore_zeros else "_"
        offset = 0
        rmap = []
        for i in range(self.bits):
            if all([bit == "_" and bit != option for bit in self.matrix[i]]):
                offset += 1
                val = 0
            else:
                val = (offset ^ 255) + 1  # 2s complement
            rmap.append(f"{val:02X}"[-2:])
        return Map(rmap)

    def apply_map(
        self, map_: Map, *, unified_bounds: dict[str, list[int]] = {}
    ) -> None:
        """Use Multiplied Map object to apply mapping to matrix

        Parameters
        ----------
        map_ : Map
            Map object containing the generated row mapping

        bounds : dict[str: list[int]]
            Unified bounds for all arithmetic units

        Returns
        -------
        None

        """
        if not isinstance(map_, Map):
            raise TypeError(f"Expected Map, got {type(map_)}")
        if map_.bits != self.bits:
            raise ValueError(
                f"Map bitwidth {map_.bits} does not match matrix bitwidth {self.bits}"
            )

        # -- row-wise mapping ---------------------------------------

        if rmap := map_.rmap:
            for i in range(self.bits):
                # convert signed hex to 2s complement if -ve
                if rmap[i] == "00":
                    continue
                if (val := int(rmap[i], 16)) & 128:
                    val = (~val + 1) & 255  # 2s complement

                self.matrix[i - val], self.matrix[i] = (
                    self.matrix[i],
                    self.matrix[i - val],
                )

            return None

        # -- bounding box mapping -----------------------------------

        if unified_bounds:
            apply_complex_map(self.matrix, map_, unified_bounds)
            return None

        # -- bit-wise mapping ---------------------------------------
        # Expensive fallback
        for y in range(self.bits):
            for x in range(self.bits << 1):
                # convert signed hex to 2s complement if -ve
                if (val := int(map_.map[y][x], 16)) & 128:
                    val = (~val + 1) & 255  # 2s complement
                if val != 0:
                    self.matrix[y - val][x] = self.matrix[y][x]
                    self.matrix[y][x] = "_"

        return None

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __str__(self) -> str:
        return pretty(self.matrix)

    def __len__(self) -> int:
        return self.bits

    def __eq__(self, matrix: Any, /) -> bool:
        if not isinstance(matrix, Matrix):
            return False
        if matrix.bits != self.bits:
            return False
        for i in range(self.bits):
            if matrix.matrix[i] != self.matrix[i]:
                return False
        return True

    def __getitem__(self, index: int | slice) -> Slice:
        slice = self.matrix[index]
        return Slice(slice)

    def __iter__(self) -> Iterator[list[str]]:
        return iter(self.matrix)

    def __next__(self) -> list[str]:
        if self.index >= self.bits:
            raise StopIteration
        self.index += 1
        return self.matrix[self.index - 1]


# -- helper functions -----------------------------------------------


# ! DOCSTRING x3
def empty_rows(matrix: Matrix) -> int:
    """Return the number of empty rows in a matrix"""
    if not isinstance(matrix, Matrix):
        raise TypeError(f"Expected Matrix, got {type(matrix)}")

    empty_row = ["_" for i in range(matrix.bits * 2)]
    return sum([matrix.matrix[i] == empty_row for i in range(matrix.bits)])


def raw_empty_rows(matrix: list[list[str]]) -> int:
    """Return the number of empty rows in a raw matrix"""
    if not isppm(matrix):
        raise TypeError(f"Expected partial product matrix, got {matrix}")
    empty_row = ["_" for i in range(len(matrix[0]))]
    return sum([matrix[i] == empty_row for i in range(len(matrix))])


def raw_empty_row_pos(matrix: list[list[str]], row: int) -> list[int]:
    """Return positions of empty rows in a raw matrix"""
    if not isppm(matrix):
        raise TypeError(f"Expected partial product matrix, got {matrix}")
    empty_row = ["_" for i in range(len(matrix[0]))]
    pos = []
    for i in range(len(matrix)):
        if matrix[i] == empty_row:
            pos.append(i)
    return pos


def raw_empty_matrix(bits: int) -> list[list[str]]:
    """Build an empty partial product matrix for a given bitwidth

    Parameters
    ----------
    bits : int
        The bitwidth of the matrix

    Returns
    -------
    list[list[str]]
        An empty 2d array for the given bitwidth

    Notes
    -----
    An empty matrix is completely filled with underscores, following Multipied's convention

    Examples
    --------
    >>> raw_zero_matrix(4)
    [['_', '_', '_', '_', '_', '_', '_', '_'],
     ['_', '_', '_', '_', '_', '_', '_', '_'],
     ['_', '_', '_', '_', '_', '_', '_', '_'],
     ['_', '_', '_', '_', '_', '_', '_', '_']]



    """
    validate_bitwidth(bits)
    matrix = []
    for i in range(bits):
        matrix.append(["_"] * (bits * 2))
    return matrix


def raw_zero_matrix(bits: int) -> list[list[str]]:
    """Build a zero-filled partial product matrix for a given bitwidth

    Parameters
    ----------
    bits : int
        The bitwidth of the matrix

    Returns
    -------
    list[list[str]]
        A zero-filled 2d array for the given bitwidth

    Notes
    -----
    A zero matrix is filled with zeros on the diagonal and underscores elsewhere,
    following Multipied's convention

    Examples
    --------
    >>> raw_zero_matrix(4)
    [['_', '_', '_', '_', '0', '0', '0', '0'],
     ['_', '_', '_', '0', '0', '0', '0', '_'],
     ['_', '_', '0', '0', '0', '0', '_', '_'],
     ['_', '0', '0', '0', '0', '_', '_', '_']]

    """
    matrix = []
    zero = ["0"] * bits
    for i in range(bits):
        row = (["_"] * ((bits << 1) - bits - i)) + zero + (["_"] * i)
        matrix.append(row)
    return matrix


def aggregate_bounds(
    source: dict[str, Matrix], template_bounds: dict[str, list[tuple[int, int]]]
) -> dict[str, list[tuple[int, int]]]:
    """ """

    if not isinstance(source, dict):
        raise TypeError("source must be a dictionary")
    if not all(isinstance(matrix, Matrix) for matrix in source.values()):
        raise TypeError("all values in source must be Matrix instances")
    if not isinstance(template_bounds, dict):
        raise TypeError(f"Expected dict got {type(template_bounds)}")

    from itertools import pairwise

    for k, v in template_bounds.items():
        if k == "_":
            continue

    bounds = {}
    for ch, matrix in source.items():
        matrix_ = matrix.matrix
        if ch == "_":
            continue
        # print("ch:", ch)
        base_index = template_bounds[ch][0][1]
        # print("base index:", base_index)
        bounds[ch] = []
        for row in range(base_index, template_bounds[ch][-1][1] + 1):
            # -- entry border --------------------------------------

            if matrix_[row][0] != "_":
                bounds[ch].append((0, row))

            # -- central range --------------------------------------

            for i, pair in enumerate(pairwise(matrix_[row])):
                if pair == ("_", "_"):
                    continue

                if len(bounds[ch]) % 2 == 0:
                    bounds[ch].append((i + 1, row))
                    continue

                if len(bounds[ch]) % 2 == 1 and "_" in pair:
                    bounds[ch].append((i, row))
                    break

            # -- exit border ---------------------------------------

            if len(bounds[ch]) % 2 == 1:
                bounds[ch].append((len(matrix_[row]) - 1, row))

    return bounds


def _detect_merge_conflicts(
    bits: int,
    bounds: dict[str, list[tuple[int, int]]],
) -> dict[int, list[tuple[tuple[int, int], tuple[str, str]]]]:
    """Identify overlapping units in the given bounds.

    Complex `Templates` may contain overlapping units resulting in
    missing values in the matrix. This function detects overlapping
    values to be resolved once the merge is complete.

    Parameters
    ----------
    bits : int
        The number of bits in the target matrix.
    bounds : dict[str, list[tuple[int, int]]]
        A dictionary of bounds for each unit.

    Returns
    -------
    dict[str, list[tuple[int, int]]] | None
        A dictionary of conflicts, or None if no conflicts are found

    Notes
    -----
    Input bounds and output conflicts are in the form:
        {"<unit>": [(<start>, <end>), ...]}

    Where `(<start>, <end>)` are coordinate points in the matrix.
    """

    # Units can be merged in any order therefore both values which are
    # overlapping must be added as conflicts.

    # ! bounds are aggregated from reduced matrices.

    # Strategy:
    # > Testing for conflict
    #   > create an X-bit array for each row
    #   > iterate through aggregated bounds
    #       > assign a bound pair to given array index :: [y] = [(x0, x1), ...]
    #       > when a new pair is assigned to array test if bound pair
    #         lies within all present bound pairs in the array index.
    #
    #       [ non conflict ]
    #
    #           inbound_pair = (3, y), (7, y), unit = "B"
    #
    #         check inbound_pair conflicts:
    #           [y] = [(0, 2)] -> 2 < 3 and 7 < inf -> True -> no conflict
    #
    #       [ conflict ]
    #
    #           inbound_pair = (6, y), (15, y), unit = "C"
    #
    #         check inbound_pair conflicts:
    #
    #           [y] = [(0, 2), (3, 7)] -> 7 < 6 and 15 < inf -> False -> conflict
    #
    #       > if conflicts, take conflicting region and units present:
    #
    #           {"B": [(6, y), (7, y)], "C": [(6, y), (7, y)]}
    #

    validate_bitwidth(bits)
    from itertools import batched

    row_bounds = [[] for _ in range(bits)]
    row_units = [[] for _ in range(bits)]
    conflicts = {}

    # ! flaky code warning ! #
    # the following highly depends on coordinate bounds arriving
    # independent of which row. E.g. if bounds pair:
    #       (3, 0), (_, 0)
    # enter, the following is dependent that if any more bounds
    # exist for row 0, then the bounds pair
    #       (x < 3, 0), (_, 0)
    # will NEVER arrive and new bounds will be on the right of
    # the original bounds
    # ! sorting only solves half the problem ! #
    #
    # By grouping units into the conflicting bounds this problem
    # can *mostly* be resolved

    # -- collecting bounds ------------------------------------------
    # (start_x, end_x, unit)
    for unit, coords in bounds.items():
        for start, end in batched(coords, 2, strict=False):
            # print(start, end)
            if start[1] != end[1]:
                raise ValueError(f"Missing bound pair for row {start[1]}")

            row_bounds[start[1]].append((start[0], end[0], unit))
            row_units[start[1]].append(unit)

    # -- find + restrict conflict bounds ----------------------------
    # [(start_x, end_x, unit), ...] -> ((over, lap), (units, present))
    #
    # TODO : Overlap determines which unit's output to move to resolve conflict
    # CURR : just choose right most unit for simplicity
    for i, row in enumerate(row_bounds):
        last = (-1, -1)
        for pairs in pairwise(sorted(row, key=lambda x: x[0])):
            print(pairs)
            if len(pairs) == 1:
                continue
            curr_bound, next_bound = pairs
            if last[1] > curr_bound[1]:
                curr_bound = last

            if curr_bound[1] >= next_bound[0]:  # conflict
                # print(sorted(row, key=lambda x: x[0]))

                conflict_payload = (
                    (
                        max(curr_bound[0], next_bound[0]),
                        min(curr_bound[1], next_bound[1]),
                    ),
                    (curr_bound[-1], next_bound[-1]),
                )
                conflicts.setdefault(i, []).append(conflict_payload)
                last = curr_bound

    return conflicts


def matrix_merge(
    source: dict[str, Matrix],
    bounds: dict[str, list[tuple[int, int]]],
    *,
    complex: bool = False,
) -> Matrix:
    """Merge multiple matrices into a single matrix using pre calculated bounds

    Parameters
    ----------
    source : dict[str, Matrix]
        A dictionary of matrices to merge

    bounds : dict[str, list[tuple[int, int]]]
        A dictionary of bounds for each matrix

    complex : bool, optional, default: False
        Performs additional checks during merge

    Returns
    -------
    Matrix

    Examples
    --------
    >>> source = {'A': Matrix([[1, _], [3, _]]),
                  'B': Matrix([[_, 6], [_, 8]])}
    >>> bounds = {'A': [(0, 0), (0, 0), (1, 1), (1, 1)],
    >>>           'B': [(0, 1), (0, 1), (0, 1), (0, 1)]}
    >>> matrix_merge(source, bounds)
    Matrix([[1, 6], [4, 8]])

    """
    if not isinstance(source, dict):
        raise TypeError("Source must be a dictionary")
    if not all(isinstance(val, Matrix) for val in source.values()):
        raise TypeError("All values of source must be of type Matrix")
    if len(source) < 2:
        raise ValueError("Source must contain at least two matrices")
    if not (
        len(bounds) == len(source) or ("_" in source and len(bounds) == len(source) - 1)
    ):
        raise ValueError(
            "Source must contain the same number of matrices as bounds"
            f"\nSources: \n{list(source.keys())}"
            f"\nBounds: \n{list(bounds.keys())}"
        )

    litmus = next(i for i in source.values())
    bits = litmus.bits
    conflicts = {}

    if complex:  # set upon Template instantiation
        # == expensive conflict search ==============================
        # ((over, lap), (units, present)) : ((int, int), (str, str))
        conflicts = _detect_merge_conflicts(bits, bounds)
        print(conflicts)

    # -- lossy merge ------------------------------------------------
    output = raw_empty_matrix(bits)
    for unit, matrix in source.items():
        if unit == "_":
            continue
        for start, end in batched(bounds[unit], 2):
            if start[1] != end[1]:
                raise ValueError(f"Missing bound pair for row {start[1]}")
            y = start[1]
            for x in range(start[0], end[0] + 1):
                output[y][x] = matrix.matrix[y][x]

    if complex:
        # == cast missing values to columns =========================
        columns = [[] for _ in range(bits << 1)]
        for row, conflict_ in conflicts.items():
            for overlap, units in conflict_:
                start, end = overlap

                # -- determine which unit was overwritten -----------
                if (
                    source[units[0]].matrix[row][start : end + 1]
                    == output[row][start : end + 1]
                ):
                    # units[1] was overwritten
                    for i in range(start, end + 1):
                        columns[i].append((source[units[1]].matrix[row][i], units[1]))
                else:
                    # units[0] was overwritten
                    for i in range(start, end + 1):
                        columns[i].append((source[units[0]].matrix[row][i], units[0]))

        print(columns)

        # == insert missing values ==================================
        for x, recovered_bits in enumerate(columns):
            for bit_info in recovered_bits:
                # highest y index of original bound
                base_index = bounds[bit_info[1]][0][1]

                # cycle column until empty slot found
                for y in range(bits):
                    if output[(y + base_index) % bits][x] == "_":
                        output[(y + base_index) % bits][x] = bit_info[0]
                        break

    return Matrix(output)


def matrix_scatter(
    source: list[list], bounds: dict[str, list[tuple[int, int]]], fmt: str = "auto"
) -> dict[str, list[list]]:
    """Cast matrix subsets to initialised matrix. Each subset based on provided bounds.

    Parameters
    ----------
    source : list[list]
        Partial Product matrix to scatter.

    bounds : dict[str, list[tuple[int, int]]]
        The bounds for each unit to extract from the source.

    fmt : str, optional, default: "auto".
        "auto" : Infer format from source.
        "empty" : :func:`raw_empty_matrix`
        "zero" : :func:`raw_zero_matrix`
        "map" : :func:`raw_map_matrix`

    Returns
    -------
    dict[str, list[list]]
        A dictionary of matrices containing the subset of source based on the provided bounds.

    Notes
    -----
    Each unit is extracted and placed at the same position within an initialised matrix
    with the same shape as the source.

    See also
    --------
    :func:`collect_template_units` for bound extraction

    Examples
    --------
    >>> source = [[0, 1, 2],
    >>>           [3, 4, 5],
    >>>           [6, 7, 8]]
    >>> bounds = {"A": [(0, 0), (0, 1)],
    >>>           "B": [(1, 1), (1, 2)]}
    >>> matrix_scatter(source, bounds, fmt=empty)
    [[[0, 1, _],
      [_, _, _],
      [_, _, _]],
     [[_, _, _],
      [_, 4, 5],
      [_, _, _]]]

    """

    if isinstance(bounds, dict):
        if not all([ischar(k) for k in bounds.keys()]):
            raise ValueError("Unrecognised Bounds")
    else:
        raise TypeError(f"Expected Dict got {type(bounds)}")

    if not isinstance(source, list) and not all(
        [isinstance(row, list) for row in source]
    ):
        raise TypeError(f"Expected List[List] got {type(source)}")

    if fmt == "auto":
        _litmus = source[0][0]
        if ischar(_litmus) or (isint(_litmus) and (_litmus == "0" or _litmus == "1")):
            fmt = "empty"
        elif ishex2(_litmus):
            fmt = "map"
        else:
            fmt = "zero"

    match fmt:
        case "empty":
            dest_matrix = [["_" for _ in row] for row in source]
        case "zero":
            dest_matrix = [["0" for _ in row] for row in source]
        case "map":
            dest_matrix = [["00" for _ in row] for row in source]
        case _:
            raise ValueError(f"Unrecognised fmt: {fmt}")

    allchars = list(bounds.keys())

    output = {}
    for ch in allchars:
        if len(bounds[ch]) % 2 != 0:
            raise ValueError(f"Odd number of bounds for {ch}")

        dest_matrix_copy = deepcopy(dest_matrix)

        i = 0
        while i < len(bounds[ch]):
            if bounds[ch][i][1] != bounds[ch][i + 1][1]:
                _start = bounds[ch][i]
                _end = bounds[ch][i + 1]
                raise ValueError(
                    f"Bounding box error for unit '{ch}' "
                    f"Points:{_start}, {_end}, error:  {_start[1]} != {_end[1]}"
                )
            start = bounds[ch][i][0]
            end = bounds[ch][i + 1][0]
            row = bounds[ch][i][1]

            for col in range(start, end + 1):  # include end
                dest_matrix_copy[row][col] = source[row][col]

            i += 2

        output[ch] = dest_matrix_copy

    return output
