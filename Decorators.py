class memo:
    def __init__(self, fn):
        self.fn, self.m = fn, {}
    def __call__(self, *k):
        kk = k[0] if len(k)==1 else k
        if kk not in self.m: self.m[kk] = self.fn(*k)
        return self.m[kk]


from time import time
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
        # print 'Time {}.{}.{}'.format(h,m,s)
        return fn, (h,m,s)