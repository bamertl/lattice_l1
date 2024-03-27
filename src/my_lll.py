import numpy as np


"""
LLL Algorithm
https://kth.diva-portal.org/smash/get/diva2:1674082/FULLTEXT01.pdf
"""
def vector_norm(v):
    return np.sqrt(np.dot(v, v))


def gram_schmidt(W):
    W = np.array(W, dtype=np.float64)
    V = W.copy()
    for i in range(1, W.shape[0]): # V[0] = W[0]
        for j in range(i):
            ph_i_j = np.dot(V[i], V[j]) / np.dot(V[j], V[j])
            V[i] -= ph_i_j * V[j]
    return V

def check_condition(U, delta, mu_k, k):
    return vector_norm(U[k]) ** 2 >= (delta - mu_k ** 2) * vector_norm(U[k-1]) ** 2


def get_mu(Basis, Ortho, k, j):
    return np.dot(Basis[k], Ortho[j]) / np.dot(Ortho[j], Ortho[j])


def lll_reduction(Basis, delta=0.75):
    """Apply the LLL algorithm to the basis B with delta as the Lovász condition."""
    Basis = np.array(Basis, dtype=float)  # Use float for calculations
    Ortho = gram_schmidt(Basis)
    n = len(Basis)
    k = 1
    while k < n:
        for j in range(k-1, -1, -1):
            mu = get_mu(Basis, Ortho, k, j) 
            if abs(mu) > 0.5:
                Basis[k] = Basis[k] - Basis[j] * round(mu)
                Ortho = gram_schmidt(Basis)  # Recompute U after modification
        mu_k = get_mu(Basis, Ortho, k, k-1) 
        if check_condition(Ortho, delta, mu_k, k):
            k += 1
        else:
            #swap
            element = Basis[[k, k-1]]
            Basis[[k, k-1]] = Basis[[k-1, k]]
            Basis[[k -1, k]] = element

            # Update affected variables
            Ortho = gram_schmidt(Basis)

            # 𝑘 = max(2, 𝑘 − 1
            k = max(k-1, 1)

    # Convert the basis back to integers, if possible
    Basis = np.rint(Basis).astype(int)
    return Basis
