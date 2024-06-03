import numpy as np
from math import comb, log, exp
import sage.all as sage

"""
Initialize a random linear code.
:param n: int, length of the code
:param k: int, dimension of the code
:param q: int, modulus (ring or field size) 
"""
class RandomLinearCode:
    def __init__(self, n, k, q):
        self.F = sage.GF(q)
        self.n = n
        self.k = k
        self.q = q
        if k > n:
            raise ValueError("k must not exceed n.")
        self.generator_matrix = self._generate_matrix()
        self.estimated_minimum_distance = self._estimate_minimum_distance()
        self.actual_min_distance = self.min_distance_sage()
        self.t = (self.actual_min_distance - 1) // 2

    def min_distance_sage(self):
        self.G = sage.Matrix(self.F, self.generator_matrix)
        self.sage_code = sage.codes.LinearCode(self.G)
        min_distance = self.sage_code.minimum_distance()
        return min_distance
        
    """Estimate the minimum distance d for large n using the Gilbert-Varshamov Bound."""
    def _estimate_minimum_distance(self):
        M = self.q**self.k  # Size of the code C
        log_M = self.k * log(self.q)
    
        # Estimate for d using an approximation
        low, high = 1, self.n
        while low < high:
            mid = (low + high + 1) // 2
            sum_terms = sum(comb(self.n, i) * (self.q - 1)**i for i in range(mid))
            if log(sum_terms) - self.n * log(self.q) > -log_M:
                high = mid - 1
            else:
                low = mid
        return low

    """Get the kxk identy matrix and then add n-k columns random columns to it """
    def _generate_matrix(self):
        matrix = np.eye(self.k, dtype=int)
        # now add random n-k columns to the matrix
        random_part = np.random.randint(0, self.q, size=(self.k, self.n - self.k))
        print(matrix)
        print("Random" , random_part)
        matrix = np.hstack([matrix, random_part])
        print("Matrix", matrix)
        return matrix

    """ Generate a random message of length k"""
    def get_random_message(self):
        return np.random.randint(0, self.q, size=self.k)

    """ Generate random error vector of maximum weight t, make sure the error vector is not all zeros, if t = 0 throw error"""
    def get_random_error_vector(self):
        if self.t == 0:
            raise ValueError("t must be greater than 0.")
        error_vector = np.zeros(self.n, dtype=int)
        while np.count_nonzero(error_vector) == 0:
            error_positions = np.random.choice(self.n, self.t, replace=False)
            error_vector[error_positions] = np.random.choice(self.q, self.t)
        return error_vector
    
    """ Encode a message using the generator matrix. """
    def encode(self, message):
        if len(message) != self.k:
            raise ValueError("Message length must be equal to k.")
        return np.dot(message, self.generator_matrix) % self.q

    def __str__(self):
        return f"RandomLinearCode(n={self.n}, k={self.k}, q={self.q}) \nGenerator Matrix:\n{self.generator_matrix} \nEstimated Minimal Minimum Distance: {self.estimated_minimum_distance} --> Max error weight by estimation t={self.t}"

