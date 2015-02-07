###################################################################################
###                        GENERALIZED COMPOSITIONS                             ###
###                                                                             ###
###                DETERMINE NUMBER OF INTEGER SOLUTIONS X TO:                  ###
###                        sum( C[i] * X[i] )  =  n                             ###
###                        sum( X[i]        )  =  m                             ###
###                          L[i] <= X[i] <= U[i]                               ###
###                                                                             ###
###################################################################################
###                                                                             ###
###  BOUNDS                                                                     ###
###      TIGHT WORST CASE                                                       ###
###      LOOSE AVERAGE CASE          :  O( n m^2 k )     time                   ###
###                                  :  O( n m )         space                  ###
###                                                                             ###
###  CHANGE OF VARIABLES             :  O( k )           runtime                ###
###      OPTIMIZE IV's                  L -> 0,          lower bounds set to 0  ###
###                                     U -> lub         upper bounds minimized ###
###                                     X -> U-Y         reflection             ###
###                                     C -> abs(C)      positive coefficients  ###
###                                     C -> C/gcd(C)    coefficients reduced   ###
###                                                                             ###
###                                                                             ###
###  INPUT                     :  m,n,k,C,L,U integers                          ###
###  OUTPUT                    :  reduced input (m,n,k,C,L,U)'                  ###
###                               S number of solutions for each i,j <= n',m'   ###
###                                                                             ###
###################################################################################


from math import factorial as F
from fractions import gcd

def GCD(x):     return reduce(gcd, x[1:], x[0])                             # GCD OF A LIST
def B(n,k):     return 0 if n<k or k<0 else F(n)/F(n-k)/F(k)                # BINOMIAL COEFFICIENTS
def IE(n,k,u):  return sum( (-1)**i * B(k,i) * B(n+k-1-(u+1)*i,k-1)         # INCLUSION EXCLUSION
                    for i in xrange( min( k, int(n/(u+1)) ) + 1 ))



def change_of_variables(m, n, k, C, L, U):
    L    =  [ -U[i] if C[i]<0 else L[i]             for i in xrange(k) ]
    U    =  [ -L[i] if C[i]<0 else U[i]             for i in xrange(k) ]
    C    =  [ -C[i] if C[i]<0 else C[i]             for i in xrange(k) ]    # SET C > 0
    gC   =  GCD(C)
    C    =  [ C[i]/gC                               for i in xrange(k) ]    # REDUCE C
    n   /=  gC
    m   -=  sum( L )                                                        # SET L=0
    n   -=  sum( C[i] * L[i]                        for i in xrange(k) )
    U    =  [ min( m, U[i]-L[i] )                   for i in xrange(k) ]
    U    =  [ min( U[i], n/C[i] ) if C[i] else U[i] for i in xrange(k) ]    # MINIMIZE U
    L    =  [ 0 ] * k
    nmax =  sum( C[i] * U[i]                        for i in xrange(k) )
    mmax =  sum( U )

    if nmax>n and mmax>m and (nmax-n)*(mmax-m)<n*m:                         # REFLECTION
        n,m  =  nmax-n, mmax-m
    nmax, mmax = min(n,nmax), min(m,mmax)

    return m,n,k,C,L,U




def count_solutions(m, n, k, C, L, U):

    m,n,k,C,L,U = change_of_variables( m,n,k,C,L,U )
    nmax = min( n, sum( C[i] * U[i] for i in xrange(k) ) )
    mmax = min( m, sum(U) )

    if  n<0  or  m<0  or  min(U)<0:
        return [[0]], (m,n,k,C,L,U)

    S = [ [0]*(n+1) for i in xrange(m+1) ]
    S[0][0] = 1

    for i in xrange(k):
        SS = [ list(s) for s in S ]                             # can probably reorder DP
        for x in xrange(1, U[i]+1):
            for m_ in xrange(x, mmax+1):                        # I wish you could use n', m'
                for n_ in xrange(C[i]*x, nmax+1):               # could splice for speedup
                    S[m_][n_] += SS[m_-x][n_-C[i]*x]

    return S, (m,n,k,C,L,U)




if __name__ == "__main__":
    m = 50                              # sum X
    n = 100                             # sum C.X
    k = 20                              # number of unknowns
    C = range(1,k+1)                    # coefficients
    L = [0]*k                           # lower bounds
    U = [n]*k                           # upper bounds

    S,(n,m,k,C,L,U) = count_solutions( m,n,k,C,L,U )
    print 'Number of Solutions:', S[-1][-1]

    if n==m and min(C)==1==max(C) and min(U)==max(U):
        print 'Inclusion Exclusion IE({},{},{})='.format(n,k,U[0]),
        print IE(n,k,U[0])
