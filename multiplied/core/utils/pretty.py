from copy import deepcopy
from typing import Any
from multiplied import Matrix, Slice, Map, Algorithm, Template
import io



def pretty(listy_object: Any | Algorithm | Template | Matrix | Slice | Map) -> str:
    """Format Multiplied types, or list as a string.

    Parameters
    ----------
    listy_object : Any
        List or Dict style object to format as a string.

    Returns
    -------
    str

    Examples
    --------

    >>> pretty(mp.Matrix(4))
    ____0000
    ___0000_
    __0000__
    _0000___
    """

    if not isinstance(listy_object, (
        Algorithm, Template, Matrix, Slice, Map,
        list, dict,
    )):
        raise TypeError(f"Unsupported type {type(listy_object)}")

    match listy_object:
        case (Matrix() | Slice() | Map() | list()):
            return pretty_nested_list(listy_object)
        case Template():
            return pretty_nested_list(listy_object.template)
        case (Algorithm() | dict()):
            return pretty_dict(listy_object)
        case _:
            raise TypeError(f"Unsupported type {type(listy_object)}")

def pretty_dict(listy_dict: Any) -> str:
    """Format Dict type object as a string:

    >>> {0: [[1, _, _],[_, 2, _],[_, _, 3]],
    >>>  1: [[a, _, _],[_, b, _],[_, _, c]],
    >>>  2: [[x, y, z],[x, y, z],[x, y, z]]}
    0:{
    1__
    _2_
    __3
    }
    ...
    """

    pretty = io.StringIO()
    for key, value in listy_dict.items():
        pretty.write(f"\n{key}:")
        pretty.write('{\n')

        # ! Not sure if this is the best way to avoid + or += concatination
        for item_, list_ in value.items():
            if isinstance(list_, Map):
                pretty.write(f"\n{item_}:")
                pretty.write('{')
                pretty.write(f"\n\n{pretty_nested_list(list_, whitespace=True)}")
                pretty.write('}\n')
                continue
            pretty.write(f"\n{item_}:")
            pretty.write('{')
            pretty.write(f"\n\n{str(list_)}")
            pretty.write('}\n')
    return pretty.getvalue()

def pretty_nested_list(listy_object: Any, *, whitespace=False) -> str:
    """Format nested list as a string.

    Parameters
    ----------
    listy_object : Any
        The nested list to be formatted.
    whitespace : bool, optional
        Whether to add whitespace between elements, by default False.


    Examples
    --------
    >>> pretty_nested_list([[1, _, _],[_, 2, _],[_, _, 3]])
    1__
    _2_
    __3
    """
    whitespace = " " if whitespace else ""
    pretty = io.StringIO()
    for i in deepcopy(listy_object):
        row = [str(x) + whitespace for x in i]
        pretty.write("".join(row) + "\n")
    return pretty.getvalue()

# Needs some work
def mprint(matrix: Any):
    """Wrapper for print(mp.pretty)"""
    print(pretty(matrix))
