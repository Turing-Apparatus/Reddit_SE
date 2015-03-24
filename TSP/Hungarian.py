from itertools import product
from collections import defaultdict as ddict
from random import randint, random
inf = float('inf')


# MIN AND MAX OF A MATRIX
def mmin(A): return min ( min(A[i]) for i in xrange(len(A)) )
def mmax(A): return max ( max(A[i]) for i in xrange(len(A)) )


# RETURN ADJACENCY LIST GIVEN AN EDGE SET
def adjacency(E):
    Ea = ddict(set)
    for (i,j) in E: Ea[i].add(j)
    return Ea



# MAKE C SQUARE AND NONNEGATIVE
def standard(C):
    n,m = len(C), len(C[0])
    mn,mx = mmin(C), mmax(C)
    d,mx = max(n,m), mx+abs(mn)
    if mn == inf:
        print 'ERROR: NO PERFECT MATCHING'
        exit()
    return [[ C[i][j]-mn if (i<n and j<m) else mx   for j in xrange(d)]
                                                    for i in xrange(d)]



# SUBTRACT ROW MINIMUM FROM EACH ROW
def minimize_rows(W,Ea,n):
    for i in xrange(n):
        mr = min(W[i])
        if mr < inf:
            W[i] = [x-mr for x in W[i]]
            Ea[i] |= set([n+j for j in xrange(n) if W[i][j]==0])



# SUBTRACT COLUMN MINIMIUM FROM EACH COLUMN
def minimize_cols(W,Ea,n):
    for j in xrange(n):
        mc = min(W[i][j] for i in xrange(n))
        if mc < inf:
            for i in xrange(n): W[i][j] -= mc
    for i in xrange(n):
        Ea[i] |= set([n+j for j in xrange(n) if W[i][j]==0])



# FIND A MAXIMUM MATCHING OF E
def max_match(Ea,A,B,n):
    path,M,P = True, set(), set()
    while path:
        M ^= P                                          # (M-P) | (P-M)
        (path,P) = aug_path(Ea,M,A,B,n)
    return M,P



# FIND AN AUGMENTING PATH OR ELSE RETURN REACHABLE NODES L FROM EXPOSED A
# (A-L) U (B^L) IS AN OPTIMUM VERTEX COVER OF E
def aug_path(Ea,M,A,B,n):
    Ma = adjacency(M)
    rMa = adjacency( (j,i) for (i,j) in M )
    A_ = A - set(Ma)                                    # EXPOSED A
    B_ = B - set(rMa)                                   # EXPOSED B
    prev = [-1]*(2*n)
    it, L, nodes = 0, A_, A_

    while nodes:                                        # BFS
        next = set()
        for i in nodes:
            J = (Ea[i]-Ma[i]-L if it%2==0 else rMa[i]-L)
            for j in J: prev[j] = i
            next |= J
        L,nodes,it = L|next, next, it+1

        if nodes & B_:                                  # PATH FOUND
            i = (nodes & B_).pop()
            P = set([(prev[i],i)])
            while prev[i] != -1:
                i,j = prev[i],i
                P.add((min(i,j),max(i,j)))
            return True,P

    return False,L



# FIND MINIMUM WEIGHT PERFECT MATCHING OF C
def hungarian(C):
    W = standard(C)                             # DUAL MATRIX wij = cij - ui - vj (square, nonnegative)
    n = len(W)                                  # NUMBER OF WORKERS
    A = set(range(n))                           # WORKERS
    B = set(range(n,2*n))                       # TASKS
    Ea = {i:set() for i in A}                   # ADJACENCY LIST FOR E = {(i,j) : wij=0}
    H = set()

    minimize_rows(W,Ea,n)                        # ui = min cij over j
    minimize_cols(W,Ea,n)                        # vj = min cij-ui over i

    while len(H) < n:

        H,L = max_match(Ea,A,B,n)                                   # MAXIMUM MATCHING OF SUBGRAPH E
        if len(H) == n: return [(i,j%n) for (i,j) in H]
        d = min( W[i][j%n] for i,j in product(A&L,B-L) )            # MINIMUM UNCOVERED ELEMENT
        if d == inf:
            print 'ERROR: NO PERFECT MATCHING'
            exit()
        for i,j in product(A&L,A):
            W[i][j] -= d                                            # SUBTRACT d FROM UNTICKED ROWS
            if W[i][j]==0: Ea[i].add(n+j)
        for i,j in product(A,B&L):
            W[i][j%n] += d                                          # ADD d TO TICKED COLUMNS
            if W[i][j%n]!=0: Ea[i].discard(j)

    return [(i,j%n) for (i,j) in H]




if __name__ == "__main__":
    n = 100
    C = [[randint(1,1000) for i in xrange(n)] for j in xrange(n)]
    M = hungarian(C)
    print sum (C[i][j] for (i,j) in M)

