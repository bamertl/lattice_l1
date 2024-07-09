def lsphere(n, d, q): #points in a Lee sphere
	R.<z> = PolynomialRing(QQ, 'z')
	s = sum([1] + [2*z^i for i in range(1, floor(q / 2) + 1)])
	return list(s^n)[d]

def lball(n, t, q): #points in a Lee ball
	return sum([lsphere(n, r, q) for r in range(0, t + 1)])

def lgv(n, c, q): #return GV min. dist. given # of codewords
	(b, i) = (0, 0)
	while c*b < q^n:
		(b, i) = (b + lsphere(n, i, q), i + 1)
	return i

def lgvk(n, k, q): #return GV min. dist. for free code of dim. k
	return lgv(n, q^k, q)
