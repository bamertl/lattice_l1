from sage.all import *
from src import my_lll
import numpy as np
from tqdm import tqdm


def one_test(m):
    MY_MLLL = my_lll.lll_reduction(m)
    SAGE_MLLL = np.array(m.LLL())
    print("mine \n", MY_MLLL)
    print("their\n",SAGE_MLLL)
    # assert that the matrixes are equal, simply assert doesn't work here
    assert (MY_MLLL == SAGE_MLLL).all()


def generate_random_linearly_independent_matrix(k, j):
    # Ensure valid dimensions
    if k <= 0 or j <= 0:
        raise ValueError("Dimensions k and j must be greater than 0.")
    
    # Create an empty matrix of the desired dimensions
    matrix = np.zeros((k, j), dtype=int)
    
    # Fill in the matrix to ensure linear independence
    min_dim = min(k, j)
    for i in range(min_dim):
        matrix[i, i] = 1  # Ensuring part of the matrix has linearly independent vectors
    
    # Fill the rest of the matrix with random values
    if k > j:
        # If more rows than columns, fill the extra rows randomly
        matrix[j:k, :] = np.random.randint(-10, 10, size=(k - j, j))
    elif j > k:
        # If more columns than rows, fill the extra columns randomly
        matrix[:, k:j] = np.random.randint(-10, 10, size=(k, j - k))
    else:
        # For extra randomness in square matrices, add random values but keep diagonal dominance
        for i in range(k):
            for j in range(i + 1, k):
                matrix[i, j] = np.random.randint(-10, 10)
                matrix[j, i] = np.random.randint(-10, 10)

    return matrix

def test_custom_lll():
    print("hi")
    for i in tqdm(range(10)):
        m = generate_random_linearly_independent_matrix(3, 3)
        # cast do sage matrix
        m = matrix(m)
        one_test(m)    
    print("All successfull")

test_custom_lll()