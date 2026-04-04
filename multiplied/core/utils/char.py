####################################################
# Generating, Testing, and Manipulating Characters #
####################################################

from collections.abc import Generator

from multiplied.core.utils.bool import isalpha, ischar, ishex2, isint, isppm


def chargen(start: str = "A") -> Generator[str]:
    """Return Generator  characters from A to Z.

    Yields
    ------
    str


    Example
    -------
    >>> x = chargen()

    >>> next(x)
    'A'
    >>> next(x)
    'B'
    >>> next(x)
    'C'
    """
    if not isalpha(start):
        raise TypeError("Start must be a single alphabetic character")
    i = 0
    while True:
        yield chr((i % 26) + 65)
        i += 1


def chartff(ch: str) -> Generator[str]:
    """Generator to flip flop between upper and lowercase characters.

    Parameters
    ----------
    ch: str
        Single alphabetic character to flip flop.

    Yields
    ------
    str
        Upper or lowercase version of the input character.

    Raises
    ------
    ValueError
        If input is not a single alphabetic character.

    Examples
    --------
    >>> x = chartff('a')
    >>> next(x)
    'a'
    >>> next(x)
    'A'
    >>> next(x)
    'a'
    """
    from .bool import ischar

    if not ischar(ch):
        raise TypeError("Input must be a single alphabetic character")

    # match first case with input case
    i = True if ord(ch) < 97 else False

    while True:
        if i := not (i):  # toggle flip flop
            yield ch.lower()
        else:
            yield ch.upper()


def allchars(matrix: list[list[str]], *, hash: list[int | bool] = []) -> set[str]:
    """Returns set of unique characters from a nested list.

    Parameters
    ----------
    matrix: list[list[str]]
        Matrix of characters to extract unique characters from.
    hash: list[int | bool], optional
        List of bools or 0s and 1s indicating if a row contains characters.

    Return
    ------
    set[str]


    Notes
    -----
    Ignores underscore characters and converts characters to uppercase

    See Also
    --------
    Matrix : Multiplied 2D Matrix Object

    Examples
    --------
    >>> allchars([['A', 'B'], ['C', 'D']])
    {'A', 'B', 'C', 'D'}
    """

    if not isinstance(matrix, list) or not all(
        [isinstance(row, list) for row in matrix]
    ):
        raise TypeError("Input must be type list[list[char]]")

    if not hash:
        # By no means efficient, but gets the job done.
        # Maybe integrated into __reduce()?

        chars = set(ch for row in matrix for ch in row)
        chars.remove("_")
        return set(ch.upper() for ch in chars)

    else:
        if (h := len(hash)) != (m := len(matrix)):
            raise ValueError(f"Hash(len={h}) and matrix(len={m}) lengths do not match")
        subset = []
        for i, j in enumerate(hash):
            if j:
                subset.append(matrix[i])
        chars = set(ch for row in subset for ch in row)
        chars.remove("_")
        return set(ch.upper() for ch in chars)


def to_int_array(matrix: list[list[str]]) -> list[int]:
    """Converts a matrix of characters to a array of integers

    Parameters
    ----------
    matrix : list[list[str]]
        Matrix of characters to convert from 2D Multiplied formatted matrix
        into to list of integers.

    Returns
    -------
    list[int]

    Examples
    --------
    >>> to_int_array([['_', '1', '_'], ['1', '0', '1']])
    [2, 5]

    """

    if not isinstance(matrix, list) or not all(
        [isinstance(row, list) for row in matrix]
    ):
        raise TypeError("Input must be type list[list[char]]")

    output = [0] * len(matrix)
    valid_chars = {"0", "_", "1"}
    for i, row in enumerate(matrix):
        tmp_row = [""] * len(matrix[0])
        for j, ch in enumerate(row):
            if ch not in valid_chars:
                raise ValueError(f"Expected {valid_chars}, got '{ch}' in row {i}")
            tmp_row[j] = "0" if ch in ["_", "0"] else "1"
        output[i] = int("".join(tmp_row), 2)
    return output


def infer_matrix_format(source: list[list[str]], fmt: str) -> list[list[str]]:
    """Infers the format of a litmus test string and returns a matrix of characters.

    Parameters
    ----------
    source : list[list[str]]
        Source matrix to infer format from.
    fmt : str
        Default char used in each matrix cell.
    l

    Returns
    -------
    list[list[str]]

    Examples
    --------
    >>> infer_matrix_format("auto", "FF")  # infer as "map"
    [['00', '00', '00', '00'...

    >>> infer_matrix_format("auto", "0")   # infer as "empty"
    [['_', '_', '_', '_'...

    >>> infer_matrix_format("zero", "")  # zero-filled
    [['0', '0', '0', '0'...

    """
    if not isinstance(fmt, str):
        raise TypeError(f"Expected str, got {type(fmt)}")
    if not isppm(source):
        raise TypeError(f"Expected list[list[str]], got {type(source)}")

    if fmt == "auto":
        _litmus = source[0][0]
        if ischar(_litmus) or (isint(_litmus) and (_litmus == "0" or _litmus == "1")):
            fmt = "empty"
        elif ishex2(_litmus):
            fmt = "map"
        else:
            fmt = "zero"

    bits = len(source)
    match fmt:
        case "empty":
            return [["_" for _ in range(bits << 1)] for row in range(bits)]
        case "zero":
            matrix = []
            zero = ["0"] * bits
            for i in range(bits):
                row = (["_"] * ((bits << 1) - bits - i)) + zero + (["_"] * i)
                matrix.append(row)
            return matrix
        case "map":
            return [["00" for _ in range(bits << 1)] for row in range(bits)]

        case "char": # expensive
            chars = allchars(source)
            ch = chargen()
            count = 0
            while ch in chars:
                ch = next(ch)
                if count > 26:
                    raise ValueError("Too many characters in source")
                count += 1
                matrix = []

                fill = [ch] * bits
                for i in range(bits):
                    row = (["_"] * ((bits << 1) - bits - i)) + fill + (["_"] * i)
                    matrix.append(row)
                return matrix
        case _:
            raise ValueError(f"Unrecognised fmt: {fmt}")

    raise ValueError("Something went wrong")
