###############################################################
###     DETERMINE NUMBER OF SOLUTIONS TO:                   ###
###         sum( Ci * Xi ) = n      Xi unknown              ###
###         sum( Xi ) = m                                   ###
###         Li <= Xi <= Ui                                  ###
###############################################################

def count_solutions(C, L, U, n, m):

    for i in xrange(len(C)):
        U[i] -= L[i]
        n -= C[i]*L[i]
        m -= L[i]

    if n < 0 or m < 0: return 0

    U = [ min((m, U[i], n/C[i])) for i in xrange(len(U))]
    cache = [[0]*(n+1) for i in xrange(m+1)]
    cache[0][0] = 1

    for i in xrange(len(C)):
        temp = [list(ch) for ch in cache]
        for x in xrange(1, U[i]+1):
            for mm in xrange(x, m+1):
                for nn in xrange(C[i]*x, n+1):
                    cache[mm][nn] += temp[mm-x][nn-C[i]*x]
    return cache[m][n]


k = 20                              # number of unknowns
n = 100                             # sum C.X
m = 20                              # sum X
C = range(1,k+1)                    # constants
L = [0]*k                           # lower bounds
U = [6]*k                           # upper bounds


print 'Number of solutions:', count_solutions(C, L, U, n, m), '\n'
