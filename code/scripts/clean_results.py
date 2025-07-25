"""
clean_results.py

This script processes all files in the RESULTS_DIR directory, removing duplicate lines and sorting the contents of each file.
It reads each file, strips whitespace, eliminates empty lines, removes duplicates, sorts the lines, and writes the cleaned data back to the file.
This helps to clean up result files by ensuring each line is unique and ordered.

Functions:
    clean_file(filepath): Removes duplicate and empty lines from the specified file, sorts the lines, and writes the cleaned content back.
    main(): Iterates over all files in RESULTS_DIR, applying the cleaning process to each file.
"""

import os
from dir_paths import RESULTS_DIR

def clean_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    unique_lines = sorted(list(dict.fromkeys(line.strip() for line in lines if line.strip())))

    with open(filepath, 'w') as f:
        for line in unique_lines:
            f.write(line + '\n')

def main():
    for filename in os.listdir(RESULTS_DIR):
        file_path = os.path.join(RESULTS_DIR, filename)
        if os.path.isfile(file_path):
            clean_file(file_path)
            print(f"Processed {filename}")

if __name__ == "__main__":
    main()
