################################
# Import Modules Without Error #
################################

import multiplied as mp

def test_pop_empty_matrix():
    matrix = mp.Matrix(8)
    assert matrix == matrix
    assert matrix.matrix == [
        ['_', '_', '_', '_', '_', '_', '_', '_', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['_', '_', '_', '_', '_', '_', '_', '0', '0', '0', '0', '0', '0', '0', '0', '_'],
        ['_', '_', '_', '_', '_', '_', '0', '0', '0', '0', '0', '0', '0', '0', '_', '_'],
        ['_', '_', '_', '_', '_', '0', '0', '0', '0', '0', '0', '0', '0', '_', '_', '_'],
        ['_', '_', '_', '_', '0', '0', '0', '0', '0', '0', '0', '0', '_', '_', '_', '_'],
        ['_', '_', '_', '0', '0', '0', '0', '0', '0', '0', '0', '_', '_', '_', '_', '_'],
        ['_', '_', '0', '0', '0', '0', '0', '0', '0', '0', '_', '_', '_', '_', '_', '_'],
        ['_', '0', '0', '0', '0', '0', '0', '0', '0', '_', '_', '_', '_', '_', '_', '_']
    ]

def test_pop_build_matrix():
    matrix = mp.Matrix(8,a=0, b=0)
    mult_by_zero_a = mp.Matrix(8,a=0, b=42)
    mult_by_zero_b = mp.Matrix(8,a=42, b=0)
    assert matrix.bits   == mult_by_zero_a.bits
    assert matrix.bits   == mult_by_zero_b.bits
    # print(vars(matrix))
    # print(vars(mult_by_zero_a))
    # print(vars(mult_by_zero_b))

# def test_pop_agorithm(): ## POPULATION NO IMPLEMENTED ##
#     temp1 = mp.Matrix(8) # Placeholder for template <-- update this
#     temp2 = mp.Matrix(8) # Placeholder for template <-- update this
#     arg   = [temp1, temp2]
#     alg   = mp.Algorithm(temp1)
#     alg.push(arg[0])

    # print(alg.bits)
    # print(alg)
    # print(temp1.bits)
    # print(temp2.bits)


def main() -> None:
    test_pop_empty_matrix()
    test_pop_build_matrix()
    # test_pop_agorithm()

if __name__ == "__main__":
    main()
