import os
import re
import csv
import sys

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 complete_analysis.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    main(file_path)
