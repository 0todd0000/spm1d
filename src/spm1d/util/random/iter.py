



# def anova1(JJ, ss, Q=None, fwhm=None, niter=10):
# 	from . rng import anova1 as rnggen
# 	rng,(A,) = rnggen(JJ, ss)
# 	for i in range(niter):
# 		y    = rng()
# 		yield y,A


		
def anova1(JJ, ss, Q=None, fwhm=None, niter=10):
	from . iterc import anova1 as c_iter
	for y,(A,) in c_iter(J, ss, Q, fwhm, niter):
		yield y,A

def regress(J, s, Q=None, fwhm=None, niter=10):
	from . iterc import regress as c_iter
	for y,(x,) in c_iter(J, s, Q, fwhm, niter):
		yield y,x

def ttest(J, s, Q=None, fwhm=None, niter=10):
	from . iterc import ttest as c_iter
	for y,(mu,) in c_iter(J, s, Q, fwhm, niter):
		yield y,mu

def ttest_paired(J, ss, Q=None, fwhm=None, niter=10):
	return ttest2((J,J), ss, Q, fwhm, niter)

def ttest2(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import ttest2 as rnggen
	rng,(A,)  = rnggen(JJ, ss)
	i0,i1     = A==0, A==1
	for i in range(niter):
		y     = rng()
		yield y[i0], y[i1]
