import numpy as np

class Lattice:
    def __init__(self, basis_matrix):
        self.basis = np.array(basis_matrix)
        self.dim = self.basis.shape[1] ## Matrix is full rank

    def print_stats(self):
        print("Volume %f " % self.volume())
        print("orthogonality %f" % self.get_orthonogality())

    def volume(self):
        A = np.array(self.basis, dtype=np.float64)
        
        return np.abs(np.linalg.det(A))

    def get_orthonogality(self):
        A = np.array(self.basis, dtype=np.float64)
        return np.linalg.norm(A, 'fro')