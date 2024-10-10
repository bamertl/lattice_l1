import math
from sympy import primerange

def estimate_minimum_distance(n, k, q):
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
    n_values = range(11, 202)
    
    # Generate primes up to 1000
    primes = [5, 17, 211, 521]
    
    # Open file to save results
    with open("./data/minimum_distance_estimations.csv", "w") as file:
        file.write("n,k,q,estimated_d\n")
        
        # Iterate over all n, k, and prime q combinations
        for n in n_values:
            for k in range(1, n):
                for q in primes:
                    estimated_d = estimate_minimum_distance(n, k, q)
                    file.write(f"{n},{k},{q},{estimated_d}\n")
                    print(f"n={n}, k={k}, q={q} -> estimated d={estimated_d}")

if __name__ == "__main__":
    run_estimations()