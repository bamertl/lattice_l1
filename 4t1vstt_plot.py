import os
import re
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


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
    match = re.match(r"result_n(\d+)_k(\d+)_q(\d+)_estimated_t(\d+)_lee(_withMinus)?\.csv", filename)
    if match:
        n = int(match.group(1))
        k = int(match.group(2))
        q = int(match.group(3))
        estimated_t = int(match.group(4))
        variant = "withMinus" if match.group(5) else "standardLee"
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
    comparison_data = defaultdict(lambda: {'standardLee': {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0},
                                           'withMinus': {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0}})

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
            key = (n, k, q)

            comparison_data[key][variant]['good_vectors'].extend(good_vectors)
            comparison_data[key][variant]['failed_vectors'].extend(failed_vectors)
            comparison_data[key][variant]['estimated_t'] = estimated_t

    # Plot performance for each unique (n, q) combination
    for (n, k, q), data in comparison_data.items():
        plt.figure(figsize=(12, 8))

        # Calculate percentages for each variant
        standardLee_percentages = calculate_percentages(data['standardLee']['good_vectors'], data['standardLee']['failed_vectors'], q)
        withMinus_percentages = calculate_percentages(data['withMinus']['good_vectors'], data['withMinus']['failed_vectors'], q)

        # Plot each variant
        plt.scatter(list(standardLee_percentages.keys()), list(standardLee_percentages.values()), 
                    label="Standard Lee", color='green', alpha=0.75, edgecolor='black', s=100)
        
        plt.scatter(list(withMinus_percentages.keys()), list(withMinus_percentages.values()), 
                    label="WithMinus", color='red', alpha=0.75, edgecolor='black', s=100)

        plt.xlabel('Lee Weight', fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        plt.title(f'Decoding Performance: Standard Lee vs WithMinus (n={n}, q={q})', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12)
        plt.tight_layout()

        # Save the plot
        output_dir = './figs/t1vstt'
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
        print("Usage: python3 plot_withMinus_vs_standardLee.py <subfolder_path>")
        sys.exit(1)

    subfolder_path = sys.argv[1]
    main(subfolder_path)
