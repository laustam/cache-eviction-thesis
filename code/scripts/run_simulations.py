import os
import subprocess
import time
from dir_paths import DATA_DIR, CACHESIM_PATH, RESULTS_DIR

REL_CACHE_SIZES = [0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 0.001, 0.002, 0.004, 0.006, 0.008, 0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6, 0.8]

def main() -> None:
    # Ensure results dir actually exists since cachesim does not create a new directory!
    os.makedirs(RESULTS_DIR, exist_ok=True)
    sorted_data_files = sorted(os.listdir(DATA_DIR))
    start_time = time.time()

    for i, filename in enumerate(sorted_data_files):
        # Time logs
        elapsed = int(time.time() - start_time)
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"[{i+1}/{len(sorted_data_files)}], Time elapsed: {hours:02}:{minutes:02}:{seconds:02}")

        file_path = os.path.join(DATA_DIR, filename)

        if os.path.isfile(file_path):
            base_filename = os.path.splitext(filename)[0]
            cmd = [CACHESIM_PATH, file_path, 'txt', 'myFIFO,myLRU,mySIEVE', ','.join(str(x) for x in REL_CACHE_SIZES), f'--output={RESULTS_DIR}/{base_filename}_results.txt']
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()
