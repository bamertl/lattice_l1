from sage.all import *
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.error_vector import generate_marc_lee_error_vectors
from src.simulation import simulate_code
from src.linear_code.linear_code_utils import estimate_minimum_distance
from src.analysis.csv_utils import write_single_stat_to_csv
import random

seed = 42
random.seed(seed)

def do_simulation(q, n, k, result_file_name):
    random_code = codes.random_linear_code(GF(q), n, k)
    G = random_code.generator_matrix()
    min_distance = estimate_minimum_distance(n, k, q) 
    if min_distance < 3:
        raise ValueError("Estimated Minimum distance for this (n,k,q) code is less than 3")
    random_message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
    codeword = random_message * G
    t = (min_distance - 1) // 2

    max_error_weight = q-1
    error_vectors = []
    for i in range(1, max_error_weight + 1):
        error_vectors.extend(generate_marc_lee_error_vectors(n, i, 100))
    simulation_stats, _, _ = simulate_code(G, codeword, q=q, max_error_weight=max_error_weight, error_vectors=error_vectors, verbose=True)
    write_single_stat_to_csv(simulation_stats, result_file_name) 

primes = [17, 31]   
n = [11, 31]
k = [3, 16]
file_name = "simulation_results.csv"

current = 0
for prime in primes:
    for i in range(len(n)):
        current += 1
        print(f"Simulation: {current} / {len(n) * len(primes)}")
        do_simulation(prime, n[i], k[i], file_name)
