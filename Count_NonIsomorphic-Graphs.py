from  collections import  defaultdict as ddict
from  itertools   import  combinations
from  fractions   import  gcd
from  math        import  factorial as F


def partitions(n):
    p,k = [0]*(n+1), 1
    p[1] = n
    while k != 0:
        x,y,k = p[k-1]+1, p[k]-1, k-1
        while x <= y: p[k],y,k = x, y-x, k+1
        p[k] = x+y
        yield p[:k+1]


def typed(p):
    t = ddict(int)
    for i in p: t[i] += 1
    return t


def multiplicity(n,t):
    m = F(n)
    for k,v in t.items():
        m /= F(v) * k**v
    return m


def monomial(t):
    c = 0
    for x in t: c += t[x]*(x/2) + t[x]*(t[x]-1)*x/2
    for x,y in combinations(t,2):
        c += t[x]*t[y] * gcd(x,y)
    return c


def graphs(n):                              # Polya count the number of non-isomorphic graphs
    index = 0
    for p in partitions(n):                 # generate partitions of n
        t = typed(p)                        # convert partition to type
        m = multiplicity(n,t)               # count number of permutations with type t
        c = monomial(t)                     # calculate number of cycles on pairs (type_2)
        index += m<<c
    return index/F(n)



n = 30
for i in xrange(1,n+1): print i, graphs(i)


