from itertools import combinations, product
from operator import add



def glue(l,r):
    s = l | r
    if len(s) < N:
        next_tree(s)
        next_tree(s)    # comment to ignore "plane"



def next_tree(s):
    global T, count
    T[len(s)+1].append( s | set([count]) )
    count += 1



def get_trees():
    next_tree(set())
    for n in xrange(2,N+1):
        for l,r in product(T[n-1], reduce(add,T[1:n-1],[]) ):   glue(l,r)
        for l,r in combinations(T[n-1],2):                      glue(l,r)
        for t in T[n-1]:                                        next_tree(t)
        print n, len(T[n])



N = 7
T = [[] for i in xrange(N+1)]
count = 1
get_trees()


