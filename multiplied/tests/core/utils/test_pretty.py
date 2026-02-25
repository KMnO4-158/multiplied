import pytest

from multiplied.core.utils.pretty import (
    pretty,
    # pretty_dict,
    # pretty_nested_list,
    # mprint
)

ARR_2D = [
    ["_", "_", "_", "_", "a", "A", "a", "A"],
    ["_", "_", "_", "A", "a", "A", "a", "_"],
    ["_", "_", "a", "A", "a", "A", "_", "_"],
    ["_", "b", "B", "b", "B", "_", "_", "_"],
]


@pytest.mark.parametrize(
    "arr, expected",
    [
        (ARR_2D, "____aAaA\n___AaAa_\n__aAaA__\n_bBbB___\n"),
    ],
)
def test_pretty(arr, expected):
    assert pretty(arr) == expected


def test_pretty_dict(): ...


@pytest.mark.parametrize(
    "arr, expected",
    [
        (ARR_2D, "____aAaA\n___AaAa_\n__aAaA__\n_bBbB___\n"),
    ],
)
def test_pretty_nested_list(arr, expected):
    assert pretty(arr) == expected


def test_mprint(): ...
