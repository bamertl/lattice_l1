import os
import re
import csv
import sys
import numpy as np
from collections import defaultdict
import seaborn as sns
sns.set_style("whitegrid")
import matplotlib.pyplot as plt

def calculate_percentages(good_vectors, failed_vectors, q):
    def l1_norm(vector):
        return np.sum(np.abs(vector))

    def l2_norm(vector):
        return np.sqrt(np.sum(np.square(vector)))

    def lee_distance(vector, q):
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
    match = re.match(r"(.*)_n(\d+)_k(\d+)_q(\d+)_estimated_t(\d+)\.csv", filename)
    if match:
        custom_name = match.group(1)
        n = int(match.group(2))
        k = int(match.group(3))
        q = int(match.group(4))
        estimated_t = int(match.group(5))
        return custom_name, n, k, q, estimated_t
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

def plot_filtered_norms(subfolder_path):
    # Define the specific cases to plot
    target_cases = [
        {'n': 11, 'k': 4, 'q': 17},
        {'n': 23, 'k': 11, 'q': 17},
        {'n': 51, 'k': 26, 'q': 17},
        {'n': 101, 'k': 51, 'q': 17}
    ]

    for norm_type in ['L1', 'L2', 'Lee']:
        plt.figure(figsize=(12, 8))

        for filename in os.listdir(subfolder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(subfolder_path, filename)
                
                try:
                    custom_name, n, k, q, estimated_t = extract_info_from_filename(filename)
                    
                    # Filter only the specified cases with q=17
                    if not any(d['n'] == n and d['k'] == k and d['q'] == q for d in target_cases):
                        continue  # Skip files that do not match the desired cases
                    
                except ValueError:
                    print(f"Skipping file {filename}: does not match the expected pattern.")
                    continue
                
                good_vectors, failed_vectors = read_vectors_from_csv(file_path)
                
                l1_percentages, l2_percentages, lee_percentages = calculate_percentages(good_vectors, failed_vectors, q)
                
                if norm_type == 'L1':
                    percentages = l1_percentages
                    xlabel = 'L1 Norm'
                elif norm_type == 'L2':
                    percentages = l2_percentages
                    xlabel = 'L2 Norm'
                else:
                    percentages = lee_percentages
                    xlabel = 'Lee Distance'
                
                label = f"n={n}, k={k}, q={q}"
                plt.scatter(list(percentages.keys()), list(percentages.values()), 
                            s=100, label=label, alpha=0.75, edgecolor='black')
        
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        plt.title(f'{xlabel} vs Percentage of Decoded Vectors for n/k/q Cases', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12, loc='upper right', bbox_to_anchor=(1.15, 1))
        plt.tight_layout()
        plt.show()

def main(subfolder_path):
    if not os.path.isdir(subfolder_path):
        print(f"Error: {subfolder_path} is not a valid directory.")
        sys.exit(1)
    
    plot_filtered_norms(subfolder_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_experiment1.py ./data/lll1")
        sys.exit(1)
    
    subfolder_path = sys.argv[1]
    main(subfolder_path)
