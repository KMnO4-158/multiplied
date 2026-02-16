import multiplied as mp
import pandas as pd



def test_scope() -> None:
    truth = mp.truth_scope((1, 65535), (1, 1_000_000))
    for t in truth:
        print(t)

def test_shallow_generator4() -> None:
    # truth4  = mp.truth_scope((1, 15), (1, 30))
    # for t in truth4:
    #     print(t)
    truth4  = mp.truth_scope((1, 15), (1, 10))
    alg4    = mp.Algorithm(4)
    for m in mp.shallow_truth_table(truth4, alg4):
        mp.mprint(m)


def test_shallow_generator8() -> None:
    # truth8  = mp.truth_scope((2, 64), (1, 2**15))
    # for t in truth8:
    #     print(t)
    truth8  = mp.truth_scope((2, 64), (1, 22))
    alg8    = mp.Algorithm(8)
    for m in mp.shallow_truth_table(truth8, alg8):
        mp.mprint(m)

def test_truth_table() -> None:
    scope = mp.truth_scope((1, 15), (1, 10))
    alg = mp.Algorithm(4)
    alg.auto_resolve_stage()
    t = mp.truth_table(scope, alg)
    print(t)
    for m in t:
        print(m)
        for k, v in m.items():
            print(v)


def test_truth_dataframe() -> None:
    for x in mp.truth_scope((1, 15), (1, 225)):
        print(x)
    scope = mp.truth_scope((1, 15), (1, 225))
    alg = mp.Algorithm(4)
    alg.auto_resolve_stage()
    t = mp.truth_table(scope, alg)
    df = mp.truth_dataframe(scope, alg)
    print(df)


def main() -> None:
    test_scope()
    # test_shallow_generator4()
    # test_shallow_generator8()
    # test_truth_table()
    # test_truth_dataframe()



if __name__ == "__main__":
    main()
