import random
import time

from tqdm import trange

from cs.structures import RMQ, FischerHeunRMQ, HybridRMQ, PrecomputedRMQ, SparseTableRMQ

ReferenceRMQ = PrecomputedRMQ
ProposedRMQ = FischerHeunRMQ


def construct_rmq(rmq_type: str, data: list[int]) -> RMQ:
    rmq_map = {
        constructor.__name__: constructor
        for constructor in (FischerHeunRMQ, HybridRMQ, PrecomputedRMQ, SparseTableRMQ)
    }
    return rmq_map[rmq_type](data)


def print_arr_with_index(data: list[int], low: int) -> str:
    result = f"\nIndex | Data\n{'-' * 15}\n"
    for i, value in enumerate(data):
        result += f"{low+i if low else i:5d} | {value}\n"
    return result


def run_tests(minimum: int, maximum: int, num_builds: int, num_queries: int) -> None:
    print((minimum, maximum), num_builds, num_queries)
    data = [random.randint(minimum, maximum - 1) for _ in range(maximum)]

    total_build_time_ref, total_build_time_test = 0.0, 0.0
    total_run_time_ref, total_run_time_test = 0.0, 0.0
    for _ in trange(num_builds):
        # Generate reference RMQ
        t_start = time.perf_counter()
        reference_rmq = ReferenceRMQ(data)
        t_end = time.perf_counter()
        total_build_time_ref += t_end - t_start

        # Generate testing RMQ
        t_start = time.perf_counter()
        proposed_rmq = ProposedRMQ(data)
        t_end = time.perf_counter()
        total_build_time_test += t_end - t_start

        for _ in range(num_queries):
            low = random.randint(minimum, maximum - 1)
            high = random.randint(minimum, maximum - 1)
            if low > high:
                low, high = high, low
            high += 1

            # Run reference query
            t_start = time.perf_counter()
            ours = reference_rmq.rmq(low, high)
            t_end = time.perf_counter()
            total_run_time_ref += t_end - t_start

            # Run test query
            t_start = time.perf_counter()
            theirs = proposed_rmq.rmq(low, high)
            t_end = time.perf_counter()
            total_run_time_test += t_end - t_start

            if theirs < 0 or theirs > len(data):
                print(f"Out of bounds {theirs}")

            if theirs < low or theirs >= high:
                print(f"\n *** Index out of bounds: {theirs} *** \n")

            assert data[ours] == data[theirs], (
                f"Error: query produced the wrong answer:\n\n"
                f"Query: Low: {low}, High: {high}\n"
                f"{print_arr_with_index(data[low: high], low)}\n"
                f"Solution Index: {ours}, Your Index: {theirs}\n\n"
                f"Val at index {ours}: {data[ours]}, "
                f"Val at index {theirs}: {data[theirs]}"
            )
    build_queries = num_builds * num_queries
    print(
        f"Mean Reference Build Time: {total_build_time_ref / num_builds}\n"
        f"Mean Reference Query Time: {total_run_time_ref / build_queries}\n"
        f"Mean Proposed Build Time: {total_build_time_test / num_builds}\n"
        f"Mean Proposed Query Time: {total_run_time_test / build_queries}"
    )
    print("Tests completed!\n")


if __name__ == "__main__":
    random.seed(0)
    run_tests(0, 1, 10, 50)
    run_tests(22, 25, 10, 100)
    run_tests(100, 500, 100, 500)
    # run_tests(0, 10000, 5000, 100)
