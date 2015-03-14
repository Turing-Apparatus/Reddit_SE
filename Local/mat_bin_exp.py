# CONSTANT TIMES IDENTITY WITH DIMENSION k (cI)
def eye(c, k):
    M = [r[:] for r in [[0]*k]*k]
    for i in xrange(k): M[i][i] = c
    return M


# STANDARD MATRIX MULTIPLICATION XY
# mod < 0 IGNORED
def mmult(X, Y, mod):
    M = [r[:] for r in [[0]*len(Y[0])]*len(X)]
    for r in xrange(len(X)):
        for c in xrange(len(Y[0])):
            M[r][c] = sum(X[r][k] * Y[k][c] for k in xrange(len(Y)))
            if mod > 0:  M[r][c] %= mod
    return M


# MATRIX TO A POWER MODULUS
def mpow(M, e, mod):
    res = eye(1,len(M))
    if e & 1: res = mmult(res, M, mod)
    while e > 0:
        e >>= 1
        M = mmult(M, M, mod)
        if e & 1: res = mmult(res, M, mod)
    return res


if __name__=="__main__":

    M = [   [0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,1,1,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0],
            [0,1,1,1,0,0,1,0,1,0,0,0,1],
            [1,2,2,0,0,1,0,1,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1],
           [-1,0,0,0,0,0,0,0,0,0,1,0,0]  ]

    f =     [1,1,1,2,6,0,0,1,2,4,4,0,2]

    n = 10**100
    mod = 10**20

    Mn = mpow(M,n-1,mod)
    print sum(Mn[0][i]*f[i] for i in xrange(len(f))) % mod





