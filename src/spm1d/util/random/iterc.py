



def anova1(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import anova1 as rnggen
	rng,(A,) = rnggen(JJ, ss, Q, fwhm)
	for i in range(niter):
		y    = rng()
		yield y,(A,)


def regress(J, s, Q=None, fwhm=None, niter=10):
	from . rng import regress as rnggen
	rng,(x,)  = rnggen(J, s, Q, fwhm)
	for i in range(niter):
		y     = rng()
		yield y,(x,)

def ttest(J, s, Q=None, fwhm=None, niter=10):
	from . rng import ttest as rnggen
	rng,_ = rnggen(J, s, Q, fwhm)
	for i in range(niter):
		y     = rng()
		yield y,(0,)

def ttest_paired(J, ss, Q=None, fwhm=None, niter=10):
	from . rng import ttest_paired as rnggen
	rng,(A,)  = rnggen(J, ss, Q, fwhm)
	for i in range(niter):
		y     = rng()
		yield y,(A,)

def ttest2(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import ttest2 as rnggen
	rng,(A,)  = rnggen(JJ, ss, Q, fwhm)
	for i in range(niter):
		y     = rng()
		yield y,(A,)
		
		
