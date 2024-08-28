import os
import re
import csv
import sys

import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

def calculate_distances_and_percentages(good_vectors, failed_vectors, n, k, q, estimated_t):
    def l1_norm(vector):
        return np.sum(np.abs(vector))

    def l2_norm(vector):
        return np.sqrt(np.sum(np.square(vector)))

    def lee_distance(vector, q):
        return np.sum([min(v, q - v) for v in vector])
    
    def calculate_percentage(good_count, total_count):
        return (good_count / total_count) * 100 if total_count > 0 else 0

    # Dictionaries to count occurrences of each unique distance
    l1_counts = defaultdict(lambda: {'good': 0, 'failed': 0})
    l2_counts = defaultdict(lambda: {'good': 0, 'failed': 0})
    lee_counts = defaultdict(lambda: {'good': 0, 'failed': 0})
    
    # Process good vectors
    for vector in good_vectors:
        l1_value = l1_norm(vector)
        l2_value = l2_norm(vector)
        lee_value = lee_distance(vector, q)
        
        l1_counts[l1_value]['good'] += 1
        l2_counts[l2_value]['good'] += 1
        lee_counts[lee_value]['good'] += 1
    
    # Process failed vectors
    for vector in failed_vectors:
        l1_value = l1_norm(vector)
        l2_value = l2_norm(vector)
        lee_value = lee_distance(vector, q)
        
        l1_counts[l1_value]['failed'] += 1
        l2_counts[l2_value]['failed'] += 1
        lee_counts[lee_value]['failed'] += 1
    
    # Calculate percentages for each unique distance
    l1_percentages = {dist: calculate_percentage(counts['good'], counts['good'] + counts['failed'])
                      for dist, counts in l1_counts.items()}
    
    l2_percentages = {dist: calculate_percentage(counts['good'], counts['good'] + counts['failed'])
                      for dist, counts in l2_counts.items()}
    
    lee_percentages = {dist: calculate_percentage(counts['good'], counts['good'] + counts['failed'])
                       for dist, counts in lee_counts.items()}
    
    # Print results
    print(f"n: {n}, k: {k}, q: {q}, estimated_t: {estimated_t}")
    print("L1 Norm Percentages:")
    for dist, percentage in sorted(l1_percentages.items()):
        print(f"  Distance: {dist}, Good Percentage: {percentage:.2f}%")
    
    print("L2 Norm Percentages:")
    for dist, percentage in sorted(l2_percentages.items()):
        print(f"  Distance: {dist}, Good Percentage: {percentage:.2f}%")
    
    print("Lee Distance Percentages:")
    for dist, percentage in sorted(lee_percentages.items()):
        print(f"  Distance: {dist}, Good Percentage: {percentage:.2f}%")
    
    return l1_percentages, l2_percentages, lee_percentages

def plot_distances(l1_percentages, l2_percentages, lee_percentages, n, k, q):


    ylabel = "Successfully Decoded %"
    title = f"(n: {n}, k: {k}, q: {q}) Code " 


    plt.figure(figsize=(10, 6))
    plt.scatter(list(l1_percentages.keys()), list(l1_percentages.values()), 
                color='red', edgecolor='black', s=100, label='Decoded')
    plt.xlabel('L1 Norm', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.title(title + "over L1", fontsize=16, weight='bold')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)

    # Adjust the layout to avoid any overlapping and ensure everything is well-spaced
    plt.tight_layout()

    # Show the plot
    plt.show()
    
    # Plot L2 Norm percentages
    plt.figure(figsize=(10, 6))
    plt.scatter(list(l2_percentages.keys()), list(l2_percentages.values()), 
                color='blue', edgecolor='black', s=100, label='Decoded')
    plt.xlabel('L2 Norm', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.title(title + "over L2", fontsize=16, weight='bold')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()

    # Plot Lee Distance percentages
    plt.figure(figsize=(10, 6))
    plt.scatter(list(lee_percentages.keys()), list(lee_percentages.values()), 
                color='green', edgecolor='black', s=100, label='Decoded')
    plt.xlabel('Lee Distance', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.title(title + "over Lee Metric", fontsize=16, weight='bold')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()

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

def main(file_path):
    # Extract n, k, q, and estimated_t from filename
    filename = os.path.basename(file_path)
    custom_name, n, k, q, estimated_t = extract_info_from_filename(filename)
    
    # Read vectors from the CSV file
    good_vectors, failed_vectors = read_vectors_from_csv(file_path)
    
    # Print the extracted information and lengths of the arrays
    print(f"n: {n}")
    print(f"k: {k}")
    print(f"q: {q}")
    print(f"Estimated t: {estimated_t}")
    print(f"Number of good vectors: {len(good_vectors)}")
    print(f"Number of failed vectors: {len(failed_vectors)}")
    l1_perc, l2_perc, lee_perc = calculate_distances_and_percentages(good_vectors, failed_vectors, n, k, q, estimated_t)
    plot_distances(l1_perc, l2_perc, lee_perc, n, k, q)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 complete_analysis.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    main(file_path)
