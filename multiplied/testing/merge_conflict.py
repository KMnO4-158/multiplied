from itertools import batched
import multiplied as mp
from multiplied.tests import REFERENCE


def smart_matrix_merge(
    source: dict[str, mp.Matrix],
    bounds: dict[str, list[tuple[int, int]]],
    *,
    complex: bool = False,
) -> mp.Matrix:
    """Merge multiple matrices into a single matrix using pre calculated bounds

    Parameters
    ----------
    source : dict[str, Matrix]
        A dictionary of matrices to merge

    bounds : dict[str, list[tuple[int, int]]]
        A dictionary of bounds for each matrix

    complex : bool, optional, default: False
        Performs additional checks during merge

    Returns
    -------
    Matrix

    Examples
    --------
    >>> source = {'A': Matrix([[1, _], [3, _]]),
                  'B': Matrix([[_, 6], [_, 8]])}
    >>> bounds = {'A': [(0, 0), (0, 0), (1, 1), (1, 1)],
    >>>           'B': [(0, 1), (0, 1), (0, 1), (0, 1)]}
    >>> matrix_merge(source, bounds)
    Matrix([[1, 6], [4, 8]])

    """
    if not isinstance(source, dict):
        raise TypeError("Source must be a dictionary")
    if not all(isinstance(val, mp.Matrix) for val in source.values()):
        raise TypeError("All values of source must be of type Matrix")
    if len(source) < 2:
        raise ValueError("Source must contain at least two matrices")
    if len(bounds) != len(source):
        # new error message needed
        raise ValueError(
            "Source must contain the same number of matrices as bounds"
            f"\nSources: \n{list(source.keys())}"
            f"\nBounds: \n{list(bounds.keys())}"
        )
    litmus = next(i for i in source.values())
    bits = litmus.bits
    output = mp.raw_empty_matrix(bits)
    for unit, matrix in source.items():
        if bounds[unit] == "_":
            continue
        for start, end in batched(bounds[unit], 2):
            if start[1] != end[1]:
                raise ValueError(f"Missing bound pair for row {start[1]}")
            y = start[1]
            for x in range(start[0], end[0] + 1):
                print(x, y)
                output[y][x] = matrix.matrix[y][x]

            print(str(output[y]))

    print("smart")
    mp.mprint(output)


def main() -> None:
    alg = mp.Algorithm(8)
    mp.mprint(REFERENCE["mosaic_template"][8]["T"])
    template = mp.Template(REFERENCE["worst_template"][8]["T"])
    print(template)
    alg.push(template, mp.Map(REFERENCE["zero_map"][8]))
    # # alg.auto_resolve_stage()
    # print(template.result)
    # print(template.re_bounds)

    for i in alg.exec(255, 128).values():
        print(i)


if __name__ == "__main__":
    main()
