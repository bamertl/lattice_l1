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

def plot_distances(l1_percentages, l2_percentages, lee_percentages):
    # Plot L1 Norm percentages
    plt.figure(figsize=(10, 6))
    plt.plot(list(l1_percentages.keys()), list(l1_percentages.values()), marker='o', label='L1 Norm')
    plt.xlabel('Distance')
    plt.ylabel('Good Vectors Percentage')
    plt.title('L1 Norm vs Percentage of Good Vectors')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Plot L2 Norm percentages
    plt.figure(figsize=(10, 6))
    plt.plot(list(l2_percentages.keys()), list(l2_percentages.values()), marker='o', label='L2 Norm')
    plt.xlabel('Distance')
    plt.ylabel('Good Vectors Percentage')
    plt.title('L2 Norm vs Percentage of Good Vectors')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Plot Lee Distance percentages
    plt.figure(figsize=(10, 6))
    plt.plot(list(lee_percentages.keys()), list(lee_percentages.values()), marker='o', label='Lee Distance')
    plt.xlabel('Distance')
    plt.ylabel('Good Vectors Percentage')
    plt.title('Lee Distance vs Percentage of Good Vectors')
    plt.grid(True)
    plt.legend()
    plt.show()

def extract_info_from_filename(filename):
    # Regular expression to extract n, k, q, and estimated_t from the filename
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
    plot_distances(l1_perc, l2_perc, lee_perc)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 complete_analysis.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    main(file_path)
