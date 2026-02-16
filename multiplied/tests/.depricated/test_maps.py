import multiplied as mp

def test_dadda_map_4() -> None:
    bits = 4
    try:
        mp.build_dadda_map(0)
    except KeyError:
        pass
    m = mp.build_dadda_map(bits)
    mp.mprint(m)

def test_dadda_map_8() -> None:
    bits = 8
    try:
        mp.build_dadda_map(0)
    except KeyError:
        pass
    m = mp.build_dadda_map(bits)
    mp.mprint(m)

def test_resolve_simple_map() -> None:
    sm = mp.Map(
        [
            '00',
            'FF',
            'FF',
            'FF',
        ]
    )
    print(sm.rmap)
    mp.mprint(sm)
    m1 = mp.Matrix(4,a=5, b=5)
    mp.mprint(m1)
    m1map = m1.resolve_rmap(ignore_zeros=False)
    print(m1map.rmap)
    mp.mprint(m1map)

def test_empty_map_4() -> None:
    bits = 4
    m = mp.empty_map(bits)
    mp.mprint(m)

def test_empty_map_8() -> None:
    bits = 8
    m = mp.empty_map(bits)
    mp.mprint(m)

def test_apply_rmap() -> None:
    m = mp.Matrix(4,a=3, b=10)
    mp.mprint(m)
    rm = m.resolve_rmap(ignore_zeros=False)
    mp.mprint(rm.rmap)
    m.apply_map(rm)
    mp.mprint(m)

def main():
    test_dadda_map(8)
    test_resolve_simple_map()
    test_empty_map(4)
    test_apply_rmap()

if __name__ == "__main__":
    main()
