import os
import subprocess

def main() -> None:
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'synthetic_data')
    bin_path = os.path.join(os.path.dirname(__file__), '..', '_build', 'bin', 'cachesim')

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if os.path.isfile(file_path):
            cmd = [bin_path, file_path, 'txt', 'my_sieve,my_lru,my_fifo', 'auto']
            subprocess.run(cmd)
if __name__ == "__main__":
    main()
