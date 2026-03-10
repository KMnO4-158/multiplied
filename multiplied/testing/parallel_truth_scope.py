import multiplied as mp
from pathlib import Path


def main() -> None:
    from multiplied.core.truth import truth_multi_parquet
    from time import perf_counter
    import pandas as pd

    DOMAIN = (1, (2**8) - 1)
    RANGE = (1, (2**16) - 1)

    # for i in batch_truth_scope(DOMAIN, RANGE, WORKERS):
    #     print(i)

    # for i in batch_truth_scope(DOMAIN, RANGE, WORKERS):
    #     print(list(mp.truth_scope(i[0], i[1])))

    alg = mp.Algorithm(8)
    alg.auto_resolve_stage()
    # pkl_alg = test_obj_pickling(alg)
    # print(pkl_alg)

    path = Path(__file__).parent.parent.parent / "examples/datasets/test_multi"

    start = perf_counter()
    truth_multi_parquet(path, DOMAIN, RANGE, alg)
    end = perf_counter()
    print(f"\tTime: {end - start}")

    df = pd.read_parquet(path)
    pd.set_option("display.max_rows", None)

    print(df.head())
    print(df.tail())
    # print(df)

    start = perf_counter()
    scope = mp.truth_scope(DOMAIN, RANGE)
    df = mp.truth_dataframe(scope, alg)
    df.to_parquet(path.parent / "test_df.parquet")
    end = perf_counter()
    print(f"\tTime: {end - start}")
    # import pandas as pd
    # import pyarrow as pa

    # print(pa.Schema.from_pandas(df, preserve_index=False))


if __name__ == "__main__":
    main()
