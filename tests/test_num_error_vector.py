import pytest
import itertools
# Add the src directory to the Python path
from src.simulation import get_num_error_vectors_with_max_weight, get_num_error_vectors_with_weight, get_error_vectors

def test_get_num_error_vectors():
    n = 5
    q = 17
    max_error_weight = 5
    num_error_vectors = get_num_error_vectors_with_weight(n, q, max_error_weight)
    vectors = get_error_vectors(n, q, max_error_weight)
    assert num_error_vectors == len(vectors)


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
    

if  __name__ == "__main__":
    test_get_num_error_vectors()
