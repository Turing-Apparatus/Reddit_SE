import itertools as it


def primes(n):
    if n<7: return [p for p in [2,3,5] if p<=n]
    n, offset = n-n%6+6, 2-(n%6>1)
    P = [True] * (n/3)
    for i in xrange(1,int(n**0.5)/3+1):
      if P[i]:
        k=3*i+1|1
        P[      k*k/3      ::2*k] = [False] * ((n/6-k*k/6-1)/k+1)
        P[k*(k-2*(i&1)+4)/3::2*k] = [False] * ((n/6-k*(k-2*(i&1)+4)/6-1)/k+1)
    return [2,3] + [3*i+1|1 for i in xrange(1,n/3-offset) if P[i]]




def primesI(n,m):
    L = primes(int(m**.5)+1)
    P = [True] * (m-n+1)
    for p in L:
        if p*p>=n:
            P[p*p-n::p] = [False] * ((m-p*p)/p+1)
        else:
            k = (p-n%p)*(n%p>0)
            P[k::p] = [False] * ((m-n-k)/p + 1)
    return [i+n for i in xrange(2*(n<2),m-n+1) if P[i]]




def prime_generator(n):
    P = { 9: 3, 25: 5 }
    MASK = 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0,
    MODULOS = frozenset( (1, 7, 11, 13, 17, 19, 23, 29) )

    for p in [p for p in [2,3,5] if p<=n]: yield p
    if n<7: return

    for i in it.compress(
            it.islice(it.count(7), 0, n-6 if n else None, 2),
            it.cycle(MASK)):

        if i in P:
            p = P.pop(i)
            x = i + p
            while x in P or (x%30) not in MODULOS:
                x += p
            P[x] = p
        else:
            if i*i<n: P[i*i] = 2*i
            yield i



