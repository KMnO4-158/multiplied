import multiplied as mp


def test_scope() -> None:
    truth = mp.truth_scope((1, 65535), (1, 1_000_000))
    for t in truth:
        print(t)


def test_shallow_generator4() -> None:
    # truth4  = mp.truth_scope((1, 15), (1, 30))
    # for t in truth4:
    #     print(t)
    truth4 = mp.truth_scope((1, 15), (1, 10))
    alg4 = mp.Algorithm(4)
    for m in mp.shallow_truth_table(truth4, alg4):
        mp.mprint(m)


def test_shallow_generator8() -> None:
    # truth8  = mp.truth_scope((2, 64), (1, 2**15))
    # for t in truth8:
    #     print(t)
    truth8 = mp.truth_scope((2, 64), (1, 22))
    alg8 = mp.Algorithm(8)
    for m in mp.shallow_truth_table(truth8, alg8):
        mp.mprint(m)

def test_complex_templates() -> None:
    from multiplied.tests import REFERENCE
    alg = mp.Algorithm(8)
    empty_pattern = mp.Pattern(["a", "_", "_", "_", "_", "_", "_", "_"])
    print(mp.Matrix(8))
    alg.push(empty_pattern)
    print(alg)
    alg.reset(mp.Matrix(8, a=12, b=2))
    print(alg.step())

    alg = mp.Algorithm(8)
    alg.auto_resolve_stage(recursive=False)
    print(alg)

    alg = mp.Algorithm(8)
    ref_complex_template = mp.Template(REFERENCE["complex_template"][8]["T"])
    print(ref_complex_template)
    alg.push(ref_complex_template)
    alg.auto_resolve_stage()
    print(alg)
    for i in alg.exec(15, 14).values():
        print(i)


def main() -> None:
    template = mp.Template(mp.Pattern(["a", "b", "b", "c", "c", "c", "_", "_"]))
    print(template)
    for k, v in mp.matrix_scatter(template.template, template.bounds).items():
        print(k)
        mp.mprint(v)


    result = template.result
    print(result)
    for k, v in mp.matrix_scatter(result.matrix, template.re_bounds).items():
        print(k)
        mp.mprint(v)

    matrix = mp.Matrix(8, a=12, b=2)
    print(matrix)
    for k, v in mp.matrix_scatter(matrix.matrix, template.bounds).items():
        print(k)
        mp.mprint(v)

    template = mp.Template(mp.Pattern(["a", "b", "b", "c", "c", "c", "_", "_"]))
    resultant = template.result
    map = resultant.resolve_rmap()
    print(map)
    for k, v in mp.matrix_scatter(map.map, template.bounds).items():
        print(k)
        mp.mprint(v)

    print()

if __name__ == "__main__":
    main()
