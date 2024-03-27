import numpy as np
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
from itertools import product

## If modulo is prime, it is a field, if not, it is a ring and not all elements are invertible
class FiniteField:
    def __init__(self, dimensions, prime):
        self.dimensions = dimensions
        self.prime = prime

## n = number of vectors (length of code), k = dimension of each vector
class LinearCode:
    def __init__(self, finite_field, n, k):
        self.finite_field = finite_field
        self.n = n
        self.k = k
        self.generator_matrix_code = self.generate_random_generator_matrix(n, k, finite_field.prime)
        print("Generator Matrix (G) over F_{}: \n".format(finite_field.prime), self.generator_matrix_code)
        ## Print the matrix beautifully, not simple print np.array

    def generate_random_generator_matrix(self, n, k, p):
        vectors = []  # Start with an empty list of vectors
        while len(vectors) < k:
            candidate_vector = np.random.randint(0, p, size=n)
            new_vectors = vectors + [candidate_vector]
            if self._is_linearly_independent(new_vectors):
                vectors = new_vectors
        return np.array(vectors)

    """Check if a set of vectors is linearly independent."""
    def _is_linearly_independent(self, vectors):
        if len(vectors) == 0:
            return True
        # Calculate the rank of the matrix formed by vectors
        matrix = np.array(vectors)
        return np.linalg.matrix_rank(matrix, tol=1e-6) == len(vectors)

    def generate_all_codewords(self):
        k = self.generator_matrix_code.shape[0]  # Number of rows in the generator matrix
        # Generate all possible information vectors (all binary combinations of length k)
        information_vectors = list(product([0, 1], repeat=k))
        # Initialize a list to store codewords
        codewords = []
        for info_vec in information_vectors:
            # Convert info_vec to numpy array and multiply by generator matrix
            codeword = np.dot(info_vec, self.generator_matrix_code) % self.finite_field.prime 
            # Convert numpy array codeword to tuple
            codeword_tuple = tuple(codeword)
            codewords.append(codeword_tuple)
        print("All Codewords: \n", codewords)
        return codewords

""" n = length of code, k = dimension of each vector """
class ConstructionA:
    def __init__(self, finite_field, n, k):
        self.finite_field = finite_field
        self.linear_code = LinearCode(finite_field, n, k)
        self.lattice_bases = self._generate_lattice_bases(self.linear_code.generator_matrix_code, finite_field.prime)
        print("Lattice Bases (H) over F_{}: \n".format(finite_field.prime), self.lattice_bases)

    def _augment_with_canonical_basis_and_scale(self, basis_vectors, q):
        n = basis_vectors.shape[1]  # Number of columns = dimension of the space
        # Scale the original basis vectors by q
        # Create the scaled canonical basis
        scaled_canonical_basis = q * np.identity(n, dtype=int)
        # Combine the two sets of basis vectors
        augmented_basis = np.vstack((basis_vectors, scaled_canonical_basis))
        return augmented_basis

    def _generate_lattice_bases(self, code_generator_matrix, q):
        # First, augment the basis vectors with the canonical basis, scaled by q
        augmented_basis = self._augment_with_canonical_basis_and_scale(code_generator_matrix, q)
        print("Augmented Basis: \n", augmented_basis)
        # Convert to a sympy Matrix
        sympy_matrix = Matrix(augmented_basis.tolist())
        # Compute the HNF
        H = hermite_normal_form(sympy_matrix.T)   
        return np.array(H.T)  # Transpose to get back to the original orientation