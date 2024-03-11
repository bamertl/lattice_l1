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
            V[i] -= (np.dot(V[i], V[j]) / np.dot(V[j], V[j])) * V[j] # U[i] * U[j] / U[j] ^ 2
    return V

def check_condition(U, delta, mu_k, k):
    return vector_norm(U[k]) ** 2 >= (delta - mu_k ** 2) * vector_norm(U[k-1]) ** 2


def lll_reduction(B, delta=0.75):
    """Apply the LLL algorithm to the basis B with delta as the Lovász condition."""
    B = np.array(B, dtype=float)  # Use float for calculations
    U = gram_schmidt(B)
    n = len(B)
    k = 1
    while k < n:
        for j in range(k-1, -1, -1):
            mu = np.dot(B[k], U[j]) / np.dot(U[j], U[j])
            if abs(mu) > 0.5:
                B[k] = B[k] - round(mu) * B[j]
                U = gram_schmidt(B)  # Recompute U after modification
        mu_k = np.dot(B[k], U[k-1]) / np.dot(U[k-1], U[k-1])
        if check_condition(U, delta, mu_k, k):
            k += 1
        else:

            #swap
            element = B[[k, k-1]]
            B[[k, k-1]] = B[[k-1, k]]
            B[[k -1, k]] = element

            # Update affected variables
            U = gram_schmidt(B)

            # 𝑘 = max(2, 𝑘 − 1
            k = max(k-1, 1)

    # Convert the basis back to integers, if possible
    B = np.rint(B).astype(int)
    return B
