from itertools import permutations


def Tree(p):
    # T[k] = [parent, left, right]
    T,E = {}, [None]*(len(p)-1)
    T[p[0]] = [None]*3

    for i,k in enumerate(p[1:]):
        ant = p[0]
        while True:
            if   k>ant and T[ant][2]:     ant = T[ant][2]
            elif k<ant and T[ant][1]:     ant = T[ant][1]
            else:
                T[ant][1+(k>ant)] = k
                T[k] = [ant,None,None]
                E[i] = (k,ant) if k<ant else (ant,k)
                break

    return p[0], T, tuple(sorted(E))


def Prufer(r,T):
    n, ant  = len(T)-2, r
    P       = [None]*n

    for i in xrange(n):
        if ant==r and not T[r][1]:              # If root is a leaf
            r = ant = P[i] = T[r][2]
            continue
        while True:
            if T[ant][1]:   ant = T[ant][1]     # Go left
            elif T[ant][2]: ant = T[ant][2]     # Go right
            else:           break
        p = T[ant][0]                           # ant = smallest leaf
        T[p][1+(ant>p)] = None
        ant = P[i] = p

    return P


for n in xrange(2,10):
    P = {}
    for p in permutations(range(1,n+1)):
        r,T,E = Tree(p)
        if E not in P:
            P[E] = (Prufer(r,T))
    print n, len(P)
