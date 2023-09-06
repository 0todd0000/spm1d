



def anova1(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import anova1 as rnggen
	rng,(A,) = rnggen(JJ, ss)
	for i in range(niter):
		y    = rng()
		yield y,A


def regress(J, Q=None, fwhm=None, niter=10):
	from . iterc import regress as c_iter
	for y,(x,) in c_iter(J, Q, fwhm, niter):
		yield y,x


def ttest2(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import ttest2 as rnggen
	rng,(A,)  = rnggen(JJ, ss)
	i0,i1     = A==0, A==1
	for i in range(niter):
		y     = rng()
		yield y[i0], y[i1]

