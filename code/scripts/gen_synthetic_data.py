import subprocess
import time
import os
import re


def restore_progress() -> dict[str, str]:
    data_dir = os.path.join(os.path.dirname(__file__), "../data")
    files = [os.path.join(data_dir, f) for f in os.listdir(
        data_dir) if os.path.isfile(os.path.join(data_dir, f))]

    if not files:
        print("No files found in ../data. No progress is restored.")
        return {}

    most_recent_file = max(files, key=os.path.getmtime)
    print(f"Most recent file in ../data: {os.path.basename(most_recent_file)}")

    regex = r"alpha_(\d+\.?\d*)_objects_(\d+)_requests_(\d+)(?:\((\d+)\))?\.txt"
    match = re.search(regex, most_recent_file)

    if not match:
        print("Most recent file has an incorrect format. No progress is restored.")
        return {}

    alpha = float(match.group(1))
    nr_objects = int(match.group(2))
    nr_requests = int(match.group(3))
    file_nr = 0 if not match.group(4) else int(match.group(4))

    return {"alpha": alpha,
            "percent_unique": nr_objects/nr_requests,
            "file_nr": file_nr}


def main() -> None:
    user_input = input("Restore progress? (y/n): ").strip()

    while user_input not in ['y', 'n']:
        user_input = input("Restore progress? (y/n): ").strip()

    if user_input == 'y':
        print("Restoring progress...")
        progress = restore_progress()
        print("Restoring progress from the following values: ", progress)
        alpha_start = progress.get("alpha", 0)
        percent_unique_start = progress.get("percent_unique", 0)
        file_nr_start = progress.get("file_nr", 0)
    else:
        print("Not restoring progress...")
        alpha_start, percent_unique_start, file_nr_start = (0, 0, 0)

    nr_samples: int = 20
    alphas: list[float] = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
    percent_unique_list: list[float] = [0.01, 0.02,
                                        0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    nr_requests: int = 100000

    step_nr = 0
    total_steps = len(alphas) * len(percent_unique_list) * nr_samples
    start_time = time.time()

    for alpha in alphas:
        if alpha < alpha_start:
            step_nr += (len(percent_unique_list) * nr_samples)
            continue
        for percent_unique in percent_unique_list:
            if alpha_start == alpha and percent_unique < percent_unique_start:
                step_nr += nr_samples
                continue
            for i in range(nr_samples):
                if alpha_start == alpha and percent_unique == percent_unique_start and i < file_nr_start + 1:
                    step_nr += 1
                    continue

                step_nr += 1
                elapsed = int(time.time() - start_time)
                hours, remainder = divmod(elapsed, 3600)
                minutes, seconds = divmod(remainder, 60)
                print(
                    f"\n[{step_nr}/{total_steps}], Time elapsed: {hours:02}:{minutes:02}:{seconds:02}", end='')
                subprocess.run([
                    "python3",
                    "gen_zipf_workload.py",
                    "--alpha", str(alpha),
                    "--percent_unique", str(percent_unique),
                    "--num_requests", str(nr_requests)
                ])


if __name__ == "__main__":
    main()
