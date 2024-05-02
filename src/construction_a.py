import numpy as np
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
from itertools import product


""" n = length of code, k = dimension of each vector """
class ConstructionA:
    def __init__(self, code_generator_matrix, q):
        self.lattice_bases = self._generate_lattice_bases(code_generator_matrix, q)

    def _augment_with_canonical_basis_and_scale(self, basis_vectors, q):
        ## make sure that n > k otherwise transpose the matrix
        if basis_vectors.shape[1] < basis_vectors.shape[0]:
            basis_vectors = basis_vectors.T


        n = basis_vectors.shape[1]  # Number of columns = dimension of the space
        # Scale the original basis vectors by q
        # Create the scaled canonical basis
        scaled_canonical_basis = q * np.identity(n, dtype=int)
        # Combine the two sets of basis vectors
        augmented_basis = np.vstack((basis_vectors, scaled_canonical_basis))
        return augmented_basis.T

    def _generate_lattice_bases(self, code_generator_matrix, q):
        # First, augment the basis vectors with the canonical basis, scaled by q
        augmented_basis = self._augment_with_canonical_basis_and_scale(code_generator_matrix, q)
        print("Augmented Basis: \n", augmented_basis)
        # Convert to a sympy Matrix
        sympy_matrix = Matrix(augmented_basis.tolist())
        # Compute the HNF
        H = hermite_normal_form(sympy_matrix)   
        return np.array(H)  # Transpose to get back to the original orientation