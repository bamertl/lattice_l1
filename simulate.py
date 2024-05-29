from sage.all import *
from src.simulation import simulate_code
import random


q = 7  # Field size
n = 5  # Length of codewords
k = 2   # Dimension of the code



random_code = codes.random_linear_code(GF(q), n, k)
G = random_code.generator_matrix()
min_distance = random_code.minimum_distance()

random_message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
codeword = random_message * G
t = (min_distance - 1) // 2

simulate_code(G, codeword, q, t)