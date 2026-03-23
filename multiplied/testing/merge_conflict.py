from itertools import batched
import multiplied as mp
from multiplied.tests import REFERENCE, DADDA_TREE, WALLACE_TREE


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

ZERO_MAP = REFERENCE["zero_map"][8]

def main() -> None:
    # alg = mp.Algorithm(8)
    # mp.mprint(WALLACE_TREE[8]["T"][0])

    # alg.push(mp.Template(WALLACE_TREE[8]["T"][0]), mp.Map(WALLACE_TREE[8]["M"][0]))
    # alg.push(mp.Template(WALLACE_TREE[8]["T"][1]), mp.Map(WALLACE_TREE[8]["M"][1]))
    # alg.push(mp.Template(WALLACE_TREE[8]["T"][2]), mp.Map(WALLACE_TREE[8]["M"][2]))
    # alg.push(mp.Template(WALLACE_TREE[8]["T"][3]), mp.Map(WALLACE_TREE[8]["M"][3]))
    # alg.push(mp.Template(WALLACE_TREE[8]["T"][4]), mp.Map(ZERO_MAP))

    alg = mp.Algorithm(8, dadda=True)

    mp.mprint(DADDA_TREE[8]["T"][0])
    alg.push(mp.Template(DADDA_TREE[8]["T"][0]))
    alg.push(mp.Template(DADDA_TREE[8]["T"][1]))
    alg.push(mp.Template(DADDA_TREE[8]["T"][2]))
    alg.push(mp.Template(DADDA_TREE[8]["T"][3]))
    alg.push(mp.Template(DADDA_TREE[8]["T"][4]))


    print(alg)
    for i in alg.exec(255, 255).values():
        print(i)

if __name__ == "__main__":
    main()
