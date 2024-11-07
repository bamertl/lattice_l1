from sage.all import *
from tqdm import tqdm
import random
import csv
import os
import time  # Import time module
import numpy as np
import itertools
from sage.all_cmdline import *   # import sage library
# Seed for reproducibility

_sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_0 = Integer(0)
def lsphere(n, d, q): #points in a Lee sphere
	R = PolynomialRing(QQ, 'z', names=('z',)); (z,) = R._first_ngens(1)
	s = sum([_sage_const_1 ] + [_sage_const_2 *z**i for i in range(_sage_const_1 , floor(q / _sage_const_2 ) + _sage_const_1 )])
	return list(s**n)[d]

def V_L(n, t, q): #points in a Lee ball
	return sum([lsphere(n, r, q) for r in range(_sage_const_0 , t + _sage_const_1 )])

def estimate_minimum_distance_lee(n, k, p):
    """Find the maximum d such that the inequality holds."""
    max_term = (p**(n - k + 1) - 1) / (p - 1)
    d = 1

    while True:
        volume = V_L(n, d - 1, p)
        inequality_term = (volume - 1) / 2
        if max_term <= inequality_term:
            break
        d += 1
    return d - 1

def lee_distance(u, v, m):

    """Calculate the Lee distance between two vectors u and v in Z_m^n."""
    distance = 0
    for ui, vi in zip(u, v):
        diff = int(ui - vi)   # Calculate the modular difference
        distance += min(diff, m - diff)  # Use Lee weight definition
    return distance

def exact_minimum_lee_distance(GG, p):
    """Calculate the minimum Lee distance of a linear code with generator matrix G over Z_p."""
    # Ensure G has more columns than rows (n > k)

    G = GG.numpy()

    k, n = G.shape
    if n <= k:
        G = G.T  # Rotate matrix if necessary
        k, n = G.shape

    # Generate all possible codewords
    codewords = []

    # Generate all possible message vectors
    for m in itertools.product(range(p), repeat=k):
        # Calculate codeword c = m * G
        c = np.dot(m, G) % p
        codewords.append(tuple(c))

    # Calculate minimum non-zero Lee distance between all unique pairs of codewords
    d_min = float('inf')
    for c1, c2 in itertools.combinations(codewords, 2):
        d = lee_distance(c1, c2, p)
        d = int(d)
        if 0 < d < d_min:
            d_min = d

    return d_min

"""Run the simulation for small dimensions of n and k."""
def do_simulation(q, n, k, csv_writer):
    total_time_for_exact_min_dist = 0  # Initialize total time for exact minimum distance

    times_experiment = 3
    estimated_t_list = []
    exact_t_list = []

    for _ in tqdm(range(times_experiment), desc=f"Simulating for n={n}, k={k}, q={q}"):
        # Generate a random linear code
        random_code = codes.random_linear_code(GF(q), n, k)
        G = random_code.generator_matrix()

        # Estimate minimum distance and compute estimated t
        estimated_min_distance = estimate_minimum_distance_lee(n, k, q)
        estimated_t_list.append((estimated_min_distance - 1) // 2)  # Append to the list

        # Measure the time taken to compute the exact minimum distance
        start_time = time.time_ns()
        exact_min_distance = exact_minimum_lee_distance(G,q)
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
    q_values = [101]  # Field sizes (q=2 for binary, q=3 for ternary)

    # Dimensions of the linear codes
    dimensions = []
    for n in range(3, 10, 1):
        dimensions.append((n, 2))

    os.makedirs("data", exist_ok=True)
    # Create the output CSV file
    output_file = os.path.join("data/distance", "estimate_t_vs_real.csv")
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['n', 'k', 'q', 'Estimated t list', 'Exact t list', 'Avg Time for Exact t (s)'])  # Write header
  
        # Run simulations for each combination of q, n, and k
      
        for (n, k) in dimensions:
            for q in q_values:
                print(f"Running simulation for q={q}, n={n}, k={k}...")
                do_simulation(q, n, k, csv_writer)
                csvfile.flush()

# Run the simulation
run_simulation()
