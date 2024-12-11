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
    match = re.match(r"(.*)_n(\d+)_k(\d+)_q(\d+)_estimated_t(\d+)_(lee|l1|l2)\.csv", filename)
    if match:
        custom_name = match.group(1)
        n = int(match.group(2))
        k = int(match.group(3))
        q = int(match.group(4))
        estimated_t = int(match.group(5))
        metric = match.group(6)
        return custom_name, n, k, q, estimated_t, metric
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


def plot_q_influence(subfolder_path):
    q_influence_data = {'n=20': defaultdict(lambda: {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0}),
                        'n=50': defaultdict(lambda: {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0})}

    for filename in os.listdir(subfolder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(subfolder_path, filename)

            try:
                custom_name, n, k, q, estimated_t, metric = extract_info_from_filename(filename)
            except ValueError:
                print(f"Skipping file {filename}: does not match the expected pattern.")
                continue

            if metric == 'lee' and (n == 20 or n == 50):
                key = f'n={n}'
                good_vectors, failed_vectors = read_vectors_from_csv(file_path)
                q_influence_data[key][q]['good_vectors'].extend(good_vectors)
                q_influence_data[key][q]['failed_vectors'].extend(failed_vectors)
                q_influence_data[key][q]['estimated_t'] = estimated_t

    for n_key, data in q_influence_data.items():
        plt.figure(figsize=(12, 8))

        sorted_data = sorted(data.items(), key=lambda x: x[0])  # Sort by q values
        for q, vectors in sorted_data:
            lee_percentages = calculate_percentages(vectors['good_vectors'], vectors['failed_vectors'], q)
            label = f"p={q}, t={vectors['estimated_t']}"
            plt.scatter(list(lee_percentages.keys()), list(lee_percentages.values()), label=label, s=100, alpha=0.75, edgecolor='black')

        plt.xlabel('Lee Weight', fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        plt.title(f'Influence of p on Decoding Success Rate for {n_key}', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12, loc='upper right')
      

        output_dir = './figs/q_influence'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, f'q_influence_lee_{n_key}.png'))
        plt.close()


def main(subfolder_path):
    if not os.path.isdir(subfolder_path):
        print(f"Error: {subfolder_path} is not a valid directory.")
        sys.exit(1)

    plot_q_influence(subfolder_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 3BdecodingLee_plot.py ./data/decoding_tis1/")
        sys.exit(1)

    subfolder_path = sys.argv[1]
    main(subfolder_path)
