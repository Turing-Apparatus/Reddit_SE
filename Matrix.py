from collections import Iterable as It




# GENERATE ELEMENTS IN A MULTILEVEL ITERABLE
def flatten(iter):
	for elem in iter:
		if isinstance(elem, It) and not isinstance(elem, basestring):
			for sub in flatten(elem): yield sub
		else: yield elem




# MINIMUM/MAXIMUM ELEMENT OF MATRIX A
def mmin(A): return min ( min(A[i]) for i in xrange(len(A)) )
def mmax(A): return max ( max(A[i]) for i in xrange(len(A)) )




# INITIALIZE BY A FUNCTION ON i,j
def init(f,n,m):
	return [[f(i,j) for j in xrange(m)] for i in xrange(n)]




# CONSTANT TIMES IDENTITY WITH DIMENSION k (cI)
def eye(c, k):
	M = [r[:] for r in [[0]*k]*k]
	for i in xrange(k): M[i][i] = c
	return M




# RESHAPE A MATRIX
def reshape(M,n,m):
	if not isinstance(M[0],It) or isinstance(M[0],basestring):
		if len(M) != n*m: 	raise ValueError('resize - Dimension Mismatch')
		else:				return [M[i*m:(i+1)*m] for i in xrange(n)]
	else:
		return reshape(list(flatten(M)),n,m)




# STANDARD MATRIX MULTIPLICATION XY
def mult(X, Y, mod):
	M = [r[:] for r in [[0]*len(Y[0])]*len(X)]
	for r in xrange(len(X)):
		for c in xrange(len(Y[0])):
			M[r][c] = sum(X[r][k] * Y[k][c] for k in xrange(len(Y))) % mod
	return M




# MATRIX TO A POWER MODULUS
def pow(M, e, mod):
	res = eye(1,len(M))
	if e & 1: res = mmult(res, M, mod)
	while e > 0:
		e >>= 1
		M = mmult(M, M, mod)
		if e & 1: res = mmult(res, M, mod)
	return res




# CHOI DETERMINANT (SLOW BUT GOOD FOR INTEGERS)
def determinant(A):
	n = len(A)
	if n==1: return A[0][0]
	x = 0
	if A[0][0] == 0:
		x = max( (abs(A[i][0]),i) for i in xrange(n) )[1]
		A[0] = [A[0][j]+A[x][j] for j in xrange(n)]
	if A[0][0] == 0: return 0
	B = [[ A[0][0]*A[i+1][j+1]-A[0][j+1]*A[i+1][0]
				for j in xrange(n-1)]
				for i in xrange(n-1)]
	return determinant(B) / A[0][0]**(n-2)




# CONVERT TO STRING DELIMITED BY d
def tostring(M, d):
	w = 0
	s = ''
	for r in xrange(len(M)):
		for c in xrange(len(M[r])):
			w = max(w,len(str(M[r][c])))
	for r in xrange(len(M)):
		for c in xrange(len(M[r])):
			s += str(M[r][c]).rjust(w) + d
		s += '\n'
	return s








