from sage.all import *

import random
import csv
import os
from sage.all_cmdline import *   # import sage library
import random
import sage.all

# Set the seed for reproducibility
seed = 42
random.seed(seed)                # Set seed for Python's random module
sage.all.set_random_seed(seed)   # Set seed for SageMath's random number generato



_sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_0 = Integer(0)
def lsphere(n, d, q): #points in a Lee sphere
	R = PolynomialRing(QQ, 'z', names=('z',)); (z,) = R._first_ngens(1)
	s = sum([_sage_const_1 ] + [_sage_const_2 *z**i for i in range(_sage_const_1 , floor(q / _sage_const_2 ) + _sage_const_1 )])
	return list(s**n)[d]

def V_L(n, t, q): #points in a Lee ball
	return sum([lsphere(n, r, q) for r in range(_sage_const_0 , t + _sage_const_1 )])

def estimate_minimum_distance_lee(n, k, p):
    """Find the maximum d such that the inequality holds."""
    max_term = (p**(n - k + 1) - 1) / (p - 1)
    d = 1

    while True:
        volume = V_L(n, d - 1, p)
        inequality_term = (volume - 1) / 2
        if max_term <= inequality_term:
            break
        d += 1
    return d - 1


def lee_distance(u, v, m):
    """Calculate the Lee distance between two vectors u and v in Z_m^n."""
    distance = 0
    for ui, vi in zip(u, v):
        diff = int(ui - vi)   # Calculate the modular difference
        distance += min(diff, m - diff) % q  # Use Lee weight definition
    return distance

def lee_weight(vector,q):
    vector = [component % q for component in vector]
    return sum(min(component, q - component) % q for component in vector)

def generate_lee_error_vectors(n, vector_weight, num_vectors, q, max_tries=10000):
    unique_vectors = set()
    attempts = 0

    while len(unique_vectors) < num_vectors and attempts < max_tries:

        vector = [0] * n
        added_weight = 0
        while added_weight < vector_weight:
            available_indexes = [i for i in range(n) if abs(vector[i]) < q // 2] 
            if not available_indexes:
                print("Ran out of indexes to add weight.")
                break
            index = random.choice(available_indexes)
            vector[index] += 1
            added_weight += 1
        # Randomly invert each coordinate with a 50% probability
        vector = [component if random.random() > 0.5 else -component for component in vector]
        if lee_weight(vector, q) == vector_weight:
            unique_vectors.add(tuple(vector))
        else:
            print(f"Vector {vector} has Lee weight {lee_weight(vector, q)} instead of {vector_weight}.")
        attempts += 1

    if len(unique_vectors) < num_vectors:
        print("Only generated", len(unique_vectors), "unique error vectors out of", num_vectors, "requested.")

    return list(unique_vectors)

def get_error_vectors_lee(n, q, num_vectors, max_tries=10000):
    error_vectors = []
    for weight in range(1, q):
        error_vectors.extend(generate_lee_error_vectors(n, weight, num_vectors, q, max_tries))
    return error_vectors



"""
Error Vector Generation
Generates vectors_per_weight error vectors for weights from 1 to q-1
"""
def get_error_vectors_hamming(n, q, vectors_per_weight):
    error_vectors = []
    for i in range(1, q):
        error_vectors.extend(generate_marc_error_vectors(n, i, vectors_per_weight))

    return error_vectors

def generate_marc_error_vectors(n, t, num_vectors, max_tries=10000):
    unique_vectors = set()
    attempts = 0
    while len(unique_vectors) < num_vectors and attempts < max_tries:
        vector = get_marc_error_vector(n, t)
        unique_vectors.add(tuple(vector))
        attempts += 1

    if len(unique_vectors) < num_vectors:
        print("Only generated", len(unique_vectors), "unique error vectors out of", num_vectors, "requested.")

    return [list(v) for v in unique_vectors]
def get_marc_error_vector(n, t):
    error_vector = [0]*n
    for _ in range(t):
        idx = random.randint(0, n-1)     # get random coordinate 
        error_vector[idx] += 1   # add 1 to this coordinate
    for i in range(n):
        if random.choice([True, False]):
            error_vector[i] = -error_vector[i]
    return error_vector

"""Estimate the minimum distance d for large n using the Gilbert-Varshamov Bound."""
def estimate_minimum_distance_hamming(n,k,q):
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
def solve(G, target_vector,q, error_vector, metric):
    n = len(target_vector)
    lattice = transform_to_lattice(G,n,q)

    t = 1

    lattice = kannan_embedding(lattice, target_vector, t,q)

    result_vectors = matrix(ZZ, lattice).BKZ()
    if metric == "l2":
        shortest_vector = result_vectors[0]
    elif metric == "lee":
        shortest_vector = min(result_vectors, key=lambda x: lee_weight(x, q))
    elif metric == "l1":
        shortest_vector = min(result_vectors, key=lambda x: sum(abs(i) for i in x))

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
def simulate_code(G, code_word, q, error_vectors, metric, verbose: bool = False):

    if metric not in {"l2", "lee", "l1"}:
        raise ValueError("Metric must be one of 'l2', 'lee', 'l1'")

    n = G.ncols()
    k = G.nrows()
    kannang_t = 1

    if verbose:
        print(f"n: {n}, k: {k}, q: {q}")
    
    failed_vectors = []
    good_vectors = []
    for error_vector in error_vectors:
        received_word = (code_word + vector(GF(q),error_vector)) % q # not sure if i shouuld take the modulo here
        decoded_error_vector = solve(G, received_word, q, error_vector=error_vector, metric=metric)

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

def write_to_csv(sub_dir, n, k, q, good_vectors, failed_vectors, estimated_t, metric):

    directory = "./data"
    full_directory_path = os.path.join(directory, sub_dir)

    csv_file_path = os.path.join(full_directory_path, f"result_n{n}_k{k}_q{q}_estimated_t{estimated_t}_{metric}.csv")
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
    error_vectors_lee = get_error_vectors_lee(n, q, 500)

    random_code = codes.random_linear_code(GF(q), n, k)
    G = random_code.generator_matrix()
    min_distance = estimate_minimum_distance_hamming(n, k, q) 
    t_hamming = (min_distance - 1) // 2
    t_lee = (estimate_minimum_distance_lee(n, k, q) - 1) // 2
    if min_distance < 3:
        raise ValueError("Estimated Minimum distance for this (n,k,q) code is less than 3")

    random_message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
    codeword = random_message * G

    good_vectors_l2, failed_vectors_l2 = simulate_code(G, codeword, q=q, error_vectors=[sublist[:] for sublist in error_vectors_lee], metric="l2", verbose=True)
    write_to_csv(sub_dir, n, k, q, good_vectors_l2, failed_vectors_l2, t_hamming, metric="l2")
    good_vectors_l1, failed_vectors_l1 = simulate_code(G, codeword, q=q, error_vectors=[sublist[:] for sublist in error_vectors_lee], metric="l1", verbose=True)
    write_to_csv(sub_dir, n, k, q, good_vectors_l1, failed_vectors_l1, t_hamming, metric="l1") 
    good_vectors_lee, failed_vectors_lee = simulate_code(G, codeword, q=q, error_vectors=[sublist[:] for sublist in error_vectors_lee], metric="lee", verbose=True)
    write_to_csv(sub_dir, n, k, q, good_vectors_lee, failed_vectors_lee, t_lee, metric="lee")

primes = [5,17,101]   
n = [10,20, 30, 40, 50]
k = [5,10, 15, 20, 25]

current = 0

for prime in primes:
    for i in range(len(n)):
        current += 1
        print(f"Simulation: {current} / {len(n) * len(primes)}")
        do_simulation(prime, n[i], k[i], "decoding_tis1")
