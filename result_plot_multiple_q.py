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

def plot_l1_q_variations(subfolder_path):
    # Define valid (n, k) combinations
    valid_combinations = [
        (11, 4),
        (23, 11),
        (31, 15),
        (51, 26),
        (101, 51)
    ]
    
    # Create a dictionary to store files grouped by (n, k)
    grouped_files = defaultdict(list)

    # Filter and store files grouped by (n, k)
    for filename in os.listdir(subfolder_path):
        if filename.endswith(".csv"):
            try:
                custom_name, n, k, q, estimated_t = extract_info_from_filename(filename)
                # Filter based on valid (n, k) combinations
                if (n, k) in valid_combinations:
                    grouped_files[(n, k)].append((q, estimated_t, filename))
            except ValueError:
                print(f"Skipping file {filename}: does not match the expected pattern.")
    
    # Sort files within each (n, k) group by q in ascending order
    for key in grouped_files:
        grouped_files[key].sort(key=lambda x: x[0])  # Sort by q
    
    # Create directory for saving plots if it doesn't exist
    figs_path = os.path.join(".", "figs", "multiple_q")
    os.makedirs(figs_path, exist_ok=True)

    # Plot L1 norm for each (n, k) combination with varying q
    for (n, k), files in grouped_files.items():
        plt.figure(figsize=(12, 8))
        plt.style.use('seaborn-whitegrid')
        
        for q, estimated_t, filename in files:
            file_path = os.path.join(subfolder_path, filename)
            
            good_vectors, failed_vectors = read_vectors_from_csv(file_path)
            l1_percentages = calculate_percentages(good_vectors, failed_vectors, q)
            
            label = f"q={q}, estimated_t={estimated_t}"
            plt.scatter(list(l1_percentages.keys()), list(l1_percentages.values()), 
                        s=100, label=label, alpha=0.75, edgecolor='black')
        
        plt.xlabel('L1 Norm', fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        plt.title(f'L1 Norm vs Percentage of Decoded Vectors for n={n}, k={k}', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12, loc='upper right', bbox_to_anchor=(1.15, 1))
        plt.tight_layout()
        
        # Save plot to file
        plot_filename = f"l1_norm_n{n}_k{k}.png"
        plot_filepath = os.path.join(figs_path, plot_filename)
        plt.savefig(plot_filepath)
        print(f"Plot saved to {plot_filepath}")
        
        plt.close()

def main(subfolder_path):
    if not os.path.isdir(subfolder_path):
        print(f"Error: {subfolder_path} is not a valid directory.")
        sys.exit(1)
    
    plot_l1_q_variations(subfolder_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 result_plot_norms.py <subfolder_path>")
        sys.exit(1)
    
    subfolder_path = sys.argv[1]
    main(subfolder_path)
