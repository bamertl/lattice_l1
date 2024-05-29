from sage.all import *
from sage.modules.free_module_integer import IntegerLattice
from tqdm import tqdm
import itertools
from .solver import solve


"""
Simulate different parameters for the linear code and codeword
:param G: matrix, generator matrix of the linear code
:param code_word: vector, the codeword with an error vector added
:param q: int, modulus (ring or field size)
:param max_error_weight: int, maximum weight of the error vector, can be found out from G
"""
def simulate_code(G, code_word, q, max_error_weight):
    print("Simulating for G:", G)
    n = G.ncols()
    k = G.nrows()
    print(f"n: {n}, k: {k}, q: {q}, max_error_weight: {max_error_weight}")
    error_vectors = get_error_vectors(n, q, max_error_weight) 

    print(f"Total error vectors: {len(error_vectors)}")
    fails = 0
    success = 0
    for error_vector in tqdm(error_vectors):
        received_word = (code_word + vector(GF(q),error_vector)) % q
        decoded_error_vector = solve(G, received_word, q, max_error_weight)

        error_vector = vector(ZZ, error_vector)
        print(f"Error Vector{i}: {error_vector}")
        print(f"Decoded Error Vector{i}: {decoded_error_vector}")
        if error_vector != decoded_error_vector:
            fails += 1
        else:
            success += 1
    print(f"Fails: {fails}, Success: {success}")
        

def get_num_error_vectors_with_max_weight(n, q, max_error_weight):
    return sum(binomial(n, i) * (q - 1)**i for i in range(1, max_error_weight + 1))

def get_num_error_vectors_with_weight(n, q, error_weight):
    return binomial(n, error_weight) * (q-1)**error_weight

"""
This gets all possible error vectors of a given weight, use careful for higher dimension as this possibly takes up huge space.
"""
def get_error_vectors(n, q, error_weight):
    combinations = []
    indices_combinations = itertools.combinations(range(n), error_weight)

    value_combinations = list(itertools.product(range(1, q), repeat=error_weight))
    for indices in indices_combinations:
        for values in value_combinations:
            vector = [0] * n
            for idx, val in zip(indices, values):
                vector[idx] = val 
            combinations.append(vector)
    return combinations
