###########################################
# Algorithm Defined By Templates and Maps #
###########################################

from copy import deepcopy
from typing import Any, Iterable
import multiplied as mp

# -- TODO: sanity checks --------------------------------------------
#
# - Use setattr to block changes to self.matrix if state != 0, suggest self.reset().
#   Actually, this also applies to all attributes
class Algorithm():
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

    def __init__(self, bits: int,*, matrix: Any=None, saturation: bool=False, dadda=False) -> None:

        mp.validate_bitwidth(bits)
        if not isinstance(dadda, bool):
            raise TypeError(f"Expected dadda: bool, got {type(dadda)}")
        if not isinstance(saturation, bool):
            raise TypeError(f"Expected saturation: bool, got {type(saturation)}")
        if matrix is not None:
            if not isinstance(matrix, mp.Matrix):
                raise TypeError(f"Expected Matrix, got {type(matrix)}")
            self.matrix = matrix
        else:
            self.matrix = mp.Matrix(bits)

        self.bits       = bits
        self.dadda      = dadda
        self.state      = 0
        self.algorithm  = {}
        if self.dadda:
            hoist(self.matrix)
        self.saturation = saturation
        if self.saturation:
            self.__clamp_bitwidth()

        # -- TODO: update this when anything is modified ------------
        # create update() function
        # add to each modifying class method
        return None



    def push(self, source: mp.Template | mp.Pattern, map_: Any=None, dadda=False
    ) -> None:
        """Populate algorithm stage based on template. Generates pseudo
        result to represent output matrix

        Parameters
        ----------
        source : mp.Template | mp.Pattern
            The template or pattern to be used for the algorithm stage.
        map_ : Any, optional
            The map to be used for the algorithm stage, by default None
        dadda : bool, optional
            Whether to use the Dadda-Tree algorithm, by default False

        Returns
        -------
        None

        Notes
        -----

        Layout:
        >>> self.algorithm[x] = {
        >>>     "template" : mp.Template,
        >>>     "pseudo"   : mp.Matrix,
        >>>     "map"      : mp.Map}
        """

        if source.bits != self.bits:
            raise ValueError("Template bitwidth must match Algorithm bitwidth.")
        if map_ and not(isinstance(map_, (mp.Map))):
            raise TypeError("Invalid argument type. Expected mp.Map")

        # -- [TODO] ------------------------------------------------- #
        if map_ and not map_.rmap:                                    #
            raise NotImplementedError("Complex map not implemented")  #
        # ----------------------------------------------------------- #

        if isinstance(source, mp.Pattern):
            template = mp.Template(source)
        elif isinstance(source, mp.Template):
            template = source
        else:
            raise TypeError("Invalid argument type. Expected mp.Template")


        if not isinstance(template.result, list):
            raise ValueError("Template result is unset")


        result      = mp.Matrix(template.result)
        stage_index = len(self.algorithm)
        if not map_ and result:
            if dadda:
                res_copy = deepcopy(result)
                map_ = hoist(res_copy)
            else:
                map_ = result.resolve_rmap()
            result.apply_map(map_)
        else:
            result.apply_map(map_)

        stage = {
            'template': template,
            'pseudo': result,
            'map': map_,
        }
        self.algorithm[stage_index] = stage
        return None

    def __clamp_bitwidth(self) -> bool:
        """Saturates matrix if current matrix has carried past original bitwidth"""

        boundary = (2**self.bits)-1
        as_int   = mp.to_int_matrix(self.matrix.matrix)
        test     = [boundary < i for i in as_int]

        if any(test):
            # flood bits within boundary
            saturated_value = [['0']*self.bits + ['1']*self.bits]
            self.matrix = mp.Matrix(saturated_value + mp.empty_matrix(self.bits)[1:])
            return True
        else:
            return False

    # ! Matrix.x_checksum is only useful in the context of Algorithm.__reduce()
    # - Maybe use bounds to create x_checksum within __reduce()'s unit collection
    # - OR within, the same scope, use bounds to execute a given arithmetic unit
    # ---------------------------------------------------------------
    # Mangled as execution order is sensitive and __reduce should only
    # be called by the algorithm itself via: self.step(), or self.exec()
    def __reduce(self) -> None:
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
        #   binary adder: carry generates through propagates, with a
        #   final carry extending past original width.
        #
        #   [input-------] | [output------]
        #   ...00110110... | ..001100000...
        #   ...00101010... | ...________...

        # -- isolate units -----------------------------------------
        # ! Implement result bounding box to create single point of truth ! #
        # - currently every stage of every matrix reduction needs to resolve
        #   conflicts dynamically before merging vs doing so once via the
        #   resultant template
        bounds: dict = self.algorithm[self.state]['template'].bounds
        # -- reduce -------------------------------------------------
        n         = self.bits << 1
        results   = {}
        chars = list(bounds.keys())
        chars.remove('_')
        for ch in  chars:
            base_index = bounds[ch][0][1]
            match bounds[ch][-1][1] - bounds[ch][0][1] +1: # row height
                case 1: # NOOP
                    output = [copy(self.matrix[base_index][0])]

                case 2: # ADD
                    #TODO: make use of checksums or use bounds

                    operand_a = copy(self.matrix[base_index][0])
                    operand_b = copy(self.matrix[base_index+1][0])
                    checksum  = [False] * n

                    # -- skip empty rows ----------------------------
                    start = 0
                    while operand_a[start] == '_' and operand_b[start] == '_':
                        start += 1


                    for i in range(start, n):
                        # -- row checksum ---------------------------
                        if operand_a[i] != '_' or operand_b[i] != '_':
                            checksum[i] = True

                        # -- normalise binary -----------------------
                        if operand_a[i] == '_' and operand_b[i] != '_':
                            operand_a[i] = '0'

                        elif operand_b[i] == '_' and  operand_a[i] != '_':
                            operand_b[i] = '0'

                        elif operand_a[i] == '_' and operand_b[i] == '_':
                            operand_a[i] = '0'
                            operand_b[i] = '0'

                    # -- binary addition ----------------------------
                    bits_ = sum(checksum)
                    cout  = 1 if not checksum[0] else 0
                    int_a = int("".join(operand_a[start:start+bits_]), 2)
                    int_b = int("".join(operand_b[start:start+bits_]), 2)

                    output     = [['_']*(start-cout)]
                    output[0] += list(f"{int_a+int_b:0{bits_+cout}b}")
                    output[0] += ['_']*(n-bits_-start)


                case 3: # CSA
                    #TODO: make use of checksums or use bounds
                    operand_a = copy(self.matrix[base_index][0])
                    operand_b = copy(self.matrix[base_index+1][0])
                    operand_c = copy(self.matrix[base_index+2][0])
                    empty     = False
                    output    = [['_']*n, ['_']*n]
                    start     = 0

                    # -- skip empty rows ----------------------------
                    while (
                        operand_a[start] == '_' and
                        operand_b[start] == '_' and
                        operand_c[start] == '_'
                    ):
                        start += 1



                    # -- sum columns -------------------------------
                    for i in range(start, n):
                        csa_sum = 0
                        csa_sum += 1 if operand_a[i] == '1' else 0
                        csa_sum += 1 if operand_b[i] == '1' else 0
                        csa_sum += 1 if operand_c[i] == '1' else 0

                        output[0][i] = csa_sum # uses index to store sum in-place
                        empty  = (operand_c[i] == '_') + (operand_b[i] == '_') + (operand_a[i] == '_')
                        # -- check end of unit ----------------------
                        if empty == 3:
                            output[0][i] =  '_' # set as empty since sum unused
                            break
                        if empty == 2:
                            output[0][i]   = '1' if csa_sum & 1 else '0'
                            continue

                        # -- brute force index 0 --------------------
                        # ! remove try catch:
                        # ! handle index zero outside of loop
                        # ! unit may not even overlap index 0
                        try:
                            output[0][i]   = '1' if csa_sum & 1 else '0'
                            output[1][i-1] = '1' if csa_sum & 2 else '0'
                        except IndexError:
                            continue
                case _:
                    raise ValueError(f"Unsupported unit type, len={bounds[ch][-1][1] - bounds[ch][0][1]}")

            # -- build unit into matrix -----------------------------
            unit_result = [[]]*self.bits
            i = 0
            while i < base_index:
                unit_result[i] = ['_']*n
                i += 1
            for row in output:
                unit_result[i] = row
                i += 1
            while i < self.bits:
                unit_result[i] = ['_']*n
                i += 1
            results[ch] = mp.Matrix(unit_result)


        # -- merge units to matrix ----------------------------------
        # Merge in any order, checking for overlaps between borders
        # resolve conflicts by summing present bit positions and shifting
        # a target unit's bit

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
        if 1 < len(results):
            self.matrix = mp.matrix_merge(results, bounds)
        else:
            self.matrix = list(results.values())[0]

        # -- map ----------------------------------------------------

        self.matrix.apply_map(self.algorithm[self.state]['map'])
        self.state += 1


        return None



    def auto_resolve_stage(self, *, recursive=True,
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
            pseudo = deepcopy(self.algorithm[stage-1]['pseudo'])
        pattern = mp.resolve_pattern(pseudo)
        self.push(mp.Template(pattern, matrix=pseudo), dadda=self.dadda)
        if not recursive:
            return None

        # -- main loop ----------------------------------------------
        stage = len(self.algorithm)
        while self.bits-1 > mp.empty_rows(self.algorithm[stage-1]['pseudo']):
            if 10 < stage:
                raise IndexError('Maximum stage limit reached')
            # Stage generation
            pseudo = deepcopy(self.algorithm[stage-1]['pseudo'])
            new_pattern = mp.resolve_pattern(pseudo)
            self.push(mp.Template(new_pattern, matrix=pseudo))


            # Condition based on generated stage
            stage += 1
        return None

    def step(self) -> mp.Matrix:
        """Execute the next stage of the algorithm and update internal matrix"""
        if self.saturation:
            self.__clamp_bitwidth()
            self.__reduce()
        self.state += 1

        # getattr for matrix, template and map to peek algorithm
        return self.matrix

    def exec(self, a: int, b: int) -> dict[int, mp.Matrix]:
        """Run entire algorithm with a single set of inputs then reset internal state.

        Parameters
        ----------
        a : int
            First operand
        b : int
            Second operand

        Returns
        -------
        dict[int, mp.Matrix]
            resultant matrix indexed by stage, including initial state
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError(f"Expected int, got {type(a)} and {type(b)}")

        if a == 0 or b == 0:
            return {0: mp.Matrix(self.bits)}
        self.matrix = mp.Matrix(self.bits, a=a, b=b)
        if self.dadda:
            hoist(self.matrix)

        truth = {0: self.matrix}
        self.state = 0
        for n in range(len(self.algorithm)):
            self.__reduce()
            if self.saturation and self.__clamp_bitwidth():
                for i in range(n, len(self.algorithm)):
                    truth[i+1] = deepcopy(self.matrix)
                break
            truth[n+1] = deepcopy(self.matrix)

        self.state = 0
        return truth

    def reset(self, matrix: mp.Matrix) -> None:
        """Reset internal state and submit new initial matrix"""

        if not isinstance(matrix, mp.Matrix):
            raise TypeError(f"Expected Matrix, got {type(matrix)}")
        self.matrix = matrix
        self.state = 0
        return None

    # ! getattr for matrix, template and map to peek algorithm

    def __str__(self) -> str:
        return mp.pretty(self.algorithm)

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

# TODO: low priority
def collect_arithmetic_units(
    source: mp.Matrix,
    bounds: dict[str, list[tuple[int, int]]]
) -> list[mp.Matrix]:
    """
    Extract arithmetic units from source template into a list of templates.
    """
    ...


# TODO: implement x_checksum (current checksum is y_checksum)
# IDEA: implement x_signature and maybe y_signature:
# - A given signature will create a set for all member of an axis
# - Should help when error checking, though I don't see a use for y_signature
#
def collect_template_units(
    source: mp.Template,
) -> tuple[dict[str, mp.Template], dict[str, list[tuple[int,int]]]]:
    """Return dict of isolated arithmetic units and their bounding box.

    Parameters
    ----------
    source : Template
        The source template to extract arithmetic units from.

    Returns
    -------
    tuple[dict[str, mp.Template], dict[str, list[tuple[int,int]]]]
        A tuple containing a dictionary of isolated arithmetic units and their bounding box.

    Raises
    ------
    TypeError
        If the source is not of type Template or Matrix.

    """


    if not isinstance(source, (mp.Template, mp.Matrix)):
        raise TypeError(f"Expected type Template, Matrix got {type(source)}")

    from .utils.char import chartff
    bounds   = source.bounds
    allchars = list(bounds.keys())
    allchars.remove('_')


    units = {}
    for ch in allchars:
        matrix = mp.empty_matrix(source.bits)
        tff = chartff(ch) # toggle flip flop
        next(tff) # sync to template case sensitivity
        i = 0 # coordinate index
        expected_y = None
        while i < len(bounds[ch])-1:
            # -- intra-row boundary -------------------------------------- #
            # bound[list_of_points][coord_i][y-axis]
            # "if 2 < points have the same y for a given unit"
            if 2 < sum([p[1] == bounds[ch][i][1] for p in bounds[ch]]):
                raise ValueError(
                    f"Multiple arithmetic units found for unit '{ch}'")
            # ------------------------------------------------------------ #
            start = bounds[ch][i]
            end = bounds[ch][i+1]
            if start[1] != end[1]:
                raise ValueError(
                    f"Bounding box error for unit '{ch}' "
                    f"Points:{start}, {end}, error:  {start[1]} != {end[1]}"
                )
            # -- traverse row ---------------------------------------
            next(tff) # sync to template case sensitivity
            for x in range(start[0], end[0]+1):
                matrix[start[1]][x] = next(tff)


            # -- inter-row boundary test --------------------------------- #
            if expected_y is not None and expected_y != start[1]:
                raise ValueError(
                    f"Arithmetic unit '{ch}' spans multiple rows. "
                    f"Expected row {expected_y}, got row {start[1]}")
            expected_y = start[1]+1
            # ------------------------------------------------------------ #


            i += 2
        units[ch] = mp.Template(matrix)
    return (units, bounds)

# ________AaAaAaAa
# _______aAaAaAaA_
# ______AaAaAaAa__
# _____bBbBbBbB___
# ____BbBbBbBb____
# ___bBbBbBbB_____
# __CcCcCcCc______
# _DBbBbBbB_______

# TODO:
# [ Optimisation ]
#
# - Implement checksum tuple in Template class
# - output coordinates of moves
#
# - move to template.py
def hoist(source: mp.Matrix | mp.Template, *,
    checksum: list[int]=[],
    relative: bool=False,
) -> mp.Map:
    """collect bits to the top of the matrix and produce corresponding map.

    Parameters
    ----------
    source : mp.Matrix | mp.Template
        The source matrix or template to hoist.
    checksum : list[int], optional
        The checksum to use for hoisting, by default [].
    relative : bool, optional
        Whether to use relative coordinates, by default False.

    Returns
    -------
    mp.Map
        The resulting map after hoisting.
    """

    if not isinstance(checksum, list):
        raise TypeError(f"checksum must be a list got {type(checksum)}")

    match source:
        case mp.Matrix():
            matrix = source.matrix
        case mp.Template():
            matrix = source.template
        case _:
            raise TypeError(f"source must be a Matrix or Template objects got {type(source)}")

    bits = source.bits
    if checksum == []:
        checksum = [0]*bits

    # -- update when checksum reimplemented ------------------------- #
    y_start = 0                                                       #
    y_end   = bits                                                    #
    # --------------------------------------------------------------- #
    map_    = mp.empty_matrix(bits)

    for y in range(y_start, y_end):
        map_[y] = ['00']*(bits << 1)
    # implement x_start, x_end when checksums moved
    for x in range(bits << 1):
        y = y_start
        k = 0
        offset = 0
        column = ['0']*(y_end - y_start)
        while y < y_end:
            if matrix[y][x] == '_':
                offset += 1
                val = 0
            else:
                val = ((offset ^ 255) + 1) # 2s complement
                column[k]    = matrix[y][x]
                matrix[y][x] = '_'
                k += 1

            map_[y][x] = f"{val:02X}"[-2:]
            y += 1

        for y in range(k):
            matrix[y][x] = column[y]

    return mp.Map(map_)
