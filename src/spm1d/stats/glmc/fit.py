

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
	ndim        = Y.ndim
	if ndim == 1:
		Y       = np.array([Y]).T
	n,s         = Y.shape
	trRV        = n - rank(X)
	q           = np.diag(np.sqrt( trRV / s2 )).T if (ndim==2) else np.array( [np.sqrt( trRV / s2 )] )
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
		# self._df   = None   # effective degrees of freedom (for one contrast)
		# self._f    = None   # F statistic (for one contrast)
		# self._v    = None   # variance scale (for one contrast); same as df when equal variance is assumed
		self.model  = model
		self.b      = b      # betas (fitted parameters)
		self.e      = e      # residuals
		self.Xi     = Xi     # design pseudo-inverse
		self.y      = y      # (J,Q) dependent variable array where J=num.observations and Q=num.continuum nodes
		self.df     = 1, y.shape[0] - rank(model.X)  # degrees of freedom
		
		
		self.V      = None   # estimated (co-)variance
		self.h      = None   # estimated (co-)variance hyperparameters
		self.sse    = None
		self.mse    = None
		# self.ss     = (e ** 2).sum(axis=0)           # sum-of-squared residuals
		# self.s2     = None
		
		self._calculate_sse()
		self._estimate_variance()
		
		
		
		
		# self.mse    = None   # mean squared error
		# self.sse    = None   # sum of error squares
		
		# self._estimate_variance()
		# self._calculate_sse()
		# # if self.dvdim == 1:
		# # 	from ... geom import estimate_fwhm, resel_counts
		# # 	self.fwhm   = estimate_fwhm( e )
		# # 	self.resels = resel_counts(e, self.fwhm, element_based=False, roi=None)
		
		# self._estimate_variance()
		# self._calculate_sse()
		
		
		### ANOVA attributes
		self.h      = None   # (co-)variance hyperparameters
		
		


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
	@property
	def ss(self):
		return self.sse
	@property
	def s2(self):
		return self.mse













	'''
	ANOVA-related functions
	'''
	# def _calculate_sse(self):
	# 	y,X      = self.y, self.model.X
	# 	# PX       = X @ np.linalg.pinv(X)      # X projector
	# 	PX       = X @ self.Xi  # X projector
	# 	YIPY     = y.T @ ( np.eye( self.J ) - PX ) @ y   # eqn.9.13 denominator (Friston 2007, p.135)
	# 	self.sse = float(YIPY) if (self.dvdim==0) else np.diag(YIPY)
	# 	# self.mse     = self.sse / self.df[1]           # variance
	# 	self.s2  = self.sse / self.df[1]                  # variance

	def _calculate_sse(self):
		sse      = (self.e ** 2).sum(axis=0)           # sum-of-squared residuals
		self.sse = float(sse) if (self.dvdim==0) else sse
		self.mse = self.sse / self.df[1]           # variance
		# self.s2  = self.sse / self.df[1]           # variance


	def _estimate_variance(self):
		if self.model.QQ is not None:
			from .. _cov import reml, traceRV
			n,s           = self.y.shape
			trRV          = n - rank(self.model.X)
			# ss            = (self.e**2).sum(axis=0)
			q             = np.diag(  np.sqrt( trRV / self.ss )  ).T
			Ym            = self.y @ q
			# Ym            = self.e @ q
			YY            = Ym @ Ym.T / s
			V,h           = reml(YY, self.model.X, self.model.QQ)
			# V,h           = reml(YY, self.X, self.QQ)
			V            *= (n / np.trace(V))
			
			# trRV,trRVRV = traceRV(V, X)
			# df          = trRV**2 / trRVRV  # effective degrees of freedom
			
			
			self.V        = V
			self.h        = h
			

	# def __tstat_cov_model(Y, X, Xi, c, b, s2, Q):
	# 	from .. _cov import reml, traceRV
	# 	ndim        = Y.ndim
	# 	if ndim == 1:
	# 		Y       = np.array([Y]).T
	# 	n,s         = Y.shape
	# 	trRV        = n - rank(X)
	# 	q           = np.diag(np.sqrt( trRV / s2 )).T if (ndim==2) else np.array( [np.sqrt( trRV / s2 )] )
	# 	Ym          = Y @ q
	# 	if ndim == 1:
	# 		Ym      = np.array([Ym]).T
	# 	YY          = Ym @ Ym.T / s
	# 	V,h         = reml(YY, X, Q)
	# 	V           = V * (n / np.trace(V))
	# 	trRV,trRVRV = traceRV(V, X)
	# 	df          = trRV**2 / trRVRV  # effective degrees of freedom
	# 	t           = (c @ b)  /   ( np.sqrt( s2 * (c @ Xi @ V @ Xi.T @ c)  + eps ) )
	# 	return t, df
	
	
	
	def _calculate_effective_df(self, C=None, X=None, STAT='T'):
		X             = self.model.X if (X is None) else X
		
		if STAT=='T':
			trRV,trRVRV   = traceRV(self.V, X)
			df            = 1, trRV**2 / trRVRV  # effective degrees of freedom
			v             = self.df
		else:
			trRV,trRVRV   = traceRV(self.V, X)
			trMV,trMVMV   = traceMV(self.V, self.model.X, C)
			df0           = max(trMV**2 / trMVMV, 1.0)
			df1           = trRV**2 / trRVRV
			df            = df0, df1
			v             = trMV, trRV
		self.v            = v
		return df,v
		# self._df       = df0, df1
		# self._v       = v0, v1
		

	def calculate_f_stat(self, C, gg=False, _Xeff=None, ind=0):
		from . teststats import TestStatisticF
		# self._estimate_variance()
		# self._calculate_sse()
		
		# build projectors:
		y,X      = self.y, self.model.X
		# PX      = X @ np.linalg.pinv(X)      # X projector
		H        = np.linalg.pinv( X.T ) @ C  # text between eqns. 9.17 & 9.18 (Friston 2007, p.136)
		PH       = H @ np.linalg.inv(H.T @ H) @ H.T     # H projector
		# estimate df:
		df,v     = self._calculate_effective_df( C, _Xeff )
		v0,v1    = v
		# self.mse = self.sse / v1
		
		# f stat:
		# YIPY    = y.T @ ( np.eye( self.J ) - PX ) @ y   # eqn.9.13 denominator (Friston 2007, p.135)
		YPHYY   = y.T @ PH @ y               # eqn.9.18 (Friston 2007, p.136)
		f       = (YPHYY / v0) / self.mse    # eqn.9.13 (Friston 2007, p.135)
		ss      = YPHYY
		ms      = YPHYY / v0
		if gg:
			df  = self._calculate_adjusted_df_greenhouse_geisser(df)

		f       = float(f)  if (self.dvdim==0) else np.diag(f)
		ss      = float(ss) if (self.dvdim==0) else np.diag(ss)
		ms      = float(ms) if (self.dvdim==0) else np.diag(ms)
		
		return TestStatisticF(f, df, v, ss, ms, C, ind)






















	def calculate_t_stat(self, c, roi=None):
		# Q = None
		b,s2,X   = self.b, self.s2, self.model.X
		
		t        = (c @ b)  /   ( np.sqrt( s2 * (c @ np.linalg.inv(X.T @ X) @ c) ) + eps )
		t        = float(t)  if (self.dvdim==0) else t.flatten()
		
		if self.model.QQ is None:
			df   = self.df
		else:
			df,v = self._calculate_effective_df( STAT='T' )
		
		
		# if self.QQ is None:  # covariance not modeled
		# 	t      = (c @ b)  /   ( np.sqrt( s2 * (c @ np.linalg.inv(X.T @ X) @ c) ) + eps )
		# 	df     = self.df
		# else:
		# 	t,df   = _tstat_cov_model(self.y, X, self.Xi, c, b, s2, self.QQ, roi=roi)
		# 	df     = (1,df)
			
			
		
		return TestStatisticT(t, df, c)
		# return t,df
		
		
		
	def isequal(self, other, verbose=False):
		import pytest
		# if type(self) != type(other):
		# 	return False
			
		if self.model != other.model:
			return False
		
		if not self.df == other.df:
			return False

		for s in ['b', 'e', 'Xi', 'sse', 's2', 'y']: 
			x0,x1  = getattr(self, s), getattr(other, s)
			# if verbose:
			# 	print( f'{s}:  {x0},  {x1}' )
			if s=='sse':
				return self.sse == pytest.approx(other.sse)
			else:
				if not np.all(x0 == x1):
					return False

		return True





