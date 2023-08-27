

import numpy as np
from . teststats import TestStatisticT
from .. _cov import reml, traceRV, traceMV, _reml_old
from .. _la import rank
from ... util import array2shortstr, arraylist2str, arraytuple2str, dflist2str, objectlist2str, resels2str, scalarlist2string, DisplayParams
eps = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors




def __tstat_cov_model(Y, X, Xi, c, b, s2, Q):
	'''
	t statistic calculation given a covariance model (Q)
	
	Covariance components (V) and their hyperparameters (h)
	are estimated using REML. See spm1d.stats._cov.py for
	more details
	'''
	from .. _cov import reml, traceRV
	# print(Y)
	ndim        = 1 if (Y.ndim==1  or Y.shape[1]==1) else 2
	# if ndim == 1:
	# 	Y       = np.array([Y]).T
	n,s         = Y.shape
	trRV        = n - rank(X)
	q           = np.diag(np.sqrt( trRV / s2 )).T if (ndim==2) else np.array( [np.sqrt( trRV / s2 )] )
	# q           = np.array( [np.sqrt( trRV / s2 )] ) if isinstance(s2, float) else np.diag(np.sqrt( trRV / s2 )).T
	Ym          = Y @ q
	if ndim == 1:
		Ym      = np.array([Ym]).T
	YY          = Ym @ Ym.T / s
	V,h         = reml(YY, X, Q)
	V           = V * (n / np.trace(V))
	trRV,trRVRV = traceRV(V, X)
	df          = trRV**2 / trRVRV  # effective degrees of freedom
	t           = (c @ b)  /   ( np.sqrt( s2 * (c @ Xi @ V @ Xi.T @ c)  + eps ) )
	return t, df


def _tstat_cov_model(Y, X, Xi, c, b, s2, Q, roi=None):
	if roi is None:
		t,df      = __tstat_cov_model(Y, X, Xi, c, b, s2, Q)
	else:
		_Y,_b,_s2 = Y[:,roi], b[:,roi], s2[roi]
		_t,df     = __tstat_cov_model(_Y, X, Xi, c, _b, _s2, Q)
		t         = np.nan * np.ones(Y.shape[1])
		t[roi]    = _t
	return t, df



class GLMFit(object):


	def __init__(self, model, y, b, e, Xi):
		# print(y.shape)
		# print(1 in y.shape)
		# self._df   = None   # effective degrees of freedom (for one contrast)
		# self._f    = None   # F statistic (for one contrast)
		# self._v    = None   # variance scale (for one contrast); same as df when equal variance is assumed
		self.model  = model
		# self.V      = None   # estimated (co-)variance
		self.b      = b      # betas (fitted parameters)
		# self.dvdim  = 0 if ((y.ndim==1) or (1 in y.shape)) else 1 # dependent variable dimensionality
		self.e      = e      # residuals
		self.Xi     = Xi     # design pseudo-inverse
		# print(self.dvdim)
		
		self.y      = y      # (J,Q) dependent variable array where J=num.observations and Q=num.continuum nodes
		
		
		self.ss     = (e ** 2).sum(axis=0)   # sum-of-squared residuals
		self.ss     = float(self.ss) if (self.dvdim==0) else self.ss
		
		self.df     = 1, y.shape[0] - rank(model.X)     # degrees of freedom
		self.s2     = self.ss / self.df[1]                  # variance
		
		
		
		
		# # self.fwhm   = None   # estimated residual smoothness
		# # self.resels = None  # resel counts
		# self.h      = None   # (co-)variance hyperparameters
		# self.mse    = None   # mean squared error
		# self.sse    = None   # sum of error squares
		# self.y      = y      # (J,Q) dependent variable array where J=num.observations and Q=num.continuum nodes
		# self._estimate_variance()
		# self._calculate_sse()
		# # if self.dvdim == 1:
		# # 	from ... geom import estimate_fwhm, resel_counts
		# # 	self.fwhm   = estimate_fwhm( e )
		# # 	self.resels = resel_counts(e, self.fwhm, element_based=False, roi=None)


	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'y' , array2shortstr )
		dp.add( 'dvdim' )
		dp.add( 'b', array2shortstr )
		dp.add( 'e', array2shortstr )
		# dp.add( 'V', array2shortstr )
		# dp.add( 'h', scalarlist2string )


		# ANOVA-specific attributes:
		# if self.dvdim == 0:
		# 	dp.add( 'mse' )
		# 	dp.add( 'sse' )
		# else:
		# 	dp.add( 'mse', array2shortstr )
		# 	dp.add( 'sse', array2shortstr )

		return dp.asstr()



	@property
	def J(self):
		return self.model.J
	@property
	def QQ(self):
		return self.model.QQ


	@property
	def dvdim(self):   # dependent variable domain dimensionality
		return 0 if ((self.y.ndim==1) or (1 in self.y.shape)) else 1

	
	# def _calculate_effective_df(self, C, X=None):
	# 	X             = self.model.X if (X is None) else X
	# 	trRV,trRVRV   = traceRV(self.V, X)
	# 	trMV,trMVMV   = traceMV(self.V, self.model.X, C)
	# 	df0           = max(trMV**2 / trMVMV, 1.0)
	# 	df1           = trRV**2 / trRVRV
	# 	df            = df0, df1
	# 	v             = trMV, trRV
	# 	return df,v
	# 	# self._df       = df0, df1
	# 	# self._v       = v0, v1
	#
	# def _calculate_sse(self):
	# 	y,X      = self.y, self.model.X
	# 	PX       = X @ np.linalg.pinv(X)      # X projector
	# 	YIPY     = y.T @ ( np.eye( self.J ) - PX ) @ y   # eqn.9.13 denominator (Friston 2007, p.135)
	# 	self.sse = float(YIPY) if (self.dvdim==0) else np.diag(YIPY)



	# def _estimate_variance(self):
	# 	# i             = np.any(self.C, axis=1)
	# 	# _X            = self.X[:,i]  # design matrix excluding non-contrast columns
	# 	# _C            = self.C[i]
	# 	# X             = self.model.X
	# 	n,s           = self.y.shape
	# 	# trRV          = n - rank(_X)
	# 	trRV          = n - rank(self.model.X)
	# 	ss            = (self.e**2).sum(axis=0)
	# 	q             = np.diag(  np.sqrt( trRV / ss )  ).T
	# 	Ym            = self.y @ q
	# 	# Ym            = self.e @ q
	# 	YY            = Ym @ Ym.T / s
	# 	V,h           = reml(YY, self.model.X, self.model.QQ)
	# 	# V,h           = reml(YY, self.X, self.QQ)
	# 	V            *= (n / np.trace(V))
	# 	self.h        = h
	# 	self.V        = V



	def calculate_t_stat(self, c, roi=None):
		# Q = None
		b,s2,X = self.b, self.s2, self.model.X
		
		if self.QQ is None:  # covariance not modeled
			t      = (c @ b)  /   ( np.sqrt( s2 * (c @ np.linalg.inv(X.T @ X) @ c) ) + eps )
			df     = self.df
		else:
			t,df   = _tstat_cov_model(self.y, X, self.Xi, c, b, s2, self.QQ, roi=roi)
			df     = (1,df)
			
			
		t       = float(t)  if (self.dvdim==0) else t.flatten()
		return TestStatisticT(t, df, c)
		# return t,df
		
		
		
	# def isequal(self, other, verbose=False):
	# 	# if type(self) != type(other):
	# 	# 	return False
	#
	# 	if self.model != other.model:
	# 		return False
	#
	# 	if not self.df == other.df:
	# 		return False
	#
	# 	for s in ['b', 'e', 'Xi', 'ss', 's2', 'y']:
	# 		x0,x1  = getattr(self, s), getattr(other, s)
	# 		if not np.all(x0 == x1):
	# 			return False
	#
	# 	return True


	def isequal(self, other, verbose=False):
		import pytest
		# print(  f'isequal, verbose={verbose}' )
		# if type(self) != type(other):
		# 	return False
			
		if self.model != other.model:
			return False
		
		# if not self.df == other.df:
		# 	return False

		for s in ['b', 'e', 'ss', 'y']: 
			x0,x1  = getattr(self, s), getattr(other, s)
			if verbose:
				print( f'{s}:  {x0},  {x1}' )
			if s=='ss':
				return self.ss == pytest.approx(other.ss)
			else:
				if not np.all(x0 == x1):
					return False
			#
			# if not np.all(x0 == x1):
			# 	return False

		return True
		
		
	# def calculate_f_stat(self, C, gg=False, _Xeff=None, ind=0):
	# 	# build projectors:
	# 	y,X      = self.y, self.model.X
	# 	# PX      = X @ np.linalg.pinv(X)      # X projector
	# 	H        = np.linalg.pinv( X.T ) @ C  # text between eqns. 9.17 & 9.18 (Friston 2007, p.136)
	# 	PH       = H @ np.linalg.inv(H.T @ H) @ H.T     # H projector
	# 	# estimate df:
	# 	df,v     = self._calculate_effective_df( C, _Xeff )
	# 	v0,v1    = v
	# 	self.mse = self.sse / v1
	# 	# f stat:
	# 	# YIPY    = y.T @ ( np.eye( self.J ) - PX ) @ y   # eqn.9.13 denominator (Friston 2007, p.135)
	# 	YPHYY   = y.T @ PH @ y               # eqn.9.18 (Friston 2007, p.136)
	# 	f       = (YPHYY / v0) / self.mse    # eqn.9.13 (Friston 2007, p.135)
	# 	ss      = YPHYY
	# 	ms      = YPHYY / v0
	# 	if gg:
	# 		df  = self._calculate_adjusted_df_greenhouse_geisser(df)
	#
	# 	f       = float(f)  if (self.dvdim==0) else np.diag(f)
	# 	ss      = float(ss) if (self.dvdim==0) else np.diag(ss)
	# 	ms      = float(ms) if (self.dvdim==0) else np.diag(ms)
	#
	# 	return TestStatisticF(f, df, v, ss, ms, C, ind)


# SPM0D(design, model, fit, s)


