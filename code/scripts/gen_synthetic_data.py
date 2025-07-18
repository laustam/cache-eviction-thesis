import subprocess

def main() -> None:
    nr_samples: int = 20
    alphas: list[int] = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
    percent_unique_list: list[float] = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    nr_requests: int = 100000

    for alpha in alphas:
        for percent_unique in percent_unique_list:
            print("Percent unique:", percent_unique, percent_unique * nr_requests)
            for _ in range(nr_samples):
                subprocess.run([
                    "python3",
                    "gen_zipf_workload.py",
                    "--alpha", str(alpha),
                    "--percent_unique", str(percent_unique),
                    "--num_requests", str(nr_requests)
                ])


if __name__ == "__main__":
    main()
