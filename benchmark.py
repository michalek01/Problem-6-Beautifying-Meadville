"""Compare backtracking and greedy planting runtimes."""

import argparse
from statistics import median
from time import perf_counter

from tree_planting import plant_trees_backtracking, plant_trees_greedy


def time_algorithm(algorithm, tree_count, plots, repeats):
    samples = []
    for _ in range(repeats):
        start = perf_counter()
        result = algorithm(tree_count, plots)
        samples.append(perf_counter() - start)
        if result != (False, []):
            raise RuntimeError("benchmark workload should be infeasible")
    return median(samples)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be at least 1")

    sizes = (8, 12, 16, 20, 24)
    print("plots,requested,backtracking_seconds,greedy_seconds")
    for size in sizes:
        plots = [0] * size
        tree_count = size // 2 + 1
        backtracking_time = time_algorithm(
            plant_trees_backtracking, tree_count, plots, args.repeats
        )
        greedy_time = time_algorithm(plant_trees_greedy, tree_count, plots, args.repeats)
        print(f"{size},{tree_count},{backtracking_time:.9f},{greedy_time:.9f}")


if __name__ == "__main__":
    main()