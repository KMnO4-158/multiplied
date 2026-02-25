import pytest
import multiplied as mp


@pytest.fixture
def gen_resources_4b():
    p = mp.Pattern(["a", "a", "b", "b"])
    alg = mp.Algorithm(4)
    return p, alg


@pytest.fixture
def gen_resources_8b():
    p = mp.Pattern(["a", "a", "a", "b", "b", "b", "c", "c"])
    alg = mp.Algorithm(8)
    return p, alg


def gen_resources(bits: int, *, a=0, b=0) -> tuple[mp.Matrix, mp.Pattern, mp.Algorithm]:

    m = mp.Matrix(bits, a=a, b=b)
    match bits:
        case 4:
            p = mp.Pattern(["a", "a", "b", "b"])
        case 8:
            p = mp.Pattern(["a", "a", "a", "b", "b", "b", "c", "c"])
        case _:
            raise ValueError(f"Unsupported number of bits: {bits}")
    alg = mp.Algorithm(bits)
    return m, p, alg


def manual_test_exec_8(a: int, b: int) -> None:
    m, p, alg = gen_resources(8, a=a, b=b)
    alg.auto_resolve_stage()
    print(alg)
    print(alg.exec(a, b))
    results = alg.exec(a, b)
    for i in results.values():
        print(i)

    print(int("".join(alg.matrix.matrix[0]), 2))
    print(a * b)


def main():
    manual_test_exec_8(42, 255)
    ...


if __name__ == "__main__":
    main()
