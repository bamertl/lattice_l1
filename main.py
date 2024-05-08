from sage.all import *
import sage.all as sage
import numpy as np
from src.linear_code import RandomLinearCode
from src.construction_a import ConstructionA
from src.kanning_embedding import kanning_embedding
from src.my_lll import lll_reduction

n = 7   # Code Length
q = 7   # Field/Ring Size
k = 3   # Dimension

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

encoded_message = encoded_message + error_vector % q
print(f"Encoded Message with Error: {encoded_message}")
lattice_basis = ConstructionA(random_code.generator_matrix, q).lattice_bases
print(f"Lattice Basis:\n{lattice_basis}")

#kanning_embedding(lattice_basis, encoded_message, 1)
embedded_basis = kanning_embedding(lattice_basis, encoded_message, M)
print("Kanning Embedded\n", embedded_basis)

reduced_basis = sage.Matrix(ZZ, embedded_basis)

print("Shortest Vector:")
reduced_basis = reduced_basis.BKZ(delta=0.75)
shortest_vector = min(reduced_basis.columns(), key=lambda v: v.norm())
print(shortest_vector % q) 

# Find the shortest vector
print("Error Vector:")
print(error_vector)
print(M)
