from sage.all import *
from dataclasses import dataclass
from sage.modules.free_module_integer import IntegerLattice
from tqdm import tqdm
import itertools
import random
from .solver import solve


"""
Simulate different parameters for the linear code and codeword
:param G: matrix, generator matrix of the linear code
:param code_word: vector, the codeword with an error vector added
:param q: int, modulus (ring or field size)
:param max_error_weight: int, maximum weight of the error vector, can be found out from G

:return: SimulationStats, a dataclass containing the statistics of the simulation
"""

def simulate_code(G, code_word, q, max_error_weight, num_vectors=1000, verbose: bool = False):
    #print("Simulating for G:", G)
    n = G.ncols()
    k = G.nrows()
    t = 1
    if verbose:
        print(f"n: {n}, k: {k}, q: {q}, t:{t} max_error_weight: {max_error_weight}")
    

    error_vectors = get_error_vectors_uniform(n, q, max_error_weight, num_vectors) 

    failed_vectors = []
    good_vectors = []
    for error_vector in tqdm(error_vectors):
        received_word = (code_word + vector(GF(q),error_vector)) % q
        decoded_error_vector = solve(G, received_word, q, t)

        error_vector = vector(ZZ, error_vector)
        if error_vector != decoded_error_vector:
            failed_vectors.append(error_vector)
        else:
            good_vectors.append(error_vector)
    if verbose: 
        print(f"Fails: {len(failed_vectors)}, Success: {len(good_vectors)}")
    stats = create_stats(failed_vectors, good_vectors, G, n, q, k, t)   
    if verbose:
        print(f"Stats: {stats}")
    return stats

@dataclass
class SimulationStats:
    num_failed: int
    num_good: int

    n: int
    k: int
    q: int
    t: int

    mean_l2_norm_failed: int
    max_l2_norm_failed: int
    min_l2_norm_failed: int

    mean_l1_norm_failed: int
    max_l1_norm_failed: int
    min_l1_norm_failed: int

    mean_l2_norm_good: int
    max_l2_norm_good: int
    min_l2_norm_good: int

    mean_l1_norm_good: int
    max_l1_norm_good: int
    min_l1_norm_good: int


def create_stats(failed_vectors, good_vectors, G, n, q, k, t):
    mean_l2_norm_failed = 0 
    max_l2_norm_failed = 0
    min_l2_norm_failed = 0
    mean_l1_norm_failed = 0
    max_l1_norm_failed = 0
    min_l1_norm_failed = 0

    if len(failed_vectors) > 0:    
        mean_l2_norm_failed = int(sum([v.norm(2) for v in failed_vectors]) / len(failed_vectors))
        max_l2_norm_failed = int(max([v.norm(2) for v in failed_vectors]))
        min_l2_norm_failed = int(min([v.norm(2) for v in failed_vectors]))
        mean_l1_norm_failed = int(sum([v.norm(1) for v in failed_vectors]) / len(failed_vectors))
        max_l1_norm_failed = int(max([v.norm(1) for v in failed_vectors]))
        min_l1_norm_failed = int(min([v.norm(1) for v in failed_vectors]))    

    mean_l2_norm_good = 0
    max_l2_norm_good = 0
    min_l2_norm_good = 0
    mean_l1_norm_good = 0
    max_l1_norm_good = 0
    min_l1_norm_good = 0
    if(len(good_vectors) > 0):
        mean_l2_norm_good = int(sum([v.norm(2) for v in good_vectors]) / len(good_vectors))
        max_l2_norm_good = int(max([v.norm(2) for v in good_vectors]))
        min_l2_norm_good = int(min([v.norm(2) for v in good_vectors]))
        mean_l1_norm_good = int(sum([v.norm(1) for v in good_vectors]) / len(good_vectors))
        max_l1_norm_good = int(max([v.norm(1) for v in good_vectors]))
        min_l1_norm_good = int(min([v.norm(1) for v in good_vectors]))

    return SimulationStats(
        len(failed_vectors),
        len(good_vectors), 
        n, 
        k, 
        q, 
        t,
        mean_l2_norm_failed, 
        max_l2_norm_failed, 
        min_l2_norm_failed, 
        mean_l1_norm_failed, 
        max_l1_norm_failed, 
        min_l1_norm_failed, 
        mean_l2_norm_good, 
        max_l2_norm_good, 
        min_l2_norm_good, 
        mean_l1_norm_good, 
        max_l1_norm_good, 
        min_l1_norm_good, 
    )

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