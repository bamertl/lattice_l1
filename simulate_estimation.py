from sage.all import *
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.error_vector import generate_marc_lee_error_vectors
from src.simulation import simulate_code
from src.linear_code.distance import lgvk
from src.analysis.csv_utils import write_single_stat_to_csv
import random

seed = 42
random.seed(seed)

def do_simulation(q, n, k, result_file_name):
    random_code = codes.random_linear_code(GF(q), n, k)
    G = random_code.generator_matrix()
    min_distance = lgvk(n, k, q) 
    print(min_distance)
    if min_distance < 3:
        raise ValueError("Estimated Minimum distance for this (n,k,q) code is less than 3")
    random_message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
    codeword = random_message * G
    t = (min_distance - 1) // 2

    error_vectors = get_error_vectors_around_t(n, t, 1000)
    simulation_stats, _, _ = simulate_code(G, codeword, q=q, max_error_weight=t, error_vectors=error_vectors, verbose=True)
    write_single_stat_to_csv(simulation_stats, result_file_name) 

def get_error_vectors_around_t(n, t, num_vectors):
    spread_factor = 6
    min_t = max(1, t - spread_factor)
    max_t = t + spread_factor
    
    # Determine the number of different `t` values
    t_range = list(range(min_t, max_t + 1))
    num_t_values = len(t_range)
    vectors_per_t = num_vectors // num_t_values
    remaining_vectors = num_vectors % num_t_values
    error_vectors = []
    for t_current in t_range:
        num_vectors_current = vectors_per_t + (1 if remaining_vectors > 0 else 0)
        remaining_vectors -= 1
        error_vectors.extend(generate_marc_lee_error_vectors(n, t_current, num_vectors_current)) 
    return error_vectors

def get_10_primes_between(a, b):
    print([p for p in prime_range(a, b)][:10])

primes = [17, 31, 97, 1021]   
n = [11, 31, 51, 101]
k = [3, 16, 25, 55]
file_name = "simulation_results.csv"

def run():
    current = 0
    for prime in primes:
        for i in range(len(n)):
            current += 1
            print(f"Simulation: {current} / {len(n) * len(primes)}")
            do_simulation(prime, n[i], k[i], file_name)

run()