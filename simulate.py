from sage.all import *
from src.simulation import simulate_code, SimulationStats
from src.linear_code.linear_code_utils import estimate_minimum_distance
from src.analysis.csv_utils import write_single_stat_to_csv, read_csv_to_stats
import random

seed = 42
random.seed(seed)

def do_simulation(q, n, k):
    random_code = codes.random_linear_code(GF(q), n, k)
    G = random_code.generator_matrix()
    min_distance = estimate_minimum_distance(n, k, q) 
    if min_distance < 3:
        raise ValueError("Estimated Minimum distance for this (n,k,q) code is less than 3")
    random_message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
    codeword = random_message * G
    t = (min_distance - 1) // 2
    simulation_stats, _, _ = simulate_code(G, codeword, q, t, verbose=True)
    write_single_stat_to_csv(simulation_stats, "simulation_results3.csv") 

def get_10_primes_between_11_and_511():
    return [p for p in prime_range(4000, 5000)][:10]

primes = [11, 31, 97, 211, 503, 1051, 2053, 4049]   
n = [11, 31]
k = [3, 16]

current = 0
for prime in primes:
    for i in range(len(n)):
        current += 1
        print(f"Simulation: {current} / {len(n) * len(primes)}")
        do_simulation(prime, n[i], k[i])
