from time import perf_counter
from typing import Generator
import warnings
import multiplied as mp


def _batch_truth_scope(
    domain_: tuple[int, int], range_: tuple[int, int], workers: int
) -> Generator[tuple[tuple[int, int], tuple[int, int]]]:
    from math import log2

    print(domain_, range_, log2(range_[1] + 1))
    min_in, max_in = domain_
    min_out, max_out = range_

    slope = (max_in - min_in) / (max_out - min_out)
    print(slope)

    if (max_in - min_in) ** 2 < 1000 or (max_out - min_out) < 256:
        if workers > 1:
            warnings.warn("workers > 1 not recommended for small domains/ranges")
        yield (domain_, range_)
        return

    if workers == 2:
        adjusted_min_out = int((max_out - min_out) >> int(2 / (1 + slope)))  # heuristic
        yield (domain_, (min_out, adjusted_min_out))
        yield (domain_, (adjusted_min_out + 1, max_out))
        return

    in_batch_size = (max_in - min_in + 1) // workers
    out_batch_size = (max_out - min_out + 1) // workers
    print(f"in batch: {in_batch_size}")
    print(f"out batch: {out_batch_size}")

    first_last_ratio = in_batch_size / out_batch_size
    print(first_last_ratio)

    # heuristic balances operands / batch ===========================
    #
    # The first batch of a given scope(DOMAIN, RANGE), will always
    # produce the most operands. For complete truth tables the
    # difference is at least one order of magnitude.
    #
    # Using an estimate (acc)
    #

    balance = [0] * workers  # heuristic scaling per batch

    # -- approximate operands in first batch ------------------------
    acc = 0
    for n in range(min_out, max_out + 1):
        # over/under estimate is accounted for later
        acc += out_batch_size // n
    print(acc)

    # -- distribute linear offsets ----------------------------------
    for i in range((workers)):
        balance[i] = -int(((acc) * (1 - (slope))) // (i + 12))

    print(((max_in - min_in + 2) >> workers))
    # -- distribute dyadic (?) offsets ------------------------------
    for i in range((workers) >> ((max_in - min_in + 2) >> workers)):
        balance[-i - 1] += int(((acc) * (1 - slope))) >> (i + 3)

    print(sum(balance))

    # -- clamp to original range ------------------------------------
    rem = -sum(balance)

    # domain far from range
    if slope < 0.01:
        for i in range((workers)):
            balance[-i - 1] += rem >> int(log2(workers) + i)

        final = sum(balance)
        balance[-1] += -int(final * 0.95) + 1  # collect 95% of remainder to final batch
        balance[(workers >> 1) - 1] += -int(final * 0.05)  # 5% applied to low midpoint

    # domain close to range
    else:
        for i in range((workers)):
            balance[i] += rem >> int(log2(workers))

    print("rem", rem)
    print(sum(balance))
    # ==============================================================

    print(balance)

    r_min_chunk = min_out
    for w in range(workers):
        if w == 0:
            r_max_chunk = out_batch_size + balance[w]
        else:
            r_max_chunk = r_min_chunk + out_batch_size + balance[w]
        if r_max_chunk > max_out:
            r_max_chunk = max_out

        adjust_max_in = min(max_in, r_max_chunk)
        yield ((min_in, adjust_max_in), (r_min_chunk, r_max_chunk))
        r_min_chunk = r_max_chunk + 1


def main() -> None:
    # from multiplied.core.truth import truth_multi_parquet
    # import pandas as pd
    # from pathlib import Path

    DOMAIN = (1, (2**8) - 1)
    RANGE = (1, (2**16) - 1)
    WORKERS = 8

    # offset = (RANGE[1] + 1)// WORKERS
    # balance = [0] * WORKERS
    # balance = [-(offset) >> i for i in range(WORKERS)]
    # print(balance)

    for i in _batch_truth_scope(DOMAIN, RANGE, WORKERS):
        print(i)
    count = 0
    operands = set()
    start = perf_counter()
    for i in _batch_truth_scope(DOMAIN, RANGE, WORKERS):
        scope = list(mp.truth_scope(i[0], i[1]))
        count += len(scope)
        print(len(scope))
        operands |= set(scope)
    end = perf_counter()
    print(f"Elapsed: {end - start}s")
    start = end
    print(count)
    print(len(operands))
    # -------------------------------------------------------------------

    # for i in batch_truth_scope(DOMAIN, RANGE, WORKERS):
    #     print(i)

    # for i in batch_truth_scope(DOMAIN, RANGE, WORKERS):
    #     print(len(list(mp.truth_scope(i[0], i[1]))))

    # # pkl_alg = test_obj_pickling(alg)
    # # print(pkl_alg)
    # alg = mp.Algorithm(8)
    # alg.auto_resolve_stage()
    # for i in alg.exec(255, 255).values():
    #     print(i)
    # print(alg)
    # path = Path(__file__).parent.parent.parent / "examples/datasets/test_multi_new_map"

    # start = perf_counter()
    # truth_multi_parquet(path, DOMAIN, RANGE, alg)
    # end = perf_counter()
    # print(f"\tTime: {end - start}")

    # df = pd.read_parquet(path)
    # pd.set_option("display.max_rows", None)

    # print(df.head())
    # print(df.tail())
    # # print(df)

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
