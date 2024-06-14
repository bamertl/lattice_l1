from sage.all import *
from dataclasses import dataclass
from tqdm import tqdm
from solver import solve

"""
Simulate different parameters for the linear code and codeword
:param G: matrix, generator matrix of the linear code
:param code_word: vector, the codeword with an error vector added
:param q: int, modulus (ring or field size)
:param max_error_weight: int, maximum weight of the error vector, can be found out from G

:return: SimulationStats, a dataclass containing the statistics of the simulation
"""

def simulate_code(G, code_word, q, max_error_weight, error_vectors, verbose: bool = False):
    #print("Simulating for G:", G)
    n = G.ncols()
    k = G.nrows()
    t = 1
    if verbose:
        print(f"n: {n}, k: {k}, q: {q}, t:{t} max_error_weight: {max_error_weight}")
    
    failed_vectors = []
    good_vectors = []
    for error_vector in tqdm(error_vectors):
        received_word = (code_word + vector(GF(q),error_vector)) % q # not sure if i shouuld take the modulo here
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
    return stats, good_vectors, failed_vectors

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

    max_lee_weight_good: int
    min_lee_weight_failed: int


def create_stats(failed_vectors, good_vectors, G, n, q, k, t):
    mean_l2_norm_failed = 0 
    max_l2_norm_failed = 0
    min_l2_norm_failed = 0
    mean_l1_norm_failed = 0
    max_l1_norm_failed = 0
    min_l1_norm_failed = 0
    min_lee_weight_failed = 0

    if len(failed_vectors) > 0:    
        mean_l2_norm_failed = int(sum([v.norm(2) for v in failed_vectors]) / len(failed_vectors))
        max_l2_norm_failed = int(max([v.norm(2) for v in failed_vectors]))
        min_l2_norm_failed = int(min([v.norm(2) for v in failed_vectors]))
        mean_l1_norm_failed = int(sum([v.norm(1) for v in failed_vectors]) / len(failed_vectors))
        max_l1_norm_failed = int(max([v.norm(1) for v in failed_vectors]))
        min_l1_norm_failed = int(min([v.norm(1) for v in failed_vectors]))    
        min_lee_weight_failed: int = min([lee_weight(v, q) for v in failed_vectors])

    mean_l2_norm_good = 0
    max_l2_norm_good = 0
    min_l2_norm_good = 0
    mean_l1_norm_good = 0
    max_l1_norm_good = 0
    min_l1_norm_good = 0
    max_lee_weight_good = 0
    if(len(good_vectors) > 0):
        mean_l2_norm_good = int(sum([v.norm(2) for v in good_vectors]) / len(good_vectors))
        max_l2_norm_good = int(max([v.norm(2) for v in good_vectors]))
        min_l2_norm_good = int(min([v.norm(2) for v in good_vectors]))
        mean_l1_norm_good = int(sum([v.norm(1) for v in good_vectors]) / len(good_vectors))
        max_l1_norm_good = int(max([v.norm(1) for v in good_vectors]))
        min_l1_norm_good = int(min([v.norm(1) for v in good_vectors]))
        max_lee_weight_good = max([lee_weight(v, q) for v in good_vectors])

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
        max_lee_weight_good,
        min_lee_weight_failed
    )

def lee_weight(vector, q):
    return sum(abs(x) if abs(x) < q / 2 else q - abs(x) for x in vector)


