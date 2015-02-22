from collections import defaultdict as ddict
from itertools import combinations, product
from operator import or_, and_
from math import factorial as F




##
## MEMOIZATION CLASS
##
class memo:
    def __init__(self, fn):
        self.fn, self.m = fn, {}
    def __call__(self, *k):
        kk = k[0] if len(k)==1 else k
        if kk not in self.m: self.m[kk] = self.fn(*k)
        return self.m[kk]




##
### DELETE ENTRIES FROM THE MEMOIZATION DICTIONARY D
### THAT HAVE NOT BEEN USED RECENTLY
##
def mem_clean():
    for s in Dh.keys():
        if not Dh[s]:   del D[s], Dh[s]
        else:           Dh[s] = False




##
## BINOMIAL COEFFICIENTS AND IE COUNT
##
def B(n,k):         return 0 if n<k or k<0 else F(n)/F(n-k)/F(k)
def BB(h,b,t):      return B(b*(b+2*t), h)
@memo
def M(h,b,t):
    return sum( (-1)**k * sum( B(b,i) * B(t,k-i) * BB(h,b-i,t-k+i)
                            for i in xrange(k+1) )
                            for k in xrange(b+t+1) )




##
## CONSTRUCTS THE POSSIBLE SHAPES OF SIZE n
##
def shapes(n):

    def comp(s,m):
        if not possible(s,m): return                # prune nonshapes
        if m==0: S.append((1,)+s)                   # full DAG first layer = 1
        for i in xrange(1,m+1-(m>2)):               # full DAG second layer <= 2
            comp((i,)+s,m-i)

    def possible(s,m):
        h,b,t               = s[0], s[1], n-m-1-s[0]-s[1]   # head, body, tail
        if h>b*(b+2*t):     return False                    # too wide for below
        if m!=0:            return True
        p = [1+sum(s[:i])       for i in xrange(len(s)+1)]
        return reduce(and_, (s[i+1] <= 2*s[i]+p[i]          # too wide for above
                                for i in xrange(len(s)-1)))

    S = []
    comp((1,1),n-3)                                         # dag ends in (1,1)
    return S




##
## GIVEN A SHAPE,
## COUNTS THE NUMBER OF DAGS PER BOOLEAN ASSIGNMENT
##
def count(s):

    if s in D: return                               # memoize
    count(s[1:])

    D[s]     =  ddict(int)
    Dh[s]    =  True
    l,ll,lll =  s[0], s[1], sum(s[2:])
    n,m      =  l+ll+lll, ll+lll

    for cov,v in D[s[1:]].items():                  # for each cover of s[1:]
        if v==0:continue

        for a in xrange(1,min(2*l,ll)+1):
            for b in xrange(max(0,l>a**2),min(2*l-a,l,lll)+1):
                mult = M(l,a,b)
                if mult==0: continue
                t1 = combinations([m-x-1 for x in range(ll)], a)
                t2 = combinations([m-x-1 for x in range(ll,m)], b)
                for top in product(t1,t2):
                    x            = reduce(or_, (1<<q for q in top[0] ))
                    if b > 0: x |= reduce(or_, (1<<q for q in top[1] ))
                    D[s][x|cov] += mult*v

    if l==1:
        global T
        T[n] += D[s][(1<<m)-1]              # top layer 1 and all nodes covered





################################################################################
################################################################################

if __name__ == '__main__':

    n     =  15
    S     =  shapes(n)                       # shapes
    D     =  {(1,):{0:1}, (1,1):{1:1}}       # node coverings  (t/f assignments)
    Dh    =  {}                              # history of D    (memory clean)
    T     =  [0,1,1]+[0]*n                   # DAG counts      (solution)

    for i,shape in enumerate(S):
        if i>500 and i%500==0: mem_clean()
        count(shape)
        print i, len(S), sum(T), len(D), shape

    for i in xrange(1,n+1):
        print i, T[i]


                    #   D is a dictionary with keys {subshapes s of S}
                    #       D[s] is another dictionary with keys {cover(s)}
                    #       D[s][cover(s)] is the number of DAGS with cover(s)
                    #
                    #           eg.
                    #               s               = (1, 3, 1, 1)
                    #               cover(s)        = 011011        = 27
                    #               D[1,3,1,1][27]  = 2




