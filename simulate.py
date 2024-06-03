from sage.all import *
from src.simulation import simulate_code
from src.linear_code.linear_code_utils import estimate_minimum_distance
import random

seed = 42
random.seed(seed)

q = 211  # Field size
n = 55  # Length of codewords
k = 21   # Dimension of the code

random_code = codes.random_linear_code(GF(q), n, k)
G = random_code.generator_matrix()
min_distance = estimate_minimum_distance(n, k, q) 
random_message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
codeword = random_message * G
t = (min_distance - 1) // 2

simulate_code(G, codeword, q, t)