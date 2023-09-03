
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
	

def ttest2(JJ, ss, Q=None, fwhm=None):
	# assert isinstance(JJ, (tuple,int))
	# assert isinstance(ss, (tuple,int))
	return anova1(JJ, ss, Q, fwhm)
