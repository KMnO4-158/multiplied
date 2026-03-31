################################################
# Returns Template Objects Using User Patterns #
################################################

from copy import deepcopy
from typing import Any


from .dtypes.base import MultipliedMeta
from .matrix import (
    Matrix,
    Slice,
    empty_rows,
    matrix_merge,
    matrix_scatter,
    raw_empty_matrix,
)
from .utils.char import allchars, chargen, chartff
from .utils.pretty import pretty, pretty_nested_list
from .utils.bool import isalpha, ischar, isppm, validate_bitwidth

# == Template and Slice dependencies  =============================== #


def build_csa(
    char: str, source_slice: Slice
) -> tuple[Slice, Slice]:  # Carry Save Adder -> (template, result)
    """Create CSA template slice with source slice and chosen char.

    Parameters
    ----------
    char : str
        Character to use for the CSA template.
    source_slice : Slice
        Source slice object to use for the CSA template.

    Returns
    -------
    tuple[Slice, Slice]
        Template "slices" marked for a csa reduction and the resulting slice.

    Examples
    --------
    >>> [slice-] || [csa---] || [result]
    >>> ____0000 || ____AaAa || __AaAaAa
    >>> ___0000_ || ___aAaA_ || __aAaA__
    >>> __0000__ || __AaAa__ || ________
    """
    if not ischar(char):
        raise ValueError("Expected character. String length must equal 1")
    if not isinstance(source_slice, Slice):
        raise TypeError(f"Expected type Slice, got {type(source_slice)}")
    if len(source_slice) != 3:
        raise ValueError("Invalid template slice: must be 3 rows")

    # loop setup
    n = len(source_slice[0])
    tff = chartff(char)  # Toggle flip flop
    result = [["_"] * n, ["_"] * n, ["_"] * n]
    csa_slice = deepcopy(source_slice)

    for i in range(n):
        # Generates slice of all possible bit placements, represented
        # with a char. Lower and upper case aide in visualising changes
        # in bit position before, templates, and after, result, operation

        char = next(tff)
        csa_slice[0][i] = char if (y0 := csa_slice[0][i] != "_") else "_"
        csa_slice[1][i] = char if (y1 := csa_slice[1][i] != "_") else "_"
        csa_slice[2][i] = char if (y2 := csa_slice[2][i] != "_") else "_"

        result[0][i] = char if 1 <= (y0 + y1 + y2) else "_"
        result[1][i - 1] = char if 1 < (y0 + y1 + y2) else "_"
    return csa_slice, Slice(result)


def build_adder(
    char: str, source_slice: Slice
) -> tuple[Slice, Slice]:  # Carry Save Adder -> (template, result)
    """Create Adder template slice with zero initialised slice and chosen char.

    Parameters
    ----------
    char : str
        The character to use for the template.
    source_slice : Slice
        The source slice to use for the template.

    Returns
    -------
    tuple[Slice, Slice]
        The template "slices" for addition and the resulting slice.

    Examples
    --------
    >>> [slice-] || [adder-] || [result]
    >>> ___0000_ || ___aAaA_ || _aAaAaA_
    >>> __0000__ || __AaAa__ || ________
    """
    if not ischar(char):
        raise ValueError("Expected character. String length must equal 1")
    if not isinstance(source_slice, Slice):
        raise TypeError(f"Expected type Slice, got {type(source_slice)}")
    if len(source_slice) != 2:
        raise ValueError("Invalid template slice: must be 2 rows")

    # loop setup
    n = len(source_slice[0])
    tff = chartff(char)  # Toggle flip flop
    result = [["_"] * n, ["_"] * n]
    adder_slice = deepcopy(source_slice)  # ensure no references

    for i in range(n):
        # Generates slice of all possible bit placements, represented
        # with a char. Alternating char case aids in visualising changes
        # in bit position before, templates, and after, result, operation

        char = next(tff)
        adder_slice[0][i] = char if (y0 := adder_slice[0][i] != "_") else "_"
        adder_slice[1][i] = char if (y1 := adder_slice[1][i] != "_") else "_"
        result[0][i] = char if y0 or y1 else "_"

    # -- Add final carry -----------------------------------------
    carry = not all(ch == "_" for ch in adder_slice[1])  # sanity check

    # find index of left most instance of char, regardless of case
    index = 0
    while index < n:
        if result[0][index] in [next(tff), next(tff)]:
            break
        index += 1
    # index = min(result[0].index(next(tff)), result[0].index(next(tff)))
    if carry and 0 < index:
        result[0][index - 1] = next(tff)  # Final carry place in result template

    return adder_slice, Slice(result)


def build_noop(char: str, source_slice: Slice) -> tuple[Slice, Slice]:
    """Create a No-op template slice with zero initialised slice and chosen char.

    Parameters
    ----------
    char : str
        Character to use for the No-op template.
    source_slice : Slice
        Source slice to use for the No-op template.


    Returns
    -------
    tuple[Slice, Slice]
        Template "slices" and resulting slice. Target row unaffected

    Examples
    --------
    >>> [slice-] || [noop--] || [result]
    >>> ___0000_ || ___aAaA_ || ___aAaA_
    """
    if not ischar(char):
        raise ValueError("Expected character. String length must equal 1")
    if not isinstance(source_slice, Slice):
        raise TypeError(f"Expected type Slice, got {type(source_slice)}")
    if len(source_slice) != 1:
        raise ValueError("Invalid template slice: must be 1 rows")

    n = len(source_slice[0])
    tff = chartff(char)  # Toggle flip flop
    noop_slice = deepcopy(source_slice)  # ensure no references
    for i in range(n):
        noop_slice[0][i] = next(tff) if (noop_slice[0][i] != "_") else "_"

    return noop_slice, deepcopy(noop_slice)  # avoids pointing to same object


def build_empty_slice(source_slice: Slice) -> tuple[Slice, Slice]:
    """Create an empty template slice. Returns template "slices" and resulting slice.
    Variable length, determined by source slice.

    Parameters
    ----------
    source_slice : Slice
        Source slice to use for the empty template.

    Returns
    -------
    tuple[Slice, Slice]
        Tuple of template slices and resulting slice.


    Notes
    -----
    Used for building Templates with large runs of underscore characters.
    Underscores are used to represent empty spaces in the template.

    Examples
    --------
    >>> [slice-] || [empty-] || [result]
    >>> ???????? || ________ || ________
    >>> ???????? || ________ || ________
    >>> ...      || ...      || ...
    """

    if not isinstance(source_slice, Slice):
        raise TypeError(f"Expected type Slice, got {type(source_slice)}")

    empty_slice = deepcopy(source_slice)  # ensure no references
    for row in range(len(source_slice)):
        empty_slice.slice[row] = ["_"] * (empty_slice.bits << 1)
    return empty_slice, deepcopy(empty_slice)


# =================================================================== #


class Pattern(MultipliedMeta):
    """Simplified representation of a Template.

    Parameters
    ----------
    pattern : list[str]
        Pattern to use for the template.

    Attributes
    ----------
    pattern : list[str]
        Pattern to use for the template.
    bits : int
        Number of bits in the pattern.

    """

    def __init__(self, pattern: list[str]) -> None:
        if not (isinstance(pattern, list) and all(ischar(row) for row in pattern)):
            raise ValueError("Invalid pattern format. Expected list[char]")
        self.pattern = pattern
        self.bits = len(pattern)

        self._soft_type = list()
        return None

    def get_runs(self) -> list[tuple[int, int, int]]:
        """Returns list of tuples of length, position, and run of a given char in pattern

        Examples
        --------
        >>> Pattern(["A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "C", "C"]).get_runs()
        [(3, 0, 3), (4, 3, 4), (5, 7, 5)]
        """
        metadata = []
        i = 1
        k = 0
        while i < len(self.pattern):
            run = 1
            while i < len(self.pattern) and self.pattern[i - 1] == self.pattern[i]:
                run += 1
                i += 1
            if run < 4:
                # (arithmetic_unit, starting_row, run_length)
                metadata.append((None, i - run, run))
            else:
                # TODO: Implement Decoders
                # arithmetic_unit = decoder
                # find decoder type
                raise ValueError(f"Unsupported run length {run}")
            i += 1
            k += 1
        return metadata

    def __str__(self) -> str:
        pretty_ = ""
        for p in self.pattern:
            pretty_ += " " + p + "\n"
        return f"{'[' + pretty_[1:-1] + ']'}"

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __len__(self) -> int:
        return self.bits

    def __getitem__(self, index: int) -> str:
        return self.pattern[index]


# -- ! [ Preparing For Decoders ] !---------------------------------- #
# > Make plan for assigning a function to a given unit even if
#   they're the same run
#
# > What character will they use?
#
# > How can this decoder function be preserved, assigned and called
#   upon during template reduction AND matrix reduction?
#
# -- ! [ conflict data ] ! ------------------------------------------ #
# TODO:
# Like bounds and re_bounds, conflicts should be stored inside
# Templates as a single source of truth instead of recalculation
class Template(MultipliedMeta):
    """A structure representing collections of arithmetic units using characters.
    Generated using a partial product matrix and a Pattern or custom template

    Parameters
    ----------
    source : Pattern | list[list[str]]
        The source of the template.
    result : list[Any], optional
        The result of the template, by default [], automatically computed
    matrix : Any, optional
        The matrix of the template, by default None

    """

    def __init__(
        self,
        source: Pattern | list[list[str]],
        *,
        result: list[Any] | Matrix | None = None,
        matrix: Any = None,
    ) -> None:

        validate_bitwidth(len(source))
        self._soft_type = list()
        self.bits = len(source)
        match result:
            case Matrix():
                self.result = result
            case list():
                if allchars(result) == {} or not isppm(result):
                    raise ValueError("Invalid resultant matrix")

                self.result = Matrix(result)
            case None:
                pass
            case _:
                raise TypeError("result must be a Matrix or list[list[str]]")

        # -- pattern handling ---------------------------------------
        if isinstance(source, Pattern):
            self.pattern = source
            if matrix is None:
                matrix = Matrix(self.bits)
            self.build_from_pattern(self.pattern, matrix)
            self._complex = False
            self.conflicts = {}

        # -- template handling ---------------------------------------
        elif isinstance(source, list):
            if not isppm(source):
                raise TypeError(f"Expected partial product matrix, got {source}")
            self.template = source
            self.bounds = self.update_bounding_box(self.template)
            self._complex = True
            self.pattern = None
            self.conflicts = {}
            if result is None:
                self._reduce_template()
            else:
                self.re_bounds = self.update_bounding_box(self.result.matrix)

            # if pattern resolvable, future calculations are cheaper
            self._resolve_template_pattern()
            if self.pattern is not None:
                self._complex = False

        else:
            raise TypeError(f"Expected Pattern or list[list[str]] got {source}")

        return None

    def _resolve_template_pattern(self) -> None:
        """Attempt to resolve pattern from template source"""

        pattern = ["_"] * self.bits
        for i in range(self.bits):
            chars = set(deepcopy(self.template[i]))
            chars = {ch.upper() for ch in chars}
            if 2 < len(chars):
                self.pattern = None
                return None

            for char in chars:
                if char != "_":
                    pattern[i] = char

        self.pattern = Pattern(pattern)
        return None

    def _reduce_template(self) -> None:
        """Produce Template result and it's bounding box."""
        units, bounds = self._collect_template_units()
        re_bound = {}
        results = {}
        chars = list(bounds.keys())
        for ch in chars:
            base_index = bounds[ch][0][1]
            if ch == "_":
                results[ch] = Matrix(units["_"])
                re_bound[ch] = bounds[ch]
                continue

            match bounds[ch][-1][1] - bounds[ch][0][1] + 1:  # row height
                case 1:  # NOOP
                    output = Slice([units[ch][base_index]])
                    re_bound[ch] = bounds[ch]

                case 2:  # ADD
                    unit_slice = Slice(
                        [units[ch][base_index], units[ch][base_index + 1]]
                    )
                    output = build_adder(ch, unit_slice)[1]

                    y = bounds[ch][0][1]
                    x_right = bounds[ch][1][0]
                    x_left = bounds[ch][0][0]
                    while output[0][x_left] != "_" and -1 < x_left:
                        x_left -= 1

                    re_bound[ch] = [(x_left + 1, y), (x_right, y)]

                case 3:  # CSA
                    unit_slice = Slice(
                        [
                            units[ch][base_index],
                            units[ch][base_index + 1],
                            units[ch][base_index + 2],
                        ]
                    )
                    output = build_csa(ch, unit_slice)[1]

                    y = bounds[ch][0][1]
                    x_right = bounds[ch][1][0]
                    x_left = bounds[ch][-2][0]
                    while output[0][x_left] != "_" and 0 < x_left:
                        x_left -= 1

                    re_bound[ch] = [
                        (x_left + 1, y),
                        (x_right, y),
                        (x_left, y + 1),
                        (x_right - 1, y + 1),
                    ]

                case _:
                    raise ValueError(
                        f"Unsupported unit type, len={bounds[ch][-1][1] - bounds[ch][0][1] + 1}"
                        f"\nUnit: \n{pretty_nested_list(units[ch])}"
                    )
            unit_result = [[] for _ in range(self.bits)]
            i = 0
            while i < base_index:
                unit_result[i] = ["_"] * (self.bits << 1)
                i += 1
            for row in output:
                # print(row)
                unit_result[i] = row
                i += 1
            while i < self.bits:
                unit_result[i] = ["_"] * (self.bits << 1)
                i += 1
            # mprint(unit_result)
            results[ch] = Matrix(unit_result)

        # ! -- implement merge conflict resolution ------------------ ! #
        if 1 < len(results):
            # print("====merging====")
            # print(re_bound)
            self.result, self.conflicts = matrix_merge(
                results, re_bound, complex=self._complex
            )
            # print(re_bound)
            # print("====merging/ended====")
        else:
            self.result = list(results.values())[0]

        self.re_bounds = re_bound
        # ! --------------------------------------------------------- ! #
        return None

    # Templates must be built using matrix
    def build_from_pattern(self, pattern: Pattern, matrix: Matrix) -> None:
        """Build a simple template and it's result for a given bitwidth based
        on matrix. Defaults to empty matrix if matrix=None.

        Parameters
        ----------
        pattern : Pattern
            The pattern to build the template from.
        matrix : Matrix
            The matrix to build the template from.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the pattern is not a valid Pattern object.

        Examples
        --------
        >>> [matrix] || [pattern] || [templ.] [result]
        >>> ____0000 || [  'a',   || ____AaAa __aAaAaA
        >>> ___0000_ ||    'a',   || ___AaAa_ ________
        >>> __0000__ ||    'b',   || __BbBb__ bBbBbB__
        >>> _0000___ ||    'b'  ] || _BbBb___ ________
        """

        # -- sanity check -------------------------------------------
        if not (isinstance(pattern, Pattern)):
            raise ValueError("Expected Pattern")
        validate_bitwidth(len(pattern))

        # -- find run -----------------------------------------------
        template_slices = {}
        char = chargen()
        i = 1
        while i < len(pattern) + 1:
            run = 1

            while i < len(pattern) and pattern[i - 1] == pattern[i]:
                run += 1
                i += 1

            # -- process noop run -----------------------------------
            if pattern[i - run] == "_":
                allchar = set(pattern.pattern)
                for r in range(1, run + 1):
                    ch = next(char)
                    max_iter = 26

                    while ch.lower() in allchar:
                        if max_iter == 0:
                            raise ValueError("No available characters for template")
                        ch = next(char)
                        max_iter -= 1

                    template_slices[i - r] = build_noop(ch, matrix[i - r])
                    allchar.add(ch)

                i += run  # advance past noop run
                continue

            # -- process arithmetic units ---------------------------
            match run:
                case 1:  # Do nothing
                    template_slices[i - run] = build_noop(
                        pattern[i - run], matrix[i - run : i]
                    )
                case 2:  # Create adder
                    template_slices[i - run] = build_adder(
                        pattern[i - run], matrix[i - run : i]
                    )
                case 3:  # Create CSA row
                    template_slices[i - run] = build_csa(
                        pattern[i - run], matrix[i - run : i]
                    )
                case _:
                    raise ValueError(
                        f"Unsupported run length {run}. Use '_' for empty rows"
                    )

            i += 1

        # for x in template_slices.values():
        #     print(x)
        # -- build template and result ------------------------------
        keys = sorted(template_slices.keys())
        template = []
        result = []
        for k in keys:
            template += template_slices[k][0]
            result += template_slices[k][1]

        self.template, self.result = template, Matrix(result)
        _, self.bounds = self._collect_template_units()
        self.re_bounds = self.update_bounding_box(self.result.matrix)
        return None

    # ! currently not generalised:
    #  > detect type of transition then use appropriate function
    #
    #  > or just detect empty, '_', characters as the boundary
    #       > This option means figuring out the correct key to use
    def update_bounding_box(
        self, matrix: list[list[str]]
    ) -> dict[str, list[tuple[int, int]]]:
        """Returns dictionary of arithmetic unit and coordinates for their boundaries.

        No rigorous inter-row or intra-row boundary checking.

        Notes
        -----
        Bounds are in the form:
            {"<unit>": [(<start>, <end>), ...]}

        Where `(<start>, <end>)` are coordinate points in the matrix.
        """

        rows = self.bits
        items = self.bits << 1
        bounds = {}
        x, y = 0, 0
        while y < rows:
            # -- entry border -------------------------------------------
            key = matrix[y][0].upper()
            if key not in bounds:
                bounds[key] = []
            bounds[key].append((0, y))

            # -- central range ------------------------------------------
            while x < items - 1:
                curr = matrix[y][x].upper()
                next = matrix[y][x + 1].upper()
                if (curr == next) and isalpha(curr):
                    x += 1
                    continue
                if curr != next and (isalpha(curr) or isalpha(next)):
                    if curr not in bounds:
                        bounds[curr] = []
                    bounds[curr].append((x, y))
                    if next not in bounds:
                        bounds[next] = []
                    bounds[next].append((x + 1, y))
                    x += 1
                    continue
                x += 1

            # -- exit border --------------------------------------------
            key = matrix[y][x].upper()
            if key not in bounds:
                bounds[key] = []
            bounds[key].append((x, y))

            x = 0
            y += 1
        return bounds

    def _collect_template_units(
        self,
    ) -> tuple[dict[str, list[list[str]]], dict[str, list[tuple[int, int]]]]:
        """Return dict of isolated arithmetic units and their bounding box.

        Performs a rigorous inter-row and intra-row boundary check to ensure
        each arithmetic units are valid.

        Return
        ------
        units : dict[str, list[list[str]]]
            Dictionary of isolated arithmetic units.
        bounds : dict[str, list[tuple[int, int]]]
            Dictionary of arithmetic unit and coordinates for their boundaries.

        Notes
        -----
        Bounds are in the form:
            {"<unit>": [(<start>, <end>), ...]}

        Where `(<start>, <end>)` are coordinate points in the matrix.
        """

        from .utils.char import chartff

        bounds = self.update_bounding_box(self.template)
        allchars = list(bounds.keys())
        units = {}

        # -- find and collect units ---------------------------------
        for ch in allchars:
            if ch == "_":  # isolate non-unit area
                # extract only empty, "_", bounding box to Matrix
                units[ch] = matrix_scatter(self.template, {"_": bounds["_"]})["_"]
                continue
            matrix = raw_empty_matrix(self.bits)
            tff = chartff(ch)  # toggle flip flop
            next(tff)  # sync to template case sensitivity
            i = 0  # coordinate index
            expected_y = None
            while i < len(bounds[ch]) - 1:
                # == intra-row boundary ================================= #
                # bound[list_of_points][coord_i][y-axis]
                # "if 2 < points have the same y for a given unit"
                if 2 < sum([p[1] == bounds[ch][i][1] for p in bounds[ch]]):
                    raise ValueError(
                        f"Multiple arithmetic units found for unit '{ch}' \n{bounds}"
                    )
                # ======================================================= #
                start = bounds[ch][i]
                end = bounds[ch][i + 1]
                if start[1] != end[1]:
                    raise ValueError(
                        f"Bounding box error for unit '{ch}' "
                        f"Points:{start}, {end}, error:  {start[1]} != {end[1]}"
                    )
                # -- traverse row -----------------------------------
                next(tff)  # sync to template case sensitivity
                for x in range(start[0], end[0] + 1):
                    matrix[start[1]][x] = next(tff)

                # == inter-row boundary test ============================ #
                if expected_y is not None and expected_y != start[1]:
                    raise ValueError(
                        f"Arithmetic unit '{ch}' spans multiple rows. "
                        f"Expected row {expected_y}, got row {start[1]}"
                    )
                expected_y = start[1] + 1
                # ======================================================= #

                i += 2

            units[ch] = matrix

        # -- isolate empty area -------------------------------------
        # strat:
        # > copy input template -> empty
        # > traverse empty using bounds
        #   > overlay empty chars over existing bound regions
        #   > aggregate bounds of empty region
        # ---
        # > Empty region optimisations
        # > start with bounds for each edge assuming full span:
        #   > aka: (0, <y>), (bits << 1, <y>) for all y's / bits
        # > find total span of units in a given row
        # >

        # unified = unify_bounds(bounds)
        # for i in range(self.bits):

        return (units, bounds)

    def __str__(self) -> str:

        # ! figure out why ``pretty(self.result)`` prints twice
        return f"{pretty(self.template)}\n{pretty(self.result.matrix)}"

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __len__(self) -> int:
        return len(self.template)


# TODO: add examples
def resolve_pattern(matrix: Matrix) -> Pattern:
    """For a given matrix, progressively allocate CSAs then adders to pattern

    Parameters
    ----------
    matrix : Matrix
        The matrix to resolve the pattern for.

    Returns
    -------
    Pattern
        The resolved pattern.

    """

    from multiplied.core.utils.char import chargen

    char = chargen()
    if (empty_rows_ := empty_rows(matrix)) == matrix.bits:
        return Pattern(["_"] * matrix.bits)

    # TODO use io.StringIO()
    scope = matrix.bits - empty_rows_
    new_pattern = []
    while 0 < scope:
        ch = next(char)
        n = len(new_pattern)

        if 3 <= scope:
            new_pattern += [ch, ch, ch]
        elif 2 == scope:
            new_pattern += [ch, ch]
        elif 1 == scope:
            new_pattern += [ch]

        scope -= len(new_pattern) - n
    new_pattern += ["_"] * empty_rows_
    return Pattern(new_pattern)


"""
Decoders
--------

Complex templates will eventually allow for decoders.

Decoders can reduce 4 or more bits at a time, or be used to implement
other encoding/decoding style operations.


"""
