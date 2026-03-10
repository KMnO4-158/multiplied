from multiprocessing import Queue, Process
import tempfile

from pandas.core.generic import pickle
from pandas.io.parquet import os
import multiplied as mp
from typing import Any, Generator
from pathlib import Path


def truth_scope_worker(in_q: Queue, worker_id: int):
    # print(f"worker {worker_id} started (pid {os.getpid()})", flush=True)
    # process item
    domain_, range_ = in_q.get()
    gen = mp.truth_scope(domain_, range_)


def producer(
    gen: Generator,
    out_q: Queue,
    workers: list[Process],
):
    for item in gen:
        out_q.put(item)
    # send one sentinel per worker
    for _ in range(len(workers)):
        out_q.put(None)


def batch_truth_scope(
    domain_: tuple[int, int], range_: tuple[int, int], workers: int
) -> Generator[tuple[tuple[int, int], tuple[int, int]]]:

    min_in, max_in = domain_
    min_out, max_out = range_
    batch_size = (max_out - min_out + 1) // workers

    for w in range(workers):
        r_min_chunk = min_out + w * batch_size
        r_max_chunk = r_min_chunk + batch_size - 1
        if r_max_chunk > max_out:
            r_max_chunk = max_out
        yield (domain_, (r_min_chunk, r_max_chunk))


def parallel_truth_scope(
    domain_: tuple[int, int],
    range_: tuple[int, int],
    workers: int,
) -> None:

    task_q = Queue(maxsize=workers)
    procs = [
        Process(target=truth_scope_worker, args=(task_q, i)) for i in range(workers)
    ]
    for p in procs:
        p.start()

    producer(batch_truth_scope(domain_, range_, workers), task_q, procs)

    for p in procs:
        p.join()


def linear_range_gen(domain_: tuple[int, int], range_: tuple[int, int]) -> list[Any]:

    test = list(mp.truth_scope(domain_, range_))


def _write_temp_pickle_atomic(obj: mp.Algorithm) -> str:
    # create temp file in same dir, write to a unique tmp file, then atomically move to final name
    dirpath = tempfile.gettempdir()
    final = Path(dirpath) / f"algorithm_sharedobj_{os.getpid()}.pkl"
    tmp = Path(str(final) + ".writing")
    try:
        with open(tmp, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        # make atomic
        os.replace(tmp, final)
        os.chmod(final, 0o444)  # optional read-only
        return str(final)
    except Exception:
        try:
            tmp.unlink()
        except Exception:
            pass
        raise


def _load_shared_pickle(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)


def test_obj_pickling(obj: mp.Algorithm):

    temp_path = _write_temp_pickle_atomic(obj)
    loaded = _load_shared_pickle(temp_path)
    assert isinstance(loaded, mp.Algorithm)

    try:
        os.unlink(temp_path)
    except FileNotFoundError:
        pass

    return loaded


def main() -> None:
    from multiplied.core.truth import truth_multi_parquet
    from time import perf_counter
    import pandas as pd

    DOMAIN = (1, (2**8) - 1)
    RANGE = (1, (2**16) - 1)
    WORKERS = 8

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
