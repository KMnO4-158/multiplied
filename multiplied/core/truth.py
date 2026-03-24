###################################
# Generate Multiplier Truth Table #
###################################

from pathlib import Path

from .algorithm import Algorithm
from .matrix import Matrix
from multiprocessing import Pool, Process, Queue, cpu_count
from collections.abc import Generator
import pandas as pd
import tempfile
import pickle
import os


def truth_scope(
    domain_: tuple[int, int], range_: tuple[int, int]
) -> Generator[tuple[int, int]]:
    """Yields (a, b) from domain such that it's product (ab) lies within range

    Parameters
    ----------
    domain_: tuple[int,int]
        The maximum range of values operands a and b can be.

    range_: tuple[int,int]
        Limit a and b to range_min <= a * b <= range_max

    Yields
    ------
    tuple:
        (operand_a, operand_b)
    """

    if not all([isinstance(d, int) for d in domain_]):
        raise TypeError("Domain must be a tuple of integers.")
    if not all([isinstance(r, int) for r in range_]):
        raise TypeError("Range must be a tuple of integers.")

    min_in, max_in = domain_
    min_out, max_out = range_

    if min_in <= 0 or min_out <= 0:
        raise ValueError("Minimum input and output values must be greater than zero.")
    if (min_in > max_in) or (min_out > max_out):
        raise ValueError(
            f"Domain: {domain_} and range: {range_} must satisfy a <= b and c <= d."
        )

    if max_in**2 < min_out:
        raise ValueError(f"Range {range_} unreachable for the input domain {domain_}")

    # if min_out < min_in:
    #     warnings.warn(
    #         f"Loose domain and range alignment: min_out < min_in [{min_out} < {min_in}]"
    #     )
    # if max_out < max_in:
    #     warnings.warn(
    #         f"Loose domain and range alignment: min_out < max_in [{max_out} < {max_in}]"
    #     )

    x = min_in
    while x <= max_in:
        lower_bound = min_in
        if min_out // x >= min_in:
            lower_bound = min_out // x

        upper_bound = max_in
        if max_out // x <= max_in:
            upper_bound = max_out // x

        # lower_bound = min_out // x if min_out // x >= min_in else min_in
        # upper_bound = max_out // x if max_out // x <= max_in else max_in
        for y in range(lower_bound, upper_bound + 1):
            prod = x * y
            if min_out <= prod <= max_out:
                yield (x, y)
            if max_out < prod:
                break
        x += 1


def shallow_truth_table(scope: Generator[tuple], alg: Algorithm) -> Generator[Matrix]:
    """Return Generator of partial product matrices for all operand tuples"""

    return (Matrix(alg.bits, a=a, b=b) for a, b in scope)


def truth_table(scope: Generator, alg: Algorithm) -> Generator[dict]:
    """A generator which yields all stages of an algorithm for a given
    set of operands a, b.

    Parameters
    ----------
    scope : Generator
        A generator which yields tuples of operands a, b.
    alg : Algorithm
        An instance of the Algorithm class.


    Returns
    -------
    Generator[dict]
        A generator which yields all stages of an algorithm for a given
        set of operands a, b.


    """
    if not isinstance(scope, Generator):
        raise TypeError("Scope must be a generator.")
    if not isinstance(alg, Algorithm):
        raise TypeError(f"Expected Algorithm instance got {type(alg)}")

    for a, b in scope:
        yield alg.exec(a=a, b=b)


def _dataframe_operand_worker(a: int, b: int) -> tuple:
    return (a, b, a * b)


def _dataframe_pretty_worker(a: int, b: int, alg: Algorithm) -> list:
    pretty = []
    for matrix in alg.exec(a=a, b=b).values():
        pretty.append(str(matrix).split("\n")[:-1])
    return pretty


def _dataframe_entry_worker(a: int, b: int, alg: Algorithm) -> dict:
    entry = {}
    for stage, matrix in alg.exec(a=a, b=b).items():
        for r, row in enumerate(matrix):
            for b, bit in enumerate(row[::-1]):
                entry[f"s{stage}_p{r}_b{b}"] = 1 if bit == "1" else 0
    return entry


def truth_dataframe(scope: Generator[tuple[int, int]], alg: Algorithm) -> pd.DataFrame:
    """Execute algorithm using each pair of operands from the scope.

    Parameters
    ----------
    scope : Generator[tuple[int, int]]
        A generator that yields pairs of integers (a, b) to be used as operands.
    alg : Algorithm
        An instance of the Algorithm class representing the algorithm to be executed.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the truth table for the given algorithm.
    """
    if not isinstance(scope, Generator):
        raise TypeError("Scope must be a generator.")
    if not isinstance(alg, Algorithm):
        raise TypeError(f"Expected Algorithm instance got {type(alg)}")

    # -- duplicate generators for each pool -------------------------
    from itertools import tee

    scope1, scope2, scope3 = tee(scope, 3)

    # Uses every available core
    with Pool() as pool:
        operands = pool.starmap(_dataframe_operand_worker, scope1)
        pretty = pool.starmap(
            _dataframe_pretty_worker, ((a, b, alg) for a, b in scope2)
        )
        data = pool.starmap(_dataframe_entry_worker, ((a, b, alg) for a, b in scope3))
        pool.close()
        pool.join()

    col = [""] * ((len(alg) + 1) * alg.bits * (alg.bits << 1))
    ppm_s_col = [""] * (len(alg) + 1)
    n = 0
    for i in range(len(alg) + 1):
        for j in range(alg.bits):
            for k in range((alg.bits << 1) - 1, -1, -1):
                col[n] = f"s{i}_p{j}_b{k}"
                n += 1
        ppm_s_col[i] = f"ppm_s_{i}"

    operand_columns = pd.DataFrame(
        operands, columns=["a", "b", "output"], dtype="int32"
    )
    pretty_columns = pd.DataFrame(pretty, columns=ppm_s_col, dtype="str")
    table = pd.DataFrame(data, columns=col).astype("int8")

    return pd.concat([operand_columns, table, pretty_columns], axis=1)


# ===================================================================


def _multi_parquet_worker(gen: Generator, alg: Algorithm) -> pd.DataFrame:

    operands = []
    pretty = []
    data = []

    for a, b in gen:
        operands.append((a, b, a * b))
        entry = {}
        pretty_matrix = []
        for stage, matrix in alg.exec(a=a, b=b).items():
            pretty_matrix.append(matrix.__str__().split("\n")[:-1])
            for r, row in enumerate(matrix):
                for b, bit in enumerate(row[::-1]):
                    entry[f"s{stage}_p{r}_b{b}"] = 0 if bit in ["_", "0"] else 1
        data.append(entry)
        pretty.append(pretty_matrix)

    col = [""] * ((len(alg) + 1) * alg.bits * (alg.bits << 1))
    ppm_s_col = [""] * (len(alg) + 1)
    n = 0
    for i in range(len(alg) + 1):
        for j in range(alg.bits):
            for k in range((alg.bits << 1) - 1, -1, -1):
                col[n] = f"s{i}_p{j}_b{k}"
                n += 1
        ppm_s_col[i] = f"ppm_s_{i}"

    operand_columns = pd.DataFrame(
        operands, columns=["a", "b", "output"], dtype="int32"
    )
    pretty_columns = pd.DataFrame(pretty, columns=ppm_s_col, dtype="str")
    table = pd.DataFrame(data, columns=col).astype("int8")

    return pd.concat([operand_columns, table, pretty_columns], axis=1)


def _write_temp_pickle_atomic(obj: Algorithm) -> str:
    # create temp file in same dir, write to a unique tmp file, then atomically move to final name
    # avoids workers from racing and reading partial data
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


def _truth_scope_worker(dir: Path, tmp_file: str, in_q: Queue, worker_id: int):
    # print(f"worker {worker_id} started (pid {os.getpid()})", flush=True)
    # process item
    domain_, range_ = in_q.get()
    algorithm = _load_shared_pickle(tmp_file)
    if not isinstance(algorithm, Algorithm):
        raise TypeError("Expected Algorithm instance")
    gen = truth_scope(domain_, range_)
    df = _multi_parquet_worker(gen, algorithm)
    df.to_parquet(dir / f"part_{worker_id}_pid_{os.getpid()}.parquet")


def _batch_producer(
    gen: Generator,
    out_q: Queue,
    workers: list[Process],
):
    for item in gen:
        out_q.put(item)
    # send one sentinel per worker
    for _ in range(len(workers)):
        out_q.put(None)


def _batch_truth_scope(
    domain_: tuple[int, int], range_: tuple[int, int], workers: int
) -> Generator[tuple[tuple[int, int], tuple[int, int]]]:
    from math import log2
    import warnings

    min_in, max_in = domain_
    min_out, max_out = range_

    slope = (max_in - min_in) / (max_out - min_out)

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
    out_batch_size = (max_out - min_out + 1) // workers

    acc = 0
    for n in range(min_out, max_out + 1):
        # over/under estimate is accounted for later
        acc += out_batch_size // n

    # -- distribute linear offsets ----------------------------------
    for i in range((workers)):
        balance[i] = -int(((acc) * (1 - (slope))) // (i + 12))

    # -- distribute dyadic (?) offsets ------------------------------
    for i in range((workers) >> ((max_in - min_in + 2) >> workers)):
        balance[-i - 1] += int(((acc) * (1 - slope))) >> (i + 3)

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

    # ==============================================================

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


def truth_multi_parquet(
    dir: Path | str,
    domain_: tuple[int, int],
    range_: tuple[int, int],
    alg: Algorithm,
    workers: int = cpu_count(),
) -> None:
    """Generate a truth table and save it to a multi-part Parquet directory.

    Parameters
    ----------
    dir : Path | str
        Directory to store multi-part .parquet files

    domain_: tuple[int,int]
        The maximum range of values operands a and b can be.

    range_: tuple[int,int]
        Limit a and b to range_min <= a * b <= range_max

    alg : Algorithm
        An instance of the Algorithm class.

    workers : int=cpu_count()
        number of .parquet files to create in parallel

    """

    if not isinstance(dir, Path):
        dir = Path(dir)
    if dir.suffix != "":
        # print(dir.suffix)
        raise ValueError(f"Output directory {dir} must be a directory, not a file.")
    if workers % 2 != 0:
        raise ValueError("workers must be even")
    if workers > 64:
        raise ValueError("workers must be less than or equal to 64")

    dir.mkdir(parents=True)

    alg_pkl_path = _write_temp_pickle_atomic(alg)

    task_q = Queue(maxsize=workers)
    procs = [
        Process(target=_truth_scope_worker, args=(dir, alg_pkl_path, task_q, i))
        for i in range(workers)
    ]
    for p in procs:
        p.start()

    _batch_producer(_batch_truth_scope(domain_, range_, workers), task_q, procs)

    for p in procs:
        p.join()

    try:
        os.unlink(alg_pkl_path)
    except FileNotFoundError:
        pass
