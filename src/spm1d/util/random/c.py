
'''
Random data returned in format required for spm1d.stats.c functions 
'''
import functools

class fgen(object):
	def __init__(self, f):
		self.f = f
		exec( f'from . rng import {self.fname}' )
		self.rnggen = eval( self.fname )
		functools.update_wrapper(self, f) 

	def __call__(self, *args, **kwargs):
		rng,args_ = self.rnggen(*args, **kwargs)
		y         = rng()
		return y,args_

	@property
	def fname(self):
		return self.f.__name__
		
	
@fgen
def anova1(JJ, ss, Q=None, fwhm=None):
	pass

@fgen
def regress(J, s, Q=None, fwhm=None):
	pass

@fgen
def ttest(JJ, ss, Q=None, fwhm=None):
	pass

@fgen
def ttest_paired(J, ss, Q=None, fwhm=None):
	pass

@fgen
def ttest2(JJ, ss, Q=None, fwhm=None):
	pass



# def anova1(JJ, ss, Q=None, fwhm=None):
# 	from . rng import anova1 as rnggen
# 	rng,args = rnggen(JJ, ss, Q, fwhm)
# 	y        = rng()
# 	return y,args
#
#
# def ttest2(JJ, ss, Q=None, fwhm=None):
# 	return anova1(JJ, ss, Q=None, fwhm=None)

