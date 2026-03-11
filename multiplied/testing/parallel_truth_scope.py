from typing import Generator
import multiplied as mp
from pathlib import Path



def _batch_truth_scope(
    domain_: tuple[int, int], range_: tuple[int, int], workers: int
) -> Generator[tuple[tuple[int, int], tuple[int, int]]]:
    from math import log2
    if workers % 2 != 0:
        raise ValueError("workers must be even")
    if workers > 64:
        raise ValueError("workers must be less than or equal to 64")

    min_in, max_in = domain_
    min_out, max_out = range_

    if (max_in - min_in)**2 < 1000 or (max_out - min_out) < 100 or workers == 1:
        yield (domain_, range_)
        return

    # chosen heuristics are a band-aid until a proper solution is found
    print(1.04 - (1/log2(max_in - min_in))/1)
    scale = 1.04 - (1/log2(max_in - min_in))/1  # heuristic
    # scale = 0.5
    print((max_in - min_in)**2)
    print((max_out - min_out)**2)


    if workers == 2:
        adjusted_min_out = int((max_out - min_out) / (5 * scale))  # heuristic
        yield (domain_, (min_out, adjusted_min_out) )
        yield (domain_, (adjusted_min_out + 1, max_out))
        return

    batch_size = (max_out - min_out + 1) // workers

    offset = int((batch_size + 1) * scale)
    balance = [0] * workers

    for i in range(workers):
        if i == 0:
            balance[i] = -int(offset *(scale))
            continue
        balance[i] = balance[i - 1] + (int(offset*(scale)) >> (i + 3))

    print(balance)
    print("balance", sum(balance))
    # dist = -int(sum(balance) // ((workers + 2) * scale))
    dist = -int(sum(balance)) // workers
    print("dist", dist)
    for i in range(workers):
        balance[-i - 1] += dist # >> int(i*scale)
        # balance[i] -= dist

    print("balance", sum(balance))
    rem = sum(balance)
    print("remainder", rem)
    if rem < 0:
        # balance[0] -= int(rem*(1-scale))
        balance[-1] -= int(rem*scale)
    print(balance)

    # for i in range(workers >> 1):
    #     if i == 0:
    #         balance[i] = -(offset >> 1)
    #         continue
    #     balance[i] = -(offset >> i)

    # for i in range(workers >> 1):
    #     balance[-i - 1] = abs(balance[i])


    print(batch_size, domain_, range_)

    r_min_chunk = min_out
    for w in range(workers):
        r_max_chunk = r_min_chunk + (w + batch_size ) - 1  + balance[w]
        if r_max_chunk > max_out:
            r_max_chunk = max_out


        adjust_min_in = int(r_min_chunk ** (1/2))
        yield ((adjust_min_in, max_in), (r_min_chunk, r_max_chunk))
        r_min_chunk = r_max_chunk + 1



def batch_truth_scope(
    domain_: tuple[int, int], range_: tuple[int, int], workers: int
) -> Generator[tuple[tuple[int, int], tuple[int, int]]]:

    min_in, max_in = domain_
    min_out, max_out = range_
    total = max_out - min_out + 1

    base = total // workers                      # base size per worker
    rem = total % workers                        # remainder to distribute

    start = min_out
    for w in range(workers):
        size = base + (1 if w < rem else 0)      # give one extra to first 'rem' workers
        if size <= 0:
            r_min_chunk = r_max_chunk = start - 1  # empty chunk if more workers than items
        else:
            r_min_chunk = start
            r_max_chunk = start + size - 1
            start = r_max_chunk + 1
        if r_max_chunk > max_out:
            r_max_chunk = max_out

        adjust_min_in = int(r_min_chunk ** (1/2))
        yield ((adjust_min_in, max_in), (r_min_chunk, r_max_chunk))




def main() -> None:
    from multiplied.core.truth import truth_multi_parquet
    from time import perf_counter
    import pandas as pd


    DOMAIN = (1, (2**8) - 1)
    RANGE = (1, (2**16) - 1)
    WORKERS = 8

    offset = (RANGE[1] + 1)// WORKERS

    balance = [0] * WORKERS

    # balance = [-(offset) >> i for i in range(WORKERS)]
    # print(balance)

    # for i in _batch_truth_scope(DOMAIN, RANGE, WORKERS):
    #     print(i)

    # count = 0
    # start = perf_counter()
    # for i in _batch_truth_scope(DOMAIN, RANGE, WORKERS):
    #     scope_len = len(list(mp.truth_scope(i[0], i[1])))
    #     print(scope_len)
    #     count += scope_len
    # end = perf_counter()
    # print(f"Elapsed: {end - start}s")
    # start = end
    # print(count)

# -------------------------------------------------------------------

    """

    ((1, 255), (1, 8192))
    ((1, 255), (8193, 16384))
    ((1, 255), (16385, 24576))
    ((1, 255), (24577, 32768))
    ((1, 255), (32769, 40960))
    ((1, 255), (40961, 49152))
    ((1, 255), (49153, 57344))
    ((1, 255), (57345, 65535))
    24952
    13838
    9542
    6775
    4687
    3049
    1678
    504

    """

    # for i in batch_truth_scope(DOMAIN, RANGE, WORKERS):
    #     print(i)

    # for i in batch_truth_scope(DOMAIN, RANGE, WORKERS):
    #     print(len(list(mp.truth_scope(i[0], i[1]))))


    # # pkl_alg = test_obj_pickling(alg)
    # # print(pkl_alg)
    alg = mp.Algorithm(8)
    alg.auto_resolve_stage()

    path = Path(__file__).parent.parent.parent / "examples/datasets/test_multi_new_batch_width"

    start = perf_counter()
    truth_multi_parquet(path, DOMAIN, RANGE, alg)
    end = perf_counter()
    print(f"\tTime: {end - start}")

    df = pd.read_parquet(path)
    pd.set_option("display.max_rows", None)

    print(df.head())
    print(df.tail())
    # print(df)

    # start = perf_counter()
    # scope = mp.truth_scope(DOMAIN, RANGE)
    # df = mp.truth_dataframe(scope, alg)
    # df.to_parquet(path.parent / "test_df.parquet")
    # end = perf_counter()
    # print(f"\tTime: {end - start}")


    # import pandas as pd
    # import pyarrow as pa

    # print(pa.Schema.from_pandas(df, preserve_index=False))


if __name__ == "__main__":
    main()
