from itertools import combinations, product
from operator import add


def glue(l,r):
    global T
    s = l[1] | r[1]
    ns = len(s)
    if ns < N:
        t = 'x({},{})'.format(l[0],r[0])
        T[ns+1].append( (t,s|set([t])) )
        if l[0]!=r[0]:
            t = 'x({},{})'.format(r[0],l[0])
            T[ns+1].append( (t,s|set([t])) )




N = 7
T = [[] for i in xrange(2*N)]
T[1] = [('x',set('x'))]

for n in xrange(2,N+1):
    for l,r in product(T[n-1], reduce(add,T[1:n-1],[]) ):   glue(l,r)
    for l,r in combinations(T[n-1],2):                      glue(l,r)
    for t in T[n-1]:                                        glue(t,t)
    print n, len(T[n])



