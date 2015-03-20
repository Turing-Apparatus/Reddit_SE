from math import factorial as F


class memo:
    def __init__(self, fn):
        self.fn, self.m = fn, {}
    def __call__(self, *k):
        kk = k[0] if len(k)==1 else k
        if kk not in self.m: self.m[kk] = self.fn(*k)
        return self.m[kk]


@memo
def B(n,k):
    return 0 if n<k or k<0 else F(n)/F(n-k)/F(k)



@memo
def T(n,m,c):
    return Tp(n,m,c,None)



def Tp(n,m,c,l):
    if l>m-c+1: return Tp_(n,m,c,None)
    else:       return Tp_(n,m,c,l)



@memo
def Tp_(n,m,c,l):
    if l==None:     l = m-c+2
    if n==m==c==0:  return 1
    if n<c*r or n>m*r or m>c*l: return 0
    return (sum( B(n,k)  *  Tx(k,p,q)  *  Tp(n-k, m-p*q, c-p, q)
                        for q in xrange( m/c , min(l-1,m-c+1) +1)
                        for p in xrange( 1   , min(c,m/q)     +1)
                        for k in xrange( p*r , n              +1) ))


@memo
def Tx(n,c,l):
    if c==1:    return T1(n,l)
    if n==c==0: return 1
    if n<c*r or n>c*l*r: return 0
    return (sum( B(n-1,k-1) * T1(k,l) * Tx(n-k, c-1, l)
                            for k in xrange(r , n-(c-1)*r +1) ))



@memo
def T1(n,m):
    if n<r or n>m*r: return 0
    return ((   B(B(n,r),m)
             - sum( B(n,k) * Tp(k,m,c,None) for k in xrange(min(r,m) , n     )
                                            for c in xrange(1 , min(k/r,m) +1))
             - sum( Tp(n,m,c,None)          for c in xrange(2 , min(n/r,m) +1)) ))




def GF(n):
    for m in xrange(1,B(n,r)+1):
        gf = [T(n,m,c) for c in xrange(1,n/r+1)]
        while len(gf)>1 and gf[-1]==0: del gf[-1]
        if gf!=[0] and gf!=[]: print r,n,m, gf



def clear_memo():
    T.m.clear()
    Tp_.m.clear()
    Tx.m.clear()
    T1.m.clear()



if __name__ == "__main__":
    N = 10
    R = 2

    for r in xrange(R,R+1):
        clear_memo()
        for n in xrange(r,N+1):
            GF(n)























