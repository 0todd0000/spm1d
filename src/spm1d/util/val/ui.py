
import numpy as np


def _get_rng(J, Q=None, fwhm=None):
	if Q is None:
		rng = lambda: np.random.randn(J)
	else:
		from rft1d import randn1d
		rng = lambda: randn1d(J, Q, fwhm, pad=True)
	return rng
	

def _t_isf(alpha, df, Q=None, fwhm=None):
	if Q is None:
		from scipy.stats import t
		u = t.isf(0.05, df)
	else:
		from rft1d import t
		u = t.isf(0.05, df, Q, fwhm)
	return u

def _ttest2(y, A):
	from ... stats import ttest2
	u  = np.unique(A)
	y0 = y[A==u[0]]
	y1 = y[A==u[1]]
	return ttest2(y0, y1)

def _ttest_paired(y, A):
	from ... stats import ttest_paired
	u  = np.unique(A)
	y0 = y[A==u[0]]
	y1 = y[A==u[1]]
	return ttest_paired(y0, y1)


def val(fn, rng, valtype='h0', u=None, niter=1000, progress_bar=True):
	from . validators import FPRValidator
	val = FPRValidator(fn, rng, valtype=valtype, u=u, progress_bar=progress_bar)
	val.sim( niter=niter )
	return val
	

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
	A   = np.array([0]*J + [1]*J)
	rng = _get_rng(2*J, Q, fwhm)
	fn  = lambda y: _ttest_paired(y, A)
	u   = _t_isf(alpha, J-1, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=u, niter=niter, progress_bar=progress_bar)

def val_ttest2(JJ, Q=None, fwhm=None, valtype='h0', niter=1000, alpha=0.05, progress_bar=True):
	J0,J1 = JJ
	A     = np.array([0]*J0 + [1]*J1)
	J     = J0 + J1
	rng   = _get_rng(J, Q, fwhm)
	fn    = lambda y: _ttest2(y, A)
	u     = _t_isf(alpha, J-2, Q, fwhm)
	return val(fn, rng, valtype=valtype, u=u, niter=niter, progress_bar=progress_bar)
