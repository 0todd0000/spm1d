
'''
Random data returned in format required for spm1d.stats functions 
'''


def anova1(JJ, ss, Q=None, fwhm=None):
	from . rng import anova1 as rnggen
	rng,(A,) = rnggen(JJ, ss, Q, fwhm)
	y        = rng()
	return y,A

def ttest2(JJ, ss, Q=None, fwhm=None):
	from . rng import ttest2 as rnggen
	rng,(A,) = rnggen(JJ, ss, Q, fwhm)
	y        = rng()
	y0,y1    = y[A==0], y[A==1]
	return y0,y1