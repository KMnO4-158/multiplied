################################################
# Classes to Represent And Manage Nested Lists #
################################################

from copy import deepcopy
import multiplied as mp
from typing import Any, Iterator


# ! Review slices and their integration to the wider library
#
# IDEAS:
# - work exclusively with multiplied objects
# - Slice also slices metadata from source object
class Slice:
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

        mp.validate_bitwidth(self.bits)
        self.slice = matrix if isinstance(matrix[0], list) else [matrix]
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
        return str(mp.pretty(self.slice))

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
class Matrix:
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
        # x_checksum=[], # Add handling if supplied
        # y_checksum=[], # Add handling if supplied
    ) -> None:
        # -- sanity check -------------------------------------------
        if isinstance(source, int):
            self.bits = source
            mp.validate_bitwidth(self.bits)
            self.__build_matrix(a, b)
            return
        elif isinstance(source, (list, Slice)) and isinstance(source[0], list):
            self.bits = len(source)
            mp.validate_bitwidth(self.bits)
        else:
            raise TypeError(f"Expected integer or nested list, got {type(source)}")

        self.matrix = source

        # -- process custom matrix ----------------------------------
        # row_len  = self.bits << 1
        # x_checksum = [0] * row_len
        # y_checksum = [0] * self.bits
        # # ! needs refactor
        # for i, row in enumerate(source):
        #     if not isinstance(row, (list, Slice)):
        #         raise ValueError("Invalid input. Expected list or slice.")
        #     if row_len != len(row):
        #         raise ValueError("Inconsistent rows. Matrix must be 2m * m")
        #     ch = 0
        #     while ch < row_len:
        #         if ch == row_len or row[ch] == '0' or row[ch] == '1':
        #             for x in range(ch, row_len):
        #                 if row[x] == '_':
        #                     break
        #                 x_checksum[x] = 1
        #             y_checksum[i]
        #             break
        #         else:
        #             ch += 1

        # self.x_checksum = x_checksum
        # self.y_checksum = y_checksum
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

        mp.validate_bitwidth((bits := self.bits))
        if (operand_a > ((2**bits) - 1)) or (operand_b > ((2**bits) - 1)):
            raise ValueError("Operand bit width exceeds matrix bit width")

        # -- catch multiply by zero ---------------------------------
        if operand_a == 0 or operand_b == 0:
            self.__zero_matrix(bits)
            # self.y_checksum = [0]*bits
            # self.x_checksum = [0]*(bits*2)
            return None

        # -- generate -----------------------------------------------
        # convert to binary, removing '0b' and padding with zeros
        a = bin(operand_a)[2:].zfill(bits)
        b = bin(operand_b)[2:].zfill(bits)
        # y_checksum = [0]*bits
        # x_checksum = [0]*(bits*2)
        matrix = []
        for i in range(bits - 1, -1, -1):
            if b[i] == "0":
                matrix.append(["_"] * (i + 1) + ["0"] * (bits) + ["_"] * (bits - i - 1))
            elif b[i] == "1":
                matrix.append(["_"] * (i + 1) + list(a) + ["_"] * (bits - i - 1))
                # y_checksum[i] = 1
                # for j, bit in enumerate(list(a)):
                # x_checksum[i+j] = 1

        self.matrix = matrix
        # self.y_checksum = y_checksum
        # self.x_checksum = x_checksum
        return None

    def __checksum(self) -> None:
        """Calculate checksums for rows and columns of the matrix"""

        row_len = self.bits << 1
        y_checksum = [0] * self.bits
        x_checksum = [0] * row_len
        for i, row in enumerate(self.matrix):
            if len(row) != row_len:
                raise ValueError("Inconsistent row length")

            ch = 0
            while ch < row_len:
                if row[ch] == "0" or row[ch] == "1":
                    y_checksum[ch] = 1
                    for x in range(ch, row_len):
                        if row[x] == "_":
                            break
                        x_checksum[x] = 1
                    break
                else:
                    ch += 1

        self.x_checksum = x_checksum
        self.y_checksum = y_checksum
        return None

    def resolve_rmap(self, *, ignore_zeros: bool = True) -> mp.Map:
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
        return mp.Map(rmap)

    # ! Update to use checksums  or coordinates
    def apply_map(self, map_: mp.Map) -> None:
        """Use Multiplied Map object to apply mapping to matrix

        Parameters
        ----------
        map_ : Map
            Map object containing the generated row mapping

        Returns
        -------
        None

        """
        if not isinstance(map_, mp.Map):
            raise TypeError(f"Expected Map, got {type(map_)}")
        if map_.bits != self.bits:
            raise ValueError(
                f"Map bitwidth {map_.bits} does not match matrix bitwidth {self.bits}"
            )

        # -- row-wise mapping ---------------------------------------

        if rmap := map_.rmap:
            # matrix = deepcopy(self.matrix) # TODO make this modify in-place
            for i in range(self.bits):
                # convert signed hex to 2s complement if -ve
                if (val := int(rmap[i], 16)) & 128:
                    val = (~val + 1) & 255  # 2s complement
                # matrix[i]     = ["_"] * (self.bits*2)
                self.matrix[i - val], self.matrix[i] = (
                    self.matrix[i],
                    self.matrix[i - val],
                )

                # deprecate checksum in favor of coordinates
                # self.y_checksum[i]     = 0
                # self.y_checksum[i-val] = 1
            # self.matrix = matrix

            return None

        # -- bit-wise mapping ---------------------------------------
        # TODO Update to use coordinates -- way too expensive currently
        for y in range(self.bits):
            for x in range(self.bits << 1):
                # convert signed hex to 2s complement if -ve
                if (val := int(map_.map[y][x], 16)) & 128:
                    val = (~val + 1) & 255  # 2s complement
                if val != 0:
                    self.matrix[y - val][x] = self.matrix[y][x]
                    self.matrix[y][x] = "_"

        self.checksum = [0] * self.bits
        return None

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __str__(self) -> str:
        return mp.pretty(self.matrix)

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


def empty_rows(matrix: Matrix) -> int:
    """Return the number of empty rows in a matrix"""
    if not isinstance(matrix, Matrix):
        raise TypeError(f"Expected Matrix, got {type(matrix)}")

    empty_row = ["_" for i in range(matrix.bits * 2)]
    return sum([matrix.matrix[i] == empty_row for i in range(matrix.bits)])


def raw_empty_matrix(bits: int) -> list[list[str]]:
    """Build an empty 2d array for a given bitwidth

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

    """
    mp.validate_bitwidth(bits)
    matrix = []
    for i in range(bits):
        matrix.append(["_"] * (bits * 2))
    return matrix


def raw_zero_matrix(bits: int) -> list[list[str]]:
    """Build a zero-filled 2d array for a given bitwidth

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

    """
    matrix = []
    zero = ["0"] * bits
    for i in range(bits):
        row = (["_"] * ((bits << 1) - bits - i)) + zero + (["_"] * i)
        matrix.append(row)
    return matrix


# TODO: update example
def matrix_merge(
    source: dict[str, Matrix],
    bounds: dict[str, list[tuple[int, int]]],
    *,
    carry: bool = True,
) -> Matrix:
    """Merge multiple matrices into a single matrix using pre calculated bounds

    Parameters
    ----------
    source : dict[str, Matrix]
        A dictionary of matrices to merge

    bounds : dict[str, list[tuple[int, int]]]
        A dictionary of bounds for each matrix

    carry : bool=True, optional, default: True
        Whether to carry over the carry bit

    Returns
    -------
    Matrix

    Examples
    --------
    >>> source = {'A': Matrix([[1, _], [3, _]]), 'B': Matrix([[_, 6], [_, 8]])}
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
    if len(bounds) != len(source):
        # new error message needed
        raise ValueError("Source must contain the same number of matrices as bounds")

    bits = list(source.values())[0].bits
    output = raw_empty_matrix(bits)
    for unit, matrix in source.items():
        if bounds[unit] == "_":
            continue

        # new bounding box covering whole result
        box_left = min(i[0] for i in bounds[unit])
        box_right = max(i[0] for i in bounds[unit])
        i = 0
        while i < len(bounds[unit]) - 1:
            # ..., left coord : right coord, ...
            left, right = bounds[unit][i], bounds[unit][i + 1]
            if (y := left[1]) != right[1]:
                raise ValueError(f"Missing bound pair for row {y}")
            for j in range(box_left, box_right + 1):
                output[y][j] = matrix.matrix[y][j]

            i += 2
    return Matrix(output)


def matrix_scatter(
    source: list[list],
    bounds: dict[str, list[tuple[int, int]]],
    fmt: str="auto"
) -> dict[str, list[list]]:
    """Return list of matrices containing subset of source matrix based on provided bounds.

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
    [[[0, 1, _], [_, _, _], [_, _, _]],
     [[_, _, _], [_, 4, 5], [_, _, _]]]

    """

    if isinstance(bounds, dict):
        if not all([mp.ischar(k) for k in bounds.keys()]):
            raise ValueError("Unrecognised Bounds")
    else:
        raise TypeError(f"Expected Dict got {type(bounds)}")

    if not isinstance(source, list) and not all([isinstance(row, list) for row in source]):
        raise TypeError(f"Expected List[List] got {type(source)}")

    if fmt == "auto":
        _litmus = source[0][0]
        if mp.ischar(_litmus) or (mp.isint(_litmus) and (_litmus == "0" or _litmus == "1")):
            fmt = "empty"
        elif mp.ishex2(_litmus):
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

            for col in range(start, end + 1): # include end
                dest_matrix_copy[row][col] = source[row][col]

            i += 2

        output[ch] = dest_matrix_copy

    return output
