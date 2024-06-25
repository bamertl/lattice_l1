from sage.all import *
import itertools
import random

def get_num_error_vectors_with_max_weight(n, q, max_error_weight):
    return sum(binomial(n, i) * (q - 1)**i for i in range(1, max_error_weight + 1))

def get_num_error_vectors_with_weight(n, q, error_weight):
    return binomial(n, error_weight) * (q-1)**error_weight


def get_marc_lee_error_vector(n, t):
    error_vector = [0]*n
    for _ in range(t):
        idx = random.randint(0, n-1)     # get random coordinate 
        error_vector[idx] += 1   # add 1 to this coordinate
    for i in range(n):
        if random.choice([True, False]):
            error_vector[i] = -error_vector[i]
    return error_vector

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

""" 
Gets errors with max lee weight of t, includes negative numbers for the upper spectrum
"""
def get_error_vectors_with_negative(n,q):
    error_vectors = []
    for i in range(q):
        for j in range(3):
            error_vector = [0]*n
            error_vector[j] = i - int(q/2)
            error_vectors.append(error_vector)
            error_vector = [0] * n
    return error_vectors

def get_all_error_vectors_from_band(n,q):
    error_vectors = []
    for i in range(q):
        for j in range(3):
            error_vector = [0]*n
            error_vector[j] = i
            error_vectors.append(error_vector)
            error_vector = [0] * n
    return error_vectors



"""
This gets a number of error vectors uniformly distribued from all possible error_vectors, use this for larger n and q 
"""
def get_error_vectors_uniform(n, q, error_weight, num_vectors):
    
    total_vectors = get_num_error_vectors_with_weight(n, q, error_weight)
    print(f"Trying to fetch {num_vectors} error vectors of weight {error_weight} out of {total_vectors} total possible vectors.")

    if num_vectors > total_vectors:
        raise ValueError(f"Requested number of error vectors {num_vectors} exceeds the total possible number of error vectors {total_vectors}.")
    
    error_vectors = set()
    tries = 0
    max_tries = 10000

    while len(error_vectors) < num_vectors:
        if tries >= max_tries:
            raise RuntimeError(f"Failed to generate {num_vectors} unique error vectors within {max_tries} tries.")

        indices = random.sample(range(n), error_weight)
        values = [random.randint(1, q-1) for _ in range(error_weight)]

        vector = [0] * n
        for idx, val in zip(indices, values):
            vector[idx] = val

        vector_tuple = tuple(vector) # convert to tuple to check for uniqueness
        if vector_tuple not in error_vectors:
            error_vectors.add(vector_tuple)
        else:
            tries += 1
        
    error_vectors = [list(vector) for vector in error_vectors]
    return error_vectors

""" Will do it for the first 3 coordinates"""
def get_error_vectors_coordinate_not_uniform(n, q, num_vectors):
    per_coordinate = num_vectors // 3
    if q < per_coordinate:
        per_coordinate = q - 1
    
    error_vectors = []
    for i in range(per_coordinate // 2):
        error_vector = [0] * n
        for j in range(3):
            error_vector[j] = i 
            error_vectors.append(error_vector)
            error_vector = [0] * n

    for i in range(per_coordinate // 2):
        value = q - i - 1

        for j in range(3):
            error_vector[j] = value
            error_vectors.append(error_vector)
            error_vector = [0] * n

    # make them unique
    error_vectors = list(set([tuple(vector) for vector in error_vectors]))
    print("Total Number of Error Vectors", len(error_vectors))
    return error_vectors