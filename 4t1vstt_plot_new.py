import os
import re
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

plt.style.use("seaborn-v0_8-whitegrid")

def calculate_percentages(good_vectors, failed_vectors, q):
    def lee_distance(vector, q):
        """Calculate Lee distance after taking modulo of each component with q."""
        vector = [component % q for component in vector]
        return np.sum([min(v, q - v) for v in vector])

    def calculate_percentage(good_count, total_count):
        return (good_count / total_count) * 100 if total_count > 0 else 0

    lee_counts = defaultdict(lambda: {'good': 0, 'failed': 0})

    for vector in good_vectors:
        lee_value = lee_distance(vector, q)
        lee_counts[lee_value]['good'] += 1

    for vector in failed_vectors:
        lee_value = lee_distance(vector, q)
        lee_counts[lee_value]['failed'] += 1

    lee_percentages = {dist: calculate_percentage(counts['good'], counts['good'] + counts['failed'])
                       for dist, counts in lee_counts.items()}

    return lee_percentages


def extract_info_from_filename(filename):
    match = re.match(r"result_n(\d+)_k(\d+)_q(\d+)_estimated_t(\d+)_lee_(.+)?\.csv", filename)

    if match:
        n = int(match.group(1))
        k = int(match.group(2))
        q = int(match.group(3))
        estimated_t = int(match.group(4))
        variant = match.group(5)
        return n, k, q, estimated_t, variant
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


def plot_withMinus_vs_standardLee(subfolder_path):
    comparison_data = defaultdict(lambda: {'t1': {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0},
                                           'tt': {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0},
                                           'thalf': {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0}})

    # Process each file in the folder
    for filename in os.listdir(subfolder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(subfolder_path, filename)

            try:
                n, k, q, estimated_t, variant = extract_info_from_filename(filename)
            except ValueError:
                print(f"Skipping file {filename}: does not match the expected pattern.")
                continue

            good_vectors, failed_vectors = read_vectors_from_csv(file_path)
            key = (n, k, q, estimated_t)

            comparison_data[key][variant]['good_vectors'].extend(good_vectors)
            comparison_data[key][variant]['failed_vectors'].extend(failed_vectors)
            comparison_data[key][variant]['estimated_t'] = estimated_t

    # Plot performance for each unique (n, q) combination
    for (n, k, q, estimated_t), data in comparison_data.items():
        plt.figure(figsize=(12, 8))

        # Calculate percentages for each variant
        t1 = calculate_percentages(data['t1']['good_vectors'], data['t1']['failed_vectors'], q)
        tt = calculate_percentages(data['tt']['good_vectors'], data['tt']['failed_vectors'], q)
        thalf = calculate_percentages(data['thalf']['good_vectors'], data['thalf']['failed_vectors'], q)

        # Plot each variant
        plt.plot(list(t1.keys()), list(t1.values()), 
                label="$\mu = 1$", color='green', alpha=0.75, linewidth=2, marker='o', markersize=6)

        plt.plot(list(tt.keys()), list(tt.values()), 
                label="$\mu = \mathrm{lee\_weight(error\_vector)}$", color='red', alpha=0.75, linewidth=2, marker='o', markersize=6)

        plt.plot(list(thalf.keys()), list(thalf.values()),
                label="$\mu = \mathrm{lee\_weight(error\_vector)}/2$", color='blue', alpha=0.75, linewidth=2, marker='o', markersize=6)

        plt.xlabel('Lee Weight', fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        plt.title(f'Decoding Performance with different $\mu$ (n={n}, p={q}, t={estimated_t})', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12)
        plt.tight_layout()

        # Save the plot
        output_dir = './figs/t1vst'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, f'performance_n{n}_q{q}.png'))
        plt.close()


def main(subfolder_path):
    if not os.path.isdir(subfolder_path):
        print(f"Error: {subfolder_path} is not a valid directory.")
        sys.exit(1)

    plot_withMinus_vs_standardLee(subfolder_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 4t1vstt_plot.py ./data/decoding_tall/")
        sys.exit(1)

    subfolder_path = sys.argv[1]
    main(subfolder_path)
