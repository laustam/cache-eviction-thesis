import os
import subprocess

def main() -> None:
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    bin_path = os.path.join(os.path.dirname(__file__), '..', '_build', 'bin', 'cachesim')

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if os.path.isfile(file_path):
            # Ensure results dir actually exists since cachesim does not create a new directory!
            results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
            os.makedirs(results_dir, exist_ok=True)

            cmd = [bin_path, file_path, 'txt', 'my_sieve,my_lru,my_fifo', 'auto', f'--output=../results/{filename[:-4]}_results.txt']
            subprocess.run(cmd)
if __name__ == "__main__":
    main()
