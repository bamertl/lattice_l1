import math
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_0 = Integer(0)
def lsphere(n, d, q): #points in a Lee sphere
	R = PolynomialRing(QQ, 'z', names=('z',)); (z,) = R._first_ngens(1)
	s = sum([_sage_const_1 ] + [_sage_const_2 *z**i for i in range(_sage_const_1 , floor(q / _sage_const_2 ) + _sage_const_1 )])
	return list(s**n)[d]

def V_L(n, t, q): #points in a Lee ball
	return sum([lsphere(n, r, q) for r in range(_sage_const_0 , t + _sage_const_1 )])

def estimate_minimum_distance_lee(n, k, p):
    """Find the maximum d such that the inequality holds."""
    max_term = (p**(n - k + 1) - 1) / (p - 1)
    d = 1

    while True:
        volume = V_L(n, d - 1, p)
        inequality_term = (volume - 1) / 2
        if max_term <= inequality_term:
            break
        d += 1
    return d - 1

def estimate_minimum_distance_hamming(n, k, q):
    log_M = k * math.log(q)
    # Estimate for d using an approximation
    low, high = 1, n
    while low < high:
        mid = (low + high + 1) // 2
        sum_terms = sum(math.comb(n, i) * (q - 1)**i for i in range(mid))
        if math.log(sum_terms) - n * math.log(q) > -log_M:
            high = mid - 1
        else:
            low = mid
    return low


def run_estimations():
    # n between 11 and 101
    n_values = range(11, 50)
    
    # Generate primes up to 1000
    primes = [5, 17, 101]
    
    # Open file to save results
    with open("./data/distance/minimum_distance_estimations_lee.csv", "w") as file_lee, \
        open("./data/distance/minimum_distance_estimations_hamming.csv", "w") as file_hamming:
        file_lee.write("n,k,q,estimated_d\n")
        file_hamming.write("n,k,q,estimated_d\n")
        
        # Iterate over all n, k, and prime q combinations
        for n in n_values:
            k = n // 2
            for q in primes:
                estimated_d_lee = estimate_minimum_distance_lee(n, k, q)
                estimated_d_hamming = estimate_minimum_distance_hamming(n, k, q)
                file_lee.write(f"{n},{k},{q},{estimated_d_lee}\n")
                file_hamming.write(f"{n},{k},{q},{estimated_d_hamming}\n")
                print(f"n={n}, k={k}, q={q} -> estimated d Lee={estimated_d_lee}, estimated d Hamming={estimated_d_hamming}",flush=True)

if __name__ == "__main__":
    run_estimations()