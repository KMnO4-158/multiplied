from functools import cache
from pathlib import Path
import multiplied as mp
import pandas as pd
import pyarrow as pa

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

def test_export_algorithm() -> None:
    m, p, alg = gen_resources(4)
    alg.auto_resolve_stage()
    path = Path(__file__).parent.parent.parent / 'examples/algorithms/example_4b_algorithm.json'
    mp.export_algorithm(alg, str(path))



# def test_import_algorithm() -> None:
#     path = ''
#     mp.import_algorithm(path)
#


@cache
def test_export_parquet_4() -> None:
    from pathlib import Path
    import time

    start_t = time.perf_counter()
    alg = mp.Algorithm(4)
    alg.auto_resolve_stage()
    scope = mp.truth_scope((1, 15), (1, 255))
    df = mp.truth_dataframe(scope, alg)
    end_t = time.perf_counter()
    pd.set_option('display.max_columns', None)
    print(df.head())
    print(df.info())
    print(f"{end_t - start_t:.6f} seconds")
    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_4b_mult_truthtable.parquet'
    print(path)
    start_t = time.perf_counter()
    df.to_parquet(path)
    end_t = time.perf_counter()
    print(f"{end_t - start_t:.6f} seconds")
    df1 = pd.read_parquet(path)
    print(df1)
    df2 = mp.pq_extract_stages(str(path))
    print(df2)
    print(df2.columns)
    print(df2.index)
    # row = df1.loc[600]
    # print(", ".join(f"{v}" for k, v in row.items()))

@cache
def test_export_parquet_8() -> None:
    from pathlib import Path
    import time

    start_t = time.perf_counter()
    alg = mp.Algorithm(8)
    alg.auto_resolve_stage()
    scope = mp.truth_scope((1, 255), (1, 65535))
    df = mp.truth_dataframe(scope, alg)
    end_t = time.perf_counter()
    pd.set_option('display.max_columns', None)
    print(df.head())
    print(df.info())
    print(f"{end_t - start_t:.6f} seconds")
    path = Path(__file__).parent.parent.parent / 'examples/datasets/example_8b_mult_truthtable.parquet'
    print(path)
    start_t = time.perf_counter()
    df.to_parquet(path)
    end_t = time.perf_counter()
    print(f"{end_t - start_t:.6f} seconds")
    # df1 = pd.read_parquet(path)
    # row = df1.loc[600]
    # print(", ".join(f"{v}" for k, v in row.items()))




def main() -> None:
    # import cProfile
    # import pstats
    test_export_parquet_4()
    # test_export_parquet_8()
    # test = cProfile.Profile()
    # test.enable()
    # test_export_parquet_8()
    # test.disable()
    # pstats.Stats(test).strip_dirs().sort_stats("time").print_stats(30)



if __name__ == "__main__":
    main()
