
def V_L(n, t, p):
    """Calculate the volume of a Lee sphere of radius t in n-dimensional space over an alphabet of size p using dynamic programming."""
    # Initialize a DP table where dp[i][j] is the volume of a Lee sphere in i dimensions with radius j
    dp = [[0] * (t + 1) for _ in range(n + 1)]
    
    # Base case: In 0 dimensions, the volume is 1 for radius 0 (only the origin)
    for j in range(t + 1):
        dp[0][j] = 1

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(t + 1):
            # Start with the volume of the previous dimension at the same radius
            dp[i][j] = dp[i - 1][j]
            # Add contributions for each possible step size k within the limit
            for k in range(1, min(j, (p - 1) // 2) + 1):
                dp[i][j] += 2 * dp[i - 1][j - k]  # Both positive and negative shifts within bounds

    return dp[n][t]

def find_max_t(n, k, p):
    """Find the maximum d such that the inequality holds."""
    max_term = (p**(n - k + 1) - 1) / (p - 1)
    d = 1

    while True:
        volume = V_L(n, d - 1, p)
        inequality_term = (volume - 1) / 2
        if max_term <= inequality_term:
            break
        d += 1

    return (d - 1) // 2


def run_estimations():
    # n between 11 and 101
    n_values = range(11, 202)
    
    # Generate primes up to 1000
    primes = [5, 17, 211, 521]
    
    # Open file to save results
    with open("./data/minimum_distance_estimations_lee.csv", "w") as file:
        file.write("n,k,q,estimated_d\n")
        
        # Iterate over all n, k, and prime q combinations
        for n in n_values:
            for k in range(1, n):
                for q in primes:
                    estimated_t = find_max_t(n, k, q)
                    file.write(f"{n},{k},{q},{estimated_t}\n")
                    print(f"n={n}, k={k}, q={q} -> estimated t={estimated_t}", flush=True)

if __name__ == "__main__":
    run_estimations()