
'''
Random data returned in format required for spm1d.stats.c functions 
'''



def anova1(JJ, ss, Q=None, fwhm=None):
	from . rng import anova1 as rnggen
	rng,args = rnggen(JJ, ss, Q, fwhm)
	y        = rng()
	return y,args
	
	
def ttest2(JJ, ss, Q=None, fwhm=None):
	return anova1(JJ, ss, Q=None, fwhm=None)

