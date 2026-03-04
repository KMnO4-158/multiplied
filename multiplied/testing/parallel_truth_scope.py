from multiprocessing import Queue, Process, cpu_count
import warnings
import multiplied as mp
from typing import Any, Generator

def oprands(a_start, a_end, b_start, b_end):
    for a in range(a_start, a_end):
        for b in range(b_start, b_end + 1):
            yield (a, b)
            yield (b, a)


def worker(in_q: Queue, result_q: Queue, worker_id: int):
    while True:
        item = in_q.get()
        if item is None:          # sentinel to stop
            break
        # process item
        print(f"worker {worker_id} got {item}")
        a_start, a_end, b_start, b_end = item
        data = list(oprands(a_start, a_end, b_start, b_end))
        result_q.put(data)
    result_q.put(None)

def producer(
    gen: Generator,
    out_q: Queue,
    n_workers: int,
):
    for item in gen:
        out_q.put(item)
    # send one sentinel per worker
    for _ in range(n_workers):
        out_q.put(None)


def batch_truth_scope(
    domain_: tuple[int, int],
    range_: tuple[int, int],
    batch_size: int=1000
) -> Generator[Generator[tuple[int, int]]]:

    if batch_size < domain_[1]:
        raise ValueError("Batch size must be at least domain max")
    if batch_size < 100:
        warnings.warn("Detected small batch size, consider increasing")

    # + IMAGINARY SANITY CHECKS


    min_in, max_in = domain_

    batches = ((max_in * (max_in - min_in + 1)) // batch_size)
    if batches == 0:
        batches = 1
        batch_size = max_in

    # # In Multiplied implementation use WORKERS (batches) as a
    # print(f"Batches: {batches}")
    # print(f"Batch Size: {batch_size}")
    # print(f"Total items: {(max_in * (max_in - min_in + 1))}")


    b_start, b_end = domain_
    a_start = min_in
    for batch in range(batches):
        a_end = a_start + batch_size

        yield (a_start, a_end, b_start, b_end)
        a_start = a_end

def parallel_range_gen(
    domain_: tuple[int, int],
    range_: tuple[int, int],
    batch_size: int,
) -> list[list]:

    min_in, max_in = domain_

    batches = ((max_in * (max_in - min_in + 1)) // batch_size)
    if batches == 0:
        batches = 1
        batch_size = max_in

    # In Multiplied implementation use WORKERS (batches) as a
    print(f"Batches: {batches}")
    print(f"Batch Size: {batch_size}")
    print(f"Total items: {(max_in * (max_in - min_in + 1))}")

    task_q = Queue(maxsize=100)
    result_q = Queue()
    procs = [Process(target=worker, args=(task_q, result_q, i)) for i in range(batches)]

    for p in procs:
        p.start()

    producer(batch_truth_scope(domain_, range_, batch_size), task_q, batches)

    # collect results until we see n_workers None sentinels
    done = 0
    results = []
    while done < batches:
        r = result_q.get()
        if r is None:
            done += 1
        else:
            results.append(r)

    for p in procs:
        p.join()

    print(procs)
    # print(results)

    return results


def linear_range_gen(
    domain_: tuple[int, int],
    range_: tuple[int, int]
) -> list[list[Any]]:

    return [[t for t in mp.truth_scope(domain_, range_)]]



def main() -> None:
    # itertools.product([i for i in DOMAIN[1]], repeat=2)
    DOMAIN = (1, 1000)
    RANGE = (1, 10000)
    BATCH_SIZE = 10000
    ranges = parallel_range_gen(DOMAIN, RANGE, BATCH_SIZE)
    for i in ranges:
        print(i)

if __name__ == "__main__":
    main()
