import multiplied as mp
from multiplied.tests import REFERENCE

"""
Strategy:

    > Upon creation calculate bounds
    > add a __setattr__ function to update bounds if map is modified

"""

def unify_bounds(bounds: dict) -> dict:
    """Returns a simplified bound for non empty characters

    Parameters
    ----------
    bounds : dict
        Bounding box for each arithmetic unit in Template object

    Returns
    -------
    dict
        Unified bounds where  {y : [x0, x1]}

    See Also
    --------
    :func:`update_bounding_box`
    """
    if not isinstance(bounds, dict):
        raise TypeError(f"Expected dict got {type(bounds)}")
    if bounds.get("_") is None:
        raise ValueError("Bounds must have a `_` key")

    unified_row_bounds = {}
    for k, unit_bounds in bounds.items():
        if k == "_":
            continue
        for item, row in unit_bounds:
            if unified_row_bounds.get(row) is None:
                unified_row_bounds[row] = []
            unified_row_bounds[row].append(item)

    return unified_row_bounds

def apply_complex_map(matrix: mp.Matrix, map: mp.Map, bounds: dict) -> None:
    """Applies a complex mapping to source Matrix

    Parameters
    ----------
    matrix : mp.Matrix
        Matrix to apply mapping to

    map : mp.Map
        Multiplied Map object to apply mapping from

    bounds : dict[str: list[int]]
        Unified bounds for all arithmetic units
    """
    if not all([isinstance(r, int) for r in bounds]):
        raise TypeError("Expected all row bounds to be integers")

    for row in sorted(bounds.keys()):
        if not isinstance(bounds[row], list):
            raise TypeError("Expected row bounds to be a list")

        for col in range(bounds[row][0], bounds[row][1] + 1):
            if map.map[row][col] == "00":
                continue
            if (offset := int(map.map[row][col], 16)) & 128:
                offset = (~offset + 1) & 255  # 2s complement

            matrix.matrix[row - offset][col] = matrix.matrix[row][col]
            matrix.matrix[row][col] = "_"

    return None



def main() -> None:
    ref_dadda_map = REFERENCE["dadda_map"][8]
    print(mp.Map(ref_dadda_map))

    count = 0
    for y in ref_dadda_map:
        for x in y:
            if x == "00":
                count += 1

    shape = (len(ref_dadda_map), len(ref_dadda_map[0]))
    print(f"Cycles wasted: {count}")
    print(f"Efficiency: % {100 * count / (shape[0] * shape[1])}")

    template = mp.Template(mp.Pattern(REFERENCE["pattern"][8]))
    print(template)
    print(template.bounds)
    print(template.re_bounds)
    unified_bounds = unify_bounds(template.bounds)
    print(unified_bounds)

    unified_bounds = unify_bounds(template.re_bounds)
    print(unified_bounds)

    matrix = mp.Matrix(8, a=128, b = 255)
    noop_template = mp.Template(mp.Pattern(REFERENCE["noop_pattern"][8]))
    print(matrix)
    apply_complex_map(matrix, mp.Map(ref_dadda_map), unify_bounds(noop_template.bounds))
    print(matrix)




if __name__ == "__main__":
    main()
