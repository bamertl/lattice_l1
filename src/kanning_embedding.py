import numpy as np

def kanning_embedding(lattice_basis, target_vector, embedding_scale_factor):
    lattice_basis = lattice_basis
    target_vector_2d = target_vector.reshape(-1, 1)
    lattice_basis = np.concatenate((lattice_basis, target_vector_2d), axis=1)
    additional_row = np.zeros((1, lattice_basis.shape[1]), dtype=int)
    additional_row[0, -1] = embedding_scale_factor
    lattice_basis = np.concatenate((lattice_basis, additional_row), axis=0)
    return lattice_basis

