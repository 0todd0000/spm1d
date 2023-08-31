

import numpy as np
from .. _cov import reml, traceRV, traceMV, _reml_old
from .. _la import rank
from ... util import array2shortstr, arraylist2str, arraytuple2str, dflist2str, objectlist2str, resels2str, scalarlist2string, DisplayParams
eps = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors








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
		# self.df0    = 1, y.shape[0] - rank(model.X)  # degrees of freedom  (for a t contrast under an assumption of equal variance)
		self.df0    = self.model.df0   # degrees of freedom
		# self.df     = None   # degrees of freedom (possibly adjusted for unequal variance and non-sphericity)
		self.V      = None   # estimated (co-)variance  (only used when equal variance is NOT assumed)
		self.h      = None   # estimated (co-)variance hyperparameters  (only used when equal variance is NOT assumed)
		self.sse    = None   # sum of squared errors
		self.mse    = None   # mean squared error
		
		self.sse    = (self.e ** 2).sum(axis=0)
		# v1          = self.mode.dfe0
		self.mse    = self.sse / self.model.dfe0
		# self._estimate_variance()
		# self.mse = self.sse / self.df0[1]
		
		
		# self._estimate_variance()
		# self._calculate_sse_mse()
		


	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'y' , array2shortstr )
		dp.add( 'dvdim' )
		dp.add( 'b', array2shortstr )
		dp.add( 'e', array2shortstr )
		dp.add( 'V', array2shortstr )
		dp.add( 'h', scalarlist2string )
		if self.dvdim == 0:
			dp.add( 'mse' )
			dp.add( 'sse' )
		else:
			dp.add( 'mse', array2shortstr )
			dp.add( 'sse', array2shortstr )
		return dp.asstr()



	@property
	def J(self):
		return self.model.J
	# @property
	# def df0(self):   # degrees of freedom  (under an assumption of equal variance)
	# 	return self.model.df0
	# @property
	# def dfe(self):   # error degrees of freedom
	# 	return self.model.dfe
	@property
	def dvdim(self):   # dependent variable domain dimensionality
		return 0 if ((self.y.ndim==1) or (1 in self.y.shape)) else 1

	# previous properties (unneeded)
	# @property
	# def QQ(self):
	# 	return self.model.QQ
	# @property
	# def ss(self):
	# 	return self.sse
	# @property
	# def s2(self):   # variance
	# 	return self.mse













	'''
	ANOVA-related functions
	'''
	# def _calculate_sse_mse(self):  # these are the previous estimates but the new function below is much faster and seems to produce the same results
	# 	y,X      = self.y, self.model.X
	# 	# PX       = X @ np.linalg.pinv(X)      # X projector
	# 	PX       = X @ self.Xi  # X projector
	# 	YIPY     = y.T @ ( np.eye( self.J ) - PX ) @ y   # eqn.9.13 denominator (Friston 2007, p.135)
	# 	self.sse = float(YIPY) if (self.dvdim==0) else np.diag(YIPY)
	# 	# self.mse     = self.sse / self.df[1]           # variance
	# 	self.s2  = self.sse / self.df[1]                  # variance  (same as previous:  self.mse = self.sse / self.df[1] )

	# def _calculate_sse_mse(self):
	# 	self.sse = (self.e ** 2).sum(axis=0)
	# 	self.mse = self.sse / self.df0[1]

	# def _estimate_variance(self):
	# 	if self.model.QQ is not None:
	# 		from .. _cov import reml, traceRV
	# 		n,s           = self.y.shape
	# 		trRV          = n - rank(self.model.X)
	# 		q             = np.diag(  np.sqrt( trRV / self.sse )  ).T
	# 		Ym            = self.y @ q
	# 		# Ym            = self.e @ q
	# 		YY            = Ym @ Ym.T / s
	# 		V,h           = reml(YY, self.model.X, self.model.QQ)
	# 		# V,h           = reml(YY, self.X, self.model.QQ)
	# 		V            *= (n / np.trace(V))
	#
	# 		# trRV,trRVRV = traceRV(V, X)
	# 		# df          = trRV**2 / trRVRV  # effective degrees of freedom
	#
	#
	# 		self.V        = V
	# 		self.h        = h

	
	# def _calculate_effective_df(self, C=None, X=None, STAT='T'):
	# 	if STAT=='T':
	# 		trRV,trRVRV   = traceRV(self.V, self.model.X)
	# 		self.df       = 1, trRV**2 / trRVRV  # effective degrees of freedom
	# 	elif STAT=='F':
	# 		X             = self.model.X if (X is None) else X
	# 		trRV,trRVRV   = traceRV(self.V, X)
	# 		trMV,trMVMV   = traceMV(self.V, self.model.X, C)
	# 		df0           = max(trMV**2 / trMVMV, 1.0)
	# 		df1           = trRV**2 / trRVRV
	# 		self.df       = df0, df1
	# 		self.df0      = trMV, trRV
	# 		self.mse      = self.sse / self.df0[1]


	def _greenhouse_geisser_adjustment(self):
		pass
		#
		# # this works for 0D data:
		# if self.dvdim==1:
		# 	y      = self.y.ravel()
		# 	ytable = np.vstack(  [y[self.A==u]  for u in self.uA]  )
		# 	k,n    = ytable.shape
		# 	S      = np.cov(ytable, ddof=1)
		# else:
		# 	S       = np.array([h*q  for h,q in zip(self.h, self.model.QQ)]).sum(axis=0)  # Eqn.10.14  (Friston, 2007)
		# 	k       = self.uA.size
		# 	n       = self.J / k
		# # # my BAD 1D attempt:
		# # k      = self.uA.size
		# # n      = self.J / k
		# # S      = self.V
		#
		# # # new 1D attempt:
		# # S       = np.array([h*q  for h,q in zip(self.h, self.model.QQ)]).sum(axis=0)  # Eqn.10.14  (Friston, 2007)
		# # k       = self.uA.size
		# # n       = self.J / k
		# # eps    = _greenhouse_geisser( S, k )
		#
		# w,v     = np.linalg.eig( S )
		# ind     = w.argsort()[::-1]
		# v       = v[:,ind]
		# M       = v[:,:k-1]
		# Sz      = M.T @ S @ M
		# w,_     = np.linalg.eig( Sz )
		# e       = w.sum()**2 / (   (k-1) * (w**2).sum()   )   # Eqn.13.37, Friston et al. (2007), p.176
		# self._df = (k-1)*e, (n-1)*(k-1)*e    # Eqn.13.36, Friston et al. (2007), p.176
	
	# def calculate_f_stat(self, C, gg=False, _Xeff=None, ind=0):
	# 	from . teststats import TestStatisticF
	#
	# 	self._calculate_effective_df( C, _Xeff, STAT='F' )
	# 	# if self.model.QQ is None:
	# 	# 	self.df  = int(self.df[0]), int(self.df[1])
	#
	# 	# build projectors:
	# 	y,X      = self.y, self.model.X
	# 	# PX      = X @ np.linalg.pinv(X)      # X projector
	# 	H        = np.linalg.pinv( X.T ) @ C  # text between eqns. 9.17 & 9.18 (Friston 2007, p.136)
	# 	PH       = H @ np.linalg.inv(H.T @ H) @ H.T     # H projector
	#
	#
	# 	# f stat:
	# 	v0      = self.df0[0]
	# 	# YIPY    = y.T @ ( np.eye( self.J ) - PX ) @ y   # eqn.9.13 denominator (Friston 2007, p.135)
	# 	YPHYY   = y.T @ PH @ y               # eqn.9.18 (Friston 2007, p.136)
	# 	f       = (YPHYY / v0) / self.mse    # eqn.9.13 (Friston 2007, p.135)
	# 	ss      = YPHYY
	# 	ms      = YPHYY / v0
	#
	# 	# greenhouse_geisser adjustment:
	# 	# if gg:
	# 	# 	self.df  = self._greenhouse_geisser_adjustment(df)
	# 	f       = float(f)  if (self.dvdim==0) else np.diag(f)
	# 	ss      = float(ss) if (self.dvdim==0) else np.diag(ss)
	# 	ms      = float(ms) if (self.dvdim==0) else np.diag(ms)
	#
	# 	return TestStatisticF(f, self.df, self.df0, ss, ms, C, ind)


	def _calculate_effective_df_f(self, V, C, X=None):
		X             = self.model.X if (X is None) else X
		trRV,trRVRV   = traceRV(V, X)
		trMV,trMVMV   = traceMV(V, self.model.X, C)
		df            = max(trMV**2 / trMVMV, 1.0), trRV**2 / trRVRV
		# self.df       = df0, df1
		# self.df0      = trMV, trRVRV
		_df0      = trMV, trRVRV
		print( _df0 )
		
		# self.mse      = self.sse / self.df0[1]
		return df

	# def _estimate_variance_t(self, QQ):
	# 	from .. _cov import reml, traceRV
	# 	n,s           = self.y.shape
	# 	trRV          = n - rank(self.model.X)
	# 	q             = np.diag(  np.sqrt( trRV / self.sse )  ).T
	# 	Ym            = self.y @ q
	# 	# Ym            = self.e @ q
	# 	YY            = Ym @ Ym.T / s
	# 	V,h           = reml(YY, self.model.X, QQ)
	# 	# V,h           = reml(YY, self.X, self.model.QQ)
	# 	V            *= (n / np.trace(V))
	#
	# 	# trRV,trRVRV = traceRV(V, X)
	# 	# df          = trRV**2 / trRVRV  # effective degrees of freedom
	# 	self.V        = V
	# 	self.h        = h
	# 	return V,h
	# 	#
	# 	# self.V        = V
	# 	# self.h        = h


	def calculate_f_stat(self, C, gg=False, _Xeff=None, ind=0):
		from . teststats import TestStatisticF
		
		if self.model.QQ is None:
			df   = self.model.df0[ind]
			
		else:
			V,_  = self._estimate_variance_t( self.model.QQ )
			df   = self._calculate_effective_df_f( V, C, _Xeff )
		# if self.model.QQ is None:
		# 	self.df  = int(self.df[0]), int(self.df[1])
		
		# build projectors:
		y,X      = self.y, self.model.X
		# PX      = X @ np.linalg.pinv(X)      # X projector
		H        = np.linalg.pinv( X.T ) @ C  # text between eqns. 9.17 & 9.18 (Friston 2007, p.136)
		PH       = H @ np.linalg.inv(H.T @ H) @ H.T     # H projector
		
		
		# f stat:
		v0      = self.model.df0[ind][0]
		# v0      = self.model.dfe0
		
		# YIPY    = y.T @ ( np.eye( self.J ) - PX ) @ y   # eqn.9.13 denominator (Friston 2007, p.135)
		YPHYY   = y.T @ PH @ y               # eqn.9.18 (Friston 2007, p.136)
		f       = (YPHYY / v0) / self.mse    # eqn.9.13 (Friston 2007, p.135)
		ss      = YPHYY
		ms      = YPHYY / v0

		# greenhouse_geisser adjustment:
		# if gg:
		# 	self.df  = self._greenhouse_geisser_adjustment(df)
		f       = float(f)  if (self.dvdim==0) else np.diag(f)
		ss      = float(ss) if (self.dvdim==0) else np.diag(ss)
		ms      = float(ms) if (self.dvdim==0) else np.diag(ms)
		
		# TestStatisticT(t, df, c, df0=df0)
		# f, df, v, ss, ms, C, ind=0, df0=None
		return TestStatisticF(f, df, ss, ms, C, ind=ind, df0=self.df0[ind])















	def _calculate_effective_df_t(self, X, V):
		trRV,trRVRV   = traceRV(V, X)
		df            = 1, trRV**2 / trRVRV
		return df


	def _estimate_variance_t(self, QQ):
		from .. _cov import reml, traceRV
		n,s           = self.y.shape
		trRV          = n - rank(self.model.X)
		q             = np.diag(  np.sqrt( trRV / self.sse )  ).T
		Ym            = self.y @ q
		# Ym            = self.e @ q
		YY            = Ym @ Ym.T / s
		V,h           = reml(YY, self.model.X, QQ)
		# V,h           = reml(YY, self.X, self.model.QQ)
		V            *= (n / np.trace(V))
		
		# trRV,trRVRV = traceRV(V, X)
		# df          = trRV**2 / trRVRV  # effective degrees of freedom
		self.V        = V
		self.h        = h
		return V,h
		#
		# self.V        = V
		# self.h        = h



	def calculate_t_stat(self, c, roi=None):
		from . teststats import TestStatisticT
		self.mse      = self.sse / self.df0[1]
		if self.model.QQ is None:
			b,s2,X     = self.b, self.mse, self.model.X
			t          = (c @ b)  /   ( np.sqrt( s2 * (c @ np.linalg.inv(X.T @ X) @ c) ) + eps )
			df0        = None
			df         = self.df0
		else:
			V,_        = self._estimate_variance_t( self.model.QQ )
			b,s2,Xi    = self.b, self.mse, self.Xi
			t          = (c @ b)  /   ( np.sqrt( s2 * (c @ Xi @ V @ Xi.T @ c)  + eps ) )
			# self._calculate_effective_df( STAT='T' )
			df0        = self.df0
			df         = self._calculate_effective_df_t(self.model.X, V)
		t        = float(t)  if (self.dvdim==0) else t.flatten()
		return TestStatisticT(t, df, c, df0=df0)
		
		
		
	def isequal(self, other, verbose=False):
		import pytest
		# if type(self) != type(other):
		# 	return False
			
		if self.model != other.model:
			return False
		
		if not self.df == other.df:
			return False

		for s in ['b', 'e', 'Xi', 'sse', 'mse', 'y']: 
			x0,x1  = getattr(self, s), getattr(other, s)
			# if verbose:
			# 	print( f'{s}:  {x0},  {x1}' )
			if s=='sse':
				return self.sse == pytest.approx(other.sse)
			else:
				if not np.all(x0 == x1):
					return False

		return True





