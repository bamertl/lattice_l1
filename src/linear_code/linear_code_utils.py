import math
from sage.all import *


"""Estimate the minimum distance d for large n using the Gilbert-Varshamov Bound."""
def estimate_minimum_distance(n,k,q):
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

# points in a lee sphere
def lsphere(n, d, q):
    z = PolynomialRing(QQ, 'z').gen()
    s = sum([1] + [2*z**i for i in range(1, floor(q / 2) + 1)])   #test    
    return list(s**n)[d]

def lball(n, t, q): #points in a Lee ball
	return sum([lsphere(n, r, q) for r in range(0, t + 1)])

def lgv(n, c, q): #return GV min. dist. given # of codewords
	(b, i) = (0, 0)
	while c**b < q**n:
		(b, i) = (b + lsphere(n, i, q), i + 1)
	return i

def lgvk(n, k, q): #return GV min. dist. for free code of dim. k
	return lgv(n, q**k, q)