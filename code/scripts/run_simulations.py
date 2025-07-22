import os
import subprocess
import time

def main() -> None:
    """
    # DIRECTORY SETUP:

    ├── code                        # PARENT_DIR
    |   ├── bin/
    |   |   ├── bin/
    |   |   |   ├── cachesim        # CACHESIM_PATH
    |   |   |   └── ...
    |   ├── data/                   # DATA_DIR
    |   ├── scripts/                # SCRIPTS_DIR
    |   ├── results/                # RESULTS DIR
    |   └── ...
    └── ...
    """

    SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.dirname(SCRIPTS_DIR)
    DATA_DIR = os.path.join(PARENT_DIR, 'data')
    CACHESIM_PATH = os.path.join(PARENT_DIR, '_build', 'bin', 'cachesim')
    RESULTS_DIR = os.path.join(PARENT_DIR, 'results')

    # Ensure results dir actually exists since cachesim does not create a new directory!
    os.makedirs(RESULTS_DIR, exist_ok=True)

    sorted_data_files = sorted(os.listdir(DATA_DIR))
    start_time = time.time()

    for i, filename in enumerate(sorted_data_files):
        elapsed = int(time.time() - start_time)
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"[{i+1}/{len(sorted_data_files)}], Time elapsed: {hours:02}:{minutes:02}:{seconds:02}")
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.isfile(file_path):
            base_filename = os.path.splitext(filename)[0]
            cmd = [CACHESIM_PATH, file_path, 'txt', 'my_sieve,my_lru,my_fifo', 'auto', f'--output={RESULTS_DIR}/{base_filename}_results.txt']
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if __name__ == "__main__":
    main()
