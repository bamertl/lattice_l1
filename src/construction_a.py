import numpy as np
import sympy as sp
from itertools import product
from sage.all import *
import sage.all as sage
import sage.matrix.matrix_integer_dense_hnf as matrix_integer_dense_hnf


""" n = length of code, k = dimension of each vector """
class ConstructionA:
    def __init__(self, code_generator_matrix, q):
        self.lattice_bases = self._generate_lattice_bases(code_generator_matrix, q)

    def _augment_with_canonical_basis_and_scale(self, basis_vectors, q):
        ## make sure that rows are greater than columns
        if basis_vectors.shape[0] < basis_vectors.shape[1]:
            basis_vectors = basis_vectors.T
        n = basis_vectors.shape[0]  # = n which is > l
        # Scale the original basis vectors by q
        # Create the scaled canonical basis
        scaled_canonical_basis = q * np.identity(n, dtype=int)
        # Combine the two sets of basis vectors, this could also be done with basis.T and then vstack, doesn't matter really
        print("Basis Vectors", basis_vectors)
        print("Scaled Canonical Basis", scaled_canonical_basis)

        augmented_basis = np.concatenate((basis_vectors, scaled_canonical_basis), axis=1)
        return augmented_basis

    def _generate_lattice_bases(self, code_generator_matrix, q):
        # First, augment the basis vectors with the canonical basis, scaled by q
        augmented_basis = self._augment_with_canonical_basis_and_scale(code_generator_matrix, q)
        print("Augmented Basis", augmented_basis)
        # Convert to a sympy Matrix
        A = sage.Matrix(ZZ, augmented_basis)
        H = matrix_integer_dense_hnf.hnf(A.transpose(), include_zero_rows=False)
        print(H)
        numpy_arr = H[0].numpy().T
        return numpy_arr  # Transpose to get lower triangular form