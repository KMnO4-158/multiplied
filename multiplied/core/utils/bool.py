#################################
# Commonly Reused Sanity Checks #
#################################

from typing import Any


SUPPORTED_BITWIDTHS = {4, 8}


def validate_bitwidth(bits: int) -> None:
    """Raise ValueError if bitwidth is supported by Multiplied"""

    if not isinstance(bits, int):
        raise TypeError(f"Unsupported type {type(bits)}. Expected {SUPPORTED_BITWIDTHS}")
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
