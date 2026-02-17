################################################
# Returns Template Objects Using User Patterns #
################################################

from copy import deepcopy
from typing import Any
from .utils.bool import isalpha, ischar
import multiplied as mp

# -- Template and Slice dependencies  ------------------------------- #

def build_csa(char: str, source_slice: mp.Slice
) -> tuple[mp.Slice, mp.Slice]: # Carry Save Adder -> (template, result)
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
    if not isinstance(source_slice, mp.Slice):
        raise TypeError(f"Expected type mp.Slice, got {type(source_slice)}")
    if len(source_slice) != 3:
        raise ValueError("Invalid template slice: must be 3 rows")

    # loop setup
    n         = len(source_slice[0])
    tff       = mp.chartff(char) # Toggle flip flop
    result    = [['_']*n, ['_']*n, ['_']*n]
    csa_slice = deepcopy(source_slice)

    for i in range(n):
        # Generates slice of all possible bit placements, represented
        # with a char. Lower and upper case aide in visualising changes
        # in bit position before, templates, and after, result, operation

        char = next(tff)
        csa_slice[0][i] = char if (y0:=csa_slice[0][i] != '_') else '_'
        csa_slice[1][i] = char if (y1:=csa_slice[1][i] != '_') else '_'
        csa_slice[2][i] = char if (y2:=csa_slice[2][i] != '_') else '_'

        result[0][i]    = char if 1 <= (y0+y1+y2) else '_'
        result[1][i-1]  = char if 1 <  (y0+y1+y2) else '_'
    return csa_slice, mp.Slice(result)

def build_adder(char: str, source_slice: mp.Slice
) -> tuple[mp.Slice, mp.Slice]: # Carry Save Adder -> (template, result)
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
    if not isinstance(source_slice, mp.Slice):
        raise TypeError(f"Expected type mp.Slice, got {type(source_slice)}")
    if len(source_slice) != 2:
        raise ValueError("Invalid template slice: must be 2 rows")

    # loop setup
    n           = len(source_slice[0])
    tff         = mp.chartff(char) # Toggle flip flop
    result      = [['_']*n, ['_']*n]
    adder_slice = deepcopy(source_slice) # ensure no references

    for i in range(n):
        # Generates slice of all possible bit placements, represented
        # with a char. Alternating char case aids in visualising changes
        # in bit position before, templates, and after, result, operation

        char = next(tff)
        adder_slice[0][i] = char if (y0:=adder_slice[0][i] != '_') else '_'
        adder_slice[1][i] = char if (y1:=adder_slice[1][i] != '_') else '_'
        result[0][i]      = char if y0 or y1 else '_'

    # -- Add final carry -----------------------------------------
    carry = not all(ch == '_' for ch in adder_slice[1]) # sanity check

    # find index of left most instance of char, regardless of case
    index = min(result[0].index(next(tff)), result[0].index(next(tff)))
    if carry and 0 < index:
        result[0][index-1] = next(tff) # Final carry place in result template

    return adder_slice, mp.Slice(result)

def build_noop(char: str, source_slice: mp.Slice
) -> tuple[mp.Slice, mp.Slice]:
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
    if not isinstance(source_slice, mp.Slice):
        raise TypeError(f"Expected type mp.Slice, got {type(source_slice)}")
    if len(source_slice) != 1:
        raise ValueError("Invalid template slice: must be 1 rows")

    n          = len(source_slice[0])
    tff        = mp.chartff(char) # Toggle flip flop
    noop_slice = deepcopy(source_slice) # ensure no references
    for i in range(n):
        noop_slice[0][i] = next(tff) if (noop_slice[0][i] != '_') else '_'

    return noop_slice, deepcopy(noop_slice) # avoids pointing to same object

def build_empty_slice(source_slice: mp.Slice) -> tuple[mp.Slice, mp.Slice]:
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

    if not isinstance(source_slice, mp.Slice):
        raise TypeError(f"Expected type mp.Slice, got {type(source_slice)}")

    empty_slice = deepcopy(source_slice) # ensure no references
    for row in range(len(source_slice)):
        for i in range(empty_slice.bits):
            empty_slice[row][i] = '_'
    return empty_slice, deepcopy(empty_slice)


class Pattern:
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
    def __init__(self, pattern: list[str]):
        if not(isinstance(pattern, list) and all(ischar(row) for row in pattern)):
            raise ValueError("Error: Invalid pattern format. Expected list[char]")
        self.pattern = pattern
        self.bits    = len(pattern)

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
            while i < len(self.pattern) and self.pattern[i-1] == self.pattern[i]:
                run += 1
                i   += 1
            if run < 4:
                # (arithmetic_unit, starting_row, run_length)
                metadata.append((None, i-run, run))
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
        return f"{'['+ pretty_[1:-1]+']'}"

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __len__(self) -> int:
        return self.bits

    def __getitem__(self, index: int) -> str:
        return self.pattern[index]



# -- ! [ Preparing For Decoders ] !-------------------------------- #
#
# 1st:
#
#   Implement complex maps, arithmetic unit based isolation and
#   partial product reduction.
#
# 2st: Adopt get_runs() within build_from_pattern()
#
#   get_runs can pass all information needed about a unit then
#   pass it forward.
#
# 3nd: Use named tupes or other structures to pass information
#
#   Improves clarity as library becomes increasingly complex.
#
class Template:
    """A structure representing collections of arithmetic units using characters.
    Generated using a partial product matrix and a Pattern or custom template

    Parameters
    ----------
    source : Pattern | list[list[str]]
        The source of the template.
    result : list[Any], optional
        The result of the template, by default []
    matrix : Any, optional
        The matrix of the template, by default None

    """

    # ! THIS is where checksums need to be implemented ! #
    # > Move checksum logic from Matrix class to Template class
    # > make checksum a named tuple to easily identify x vs y?
    # > passing both checksums will be the first step in optimisation
    #


    def __init__(self, source: Pattern | list[list[str]], *,
        result: list[Any] = [],
        matrix: Any = None,
    ) -> None: # Complex or pattern



        mp.validate_bitwidth(len(source))
        self.bits   = len(source)
        self.result = result if isinstance(result, (Template, list)) else []

        # -- pattern handling ---------------------------------------
        if isinstance(source, Pattern):


            self.pattern  = source
            self.checksum = [1 if ch != '_' else 0 for ch in source]
            if matrix is None:
                matrix = mp.Matrix(self.bits)
            self.build_from_pattern(self.pattern, matrix)

        # -- template handling ---------------------------------------
        elif (
            isinstance(source, list) and
            all([isinstance(i, list) for i in source]
            )
        ):
            self.template = source
            self.pattern  = []
            self.__checksum()

        else:
            raise TypeError
        self.bounds = self.find_bounding_box()
        return None



    def __checksum(self) -> None:
        row_len  = self.bits << 1
        checksum = [0] * self.bits
        for i, row in enumerate(self.template):
            if len(row) != row_len:
                raise ValueError("Inconsistent row length")

            empty = 0
            for ch in row:
                if not ischar(ch):
                    raise TypeError(f"Expected character, got {ch}")
                if ch == '_':
                    empty += 1
                else:
                    break

            if empty != row_len:
                checksum[i] = 1
        self.checksum = checksum
        return None

    # Templates must be built using matrix
    def build_from_pattern(self, pattern: Pattern, matrix: mp.Matrix
    ) -> None:
        """Build a simple template and it's result for a given bitwidth based
        on matrix. Defaults to empty matrix if matrix=None.

        Parameters
        ----------
        pattern : Pattern
            The pattern to build the template from.
        matrix : mp.Matrix
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
        if not(isinstance(pattern, Pattern)):
            raise ValueError("Expected Pattern")
        mp.validate_bitwidth(len(pattern))

        # -- find run -----------------------------------------------
        template_slices = {}
        i = 1
        while i < len(pattern)+1:
            run = 1
            # replaced with get_runs when decoders are implemented
            # decoders will likely take special characters to extract the type
            # and likely require passing named tuples to current func to make
            # things clearer
            #
            # see [ Preparing For Decoders ] ^
            while i < len(pattern) and pattern[i-1] == pattern[i]:

                run += 1
                i   += 1

            # TODO: Add checks for templates which do not make sense for a given matrix #
            match run:
                case 1: # Do nothing
                    template_slices[i-run] = build_noop(pattern[i-run], matrix[i-run:i])
                case 2: # Create adder
                    template_slices[i-run] = build_adder(pattern[i-run], matrix[i-run:i])
                case 3: # Create CSA row
                    template_slices[i-run] = build_csa(pattern[i-run], matrix[i-run:i])
                case _:
                    if pattern[i-run] != '_':
                        raise ValueError(f"Unsupported run length {run}. Use '_' for empty rows")

                    template_slices[i-run] = build_empty_slice(matrix[i-run:i])

            i += 1

        template = []
        result = []
        for i in template_slices.values():
            template += i[0]
            result   += i[1]

        self.template, self.result = template, result
        return None


    # ! currently not generalised:
    #  > detect type of transition then use appropriate function
    #
    #  > or just detect empty, '_', characters as the boundary
    #       > This option means figuring out the correct key to use
    def find_bounding_box(self) -> dict[str, list[tuple[int, int]]]:
        """Returns dictionary of arithmetic unit and coordinates for their boundaries."""

        matrix = self.template
        rows   = self.bits
        items  = self.bits << 1
        bounds = {}
        x, y   = 0, 0
        while y < rows:

            # -- entry border -------------------------------------------
            key = matrix[y][0].upper()
            if key not in bounds:
                bounds[key] = []
            bounds[key].append((0, y))

            # -- central range ------------------------------------------
            while x < items-1:
                curr = matrix[y][x].upper()
                next = matrix[y][x+1].upper()
                if (curr == next) and isalpha(curr):
                    x += 1
                    continue
                if curr != next and (isalpha(curr) or isalpha(next)):
                    if curr not in bounds:
                        bounds[curr] = []
                    bounds[curr].append((x, y))
                    if next not in bounds:
                        bounds[next] = []
                    bounds[next].append((x+1, y))
                    x += 1
                    continue
                x += 1

            # -- exit border --------------------------------------------
            key = matrix[y][x].upper()
            if key not in bounds:
                bounds[key] = []
            bounds[key].append((x, y))

            x  = 0
            y += 1

        return bounds

    # TODO: implement x_checksum (current checksum is y_checksum)
    # IDEA: implement x_signature and maybe y_signature:
    # - A given signature will create a set for all member of an axis
    # - Should help when error checking, though I don't see a use for y_signature
    #
    def collect_template_units(self) -> tuple[dict[str, list], dict[str, list[tuple[int,int]]]]:
        """Return dict of isolated arithmetic units and their bounding box."""

        from .utils.char import chartff
        bounds   = self.find_bounding_box()
        allchars = list(bounds.keys())
        allchars.remove('_')


        units = {}
        for ch in allchars:
            matrix = mp.empty_matrix(self.bits)
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
            units[ch] = matrix
        return (units, bounds)



    # To be used in complex template results
    def merge(self, templates: list[Any]) -> None:
        """
        Merge multiple template slices into a single template.
        """
        assert isinstance(templates, list)
        # This looks terrible... Works tho?
        # templates[template[row[str]]]
        assert isinstance(templates[0][0][0][0], str)


        if len(templates) == 0:
            raise ValueError("No templates provided")

        self.merged = None # PLACEHOLDER #
        ...

    def __str__(self) -> str:
        return f"{mp.pretty(self.template)}\n{mp.pretty(self.result)}"

    def __repr__(self) -> str:
        return f"<multiplied.{self.__class__.__name__} object at {hex(id(self))}>"

    def __len__(self) -> int:
        return len(self.template)



# TODO: add examples
def resolve_pattern(matrix: mp.Matrix) -> Pattern:
    """For a given matrix, progressively allocate CSAs then adders to pattern

    Parameters
    ----------
    matrix : mp.Matrix
        The matrix to resolve the pattern for.

    Returns
    -------
    Pattern
        The resolved pattern.

    """

    from multiplied.core.utils.char import chargen
    char  = chargen()
    if (empty_rows := mp.empty_rows(matrix)) == matrix.bits:
        return Pattern(['_'] * matrix.bits)

    # TODO use io.StringIO()
    scope = matrix.bits - empty_rows
    new_pattern = []
    while 0 < scope:
        ch  = next(char)
        n   = len(new_pattern)

        if 3 <= scope:
            new_pattern += [ch, ch, ch]
        elif 2 == scope:
            new_pattern += [ch, ch]
        elif 1 == scope:
            new_pattern += [ch]

        scope -= len(new_pattern) - n
    new_pattern += ['_'] * empty_rows
    return Pattern(new_pattern)


def build_noop_template(self, pattern: Pattern, *, dadda=False) -> None:
    """Create template for zeroed matrix using pattern"""


"""
Complex templates implement decoders and bit-mapping.

Decoders reduce 4 or more bits at a time.

Bit mapping defines where bits are placed in each stage,
enabling complex implementations and possible optimisations.
"""
