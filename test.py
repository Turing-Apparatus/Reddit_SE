# def compositions(n):

#     def comp(c,r):
#         # if r==0: C.append(c + [1,1])
#         if r==0: C.append([1]+c+[1,1])
#         else:
#             for i in xrange(1,r+1-(r>3)):
#                 comp(c+[i],r-i)

#     if n<=3: return [[1]*n]
#     C = []
#     comp([1],n-4)
#     comp([2],n-5)
#     return C

# for c in compositions(8): print c, sum(c)

class timer:
    def __init__(self, fn):
        self.fn = fn
    def __call__(self, *k):
        tic = time()
        fn  = self.fn(*k)
        toc = time()-tic
        h   = int(toc)/3600
        m   = int(toc-3600*h)/60
        s   = round(toc-3600*h-60*m,2)
        print 'Time {}.{}.{}'.format(h,m,s)
        return fn

from math import log, pi, ceil, sqrt, factorial as F

def f(x): return x/sqrt(log(x))
def B(n,k): return 0 if n<k or k<0 else F(n)/F(n-k)/F(k)
def catalan(n): return B(2*n,n)/(n+1)

print '[0 , 1',
for n in xrange(3,30):
    xlo = 2
    xhi = n*n
    target = n/2. * sqrt(pi/log(4))
    while xhi - xlo > .00001:
        mid = (xlo+xhi)/2.0
        if f(mid)<target:   xlo = mid
        else:               xhi = mid


    x = int(xlo)
    if abs(target-f(x)) > abs(target-f(x+1)): x=x+1
    print x, f(x), xlo, f(xlo), target
    print n, catalan(x)
    # print ', {}'.format(catalan(x)),

# print '];'
