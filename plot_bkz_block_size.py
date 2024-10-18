import os
import re
import csv
import sys
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

def calculate_percentages(good_vectors, failed_vectors, q):
    def l1_norm(vector):
        return np.sum(np.abs(vector))

    def calculate_percentage(good_count, total_count):
        return (good_count / total_count) * 100 if total_count > 0 else 0

    l1_counts = defaultdict(lambda: {'good': 0, 'failed': 0})
    
    for vector in good_vectors:
        l1_value = l1_norm(vector)
        l1_counts[l1_value]['good'] += 1
    
    for vector in failed_vectors:
        l1_value = l1_norm(vector)
        l1_counts[l1_value]['failed'] += 1
    
    l1_percentages = {dist: calculate_percentage(counts['good'], counts['good'] + counts['failed'])
                      for dist, counts in l1_counts.items()}
    
    return l1_percentages

def extract_info_from_filename(filename):
    match = re.match(r"(.*)_n(\d+)_k(\d+)_q(\d+)_estimated_t(\d+)_block_size(\d+)\.csv", filename)
    if match:
        custom_name = match.group(1)
        n = int(match.group(2))
        k = int(match.group(3))
        q = int(match.group(4))
        estimated_t = int(match.group(5))
        block_size = int(match.group(6))
        return custom_name, n, k, q, estimated_t, block_size
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

def plot_block_size_effect(bkz_folder):
    target_cases = [
        {'n': 51, 'k': 26, 'q': 5},
        {'n': 31, 'k': 15, 'q': 5},
        {'n': 23, 'k': 11, 'q': 5}
    ]

    for target_case in target_cases:
        n = target_case['n']
        k = target_case['k']
        q = target_case['q']

        plt.figure(figsize=(12, 8))
        block_size_data = []

        for filename in os.listdir(bkz_folder):
            if filename.endswith(".csv"):
                file_path = os.path.join(bkz_folder, filename)
                
                try:
                    custom_name, file_n, file_k, file_q, estimated_t, block_size = extract_info_from_filename(filename)
                    
                    if not (file_n == n and file_k == k and file_q == q):
                        continue  # Skip files that do not match the desired case
                    
                except ValueError:
                    print(f"Skipping file {filename}: does not match the expected pattern.")
                    continue
                
                good_vectors, failed_vectors = read_vectors_from_csv(file_path)
                l1_percentages = calculate_percentages(good_vectors, failed_vectors, q)
                
                if l1_percentages:
                    block_size_data.append((block_size, l1_percentages))
        
        # Sort block sizes
        block_size_data.sort(key=lambda x: x[0])
        
        for block_size, l1_percentages in block_size_data:
            plt.plot(list(l1_percentages.keys()), list(l1_percentages.values()), label=f'Block Size {block_size}', marker='o', linestyle='-', linewidth=2)
        
        xlabel = 'L1 Norm'
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        plt.title(f'L1 Norm vs Percentage of Decoded Vectors for n={n}, k={k}, q={q}', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True)
        plt.legend(fontsize=12, loc='upper right')
        plt.tight_layout()
        
        # Save the figure
        output_dir = './figs/bkz_block_size/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.savefig(f'{output_dir}l1_norm_n{n}_k{k}_q{q}.png')
        
        plt.show()

def main(bkz_folder):
    if not os.path.isdir(bkz_folder):
        print(f"Error: The folder path is not a valid directory.")
        sys.exit(1)
    
    plot_block_size_effect(bkz_folder)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_block_size_effect.py <bkz_folder_path>")
        sys.exit(1)
    
    bkz_folder_path = sys.argv[1]
    main(bkz_folder_path)
