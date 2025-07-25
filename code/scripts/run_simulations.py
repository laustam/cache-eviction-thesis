import os
import subprocess
import time
from dir_paths import DATA_DIR, CACHESIM_PATH, RESULTS_DIR

def main() -> None:
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
            # already run: [0.003, 0.01, 0.03, 0.1, 0.2, 0.4, 0.8]
            cmd = [CACHESIM_PATH, file_path, 'txt', 'my_fifo,my_lru,my_sieve', '0.0001, 0.0002', f'--output={RESULTS_DIR}/{base_filename}_results.txt']
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if __name__ == "__main__":
    main()
