import numpy as np
from math import comb, log, exp

class RandomLinearCode:
    def __init__(self, n, k, q):
        """
        Initialize a random linear code.
        :param n: int, length of the code
        :param k: int, dimension of the code
        :param q: int, modulus (ring or field size) 
        """
        self.n = n
        self.k = k
        self.q = q
        if k > n:
            raise ValueError("k must not exceed n.")
        self.estimated_minimum_distance = self._estimate_minimum_distance()
        self.generator_matrix = self._generate_matrix()
        self.t = (self.estimated_minimum_distance - 1) // 2

    def calculate_exact_minimum_distance(self):

        min_distance = self.n   # Start with the maximum possible distance, which is n

        # Loop over all possible non-empty subsets of row indices
        for i in range(1, 2**self.k):
            codeword = np.zeros(self.n, dtype=int)
            # Generate the codeword by summing selected rows
            for j in range(self.k):
                if i & (1 << j):  # Check if the j-th bit of i is set
                    codeword = (codeword + self.generator_matrix[j]) % self.q

            weight = np.count_nonzero(codeword)
            if weight < min_distance:
                min_distance = weight
                # Early exit if a codeword of weight 1 is found
                if min_distance == 1:
                    break

        return min_distance


    def _estimate_minimum_distance(self):
        """
         Estimate the minimum distance d for large n using the Gilbert-Varshamov Bound.
    
        Parameters:
        n (int): Length of the code.
        k (int): Dimension of the code.
        q (int): Size of the symbol alphabet (prime number).

        Returns:
        int: Approximate minimum distance d.
        """
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

    def _generate_matrix(self):
        """
        Attempt to generate a random k x n generator matrix with linearly independent rows over GF(q).
        :return: np.array, a k x n generator matrix with elements in GF(q)
        """
        matrix = np.zeros((0, self.n), dtype=int)
        max_attempts = 1000
        attempts = 0

        while matrix.shape[0] < self.k and attempts < max_attempts:
            new_row = np.random.randint(0, self.q, size=(1, self.n))
            if self._is_independent(new_row, matrix):
                matrix = np.vstack([matrix, new_row])
            attempts += 1
        
        if matrix.shape[0] < self.k:
            raise ValueError("Failed to generate a matrix with linearly independent rows after 1000 attempts.")
        return matrix


    def _is_independent(self, new_row, existing_matrix):
        """
        Check if a new row is linearly independent from the rows of the existing matrix.
        
        :param new_row: np.array, the new row to test
        :param existing_matrix: np.array, the existing matrix of rows
        :return: bool, True if the row is independent, False otherwise
        """
        if existing_matrix.size == 0:
            return True
        test_matrix = np.vstack([existing_matrix, new_row])
        rank = np.linalg.matrix_rank(test_matrix % self.q)
        return rank > existing_matrix.shape[0]

    def get_random_message(self):
        """
        Generate a random message of length k
        """
        return np.random.randint(0, self.q, size=self.k)

    def get_random_error_vector(self):
        """ Generate random error vector of maximum weight t"""
        error_vector = np.zeros(self.n, dtype=int)
        error_positions = np.random.choice(self.n, self.t, replace=False)
        error_vector[error_positions] = np.random.choice(self.q, self.t)
        return error_vector

    def encode(self, message):
        """
        Encode a message using the generator matrix.
        
        :param message: np.array, a 1D array of length k with elements in GF(q)
        :return: np.array, encoded message of length n
        """
        if len(message) != self.k:
            raise ValueError("Message length must be equal to k.")
        return np.dot(message, self.generator_matrix) % self.q

    def __str__(self):
        return f"RandomLinearCode(n={self.n}, k={self.k}, q={self.q}) \nGenerator Matrix:\n{self.generator_matrix} \nEstimated Minimal Minimum Distance: {self.estimated_minimum_distance} --> Max error weight by estimation t={self.t}"

