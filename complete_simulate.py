from sage.all import *

from tqdm import tqdm
import random
import csv
import os

seed = 42
random.seed(seed)

"""
Error Vector Generation
Generates vecotors_per_weight error vectors for weights from 1 to q-1
"""
def get_error_vectors(n, q, vectors_per_weight):
    error_vectors = []
    for i in range(1, q):
        error_vectors.extend(generate_marc_lee_error_vectors(n, i, vectors_per_weight))

    return error_vectors

def generate_marc_lee_error_vectors(n, t, num_vectors, max_tries=10000):
    unique_vectors = set()
    attempts = 0
    while len(unique_vectors) < num_vectors and attempts < max_tries:
        vector = get_marc_lee_error_vector(n, t)
        unique_vectors.add(tuple(vector))
        attempts += 1

    if len(unique_vectors) < num_vectors:
        print("Only generated", len(unique_vectors), "unique error vectors out of", num_vectors, "requested.")

    return [list(v) for v in unique_vectors]
def get_marc_lee_error_vector(n, t):
    error_vector = [0]*n
    for _ in range(t):
        idx = random.randint(0, n-1)     # get random coordinate 
        error_vector[idx] += 1   # add 1 to this coordinate
    for i in range(n):
        if random.choice([True, False]):
            error_vector[i] = -error_vector[i]
    return error_vector

"""Estimate the minimum distance d for large n using the Gilbert-Varshamov Bound."""
def estimate_minimum_distance(n,k,q):
    log_M = k * math.log(q)
    # Estimate for d using an approximation
    low, high = 1, n
    while low < high:
        mid = (low + high + 1) // 2
        sum_terms = sum(math.comb(n, i) * (q - 1)**i for i in range(mid))
        if math.log(sum_terms) - n * math.log(q) > -log_M:
            high = mid - 1
        else:
            low = mid
    return low

"""
This transforms the code into a lattice and then embeds it with the target vector 
and finally tries to solve the shortest vector problem to find the error vector that was added to the codeword.
:param G: matrix, generator matrix of the linear code
:param target_vector: vector, the codeword with an error vector added
:param q: int, modulus (ring or field size)
:param t: int, value to add to the new dimension from the embedding

returns the error vector (hopefully)
"""
def solve(G, target_vector,q, t):
    n = len(target_vector)
    lattice = transform_to_lattice(G,n,q)
    lattice = kannan_embedding(lattice, target_vector, t,q)

    shortest_vector = matrix(ZZ, lattice).BKZ()[0]
    # return only first n elements of shortest vector, the last element is the t (added dimension in kannan embedding)
    return vector(shortest_vector[:n])

"""
Transforms to lattice by embedding with q*I_n and then calculating the Hermite Normal Form
"""
def transform_to_lattice(G, n, q):
    G = matrix(ZZ, G)
    G.change_ring(ZZ)
    I_n = identity_matrix(ZZ, n) * q
    augmented_matrix = G.T.augment(I_n).T
    return augmented_matrix.hermite_form(include_zero_rows=False)

"""
Kannan Embedding to transform BDD Problem to Shortest Vector Problem
"""
def kannan_embedding(lattice, target_vector, t,q):
    
    # Embed the target vector into the lattice
    target_vector = target_vector.change_ring(ZZ)
    # apply marc-lee projection
    target_vector = target_vector.apply_map(lambda x: x - q if x > q/2 else x) 
    lattice = lattice.stack(target_vector) # adds as row
    zeros = vector(ZZ, [0] * (len(target_vector) + 1))
    zeros[-1] = t
    return lattice.augment(zeros) # adds as columns

"""
Simulate different parameters for the linear code and codeword
:param G: matrix, generator matrix of the linear code
:param code_word: vector, the codeword with an error vector added
:param q: int, modulus (ring or field size)
:param max_error_weight: int, maximum weight of the error vector, can be found out from G

:return: SimulationStats, a dataclass containing the statistics of the simulation
"""
def simulate_code(G, code_word, q, error_vectors, verbose: bool = False):
    n = G.ncols()
    k = G.nrows()
    kannang_t = 1

    if verbose:
        print(f"n: {n}, k: {k}, q: {q}")
    
    failed_vectors = []
    good_vectors = []
    for error_vector in tqdm(error_vectors):
        received_word = (code_word + vector(GF(q),error_vector)) % q # not sure if i shouuld take the modulo here
        decoded_error_vector = solve(G, received_word, q, kannang_t)

        error_vector = vector(ZZ, error_vector)
        if error_vector != decoded_error_vector:
            failed_vectors.append(error_vector)
        else:
            good_vectors.append(error_vector)
    if verbose: 
        print(f"Fails: {len(failed_vectors)}, Success: {len(good_vectors)}")
    return good_vectors, failed_vectors

"""
Write to CSV
"""

custom_name = "simulation_results"

def write_to_csv(sub_dir, n, k, q, good_vectors, failed_vectors, estimated_t):

    directory = "./data"
    full_directory_path = os.path.join(directory, sub_dir)

    csv_file_path = os.path.join(full_directory_path, f"result_n{n}_k{k}_q{q}_estimated_t{estimated_t}.csv")
    os.makedirs(full_directory_path, exist_ok=True)

    batch_size = 1000  # Adjust this based on memory capacity
    batch = []
    file_exists = os.path.isfile(csv_file_path)

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the headers (optional)
        if not file_exists:
            writer.writerow(['Vector Type', 'Vector'])
        
        for vector in good_vectors:
            batch.append(['G'] + list(vector))
            if len(batch) >= batch_size:
                writer.writerows(batch)
                batch.clear()

        for vector in failed_vectors:
            batch.append(['F'] + list(vector))
            if len(batch) >= batch_size:
                writer.writerows(batch)
                batch.clear()

        if batch:
            writer.writerows(batch)
            batch.clear()

def do_simulation(q, n, k,  sub_dir):
    error_vectors = get_error_vectors(n, q, 200) 

    for _ in range(10):
        random_code = codes.random_linear_code(GF(q), n, k)
        G = random_code.generator_matrix()
        min_distance = estimate_minimum_distance(n, k, q) 
        t = (min_distance - 1) // 2
        if min_distance < 3:
            raise ValueError("Estimated Minimum distance for this (n,k,q) code is less than 3")

        random_message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
        codeword = random_message * G

        good_vectors, failed_vectors = simulate_code(G, codeword, q=q, error_vectors=[sublist[:] for sublist in error_vectors], verbose=True)
        write_to_csv(sub_dir, n, k, q, good_vectors, failed_vectors, t)
    
primes = [17]   
n = [11, 31, 61, 101]
k = [3, 16, 30, 52]


current = 0

for prime in primes:
    for i in range(len(n)):
        current += 1
        print(f"Simulation: {current} / {len(n) * len(primes)}")
        do_simulation(prime, n[i], k[i], "experiment2")
