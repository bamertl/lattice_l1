import os
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

plt.style.use("seaborn-v0_8-whitegrid")
def calculate_success_rate(good_vectors, failed_vectors):
    total_attempts = len(good_vectors) + len(failed_vectors)
    if total_attempts == 0:
        return 0
    success_rate = (len(good_vectors) / total_attempts) * 100
    return success_rate

def extract_info_from_filename(filename):
    # Extract parameters from filename, including the block size
    match = re.match(r"result_n(\d+)_k(\d+)_q(\d+)_estimated_t(\d+)_lee_(\d+)\.csv", filename)
    if match:
        n = int(match.group(1))
        k = int(match.group(2))
        q = int(match.group(3))
        estimated_t = int(match.group(4))
        block_size = int(match.group(5))
        return n, k, q, estimated_t, block_size
    else:
        raise ValueError("Filename does not match the expected pattern.")

def read_vectors_from_csv(file_path):
    good_vectors = []
    failed_vectors = []

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
            vector_type = row[0]
            vector = [int(x) for x in row[1:] if x]  # Convert vector elements to integers

            if vector_type == 'G':
                good_vectors.append(vector)
            elif vector_type == 'F':
                failed_vectors.append(vector)
    return good_vectors, failed_vectors

def calculate_lee_weight(vector, q):
    """Calculate Lee weight of a vector."""
    return np.sum([min(v % q, q - (v % q)) for v in vector])

def plot_success_by_lee_weight(folder_path):
    # Dictionary to store success rates by (n, k, q), block size, and Lee weight
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    # Process each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            try:
                n, k, q, estimated_t, block_size = extract_info_from_filename(filename)
            except ValueError:
                print(f"Skipping file {filename}: does not match the expected pattern.")
                continue

            good_vectors, failed_vectors = read_vectors_from_csv(file_path)
            
            # Calculate success rate by Lee weight
            for vector in good_vectors:
                lee_weight = calculate_lee_weight(vector, q)
                data[(n, k, q)][block_size][lee_weight].append(1)  # Success

            for vector in failed_vectors:
                lee_weight = calculate_lee_weight(vector, q)
                data[(n, k, q)][block_size][lee_weight].append(0)  # Failure

    # Create a plot for each (n, k, q) combination
    output_dir = './figs/bkz_block_size'
    os.makedirs(output_dir, exist_ok=True)

    for (n, k, q), block_data in data.items():
        plt.figure(figsize=(10, 6))

        # Sort block_data by block size
        sorted_block_data = dict(sorted(block_data.items()))

        for block_size, lee_weights in sorted_block_data.items():
            # Calculate average success rate for each Lee weight
            avg_success_rates = {lee_weight: np.mean(results) * 100 for lee_weight, results in lee_weights.items()}
            
            # Sort data by Lee weight for plotting
            sorted_lee_weights = sorted(avg_success_rates.keys())
            sorted_success_rates = [avg_success_rates[weight] for weight in sorted_lee_weights]

            # Plot each block size as a separate line
            plt.plot(sorted_lee_weights, sorted_success_rates, marker='o', linestyle='-', linewidth=2, label=f'Block Size {block_size}')

        # Set up plot labels and title
        plt.xlabel('Lee Weight', fontsize=14)
        plt.ylabel('Average Success Rate (%)', fontsize=14)
        plt.title(f'Decoding Success Rate vs Lee Weight (n={n}, k={k}, p={q})', fontsize=16, weight='bold')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend(title="BKZ Block Size", fontsize=12)
        plt.tight_layout()

        # Save the plot for this (n, k, q) combination
        plt.savefig(os.path.join(output_dir, f'success_by_lee_weight_n{n}_k{k}_q{q}.png'))
        plt.close()

def main(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return
    
    plot_success_by_lee_weight(folder_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 6plot_bkz_block_sizes.py ./data/bkz_block_size/")
        sys.exit(1)

    subfolder_path = sys.argv[1]
    main(subfolder_path)
