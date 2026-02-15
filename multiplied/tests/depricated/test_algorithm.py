import multiplied as mp



def gen_resources(bits: int, *, a=0, b=0
) -> tuple[mp.Matrix, mp.Pattern, mp.Algorithm]:
    m = mp.Matrix(bits, a=a, b=b)
    match bits:
        case 4:
            p = mp.Pattern(['a','a','b','b',])
        case 8:
            p = mp.Pattern(['a','a','a','b','b','b','c','c'])
        case _:
            raise ValueError(f"Unsupported number of bits: {bits}")
    alg = mp.Algorithm(bits)
    return m, p, alg

def test_step_4() -> None:
    m, p, alg = gen_resources(4, a=15, b=15)
    alg.push(p)
    print(alg.matrix)
    alg.step()
    print(alg.matrix)

def test_step_8() -> None:
    m, p, alg = gen_resources(8, a=255, b=255)
    alg.push(p)
    print(alg.matrix)
    alg.step()
    print(alg.matrix)



def manual_test_exec(a: int, b: int) -> None:
    m, p, alg = gen_resources(8, a=a, b=b)
    alg.auto_resolve_stage()
    print(alg)
    print(alg.exec(a, b))
    results = (alg.exec(a, b))
    for k, i in results.items():
        print('result: ', k)
        print(i)

def test_exec_4() -> None:
    a = 15
    b = 15
    m, p, alg = gen_resources(8, a=a, b=b)
    alg.auto_resolve_stage()
    print(alg)
    print(alg.exec(a, b))
    results = (alg.exec(a, b))
    for k, i in results.items():
        print('result: ', k)
        print(i)

def test_exec_8() -> None:
    a = 255
    b = 255
    m, p, alg = gen_resources(8, a=a, b=b)
    alg.auto_resolve_stage()
    print(alg)
    print(alg.exec(a, b))
    results = (alg.exec(a, b))
    for k, i in results.items():
        print('result: ', k)
        print(i)


def test_auto_resolve_single_4() -> None:
    p = mp.Pattern(['a','a','b','b'])
    alg = mp.Algorithm(4)
    alg.push(p)
    print(alg)
    # alg.auto_resolve_pattern(p, m)
    t2 = mp.Template(mp.Pattern(['a','a','b','c']), matrix=alg.algorithm[0]['pseudo'])
    alg.push(t2)
    print(alg)


def test_manual_population_8() -> None:
    p = mp.Pattern(['a','a','b','b','c','c','d','d'])
    alg = mp.Algorithm(8)
    alg.push(p)
    print(alg)
    # alg.auto_resolve_pattern(p, m)
    t2 = mp.Template(mp.Pattern(['a','a','b','b','_','_','_','_']), matrix=alg.algorithm[0]['pseudo'])
    alg.push(t2)
    t3 = mp.Template(mp.Pattern(['a','a','_','_','_','_','_','_']), matrix=alg.algorithm[1]['pseudo'])
    alg.push(t3)


def test_auto_resolve_recursive_full_4() -> None:
    m, p, alg = gen_resources(4, a= 6, b=7)
    alg.auto_resolve_stage()
    print(alg)


def test_auto_resolve_recursive_full_8() -> None:
    m, p, alg2 = gen_resources(8, a=12, b=42)
    alg2.auto_resolve_stage()
    print(alg2)



def test_isolate_arithmetic_units() -> None:
    template = mp.Template(mp.Pattern(['a','a','b','c']), matrix=mp.Matrix(4))
    isolated_units, bounds = template.collect_template_units()
    print(template)
    print(isolated_units)
    # for k, v in isolated_units.items():
    #     print(v.checksum) # <- broken

def test_err_duplicate_units() -> None:
    template = mp.Template(mp.Pattern(['a','a','b','b','c','c','d','d']), matrix=mp.Matrix(8))
    try:
        isolated_units, bounds = template.collect_template_units()
    except SyntaxError:
        pass

    template = mp.Template([
        ['_', '_', '_', '_', '_', '_', '_', '_', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a'],
        ['_', '_', '_', '_', '_', '_', '_', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', '_'],
        ['_', '_', '_', '_', '_', '_', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', '_', '_'],
        ['_', '_', '_', '_', '_', 'b', 'B', 'b', 'B', 'b', 'B', 'b', 'B', '_', '_', '_'],
        ['_', '_', '_', '_', 'B', 'b', 'B', 'b', 'B', 'b', 'B', 'b', '_', '_', '_', '_'],
        ['_', '_', '_', 'b', 'B', 'b', 'B', 'b', 'B', 'b', 'B', '_', '_', '_', '_', '_'],
        ['_', '_', 'C', 'c', 'C', 'c', 'C', 'c', 'C', 'c', '_', '_', '_', '_', '_', '_'],
        ['_', 'C', 'c', 'C', 'c', 'C', 'c', 'C', 'c', '_', '_', '_', '_', '_', '_', '_']
        ],
        result = [
            ['_', '_', '_', '_', '_', '_', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a'],
            ['_', '_', '_', '_', '_', '_', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', 'b', 'B', 'b', 'B', 'b', 'B', 'b', 'B', 'b', 'B', '_', '_', '_'],
            ['_', '_', '_', 'B', 'b', 'B', 'b', 'B', 'b', 'B', 'b', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['C', 'c', 'C', 'c', 'C', 'c', 'C', 'c', 'C', 'c', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
        ])

    print(template)
    # bounds   = mp.find_bounding_box(template)
    isolated_units = template.collect_template_units()
    # try:
    #     isolated_units = mp.isolate_arithmetic_units(template)
    # except SyntaxError:
    #     print('passed')
    #     isolated_units = []


    for b in template.find_bounding_box().items():
        print(b)



    for i in isolated_units:
        print(i)
        # print(i.checksum)

def test_algorithm_reuse_8() -> None:
    a = 15
    b = 15
    m, p, alg = gen_resources(8, a=a, b=a)
    alg.push(p)
    alg.auto_resolve_stage()
    print(alg)

    a=15
    b=15
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

    a=255
    b=255
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

    a=69
    b=255
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

def test_algorithm_reuse_4() -> None:
    a = 15
    b = 15
    m, p, alg = gen_resources(4, a=a, b=a)
    alg.push(p)
    alg.auto_resolve_stage()
    print(alg)

    a=15
    b=15
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

    a=2
    b=9
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

    a=15
    b=13
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

def test_exec_docs() -> None:
    p = mp.Pattern(['a','a','b','b','c','c','d','d'])
    alg = mp.Algorithm(8)
    alg.push(p)
    alg.auto_resolve_stage()
    a=42
    b=255
    for m in alg.exec(a, b).values():
        print(m)

    # convert result to decimal
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

def test_exec_saturation_4() -> None:
    alg = mp.Algorithm(4, saturation=True)
    alg.auto_resolve_stage()
    a=2
    b=15
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print(int("".join(alg.matrix.matrix[0]), 2), '<- saturated')
    print(a*b, '<- unsaturated')


def test_exec_saturation_8() -> None:
    alg = mp.Algorithm(8, saturation=True)
    alg.auto_resolve_stage()
    a=2
    b=255
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print(int("".join(alg.matrix.matrix[0]), 2), '<- saturated')
    print(a*b, '<- unsaturated')

def test_exec_dadda_4() -> None:
    alg = mp.Algorithm(4, dadda=True)
    alg.auto_resolve_stage()
    a=7
    b=15
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print()
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

def test_exec_dadda_8() -> None:
    alg = mp.Algorithm(8, dadda=True)
    alg.auto_resolve_stage()
    a=27
    b=255
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print()
    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a*b)

def test_exec_dadda_saturation_4() -> None:
    alg = mp.Algorithm(4, saturation=True, dadda=True)
    alg.auto_resolve_stage()
    a=2
    b=15
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print()
    print(int("".join(alg.matrix.matrix[0]), 2), '<- saturated')
    print(a*b, '<- unsaturated')


def test_exec_dadda_saturation_8() -> None:
    alg = mp.Algorithm(8, saturation=True, dadda=True)
    alg.auto_resolve_stage()
    a=2
    b=255
    output = alg.exec(a, b)
    for k, v in output.items():
        print(v)
        # mp.mprint(v['pseudo'])
    print()
    print(int("".join(alg.matrix.matrix[0]), 2), '<- saturated')
    print(a*b, '<- unsaturated')




def main():
    test_exec_docs()

    ...

if __name__ == "__main__":
    main()
