import os
import re
import csv
import sys
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt


def calculate_percentages(good_vectors, failed_vectors, q):
    def l1_norm(vector):
        return np.sum(np.abs(vector))

    def l2_norm(vector):
        return np.sqrt(np.sum(np.square(vector)))

    def lee_distance(vector, q):
        """Take modulo of the vector first."""
        vector = [component % q for component in vector]
        return np.sum([min(v, q - v) for v in vector])

    def calculate_percentage(good_count, total_count):
        return (good_count / total_count) * 100 if total_count > 0 else 0

    l1_counts = defaultdict(lambda: {'good': 0, 'failed': 0})
    l2_counts = defaultdict(lambda: {'good': 0, 'failed': 0})
    lee_counts = defaultdict(lambda: {'good': 0, 'failed': 0})
    
    for vector in good_vectors:
        l1_value = l1_norm(vector)
        l2_value = l2_norm(vector)
        lee_value = lee_distance(vector, q)
        
        l1_counts[l1_value]['good'] += 1
        l2_counts[l2_value]['good'] += 1
        lee_counts[lee_value]['good'] += 1
    
    for vector in failed_vectors:
        l1_value = l1_norm(vector)
        l2_value = l2_norm(vector)
        lee_value = lee_distance(vector, q)
        
        l1_counts[l1_value]['failed'] += 1
        l2_counts[l2_value]['failed'] += 1
        lee_counts[lee_value]['failed'] += 1
    
    l1_percentages = {dist: calculate_percentage(counts['good'], counts['good'] + counts['failed'])
                      for dist, counts in l1_counts.items()}
    
    l2_percentages = {dist: calculate_percentage(counts['good'], counts['good'] + counts['failed'])
                      for dist, counts in l2_counts.items()}
    
    lee_percentages = {dist: calculate_percentage(counts['good'], counts['good'] + counts['failed'])
                       for dist, counts in lee_counts.items()}
    
    return l1_percentages, l2_percentages, lee_percentages

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

def plot_combined_norms(subfolder_path):
    metrics_data = {'l1': defaultdict(lambda: {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0}),
                    'l2': defaultdict(lambda: {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0}),
                    'lee': defaultdict(lambda: {'good_vectors': [], 'failed_vectors': [], 'estimated_t': 0})}
    
    for filename in os.listdir(subfolder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(subfolder_path, filename)
            
            try:
                custom_name, n, k, q, estimated_t, metric = extract_info_from_filename(filename)
            except ValueError:
                print(f"Skipping file {filename}: does not match the expected pattern.")
                continue
            
            if q == 17:
                good_vectors, failed_vectors = read_vectors_from_csv(file_path)
                key = (n, k, q)
                metrics_data[metric][key]['good_vectors'].extend(good_vectors)
                metrics_data[metric][key]['failed_vectors'].extend(failed_vectors)
                metrics_data[metric][key]['estimated_t'] = estimated_t

    for metric, data in metrics_data.items():
        plt.figure(figsize=(12, 8))
        
        sorted_data = sorted(data.items(), key=lambda x: x[0][0])
        for (n, k, q), vectors in sorted_data:
            l1_percentages, l2_percentages, lee_percentages = calculate_percentages(vectors['good_vectors'], vectors['failed_vectors'], q)
            
            if metric == 'l1':
                percentages = l1_percentages
                xlabel = 'L1 Norm'
            elif metric == 'l2':
                percentages = l2_percentages
                xlabel = 'L2 Norm'
            else:
                percentages = lee_percentages
                xlabel = 'Lee Weight'
            
            label = f"n={n}, k={k}, q={q}, t={vectors['estimated_t']}"
            plt.scatter(list(percentages.keys()), list(percentages.values()), 
                        s=100, label=label, alpha=0.75, edgecolor='black')
        
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        titleadded = "Norm"
        if metric == 'lee':
            titleadded = "Lee Metric"
        plt.title(f'{xlabel} vs Percentage of Decoded Vectors for {metric.capitalize()} {titleadded}', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12, loc='upper right', bbox_to_anchor=(1.15, 1))
        plt.tight_layout()
        output_dir = './figs/3a'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, f'{metric}_norm_plot.png'))
        plt.close()

def main(subfolder_path):
    if not os.path.isdir(subfolder_path):
        print(f"Error: {subfolder_path} is not a valid directory.")
        sys.exit(1)
    
    plot_combined_norms(subfolder_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 combined_norm_analysis.py <subfolder_path>")
        sys.exit(1)
    
    subfolder_path = sys.argv[1]
    main(subfolder_path)