from sage.all import *
import sage.all as sage

from src.linear_code import RandomLinearCode
from src.construction_a import ConstructionA
from src.kanning_embedding import kanning_embedding
from src.my_lll import lll_reduction

n = 7
q = 6
k = 3

random_code = RandomLinearCode(n, k, q)
print("Shape",random_code.generator_matrix.shape)
print(random_code)
print(f"Actual minimum distance: {random_code.calculate_exact_minimum_distance()}")

## Generate random message with random_code.generate_randome_message and print it, encode it and print the encoded as well
message = random_code.get_random_message()
print(f"Message: {message}")

encoded_message = random_code.encode(message)
error_vector = random_code.get_random_error_vector()
print(f"Error Vector: {error_vector}")
print(f"Encoded Message: {encoded_message}")

encoded_message = encoded_message + error_vector % q
print(f"Encoded Message with Error: {encoded_message}")
lattice_basis = ConstructionA(random_code.generator_matrix, q).lattice_bases
print(f"Lattice Basis:\n{lattice_basis}")

#kanning_embedding(lattice_basis, encoded_message, 1)
embedded_basis = kanning_embedding(lattice_basis, encoded_message, 2*random_code.t)
print("Kanning Embedded", embedded_basis)

reduced_basis = sage.Matrix(ZZ, embedded_basis)
bkz_reduced_basis = reduced_basis.LLL()
print("Reduced Basis:")
print(bkz_reduced_basis)

# Find the shortest vector
shortest_vector = min(bkz_reduced_basis.columns(), key=lambda v: v.norm())
print("Shortest Vector Found by BKZ:")
print(shortest_vector % q) 
print("Error Vector:")
print(error_vector)
