from sage.all import *
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.error_vector import generate_marc_lee_error_vectors
from src.simulation import simulate_code
from src.linear_code.linear_code_utils import lgvk, estimate_minimum_distance
from src.analysis.csv_utils import write_single_stat_to_csv
import random

def run(n,k,q):
    random_code = codes.random_linear_code(GF(q), n, k)
    G = random_code.generator_matrix()
    min_distance = lgvk(n, k, q) 
    print("before", estimate_minimum_distance(n,k,q))
    print("after", min_distance)


n_list = [11, 31, 51, 101]
k_list = [5,15, 25, 50]

q = 3
for i in range(len(n_list)):
    n = n_list[i]
    k = k_list[i]
    run(n,k,q)