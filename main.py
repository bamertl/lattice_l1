from sage.all import *
import sage.all as sage
import numpy as np
from src.linear_code import RandomLinearCode
from src.construction_a import ConstructionA
from src.kanning_embedding import kanning_embedding
from src.my_lll import lll_reduction

n = 10   # Code Length
q = 2   # Field/Ring Size
k = 2   # Dimension

random_code = RandomLinearCode(n, k, q)
print("Shape",random_code.generator_matrix.shape)
print(random_code)
print(f"Actual minimum distance: {random_code.calculate_exact_minimum_distance()}")

## Generate random message with random_code.generate_randome_message and print it, encode it and print the encoded as well
message = random_code.get_random_message()
print(f"Message: {message}")

encoded_message = random_code.encode(message)
error_vector = random_code.get_random_error_vector()
# M = Embedding Scale Factor, should be around ||e||, set M to norm of error vector
M = np.linalg.norm(error_vector, ord = 2)


print(f"Error Vector: {error_vector}")
print(f"Encoded Message: {encoded_message}")

encoded_message = (encoded_message + error_vector) % q
print(f"Encoded Message with Error: {encoded_message}")

augmented_code = random_code.transform_generator_matrix(encoded_message)

print(f"Augmented Generator Matrix:\n{augmented_code}")

lattice_basis = ConstructionA(augmented_code, q).lattice_bases
print(f"Lattice Basis:\n{lattice_basis}")

reduced_basis = sage.Matrix(ZZ, lattice_basis)

print("Shortest Vector:")
reduced_basis = reduced_basis.BKZ(delta=0.75)
shortest_vector = min(reduced_basis.columns(), key=lambda v: v.norm())
print(shortest_vector % q) 

# Find the shortest vector
print("Error Vector:")
print(error_vector)
print(M)
