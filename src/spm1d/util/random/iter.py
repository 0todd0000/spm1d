



def anova1(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import anova1 as rnggen
	rng,(A,) = rnggen(JJ, ss)
	for i in range(niter):
		y    = rng()
		yield y,A


def ttest2(JJ, ss, Q=None, fwhm=None, niter=10):
	from . rng import ttest2 as rnggen
	rng,(A,)  = rnggen(JJ, ss)
	for i in range(niter):
		y     = rng()
		y0,y1 = y[A==0], y[A==1]
		yield y0,y1
		
		
