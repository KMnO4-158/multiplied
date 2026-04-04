###########################################
# Algorithm Defined By Templates and Maps #
###########################################

from copy import deepcopy
from itertools import batched
from typing import Any, Iterable
from .dtypes.base import MultipliedMeta
from .map import Map, raw_zero_map, unify_bounds
from .matrix import Matrix, empty_rows, get_unified_bounds, matrix_merge, matrix_scatter, raw_dadda_matrix, raw_empty_matrix, raw_matrix_overlay, raw_zero_matrix
from .template import Pattern, Template, resolve_pattern
from .utils.bool import validate_bitwidth
from .utils.char import to_int_array
from .utils.pretty import mprint, pretty


# -- TODO: sanity checks --------------------------------------------
#
# - Use setattr to block changes to self.matrix if state != 0, suggest self.reset().
#   Actually, this also applies to all attributes
class Algorithm(MultipliedMeta):
    """Manages and sequences operations via a series of stages defined by templates and maps.

    Attributes
    ----------
    bits : int
        The bitwidth of the matrix to be multiplied.
    matrix : Matrix
        The matrix to be multiplied.
    dadda : bool
        Whether to use the Dadda-Tree algorithm.
    state : int
        The current state of the algorithm.
    algorithm : dict[int, dict[str, Template | Matrix | Map]]
        The algorithm to be used.
    saturation : bool
        Whether to use saturation arithmetic. Always to original bitwidth.

    """

    def __init__(
        self,
        bits: int,
        *,
        matrix: Any = None,
        saturation: bool = False,
        dadda: bool = False,
    ) -> None:

        validate_bitwidth(bits)
        if not isinstance(dadda, bool):
            raise TypeError(f"Expected dadda: bool, got {type(dadda)}")
        if not isinstance(saturation, bool):
            raise TypeError(f"Expected saturation: bool, got {type(saturation)}")
        if matrix is not None:
            if not isinstance(matrix, Matrix):
                raise TypeError(f"Expected Matrix, got {type(matrix)}")
            self.matrix = matrix
        else:
            self.matrix = Matrix(bits)

        self.bits = bits
        self.dadda = dadda
        self.state = 0
        self.algorithm = {}
        if self.dadda:
            hoist(self.matrix)
        self.saturation = saturation
        if self.saturation:
            self._clamp_bitwidth()

        # -- TODO: update this when anything is modified ------------
        # create update() function
        # add to each modifying class method

        self._soft_type = dict
        return None

    def push(
        self, source: Template | Pattern, map_: Any = None
    ) -> None:
        """Populate algorithm stage based on template. Generates pseudo
        result to represent output matrix

        Parameters
        ----------
        source : Template | Pattern
            The template or pattern to be used for the algorithm stage.
        map_ : Any, optional
            The map to be used for the algorithm stage, by default None

        Returns
        -------
        None

        Notes
        -----

        Layout:
        >>> self.algorithm[x] = {
        >>>     "template" : Template,
        >>>     "pseudo"   : Matrix,
        >>>     "map"      : Map}
        """

        if source.bits != self.bits:
            raise ValueError("Template bitwidth must match Algorithm bitwidth.")
        if map_ and not (isinstance(map_, (Map))):
            raise TypeError("Invalid argument type. Expected Map")

        if isinstance(source, Pattern):
            template = Template(source)
        elif isinstance(source, Template):
            if source._complex and (map_ is None and not self.dadda):
                raise ValueError(f"Complex template without map.\n\n{source}")
            template = deepcopy(source)
        else:
            raise TypeError("Invalid argument type. Expected Template")

        if not isinstance(template.result, (Matrix)):
            raise ValueError("Template result is unset")

        result = template.result
        res_copy = deepcopy(result)
        stage_index = len(self.algorithm)

        # -- hybrid setup -------------------------------------------
        # Strategy:
        #
        # [ SETUP FIRST TEMPLATE ]
        # > If first template -> setup Template._hybrid
        #
        # [ UNIFIED BOUNDS ]
        # > Use _hybrid to generate unified bounds
        # > Store generated bounds within Template._hybrid_bounds
        #
        # [ APPLY MAP ]
        # > Use Template._hybrid_bounds -> hoist Template._hybrid -> generate map
        # > Template.result -> pseudo
        # > Hoisted Template._hybrid -> Algorithm._hybrid_next
        #
        # [ NEXT TEMPLATE ]
        # > If not first template -> setup map from previous stage's Template._hybrid
        #
        # > Use Algorithm._hybrid_next to setup Template._hybrid
        #   > generate zeroed matrix of _hybrid_next
        #   > use zeroed matrix -> setup Template._hybrid
        # > Use Template_hybrid > _hybrid_bounds
        # > Use Template._hybrid_bounds -> hoist Template.result -> generate map

        if self.dadda:
            if self.algorithm == {}:
                # setup Template._hybrid
                # > generate zero / dadda matrix
                hybrid_template = raw_dadda_matrix(template.bits)

                # ! these need to be merged -- requires true bounds
                # ! merge :: < overlayed "_" matrix > + < result / rebound >

                # > overlay _s Template.bounds
                raw_matrix_overlay(hybrid_template, unify_bounds(template.bounds), "_")
                # > overlay 0s Template.re_bounds
                raw_matrix_overlay(hybrid_template, unify_bounds(template.re_bounds), "0")


            else:
                # setup map from previous stage's Template._hybrid
                # > use Template._hybrid_unified -> overlay 0s to raw_empty_matrix
                # > ...

                last_template = self.algorithm[len(self.algorithm) - 1]["template"]
                last_hybrid = last_template._hybrid

                # > generate new setup
                hybrid_template = raw_empty_matrix(last_template.bits)

                # ! these need to be merged -- requires true bounds
                # ! merge :: < overlayed "_" matrix > + < result / rebound >

                # > overlay previous bounds
                raw_matrix_overlay(hybrid_template, last_template._hybrid_bounds, "0")
                # > overlay _s Template.bounds
                raw_matrix_overlay(hybrid_template, unify_bounds(template.bounds), "_")
                # > overlay 0s Template.re_bounds
                raw_matrix_overlay(hybrid_template, unify_bounds(template.re_bounds), "0")


            template._hybrid = Matrix(hybrid_template)
            mprint(template._hybrid)
            map_ = hoist(template._hybrid)  # expensive -- no bounds used
            template._hybrid_bounds = get_unified_bounds(template._hybrid.matrix)

            mprint(template._hybrid)
            res_copy.apply_map(map_)


        elif (template._complex or isinstance(map_, Map)) and not self.dadda:
            res_copy.apply_map(map_)

        elif template.pattern and not self.dadda:
            map_ = result.resolve_rmap()
            res_copy.apply_map(map_)

        else:
            ...

        stage = {
            "template": template,
            "pseudo": res_copy,
            "map": map_,
        }
        self.algorithm[stage_index] = stage
        return None

    def _clamp_bitwidth(self) -> bool:
        """Saturates matrix if current matrix has carried past original bitwidth"""

        boundary = (2**self.bits) - 1
        as_int = to_int_array(self.matrix.matrix)
        test = [boundary < i for i in as_int]

        if any(test):
            # flood bits within boundary
            saturated_value = [["0"] * self.bits + ["1"] * self.bits]
            self.matrix = Matrix(saturated_value + raw_empty_matrix(self.bits)[1:])
            return True
        else:
            return False

    # ! Matrix.x_checksum is only useful in the context of Algorithm.__reduce()
    # - Maybe use bounds to create x_checksum within __reduce()'s unit collection
    # - OR within, the same scope, use bounds to execute a given arithmetic unit
    def _reduce(self) -> None:
        """use template or pattern to reduce a given matrix."""
        from copy import copy

        # -- implementation -----------------------------------------
        #
        # Arithmetic units are defined by how many rows they cover, or
        # their 'run', the length of which determines the type of unit:
        #
        # run = 3:
        #   CSA: carry is placed to the left of source column
        #   and one row down to avoid corrupting adjacent columns.
        #
        #   [input-------] | [output------]
        #   ...00100010... | ...00100010...
        #   ...00101010... | ..00101010....
        #   ...00101010... | ...________...
        #
        # run = 2:
        #   binary adder: generates carry through propagates, with a
        #   final carry extending past original width.
        #
        #   [input-------] | [output------]
        #   ...00110110... | ..001100000...
        #   ...00101010... | ...________...

        # -- isolate units ------------------------------------------

        bounds = self.algorithm[self.state]["template"].bounds
        units = matrix_scatter(self.matrix.matrix, bounds)
        # -- reduce -------------------------------------------------
        n = self.bits << 1
        results = {}
        chars = list(bounds.keys())
        for ch in chars:
            matrix = units[ch]
            if ch == "_":
                results[ch] = Matrix(matrix)
                continue
            base_index = bounds[ch][0][1]
            unit_bounds = sorted(bounds[ch], key=lambda x: x[1])
            match bounds[ch][-1][1] - bounds[ch][0][1] + 1:  # row height
                case 1:  # NOOP
                    output = results[ch] = Matrix(matrix)
                    continue

                case 2:  # ADD
                    # TODO: make use of checksums or use bounds

                    operand_a = copy(matrix[base_index])
                    operand_b = copy(matrix[base_index + 1])
                    checksum = [False] * n

                    # -- skip empty rows ----------------------------
                    start = min(unit_bounds[0][0], unit_bounds[2][0])

                    # -- sum columns --------------------------------
                    for i in range(start, n):
                        # -- row checksum ---------------------------
                        if operand_a[i] != "_" or operand_b[i] != "_":
                            checksum[i] = True

                        # -- normalise binary -----------------------
                        if operand_a[i] == "_" and operand_b[i] != "_":
                            operand_a[i] = "0"

                        elif operand_b[i] == "_" and operand_a[i] != "_":
                            operand_b[i] = "0"

                        elif operand_a[i] == "_" and operand_b[i] == "_":
                            operand_a[i] = "0"
                            operand_b[i] = "0"

                    # -- binary addition ----------------------------
                    bits_ = sum(checksum)
                    cout = 1 if not checksum[0] else 0
                    int_a = int("".join(operand_a[start : start + bits_]), 2)
                    int_b = int("".join(operand_b[start : start + bits_]), 2)

                    output = [["_"] * (start - cout)]
                    output[0] += list(f"{int_a + int_b:0{bits_ + cout}b}")
                    output[0] += ["_"] * (n - bits_ - start)

                case 3:  # CSA
                    # TODO: make use of checksums or use bounds
                    operand_a = matrix[base_index]
                    operand_b = matrix[base_index + 1]
                    operand_c = matrix[base_index + 2]

                    empty = False
                    output = [["_"] * n, ["_"] * n]
                    start = 0

                    # -- skip empty rows ----------------------------
                    start = min(unit_bounds[0][0], unit_bounds[2][0], unit_bounds[4][0])

                    # -- sum columns --------------------------------
                    for i in range(start, n):
                        csa_sum = 0
                        csa_sum += 1 if operand_a[i] == "1" else 0
                        csa_sum += 1 if operand_b[i] == "1" else 0
                        csa_sum += 1 if operand_c[i] == "1" else 0

                        output[0][i] = csa_sum  # uses index to store sum in-place
                        empty = (
                            (operand_c[i] == "_")
                            + (operand_b[i] == "_")
                            + (operand_a[i] == "_")
                        )
                        # -- check end of unit ----------------------
                        if empty == 3:
                            output[0][i] = "_"  # set as empty since sum unused
                            break
                        if empty == 2:
                            output[0][i] = "1" if csa_sum & 1 else "0"
                            continue

                        # -- brute force index 0 --------------------
                        # ! remove try catch:
                        # ! handle index zero outside of loop
                        # ! unit may not even overlap index 0
                        try:
                            output[0][i] = "1" if csa_sum & 1 else "0"
                            output[1][i - 1] = "1" if csa_sum & 2 else "0"
                        except IndexError:
                            pass
                case _:
                    raise ValueError(
                        f"Unsupported unit type, len={bounds[ch][-1][1] - bounds[ch][0][1]}"
                    )

            # -- build unit into matrix -----------------------------
            unit_result = [[]] * self.bits

            i = 0
            while i < base_index:
                unit_result[i] = ["_"] * n
                i += 1
            for row in output:
                unit_result[i] = row
                i += 1
            while i < self.bits:
                unit_result[i] = ["_"] * n
                i += 1
            results[ch] = Matrix(unit_result)

        # ! difficult sanity checks --------------------------------- ! #
        # Complex scenarios, where NOOP, CSA and ADD units intersect
        # will require extensive checks:
        #
        #   [example--] || [region--]
        #   ...BbaAa... || ....ba....
        #   ...CcaAa... || ....ca....
        #   ...CcaAa... || ....ca....
        #
        #
        # If repeated along the same y-axis, resolution can get very tricky.
        # One method could be skipping merges and opting for merges with non
        # conflicting units, repeat until few partially merged templates remain
        # and finally resolve conflicts, if possible.
        #
        # These conflicts can quickly be found by checking the sum of possible
        # bit positions in a given region of intersecting arithmetic units.
        # The example's sum for the first column is == 3.  This should raise a
        # flag indicating it should be merged later.
        #
        # This functionality to be implemented at a later date.

        # -- merge --------------------------------------------------
        re_bounds = self.algorithm[self.state]["template"].re_bounds
        complex = self.algorithm[self.state]["template"]._complex
        conflicts = self.algorithm[self.state]["template"].conflicts

        if 1 < len(results):
            self.matrix, _ = matrix_merge(
                results, re_bounds, complex=complex, conflicts=conflicts
            )
        else:
            self.matrix = list(results.values())[0]

        # -- map ----------------------------------------------------
        self.matrix.apply_map(self.algorithm[self.state]["map"])

        return None

    def auto_resolve_stage(
        self,
        *,
        recursive=True,
    ) -> None:
        """Automatically creates new algorithm stage to reduce the previous stage.

        Parameters
        ----------
        recursive : bool
            Recursively resolve until no partial products remain else resolve a single
            stage.

        Returns
        -------
        None
        """
        stage = len(self.algorithm)
        # -- non recursive ------------------------------------------
        if not self.algorithm:
            pseudo = deepcopy(self.matrix)
        else:
            pseudo = deepcopy(self.algorithm[stage - 1]["pseudo"])
        pattern = resolve_pattern(pseudo)
        self.push(Template(pattern, matrix=pseudo))
        if not recursive:
            return None

        # -- main loop ----------------------------------------------
        stage = len(self.algorithm)
        while self.bits - 1 > empty_rows(self.algorithm[stage - 1]["pseudo"]):
            if 10 < stage:
                raise IndexError("Maximum stage limit reached")
            # Stage generation
            pseudo = deepcopy(self.algorithm[stage - 1]["pseudo"])
            new_pattern = resolve_pattern(pseudo)
            self.push(Template(new_pattern, matrix=pseudo))

            # Condition based on generated stage
            stage += 1
        return None

    def step(self) -> Matrix:
        """Execute the next stage of the algorithm and update internal matrix"""
        if self.state == len(self.algorithm):
            print("Algorithm complete")
            return self.matrix
        if self.saturation:
            self._clamp_bitwidth()
        self._reduce()
        self.state += 1

        # getattr for matrix, template and map to peek algorithm
        return self.matrix

    def exec(self, a: int, b: int) -> dict[int, Matrix]:
        """Run entire algorithm with a single set of inputs then reset internal state.

        Parameters
        ----------
        a : int
            First operand
        b : int
            Second operand

        Returns
        -------
        dict[int, Matrix]
            resultant matrix indexed by stage, including initial state
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError(f"Expected int, got {type(a)} and {type(b)}")

        if a == 0 or b == 0:
            return {0: Matrix(self.bits)}
        self.matrix = Matrix(self.bits, a=a, b=b)
        if self.dadda:
            hoist(self.matrix)

        truth = {0: self.matrix}
        self.state = 0
        for n in range(len(self.algorithm)):
            self._reduce()
            self.state += 1
            if self.saturation and self._clamp_bitwidth():
                for i in range(n, len(self.algorithm)):
                    truth[i + 1] = deepcopy(self.matrix)
                break
            truth[n + 1] = deepcopy(self.matrix)

        self.state = 0
        return truth

    def reset(self, matrix: Matrix) -> None:
        """Reset internal state and submit new initial matrix"""

        if not isinstance(matrix, Matrix):
            raise TypeError(f"Expected Matrix, got {type(matrix)}")
        self.matrix = matrix
        if self.dadda:
            hoist(self.matrix)
        self.state = 0
        return None

    # ! getattr for matrix, template and map to peek algorithm

    def __str__(self) -> str:
        return pretty(self.algorithm)

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __len__(self) -> int:
        return len(self.algorithm)

    def __getitem__(self, index) -> dict:
        return self.algorithm[index]

    def __iter__(self) -> Iterable:
        return iter(self.algorithm.items())

    def __next__(self) -> dict:
        if self.index >= len(self.algorithm):
            raise StopIteration
        self.index += 1
        return dict(self.algorithm[self.index - 1])


# -- helper functions -----------------------------------------------


# TODO: implement x_checksum (current checksum is y_checksum)
# IDEA: implement x_signature and maybe y_signature:
# - A given signature will create a set for all member of an axis
# - Should help when error checking, though I don't see a use for y_signature
#
def collect_template_units(
    source: Template,
) -> tuple[dict[str, Template], dict[str, list[tuple[int, int]]]]:
    """Return dict of isolated arithmetic units and their bounding box.

    Parameters
    ----------
    source : Template
        The source template to extract arithmetic units from.

    Returns
    -------
    tuple[dict[str, Template], dict[str, list[tuple[int,int]]]]
        A tuple containing a dictionary of isolated arithmetic units and their bounding box.

    Raises
    ------
    TypeError
        If the source is not of type Template or Matrix.

    """

    if not isinstance(source, (Template, Matrix)):
        raise TypeError(f"Expected type Template, Matrix got {type(source)}")

    from .utils.char import chartff

    bounds = source.bounds
    allchars = list(bounds.keys())
    allchars.remove("_")

    units = {}
    for ch in allchars:
        matrix = raw_empty_matrix(source.bits)
        tff = chartff(ch)  # toggle flip flop
        next(tff)  # sync to template case sensitivity
        i = 0  # coordinate index
        expected_y = None
        while i < len(bounds[ch]) - 1:
            # == intra-row boundary ================================= #
            # bound[list_of_points][coord_i][y-axis]
            # "if 2 < points have the same y for a given unit"
            if 2 < sum([p[1] == bounds[ch][i][1] for p in bounds[ch]]):
                raise ValueError(f"Multiple arithmetic units found for unit '{ch}'")
            # ======================================================= #
            start = bounds[ch][i]
            end = bounds[ch][i + 1]
            if start[1] != end[1]:
                raise ValueError(
                    f"Bounding box error for unit '{ch}' "
                    f"Points:{start}, {end}, error:  {start[1]} != {end[1]}"
                )
            # -- traverse row ---------------------------------------
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
        units[ch] = Template(matrix)
    return (units, bounds)


# ________AaAaAaAa
# _______aAaAaAaA_
# ______AaAaAaAa__
# _____bBbBbBbB___
# ____BbBbBbBb____
# ___bBbBbBbB_____
# __CcCcCcCc______
# _DBbBbBbB_______


def hoist(
    source: Matrix | Template, *,
    bounds: dict[str, list[tuple[int, int]]]={},
    unified_bounds: dict[int, list[int]]={}
) -> Map:
    """collect bits to the top of the matrix and produce corresponding map.

    Parameters
    ----------
    source : Matrix | Template
        The source matrix or template to hoist in-place.
    bounds : dict[str, list[tuple[int, int]]]
        The bounds of the arithmetic units to hoist.

    Returns
    -------
    Map
        The resulting map after hoisting.
    """

    match source:
        case Matrix():
            matrix = source.matrix
        case Template():
            matrix = source.template
        case _:
            raise TypeError(
                f"source must be a Matrix or Template objects got {type(source)}"
            )

    bits = source.bits
    map_ = raw_zero_map(bits)

    # -- BBox hoist -------------------------------------------------
    if bounds or unified_bounds:
        # Strategy:
        # > unify bounds to ensure bits are mapped top-to-bottom
        # > use bounds to select and place bits into respective columns
        # > replace selected bit with "_"
        # > use current bit position to calculate the distance
        # > place mapped distance into map
        # > place columns back into matrix

        if not unified_bounds:
            unified_bounds = unify_bounds(bounds)  # sorts bounds by row

        # since we have unified bounds, it maybe possible to keep everything in-place
        # just keep a count of existing bits in each column
        print(unified_bounds)
        col_index = [0] * (bits << 1)
        for y, xs in unified_bounds.items():
            for left, right in batched(xs, 2):
                for x in range(left, right + 1):

                    matrix[y][x], matrix[y][x] = "_", matrix[y][col_index[x]]
                    distance = ((y - col_index[x]) ^ 255) + 1  # 2s complement @ 8-bit
                    map_[y][x] = f"{distance:02X}"[-2:]
                    col_index[x] += 1

        return Map(map_)

    # -- expensive hoist --------------------------------------------
    for x in range(bits << 1):
        y = 0
        col_id = 0
        offset = 0
        column = ["0"] * (bits)  # per column, collect each char, leaving no gaps
        while y < bits:
            if matrix[y][x] == "_":
                offset += 1
                val = 0
            else:
                val = (offset ^ 255) + 1  # 2s complement @ 8-bit

                # assign to column
                column[col_id] = matrix[y][x]

                # replace with empty char to stop possible duplication
                matrix[y][x] = "_"

                col_id += 1

            map_[y][x] = f"{val:02X}"[-2:]  # signed 2-bit hex
            y += 1

        for y in range(col_id):
            matrix[y][x] = column[y]

    return Map(map_)
