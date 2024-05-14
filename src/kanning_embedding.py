import numpy as np

def kanning_embedding(lattice_basis, target_vector, embedding_scale_factor):
    lattice_basis = lattice_basis
    target_vector_2d = target_vector.reshape(1, -1)
    lattice_basis = np.concatenate((lattice_basis, target_vector_2d), axis=0)
    additional_column = np.zeros((lattice_basis.shape[0], 1), dtype=int)
    additional_column[-1, 0] = embedding_scale_factor
    lattice_basis = np.concatenate((lattice_basis, additional_column), axis=1)
    return lattice_basis

