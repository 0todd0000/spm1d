
import numpy as np


'''
---- Convenience functions ---- 
'''

def _get_rng(J, Q=None, fwhm=None):
	if Q is None:
		rng = lambda: np.random.randn(J)
	else:
		from rft1d import randn1d
		rng = lambda: randn1d(J, Q, fwhm, pad=True)
	return rng
	

def _f_isf(alpha, df, Q=None, fwhm=None):
	if Q is None:
		from scipy.stats import f
		u = f.isf(0.05, *df)
	else:
		from rft1d import f
		u = f.isf(0.05, df, Q, fwhm)
	return u


def _t_isf(alpha, df, Q=None, fwhm=None):
	if Q is None:
		from scipy.stats import t
		u = t.isf(0.05, df)
	else:
		from rft1d import t
		u = t.isf(0.05, df, Q, fwhm)
	return u





'''
---- Main validation functions ----
'''



def val(fn, rng, valtype='h0', u=None, niter=1000, progress_bar=True):
	from . validators import FPRValidator
	val = FPRValidator(fn, rng, valtype=valtype, u=u, progress_bar=progress_bar)
	val.sim( niter=niter )
	return val
	

def val_anova1(JJ, ss, Q=None, fwhm=None, valtype='h0', niter=1000, alpha=0.05, progress_bar=True):
	from ... stats import anova1
	A     = np.hstack([[i]*J for i,J in enumerate(JJ)])
	_rngs = [_get_rng(J, Q, fwhm)  for J in JJ]
	def rng():
		y = [s*_rng() for s,_rng in zip(ss,_rngs)]
		y = np.hstack(y) if (Q is None) else np.vstack(y)
		return y
	fn    = lambda y: anova1(y, A, equal_var=True)
	df    = len(JJ)-1, A.size-len(JJ)
	u     = _f_isf(alpha, df, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=u, niter=niter, progress_bar=progress_bar)


def val_anova1rm(J, ss, Q=None, fwhm=None, valtype='h0', niter=1000, alpha=0.05, progress_bar=True):
	from ... stats import anova1rm
	n     = len(ss)
	A     = np.hstack(   [ [i]*J for i in range(n) ]   )
	S     = np.hstack(   [ np.arange(J) ] * n   )
	_rngs = [_get_rng(J, Q, fwhm)]*n
	def rng():
		y = [s*_rng() for s,_rng in zip(ss,_rngs)]
		y = np.hstack(y) if (Q is None) else np.vstack(y)
		return y
	fn    = lambda y: anova1rm(y, A, S, equal_var=True)
	df_w  = A.size - n
	df_b  = J - 1
	df_e  = df_w - df_b
	df    = n-1, df_e
	u     = _f_isf(alpha, df, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=u, niter=niter, progress_bar=progress_bar)


def val_anova2(JJ, ss, Q=None, fwhm=None, valtype='h0', niter=1000, alpha=0.05, progress_bar=True):
	from ... stats import anova2
	JJ    = np.asarray(JJ)
	ss    = np.asarray(ss)
	nA,nB = JJ.shape
	AA    = np.vstack([list(range(nA))  for i in range(nB)] ).T
	BB    = np.vstack([list(range(nB))  for i in range(nA)] )
	A     = np.hstack([[x]*j  for x,j in zip(AA.ravel(), JJ.ravel())])
	B     = np.hstack([[x]*j  for x,j in zip(BB.ravel(), JJ.ravel())])
	df_a  = nA - 1
	df_b  = nB - 1
	df_ab = (nA - 1) * (nB - 1)
	df_e  = sum([j-1  for j in JJ.ravel()])
	dfA   = df_a, df_e
	dfB   = df_b, df_e
	dfAB  = df_ab, df_e
	_rngs = [_get_rng(J, Q, fwhm)  for J in JJ.ravel()]
	def rng():
		y = [s*_rng() for s,_rng in zip(ss.ravel(),_rngs)]
		y = np.hstack(y) if (Q is None) else np.vstack(y)
		return y
	fn    = lambda y: anova2(y, A, B, equal_var=True)
	df    = len(JJ)-1, A.size-len(JJ)
	uA    = _f_isf(alpha, dfA,  Q, fwhm)
	uB    = _f_isf(alpha, dfB,  Q, fwhm)
	uAB   = _f_isf(alpha, dfAB, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=[uA,uB,uAB], niter=niter, progress_bar=progress_bar)



def val_regress(J, Q=None, fwhm=None, valtype='h0', niter=1000, alpha=0.05, progress_bar=True):
	from ... stats import regress
	rng = _get_rng(J, Q, fwhm)
	x   = np.linspace(0, 1, J)
	fn  = lambda y: regress(y, x)
	u   = _t_isf(alpha, J-2, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=u, niter=niter, progress_bar=progress_bar)


def val_ttest(J, Q=None, fwhm=None, valtype='h0', niter=1000, alpha=0.05, progress_bar=True):
	from ... stats import ttest
	rng = _get_rng(J, Q, fwhm)
	fn  = lambda y: ttest(y, 0)
	u   = _t_isf(alpha, J-1, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=u, niter=niter, progress_bar=progress_bar)


def val_ttest_paired(J, Q=None, fwhm=None, valtype='h0', niter=1000, alpha=0.05, progress_bar=True):
	def _ttest_paired(y, A):
		from ... stats import ttest_paired
		u  = np.unique(A)
		y0 = y[A==u[0]]
		y1 = y[A==u[1]]
		return ttest_paired(y0, y1)
		
	A   = np.array([0]*J + [1]*J)
	rng = _get_rng(2*J, Q, fwhm)
	fn  = lambda y: _ttest_paired(y, A)
	u   = _t_isf(alpha, J-1, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=u, niter=niter, progress_bar=progress_bar)


def val_ttest2(JJ, ss=(1,1), Q=None, fwhm=None, valtype='h0', niter=1000, alpha=0.05, progress_bar=True, equal_var=False):
	def _ttest2(y, A, equal_var=False):
		from ... stats import ttest2
		u  = np.unique(A)
		y0 = y[A==u[0]]
		y1 = y[A==u[1]]
		return ttest2(y0, y1, equal_var=equal_var)
	
	J0,J1 = JJ
	J     = sum(JJ)
	A     = np.array(  [0]*J0 + [1]*J1  )
	s     = np.hstack(  [[s]*j for s,j in zip(ss,JJ)]  )
	_rng  = _get_rng(J, Q, fwhm)
	rng   = lambda: (s * _rng().T).T
	fn    = lambda y: _ttest2(y, A, equal_var=equal_var)
	u     = _t_isf(alpha, J-2, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=u, niter=niter, progress_bar=progress_bar)
