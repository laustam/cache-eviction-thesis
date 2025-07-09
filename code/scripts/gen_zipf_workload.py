import random
import math
import argparse
from collections import Counter
import os
import matplotlib.pyplot as plt

WORKLOAD_FILE_SAVE_PATH = "../data/synthetic_data"


def get_zipf_workload(num_unique: int, num_requests: int, alpha: int, debug: bool) -> list[int]:
    print(
        f"Number unique: {num_unique}, Number of requests: {num_requests}, Alpha: {alpha}")

    harmonic_sum: list[float] = sum(
        # normalise values so sum = 1
        1 / (i ** alpha) for i in range(1, num_unique + 1))
    probabilities: list[float] = [
        1 / (i ** alpha * harmonic_sum) for i in range(1, num_unique + 1)]
    cumulative_probabilities: list[float] = [
        sum(probabilities[:i+1]) for i in range(len(probabilities))]

    workload: list[int] = []
    for _ in range(num_requests):
        random_num: float = random.random()
        for i, cumulative_prob in enumerate(cumulative_probabilities):
            if random_num <= cumulative_prob:
                workload.append(i + 1)  # items are 1-indexed
                break

    if (debug):
        distribution = Counter(workload)
        sorted_distribution = dict(sorted(distribution.items()))
        print(f"Distribution: {sorted_distribution}")

    return workload


def file_save_workload(workload: list[int], filename: str):

    os.makedirs(WORKLOAD_FILE_SAVE_PATH, exist_ok=True)
    dir_path = WORKLOAD_FILE_SAVE_PATH.rstrip("/")

    output_path = os.path.join(dir_path, filename)
    base, ext = os.path.splitext(output_path)
    counter = 1
    while os.path.exists(output_path):
        output_path = f"{base}({counter}){ext}"
        counter += 1

    with open(output_path, "w") as f:
        for item in workload:
            f.write(f"{item}\n")

    print(f"Workload saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="Zipfian workload generator",
                                     description="This script generates Zipfian workloads")
    parser.add_argument('num_requests', type=int,
                        help='Number of requests to generate')
    unique_values = parser.add_mutually_exclusive_group(required=False)
    unique_values.add_argument('--num-unique', type=int,
                               help='Number of unique items (must be less than num-requsts)')
    unique_values.add_argument('--percent-unique', type=float,
                               help="Percent of unique items given as a decimal (0-1)")
    parser.add_argument('--alpha', type=float, required=True,
                        help='Zipfian exponent, representing the skewness of the workload')
    parser.add_argument('--output', type=str, help='Output file name')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Debug flag')
    args = parser.parse_args()

    num_unique = args.num_unique if not args.percent_unique else int(
        args.percent_unique * args.num_requests)
    workload = get_zipf_workload(
        num_unique, args.num_requests, args.alpha, args.debug)

    filename = args.output if args.output else f"unique {num_unique}, requests {args.num_requests}, alpha {args.alpha}.txt"
    file_save_workload(workload, filename)


if __name__ == "__main__":
    main()
