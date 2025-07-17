import subprocess

def main() -> None:
    nr_samples: int = 20
    alphas: list[int] = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
    nr_unique: int = 1000
    nr_requests: int = 100000

    for alpha in alphas:
        for _ in range(nr_samples):
            subprocess.run([
                "python3",
                "gen_zipf_workload.py",
                "--alpha", str(alpha),
                "--num_unique", str(nr_unique).replace(',', ''),
                "--num_requests", str(nr_requests).replace(',', '')
            ])


if __name__ == "__main__":
    main()
