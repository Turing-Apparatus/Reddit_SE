from collections import defaultdict as ddict
from itertools import combinations, product
from operator import or_, and_
from math import factorial as F
from time import time, sleep




##
## MEMOIZATION DECORATOR
##
class memo:
    def __init__(self, fn):
        self.fn, self.m = fn, {}
    def __call__(self, *k):
        kk = k[0] if len(k)==1 else k
        if kk not in self.m: self.m[kk] = self.fn(*k)
        return self.m[kk]




##
## MEMORY USAGE
## might not be portable
##
from resource import getrusage, RUSAGE_SELF
def mem_usage():
    global mem
    new = 1.0 * getrusage(RUSAGE_SELF).ru_maxrss / scale - mem
    mem += new
    return round(new,2), int(mem)




##
### DELETE ENTRIES FROM THE MEMOIZATION DICTIONARY D
### THAT HAVE NOT BEEN USED RECENTLY
##
def mem_clean():
    Dh[(1,)] = Dh[(1,1)] = True
    for s in Dh.keys():
        if not Dh[s]:
            del D[s], Dh[s]
            if s[0]==1 and sum(s)<n-1: Bl.add(s)
        else: Dh[s] = False




##
## BINOMIAL COEFFICIENTS AND IE COUNT
##
def B(n,k):         return 0 if n<k or k<0 else F(n)/F(n-k)/F(k)
def BB(h,b,t):      return B(b*(b+2*t), h)      # count plane trees
# def BB(h,b,t):    return B(B(b,2)+b*t,h)        # forget the "plane"
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
        return ( reduce(and_, (s[i+1] <= 2*s[i]+p[i]        # too wide for above
                                for i in xrange(len(s)-1))) and s[1]<5 )

    S = []
    comp((1,1),n-3)                                         # dag ends in (1,1)
    return S




##
## GIVEN A SHAPE,
## COUNTS THE NUMBER OF DAGS PER BOOLEAN ASSIGNMENT
##
def count(s):

    Dh[s] = True                                    # history
    if s in D: return                               # memoize
    count(s[1:])

    D[s]     =  ddict(int)
    l,ll,lll =  s[0], s[1], sum(s[2:])
    n,m      =  l+ll+lll, ll+lll

    for cov,v in D[s[1:]].items():                  # for each cover of s[1:]
        if v==0:continue
        for a in xrange(1,min(2*l,ll)+1):                       # a children
            for b in xrange(max(0,l>a**2),min(2*l-a,l,lll)+1):  # b children
                mult = M(l,a,b)
                if mult==0: continue
                t1 = combinations([m-x-1 for x in range(ll)], a)
                t2 = combinations([m-x-1 for x in range(ll,m)], b)
                for top in product(t1,t2):
                    x            = reduce(or_, (1<<q for q in top[0] ))
                    if b > 0: x |= reduce(or_, (1<<q for q in top[1] ))
                    D[s][x|cov] += mult*v

    if l==1 and s not in Bl:
        global T
        T[n] += D[s][(1<<m)-1]              # top layer 1 and all nodes covered
        return D[s][(1<<m)-1]
    return 0




################################################################################
################################################################################

if __name__ == '__main__':

    n     =  14
    S     =  shapes(n)                       # shapes
    D     =  {(1,):{0:1}, (1,1):{1:1}}       # node coverings  (t/f coverings)
    T     =  [0,1,1]+[0]*n                   # DAG counts      (solution)

    Dh    =  {}                              # history of D    (memory clean)
    Bl    =  set()                           # black list      (memory clean)
    mem   =  0                               # memory usage
    scale =  1024*1024                       # memory usage    (MB)
    toc   =  time()

    for i,shape in enumerate(S):
        if i>0 and i%20==0: mem_clean()
        c = count(shape)
        print 'Shape {}/{}'.format(i, len(S)).ljust(20),
        print 'Time {:.2f}, {:.3f}'.format((time()-toc)/(i+1),(time()-toc)/60).ljust(23),
        print 'Cache {}, {}'.format(len(D),len(Bl)).ljust(28),
        print 'Memory (MB) {}'.format(mem_usage()).ljust(30),
        print 'T({}) = {}'.format(''.join(str(l) for l in shape), c)

    print ''
    for i in xrange(1,n+1):
        print 'T[{}] = {}'.format(i,T[i])


                    #   D is a dictionary with keys {subshapes s of S}
                    #       D[s] is another dictionary with keys {cover(s)}
                    #       D[s][cover(s)] is the number of DAGS with cover(s)
                    #
                    #           eg.
                    #               s               = (1, 3, 1, 1)
                    #               cover(s)        = 011011        = 27
                    #               D[1,3,1,1][27]  = 2




