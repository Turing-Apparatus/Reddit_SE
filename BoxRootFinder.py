from math import factorial as fact

poly = lambda f,x: sum(f[i]*x**i for i in xrange(len(f)))
ddx = lambda f: [i*f[i] for i in xrange(1,len(f))]

def bisect(a,b,prec):
	fa,fb =  poly(f,a), poly(f,b)
	while b-a > prec:
		m,fm = (a+b)/2, poly(f,(a+b)/2)
		if fa*fm<0: b,fb = m,fm
		else: a,fa = m,fm
	if abs(m-round(m))<prec: return int(round(m))
	return m

def box_roots(f,prec):
	M = max(1+abs(c/f[-1]) for c in f)
	F = [f]
	for i in xrange(len(f)-1): F.append(ddx(F[-1]))
	I = set([(-M,M)])
	O = set()

	while len(I) > 0:
		(a,b) = I.pop()
		m,r = (a+b)/2, (b-a)/2
		fm, fpm = poly(f,m), poly(F[1],m)
		boxf = sum( abs(poly(F[k],m)) * r**k / fact(k) for k in xrange(1,len(F)))
		boxpf = sum( abs(poly(F[k+1],m)) * r**k / fact(k) for k in xrange(1,len(F)-1))

		if (fm-boxf)*(fm+boxf) > 0:
			pass
		elif (fpm-boxpf)*(fpm+boxpf) > 0 and poly(f,a)*poly(f,b) < 0:
			O.add(bisect(a,b,prec))
		elif fm == 0.0:
			if fpm == 0.0: exit('Error: polynomial not sqaurefree\n')
			O.add(m)
			I.add((a,m))
			I.add((m,b))
		else:
			I.add((a,m))
			I.add((m,b))

	return O


def pretty_print(f,prec,roots):
	n = len(f)
	sf = [int(round(c)) if c == round(c) else c for c in f]
	for i,c in enumerate(sf):
		if c==-1 and i>0: 	sf[i] = ' - x^{}'.format(i)
		elif c==1 and i>0: 	sf[i] = ' + x^{}'.format(i)
		elif c<0: 			sf[i] = ' - {}x^{}'.format(-c,i)
		elif c>0: 			sf[i] = ' + {}x^{}'.format(c,i)
		else:				sf[i] = ''
	if sf[0]!='': sf[0] = sf[0][:-3]
	if sf[1]!='': sf[1] = sf[1][:-2]
	if sf[-1]!='': sf[-1] = sf[-1][3:]
	print 'f(x) =', ''.join(sf[::-1])
	print 'error:', prec, '\n'
	for r in roots: print 'f({}) = {}'.format(r,poly(f,r))
	print ''


# BOX METHOD FOR ISOLATING REAL ROOTS OF A SQUARE FREE POLYNOMIAL
#
# INPUT
#	POLYNOMIAL: AS LIST OF COEFFICIENTS, ith INDEX FOR COEFFICIENT OF x^i
# 	PRECISION prec: EACH FOUND ROOT IS WITHIN prec OF AN ACTUAL ROOT
#		NOTE: UNEXPECTED RESULTS IF TWO ACTUAL ROOTS ARE WITHIN prec of EACHOTHER

f = [-150.,145.,17.,-13.,1.] 	# (x-1)(x-5)(x+3)(x-10)
prec = 10**(-10)
roots = box_roots(f,prec)
pretty_print(f,prec,roots)



