import math
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_0 = Integer(0)
def lsphere(n, d, q): #points in a Lee sphere
	R = PolynomialRing(QQ, 'z', names=('z',)); (z,) = R._first_ngens(1)
	s = sum([_sage_const_1 ] + [_sage_const_2 *z**i for i in range(_sage_const_1 , floor(q / _sage_const_2 ) + _sage_const_1 )])
	return list(s**n)[d]

def lball(n, t, q): #points in a Lee ball
	return sum([lsphere(n, r, q) for r in range(_sage_const_0 , t + _sage_const_1 )])


#only for t < q/2
def V_L(n, t):
    """Calculate the volume of a Lee sphere of radius t in n-dimensional space."""
    volume = 0
    for i in range(n + 1):
        # Using math.comb directly for binomial coefficients
        volume += (2 ** i) * math.comb(n, i) * math.comb(t, i)
    return volume

if __name__ == "__main__":
    q = 43
    n_values = range(11, 53)
    for n in n_values:
        for k in range(1, n):
            volume = V_L(n, 5)
            volume2 = lball(n, 5, q)
            if volume == volume2:
                print("Ok", flush=True)
            else:
                print("Error", flush=True)