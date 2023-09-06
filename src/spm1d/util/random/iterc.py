



def anova1(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import anova1 as rnggen
	rng,(A,) = rnggen(JJ, ss, Q, fwhm)
	for i in range(niter):
		y    = rng()
		yield y,(A,)


def regress(J, Q=None, fwhm=None, niter=10):
	from . rng import regress as rnggen
	rng,(x,)  = rnggen(J, Q, fwhm)
	for i in range(niter):
		y     = rng()
		yield y,(x,)

def ttest2(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import ttest2 as rnggen
	rng,(A,)  = rnggen(JJ, ss, Q, fwhm)
	for i in range(niter):
		y     = rng()
		yield y,(A,)
		
		
