# Import necessary libraries
from sage.all import *
from sage.modules.free_module_integer import IntegerLattice
import random

q = 7  # Field size
n = 5  # Length of codewords
k = 2   # Dimension of the code

def generate_error_vector(t):
    error_vector = vector(ZZ, [0] * n)
    non_zero_positions = random.sample(range(n), t)
    for pos in non_zero_positions:
        error_vector[pos] = random.randint(1, q)
    return error_vector

def get_fixed_error_vector():
    error_vector = vector(ZZ, [0] * n)
    error_vector[1] = 1
    return error_vector

# Step 1: Generate a random linear code
random_code = codes.random_linear_code(GF(q), n, k)
# fixed code
G = random_code.generator_matrix()
min_distance = random_code.minimum_distance()
G = matrix(ZZ, G)
G.change_ring(ZZ)
print("Generator Matrix G:")
print(G)
print("\nMinimum Distance of the Code:", min_distance)

I_n = identity_matrix(ZZ, n) * q
augmented_matrix = G.T.augment(I_n).T
HNF = augmented_matrix.hermite_form(include_zero_rows=False)

print("\nAugmented Generator Matrix (G | q * I_n):")
print(augmented_matrix)
print("\nHermite Normal Form (HNF) of the Augmented Matrix (with zero rows removed):")
print(HNF)


message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
codeword = message * G
print("\nRandom message:")
print(message)
print("\nEncoded codeword:")
print(codeword)

t = (min_distance - 1) // 2

error = get_fixed_error_vector() 
target_vector = codeword + error
target_vector = target_vector.change_ring(ZZ)
print("\nRandom error (less than max correction error):")
print(error)
print("\nTarget vector (codeword + error):")
print(target_vector)

lattice = IntegerLattice(HNF)
print("is codeword in hnf?", codeword in HNF)

M = 1
B_prime = HNF.stack(target_vector)
zeros = vector(ZZ, [0] * (n + 1))
zeros[-1] = M
B_prime = B_prime.augment(zeros)

B_prime = matrix(ZZ, B_prime)
print("\nEmbedded lattice basis matrix B_prime:")
print(B_prime)

# Compute the shortest vector in the embedded lattice (approximation using LLL)
B_prime = B_prime.LLL()
print("Reduced: \n", B_prime)
shortest_vector = B_prime[0] % q

print("Shorted Vector: ", shortest_vector)
