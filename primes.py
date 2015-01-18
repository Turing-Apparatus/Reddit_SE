################################################################################
###  OPT
################################################################################


def isprime(P,n):                     # DETERMINE IF n IS PRIME
    root = n**.5                      # ASSUMES P CONTAINS ALL PRIMES <= sqrt(n)
    for p in P:
        if n % p == 0: return False
        elif p > root: return True
    return True


def primes(n):                        # RETURN LIST OF PRIMES <= n
    P = [2]
    for i in range(3,int(n)+1,2):
        if isprime(P,i): P.append(i)
    return P


def nextprimes(N,M,n):                # RETURN FIRST n PRIMES IN INTERVAL [N,M]
    L = []
    P = primes(M**.5)
    i = N + (N%2==0)
    while len(L)<n and i<=M:
        if isprime(P,i): L.append(i)
        i += 2
    return L



N,M,n = 10**9, 10**9+10**5, 1000
P = nextprimes(N,M,n)




################################################################################
###  SIEVE
################################################################################

def eratosthenes(N,M):
    L = {}
    for i in xrange(2,M):
        if i in L:
            p = L.pop(i)
            x = p+i
            while x in L: x += p
            L[x] = p
        else:
            if i*i<=M:  L[i*i] = i
            if i>=N:    yield i

# P2 = list(eratosthenes(N,M))[:n]



