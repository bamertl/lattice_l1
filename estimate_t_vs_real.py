from sage.all import *
from tqdm import tqdm
import random
import csv
import os
import time  # Import time module

# Seed for reproducibility
seed = 42
random.seed(seed)

"""Estimate the minimum distance d for large n using the Gilbert-Varshamov Bound."""
def estimate_minimum_distance(n, k, q):
    log_M = k * math.log(q)
    # Estimate for d using an approximation
    low, high = 1, n
    while low < high:
        mid = (low + high + 1) // 2
        sum_terms = sum(math.comb(n, i) * (q - 1)**i for i in range(mid))
        if math.log(sum_terms) - n * math.log(q) > -log_M:
            high = mid - 1
        else:
            low = mid
    return low

"""Compute the exact minimum distance using the code's properties."""
def exact_minimum_distance(random_code):
    return random_code.minimum_distance()

"""Run the simulation for small dimensions of n and k."""
def do_simulation(q, n, k, csv_writer):
    total_time_for_exact_min_dist = 0  # Initialize total time for exact minimum distance

    times_experiment = 10
    estimated_t_list = []
    exact_t_list = []

    for _ in tqdm(range(times_experiment), desc=f"Simulating for n={n}, k={k}, q={q}"):
        # Generate a random linear code
        random_code = codes.random_linear_code(GF(q), n, k)
        G = random_code.generator_matrix()

        # Estimate minimum distance and compute estimated t
        estimated_min_distance = estimate_minimum_distance(n, k, q)
        estimated_t_list.append((estimated_min_distance - 1) // 2)  # Append to the list

        # Measure the time taken to compute the exact minimum distance
        start_time = time.time_ns()
        exact_min_distance = exact_minimum_distance(random_code)
        end_time = time.time_ns()

        time_taken_ms = (end_time - start_time) / 1e9  # Time in s
        exact_t_list.append((exact_min_distance - 1) // 2)  # Append to the list

        # Calculate the time taken for exact minimum distance from ns to s
        total_time_for_exact_min_dist += time_taken_ms

    # Calculate average time for exact minimum distance calculation
    average_time_ms = total_time_for_exact_min_dist / times_experiment

    # Write data to CSV once for this configuration of n, k, q
    csv_writer.writerow([n, k, q, estimated_t_list, exact_t_list, average_time_ms])




"""Main function to run the simulation for various n, k values and write results to one CSV."""
def run_simulation():
    q_values = [5, 17]  # Field sizes (q=2 for binary, q=3 for ternary)

    # Dimensions of the linear codes
    dimensions = []
    for n in range(7, 35):
        for k in range(1, n - 5):
            dimensions.append((n, k))

    os.makedirs("data", exist_ok=True)
    # Create the output CSV file
    output_file = os.path.join("data", "estimate_t_vs_real.csv")
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['n', 'k', 'q', 'Estimated t list', 'Exact t list', 'Avg Time for Exact t (s)'])  # Write header
  
        # Run simulations for each combination of q, n, and k
      
        for (n, k) in dimensions:
            for q in q_values:
                print(f"Running simulation for q={q}, n={n}, k={k}...")
                do_simulation(q, n, k, csv_writer)

# Run the simulation
run_simulation()
