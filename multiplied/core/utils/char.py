####################################################
# Generating, Testing, and Manipulating Characters #
####################################################

from collections.abc import Generator



def chargen() -> Generator[str]:
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
        raise ValueError("Input must be a single alphabetic character")

    i = True if ord(ch) < 97 else False
    while True:
        if i := not(i): # toggle flip flop
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

    if not isinstance(matrix, list) or not all([isinstance(row, list) for row in matrix]):
        raise TypeError("Input must be type list[list[char]]")

    if not hash:
        # By no means efficient, but gets the job done.
        # Maybe integrated into __reduce()?

        chars = set(ch for row in matrix for ch in row)
        chars.remove('_')
        return set(ch.upper() for ch in chars)

    else:
        if (h := len(hash)) != (m := len(matrix)):
            raise ValueError(f"Hash(len={h}) and matrix(len={m}) lengths do not match")
        subset = []
        for i, j in enumerate(hash):
            if j:
                subset.append(matrix[i])
        chars = set(ch for row in subset for ch in row)
        chars.remove('_')
        return set(ch.upper() for ch in chars)

def to_int_matrix(matrix: list[list[str]]) -> list[int]:
    """Converts a matrix of characters to a matrix of integers

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
    >>> to_int_matrix([['_', '1', '_'], ['1', '0', '1']])
    [2, 5]

    """

    if not isinstance(matrix, list) or not all([isinstance(row, list) for row in matrix]):
        raise TypeError("Input must be type list[list[char]]")

    output = [0]*len(matrix)
    valid_chars = {'0', '_', '1'}
    for i, row in enumerate(matrix):
        tmp_row = ['']*len(matrix[0])
        for j, ch in enumerate(row):
            if ch not in valid_chars:
                raise ValueError(f"Expected {valid_chars}, got '{ch}' in row {i}")
            tmp_row[j] = '0' if ch in ['_', '0'] else '1'
        output[i] = int(''.join(tmp_row), 2)
    return output
