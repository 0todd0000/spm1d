
'''
Random number generators
'''

import numpy as np



def _get_rng(J, Q=None, fwhm=None):
	if Q is None:
		rng = lambda: np.random.randn(J)
	else:
		from rft1d import randn1d
		rng = lambda: randn1d(J, Q, fwhm, pad=True)
	return rng



def anova1(JJ, ss, Q=None, fwhm=None):
	A     = np.hstack(  [[i]*J for i,J in enumerate(JJ)]  )
	_rngs = [_get_rng(J, Q, fwhm)  for J in JJ]
	def rng():
		y = [s*r() for s,r in zip(ss,_rngs)]
		y = np.hstack(y) if (Q is None) else np.vstack(y)
		return y
	return rng,(A,)
	

def regress(J, s, Q=None, fwhm=None):
	x    = np.linspace(0, 1, J)
	_rng = _get_rng(J, Q, fwhm)
	def rng():
		y = s * _rng()
		return y
	return rng, (x,)

def ttest(J, s, Q=None, fwhm=None):
	return anova1((J,), (s,), Q, fwhm)

def ttest_paired(J, ss, Q=None, fwhm=None):
	return anova1((J,J), ss, Q, fwhm)

def ttest2(JJ, ss, Q=None, fwhm=None):
	return anova1(JJ, ss, Q, fwhm)
