#################################
# Commonly Reused Sanity Checks #
#################################

from itertools import batched
from typing import Any

# ! [ numba ]
# Nice little targets for understanding what works with the JIT and what doesn't

# ! [ pytest ]
# currently I only have integration tests.
# This is a good place to start writing unit tests


SUPPORTED_BITWIDTHS = {4, 8}


def validate_bitwidth(bits: int) -> None:
    """Raise ValueError if bitwidth is supported by Multiplied"""

    if not isinstance(bits, int):
        raise TypeError(
            f"Unsupported type {type(bits)}. Expected {SUPPORTED_BITWIDTHS}"
        )
    if bits not in SUPPORTED_BITWIDTHS:
        raise ValueError(f"Unsupported bitwidth {bits}. Expected {SUPPORTED_BITWIDTHS}")


def isint(source: Any) -> bool:
    """Return True if source converts to int"""
    match source:
        case int():
            return True
        case str():
            try:
                int(source)
                return True
            except ValueError:
                return False
        case _:
            return False


def ishex2(val: str) -> bool:
    """Return True if string represents a 2-bit hex value"""
    if not isinstance(val, str):
        return False
    if len(val) == 2:
        try:
            int(val, 16)
            return True
        except (ValueError, TypeError):
            return False
    return False


def ischar(ch: str) -> bool:
    """Return True if string is exactly one character"""
    try:
        ord(ch)
        return True
    except (ValueError, TypeError):
        return False


def isalpha(ch: str) -> bool:
    """Return True if string is exactly one alphabetic character"""
    try:
        if (65 <= ord(ch) <= 90) or (97 <= ord(ch) <= 122):
            return True
        return False
    except (ValueError, TypeError):
        return False


def isppm(nested_list: list[list[str]]) -> bool:
    """Return True if nested list represents a Partial Product matrix"""
    if not isinstance(nested_list, list):
        return False
    if not all(isinstance(row, list) for row in nested_list):
        return False
    bits = len(nested_list)
    if not all(len(row) == (bits << 1) for row in nested_list):
        return False
    if not all(ischar(val) or ishex2(val) for row in nested_list for val in row):
        return False
    return True


def isbbox(bounds: dict[str, list[tuple[int, int]]]) -> bool:
    """Return True if dict represents a recognised bounding box.

    Notes
    -----
    Tuple pairs are expected to be in the format:
    >>> # (start, y), (end, y)
    >>> [..., (x0, y), (x1, y), ...]

    Examples
    --------

    >>> isbbox({"a": [(0, 0), (4, 0)]})
    True

    >>> isbbox({
    >>>     "a": [(0, 0), (4, 0)],
    >>>     "b": [(0, 0), (4, 0)]})
    True

    >>> isbbox({"aa": [(0, 0), (4, 0)]})
    False

    >>> isbbox({"a": [(4, 0)]})
    False

    >>> isbbox({
    >>>     "a": [(0, 0), (4, 0)],
    >>>     "b": [(5, 0)]})
    False

    """
    if isinstance(bounds, dict):
        for k, v in bounds.items():
            if not ischar(k):
                print("char", k)
                return False

            # must be pairs
            if not isinstance(v, list) or len(v) % 2:
                print("len", len(v))
                return False

            # pairs must sit on same y
            for left, right in batched(v, 2):
                if not isinstance(left, tuple) or not isinstance(right, tuple):
                    print("type", left, right)
                    return False
                try:
                    if int(left[1]) != int(right[1]):
                        print("y", left[1], right[1])
                        return False
                except TypeError:
                    print("value", left[1], right[1])
                    return False
        return True
    return False
