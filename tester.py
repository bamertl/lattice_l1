from src.linear_code import RandomLinearCode
from src.construction_a import ConstructionA
n = 10
q = 6
k = 3

random_code = RandomLinearCode(n, k, q)

print(random_code)
print(f"Actual minimum distance: {random_code.calculate_exact_minimum_distance()}")

## Generate random message with random_code.generate_randome_message and print it, encode it and print the encoded as well
message = random_code.get_random_message()
print(f"Message: {message}")
encoded_message = random_code.encode(message)
print(f"Encoded Message: {encoded_message}")

lattice_basis = ConstructionA(random_code.generator_matrix, q).lattice_bases
print(f"Lattice Basis:\n{lattice_basis}")
