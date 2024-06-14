from sage.all import *
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.error_vector import get_error_vectors_with_negative
from src.simulation import simulate_code
from src.linear_code.linear_code_utils import estimate_minimum_distance
from src.analysis.plot_vectors import plot_vectors
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

    error_vectors = get_error_vectors_with_negative(n, q)

    _, good_vectors, failed_vectors = simulate_code(G, codeword, q, t, error_vectors, verbose=True)
    plot_vectors(good_vectors, failed_vectors, q) 

q = 43
n = 11
k = 3

do_simulation(q, n, k)