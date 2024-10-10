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

def plot_influence_of_k(subfolder_path):
    # Focus on q = 17
    target_q = 17
    
    # Create a dictionary to store files grouped by n
    grouped_files = defaultdict(list)

    # Filter and store files grouped by n
    for filename in os.listdir(subfolder_path):
        if filename.endswith(".csv"):
            try:
                custom_name, n, k, q, estimated_t = extract_info_from_filename(filename)
                # Filter based on q = 17
                if q == target_q:
                    grouped_files[n].append((k, estimated_t, filename))
            except ValueError:
                print(f"Skipping file {filename}: does not match the expected pattern.")
    
    # Sort files within each n group by k in ascending order
    for key in grouped_files:
        grouped_files[key].sort(key=lambda x: x[0])  # Sort by k
    
    # Create directory for saving plots if it doesn't exist
    figs_path = os.path.join(".", "figs", "multiple_k")
    os.makedirs(figs_path, exist_ok=True)

    # Plot influence of k for each n
    for n, files in grouped_files.items():
        plt.figure(figsize=(12, 8))
        plt.style.use('seaborn-whitegrid')
        
        # Create a small deterministic jitter factor based on the index of the k value
        jitter_base = 0.02  # Base jitter value for the x-axis
        for idx, (k, estimated_t, filename) in enumerate(files):
            file_path = os.path.join(subfolder_path, filename)
            
            good_vectors, failed_vectors = read_vectors_from_csv(file_path)
            l1_percentages = calculate_percentages(good_vectors, failed_vectors, target_q)
            
            # Apply a deterministic jitter based on the index
            jitter_x = jitter_base * (idx + 1) * np.sign(idx % 2 - 0.5)  # Alternates direction for jitter
            
            # Apply jitter to x coordinates
            x_values = np.array(list(l1_percentages.keys())) + jitter_x
            y_values = np.array(list(l1_percentages.values()))
            
            label = f"k={k}, estimated_t={estimated_t}"
            plt.scatter(x_values, y_values, s=100, label=label, alpha=0.75, edgecolor='black')
        
        plt.xlabel('L1 Norm', fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        plt.title(f'Influence of k on Decoding for n={n}, q={target_q}', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12, loc='upper right', bbox_to_anchor=(1.15, 1))
        plt.tight_layout()
        
        # Save plot to file
        plot_filename = f"influence_k_n{n}_q{target_q}.png"
        plot_filepath = os.path.join(figs_path, plot_filename)
        plt.savefig(plot_filepath)
        print(f"Plot saved to {plot_filepath}")
        
        plt.close()

def main(subfolder_path):
    if not os.path.isdir(subfolder_path):
        print(f"Error: {subfolder_path} is not a valid directory.")
        sys.exit(1)
    
    plot_influence_of_k(subfolder_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_influence_of_k.py <subfolder_path>")
        sys.exit(1)
    
    subfolder_path = sys.argv[1]
    main(subfolder_path)
