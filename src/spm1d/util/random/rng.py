
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
	A     = np.hstack(  [[i]*J   for i,J   in enumerate(JJ)]  )
	s     = np.hstack(  [[sss]*J for sss,J in zip(ss,JJ)]  )
	J     = sum(JJ)
	_rng  = _get_rng(J, Q, fwhm)
	def rng():
		y = (s * _rng().T).T
		return y
	return rng,(A,)


def anova1rm(J, ss, Q=None, fwhm=None):
	n     = len(ss)
	JJ    = (J,) * n
	S     = np.array( list(range(J)) * n  )
	rng,(A,) = anova1(JJ, ss, Q, fwhm)
	return rng,(A,S)

def anova2(JJ, ss, Q=None, fwhm=None):
	JJ    = np.asarray(JJ)
	ss    = np.asarray(ss)
	nA,nB = JJ.shape
	AA    = np.vstack([list(range(nA))  for i in range(nB)] ).T
	BB    = np.vstack([list(range(nB))  for i in range(nA)] )
	A     = np.hstack([[x]*j  for x,j in zip(AA.ravel(), JJ.ravel())])
	B     = np.hstack([[x]*j  for x,j in zip(BB.ravel(), JJ.ravel())])
	s     = np.hstack([[s]*j  for s,j in zip(ss.ravel(), JJ.ravel())])
	J     = JJ.sum()
	_rng  = _get_rng(J, Q, fwhm)
	def rng():
		y = (s * _rng().T).T
		return y
	return rng,(A,B)

def anova2rm(J, ss, Q=None, fwhm=None):
	ss    = np.asarray(ss)
	nA,nB = ss.shape
	AA    = np.vstack([list(range(nA))  for i in range(nB)] ).T
	BB    = np.vstack([list(range(nB))  for i in range(nA)] )
	A     = np.hstack([[x]*J  for x in AA.ravel()])
	B     = np.hstack([[x]*J  for x in BB.ravel()])
	S     = np.array( list(range(J)) * nA * nB  )
	s     = np.hstack([[s]*J  for s in ss.ravel()])
	J     = s.size
	_rng  = _get_rng(J, Q, fwhm)
	def rng():
		y = (s * _rng().T).T
		return y
	return rng,(A,B,S)

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
