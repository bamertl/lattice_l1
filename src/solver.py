from sage.all import *
from sage.modules.free_module_integer import IntegerLattice
"""
This transforms the code into a lattice and then embeds it with the target vector 
and finally tries to solve the shortest vector problem to find the error vector that was added to the codeword.
:param G: matrix, generator matrix of the linear code
:param target_vector: vector, the codeword with an error vector added
:param q: int, modulus (ring or field size)
:param t: int, value to add to the new dimension from the embedding

returns the error vector (hopefully)
"""
def solve(G, target_vector,q, t):
    n = len(target_vector)
    lattice = transform_to_lattice(G,n,q)
    lattice = kannan_embedding(lattice, target_vector, t)

    shortest_vector = matrix(ZZ, lattice).LLL()[0]
    # return only first n elements of shortest vector, the last element is the t (added dimension in kannan embedding)
    return vector(shortest_vector[:n])

"""
Transforms to lattice by embedding with q*I_n and then calculating the Hermite Normal Form
"""
def transform_to_lattice(G, n, q):
    G = matrix(ZZ, G)
    G.change_ring(ZZ)
    I_n = identity_matrix(ZZ, n) * q
    augmented_matrix = G.T.augment(I_n).T
    return augmented_matrix.hermite_form(include_zero_rows=False)

"""
Kannan Embedding to transform BDD Problem to Shortest Vector Problem
"""
def kannan_embedding(lattice, target_vector, t):
    # Embed the target vector into the lattice
    target_vector = target_vector.change_ring(ZZ)
    lattice = lattice.stack(target_vector) # adds as row
    zeros = vector(ZZ, [0] * (len(target_vector) + 1))
    zeros[-1] = 1
    return lattice.augment(zeros) # adds as columns
