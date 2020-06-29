import random
import time

from tqdm import tqdm

from src.structures.rmq import FischerHeunRMQ, HybridRMQ, PrecomputedRMQ, SparseTableRMQ

ProposedRMQ = FischerHeunRMQ
RMQ = SparseTableRMQ


def print_arr_with_index(data, low):
    result = f"\nIndex | Data\n{'-' * 15}\n"
    for i, value in enumerate(data):
        result += f"{low+i if low else i:5d} | {value}\n"
    return result


def run_tests(minimum, maximum, step, num_builds, num_queries, verbose=False):
    for _ in range(minimum, maximum + 1, step):
        data = [random.randint(minimum, maximum - 1) for _ in range(maximum)]

        total_build_time_ref, total_build_time_test = 0, 0
        total_run_time_ref, total_run_time_test = 0, 0
        for _ in tqdm(range(num_builds), disable=not verbose):
            # Generate reference RMQ
            t_start = time.perf_counter()
            reference_rmq = RMQ(data)
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
                    f"Val at index {ours}: {data[ours]}, Val at index {theirs}: {data[theirs]}"
                )
        if verbose:
            print(f"Mean Reference Build Time: {total_build_time_ref / num_builds}")
            print(f"Mean Reference Query Time: {total_run_time_ref / (num_builds * num_queries)}")
            print(f"Mean Test Build Time: {total_build_time_test / num_builds}")
            print(f"Mean Test Query Time: {total_run_time_test / (num_builds * num_queries)}")
    if verbose:
        print("Tests completed!")


def test_rmq():
    random.seed(0)
    run_tests(0, 1, 1, 10, 100)
    run_tests(15, 25, 4, 10, 100)
    # run_tests(10, 25, 15, 100, 1000)
    # run_tests(0, 10000, 5000, 100, 10000)
