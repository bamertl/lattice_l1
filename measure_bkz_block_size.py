from sage.all import *

import numpy as np
import random
import csv
import os
import time

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
def solve(G, target_vector,q, t, block_size):
    n = len(target_vector)
    start_lattice_transform_time = time.time_ns()
    lattice = transform_to_lattice(G,n,q)
    lattice_transform_time = time.time_ns() - start_lattice_transform_time
    
    start_kannan_embedding_time = time.time_ns()
    lattice = kannan_embedding(lattice, target_vector, t,q)
    kannan_embedding_time = time.time_ns() - start_kannan_embedding_time

    start_shortest_vector_time = time.time_ns()
    shortest_vector = matrix(ZZ, lattice).BKZ(block_size=block_size)[0]
    shortest_vector_time = time.time_ns() - start_shortest_vector_time
    # return only first n elements of shortest vector, the last element is the t (added dimension in kannan embedding)
    return vector(shortest_vector[:n]), lattice_transform_time, kannan_embedding_time, shortest_vector_time

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
def simulate_code(G, code_word, q, error_vectors, block_size, verbose: bool = False):
    n = G.ncols()
    k = G.nrows()
    kannang_t = 1

    lattice_transform_times = []
    kannan_embedding_times = []
    shortest_vector_times = []


    if verbose:
        print(f"n: {n}, k: {k}, q: {q}")
    
    failed_vectors = []
    good_vectors = []
    for error_vector in error_vectors:
        received_word = (code_word + vector(GF(q),error_vector)) % q # not sure if i shouuld take the modulo here
        decoded_error_vector, lattice_transform_time, kannan_embedding_time, shortest_vector_time = solve(G, received_word, q, kannang_t, block_size)
        lattice_transform_times.append(lattice_transform_time)
        kannan_embedding_times.append(kannan_embedding_time)
        shortest_vector_times.append(shortest_vector_time)
        error_vector = vector(ZZ, error_vector)
        if error_vector != decoded_error_vector:
            failed_vectors.append(error_vector)
        else:
            good_vectors.append(error_vector)
    if verbose: 
        print(f"Fails: {len(failed_vectors)}, Success: {len(good_vectors)}")
        print(f"Average lattice transform time: {sum(lattice_transform_times)/len(lattice_transform_times) / 1e6} ms with min: {min(lattice_transform_times) / 1e6} ms and max: {max(lattice_transform_times) / 1e6} ms and std: {np.std(lattice_transform_times) / 1e6}")
        print(f"Average kannan embedding time: {sum(kannan_embedding_times)/len(kannan_embedding_times) / 1e6} ms with min: {min(kannan_embedding_times) / 1e6} ms and max: {max(kannan_embedding_times) / 1e6} ms and std: {np.std(kannan_embedding_times) / 1e6}")
        print(f"Average shortest vector time: {sum(shortest_vector_times)/len(shortest_vector_times) / 1e6} ms with min: {min(shortest_vector_times) / 1e6} ms and max: {max(shortest_vector_times) / 1e6} ms and std: {np.std(shortest_vector_times) / 1e6}")

    return good_vectors, failed_vectors, lattice_transform_times, kannan_embedding_times, shortest_vector_times

"""
Write to CSV
"""

custom_name = "simulation_results"

def write_to_csv(sub_dir, n, k, q, good_vectors, failed_vectors, estimated_t, block_size):

    directory = "./data"
    full_directory_path = os.path.join(directory, sub_dir)

    csv_file_path = os.path.join(full_directory_path, f"result_n{n}_k{k}_q{q}_estimated_t{estimated_t}_block_size{block_size}.csv")
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

def write_times_to_csv(sub_dir, n, k, q, lattice_transform_times, kannan_embedding_times, shortest_vector_times, all_time_min_distance, block_size):
    directory = "./data"
    full_directory_path = os.path.join(directory, sub_dir)
    csv_file_path = os.path.join(full_directory_path, f"result_times_ns.csv")
    os.makedirs(full_directory_path, exist_ok=True)

    avg_lattice_transform_time = sum(lattice_transform_times)/len(lattice_transform_times)
    stv_lattice_transform_time = np.std(lattice_transform_times)
    avg_kannan_embedding_time = sum(kannan_embedding_times)/len(kannan_embedding_times)
    stv_kannan_embedding_time = np.std(kannan_embedding_times)
    avg_shortest_vector_time = sum(shortest_vector_times)/len(shortest_vector_times)
    stv_shortest_vector_time = np.std(shortest_vector_times)

    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the headers (optional)
        if not file_exists:
            writer.writerow(['n', 'k', 'q', 
                             'avg_lattice_transform_time', 'stv_lattice_transform_time',
                             'avg_kannan_embedding_time', 'stv_kannan_embedding_time',
                             'avg_shortest_vector_time', 'stv_shortest_vector_time',
                             'all_time_min_distance', 'block_size'])

        writer.writerow([n, k, q, 
                         avg_lattice_transform_time, stv_lattice_transform_time,
                         avg_kannan_embedding_time, stv_kannan_embedding_time,
                         avg_shortest_vector_time, stv_shortest_vector_time,
                         all_time_min_distance, block_size])

def do_simulation(q, n, k,  sub_dir, block_size):
    error_vectors = get_error_vectors(n, q, 300) 
    random_code = codes.random_linear_code(GF(q), n, k)
    G = random_code.generator_matrix()
    #measure time of estimate_minimum_distance
    start_time_min_distance = time.time_ns()
    min_distance = estimate_minimum_distance(n, k, q)
    end_time_min_distance = time.time_ns()
    all_time_min_distance = end_time_min_distance - start_time_min_distance

    t = (min_distance - 1) // 2
    if min_distance < 3:
        raise ValueError("Estimated Minimum distance for this (n,k,q) code is less than 3")

    random_message = vector(GF(q), [random.randint(0, q-1) for _ in range(k)])
    codeword = random_message * G
    good_vectors, failed_vectors, lattice_transform_times, kannan_embedding_times, shortest_vector_times = simulate_code(G, codeword, q=q, error_vectors=[sublist[:] for sublist in error_vectors], block_size=block_size, verbose=True)
    write_to_csv(sub_dir, n, k, q, good_vectors, failed_vectors, t, block_size)
    write_times_to_csv(sub_dir, n, k, q, lattice_transform_times, kannan_embedding_times, shortest_vector_times, all_time_min_distance, block_size)


    print(f"Average time for estimate_minimum_distance: {all_time_min_distance} ns or {(all_time_min_distance)/10**6} ms")

primes = [5,17]   
n = [23,23,23,  31, 31,31, 51,51,51]
k = [7,11,15,   11, 15,19, 26,34,42]


current = 0

for prime in primes:
    for i in range(len(n)):
        max_block_size = n[i]  # Set the maximum block size to n[i]
        for block_size in range(10, max_block_size, 10):  # Step by 10, starting from 10 to max_block_size
            current += 1
            print(f"Simulation: {current} / {len(n) * len(primes) * ((max_block_size - 10) // 10 + 1)}")
            try:
                do_simulation(prime, n[i], k[i], "bkz_block_size", block_size=block_size)
            except ValueError as e:
                print(f"An error occurred: {e}")
