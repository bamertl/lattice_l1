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

def average_percentages(percentages_list):
    averaged_percentages = defaultdict(list)
    
    for percentages in percentages_list:
        for norm_value, percentage in percentages.items():
            averaged_percentages[norm_value].append(percentage)
    
    averaged_percentages = {norm_value: np.mean(percentage_list) 
                            for norm_value, percentage_list in averaged_percentages.items()}
    
    return averaged_percentages

def plot_filtered_norms(bkz_folder, lll_folder):
    target_cases = [
        {'n': 11, 'k': 4, 'q': 17},
        {'n': 23, 'k': 11, 'q': 17},
        {'n': 51, 'k': 26, 'q': 17},
        {'n': 101, 'k': 51, 'q': 17}
    ]

    colors = ['blue', 'red']  # Blue for bkz, Red for lll
    folders = [bkz_folder, lll_folder]
    labels = ['BKZ', 'LLL']

    for norm_type in ['L1', 'L2', 'Lee']:
        plt.figure(figsize=(12, 8))

        for folder_idx, folder in enumerate(folders):
            color = colors[folder_idx]
            label_prefix = labels[folder_idx]
            percentages_list = []

            for filename in os.listdir(folder):
                if filename.endswith(".csv"):
                    file_path = os.path.join(folder, filename)
                    
                    try:
                        custom_name, n, k, q, estimated_t = extract_info_from_filename(filename)
                        
                        if not any(d['n'] == n and d['k'] == k and d['q'] == q for d in target_cases):
                            continue  # Skip files that do not match the desired cases
                        
                    except ValueError:
                        print(f"Skipping file {filename}: does not match the expected pattern.")
                        continue
                    
                    good_vectors, failed_vectors = read_vectors_from_csv(file_path)
                    l1_percentages, l2_percentages, lee_percentages = calculate_percentages(good_vectors, failed_vectors, q)
                    
                    if norm_type == 'L1':
                        percentages = l1_percentages
                    elif norm_type == 'L2':
                        percentages = l2_percentages
                    else:
                        percentages = lee_percentages
                    
                    percentages_list.append(percentages)
            
            if percentages_list:
                avg_percentages = average_percentages(percentages_list)
                
                label = f"{label_prefix}: Avg"
                plt.plot(list(avg_percentages.keys()), list(avg_percentages.values()), 
                         label=label, color=color, marker='o', linestyle='-', linewidth=2)

        xlabel = norm_type + ' Norm' if norm_type != 'Lee' else 'Lee Distance'
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel('Successfully Decoded (%)', fontsize=14)
        plt.title(f'Average {xlabel} vs Percentage of Decoded Vectors for n/k/q Cases', fontsize=16, weight='bold')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12, loc='upper right', bbox_to_anchor=(1.15, 1))
        plt.tight_layout()
        plt.show()

def main(bkz_folder, lll_folder):
    if not os.path.isdir(bkz_folder) or not os.path.isdir(lll_folder):
        print(f"Error: One or both folder paths are not valid directories.")
        sys.exit(1)
    
    plot_filtered_norms(bkz_folder, lll_folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 plot_bkz_vs_lll.py <bkz_folder_path> <lll_folder_path>")
        sys.exit(1)
    
    bkz_folder_path = sys.argv[1]
    lll_folder_path = sys.argv[2]
    main(bkz_folder_path, lll_folder_path)
