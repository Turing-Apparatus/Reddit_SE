from Hungarian import hungarian, mmax
from random import randint as randint
from itertools import permutations
inf = float('inf')


## FIND SUBTOURS / CHAINS
def cycles(tour):

    T,C,S = dict(tour), [], {}

    while T != {}:

        k,v = T.popitem()
        c = [k]

        while v in T:
            c.append(v)
            v = T.pop(v)

        if v in S:
            C[S[v]] = c + C[S[v]]
            S[c[0]] = S[v]
        else:
            if v != c[0]: c.append(v)
            S[c[0]] = len(C)
            C.append(c)

    return sorted(C, key=lambda x: len(x))




## BRANCH AND BOUND (EASTMAN'S ALGORITHM I THINK?)
def TSP(G):

    n = len(G)
    ground = set(range(n))
    up_tour = None                                                 # TODO: start with approximation
    up_bound = inf                                                 # UPPER BOUND
    Q = [(0,{},set())]                                             # TODO: priority queue

    while len(Q)>0:

        ind  = min( (Q[i][0],i) for i in xrange(len(Q)))[1]
        (lb, include, omit) = Q[ind]
        del Q[ind]

        # print lb, up_bound, len(Q)                                    # IF TAKING FOREVER
        if lb >= up_bound:                                              # LOWER BOUND >= UPPER BOUND
            return up_tour, up_bound

        rmap =  sorted(ground - set(include.keys()))
        cmap =  sorted(ground - set(include.values()))
        cyc  =  cycles(include)
        o2   =  omit | set([(c[-1],c[0]) for c in cyc])                 # NEW EDGE NOT IN CYCLE

        G_   =  [ [inf if (i,j) in o2 else G[i][j] for j in cmap ] for i in rmap ]
        hung =  [ (rmap[r],cmap[c]) for r,c in hungarian(G_) ]
        tour =  { i:j for i,j in include.items() + hung }
        cost =  sum( G[i][j] for i,j in tour.items() )                  # TODO: hungarian recurse
        cyc  =  cycles(tour)

        if len(cyc) == 1 and cost <= up_bound:                          # BOUND
            up_tour, up_bound = cyc[0], cost

        elif len(cyc)>1 and cost < up_bound:                            # BRANCH
            c_ = cyc[0]
            for i,u in enumerate(c_):
                e = (u,c_[(i+1)%len(c_)])
                if e not in include.items() and e not in omit:
                    Q.append((cost, {i:j for i,j in include.items() + [e]}, omit))
                    Q.append((cost, include, omit | set([e])))
                    break

    return up_tour, up_bound



## BRUTE FORCE: DON'T USE IF n>10
def TSP_brute(G):
    bcost = inf
    btour = None
    n = len(G)
    for p in permutations(range(n)):
        cost = sum( G[p[i]][p[(i+1)%n]] for i in xrange(n))
        if cost < bcost:
            bcost, btour = cost, p
    return list(btour), bcost




if __name__ == "__main__":
    n = 50
    G = [[ randint(1,100) if i!=j else inf      for i in xrange(n)] # WEIGHTED ADJACENCY MATRIX
                                                for j in xrange(n)]     # int OR Fraction
                                                                    # USE inf FOR MISSING EDGES
                                                                    # NO SELF-LOOPS (DIAGONAL = inf)

    tour = TSP(G)
    # btour = TSP_brute(G)
    print '\n\nTour: {}\nCost: {}\n'.format(tour[0],tour[1])



