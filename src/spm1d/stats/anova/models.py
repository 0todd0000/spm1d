'''
ANOVA
'''

# Copyright (C) 2023  Todd Pataky



import numpy as np
import scipy.stats
import rft1d
from .. _cov import reml, traceRV, traceMV, _reml_old
from .. _la import rank
from ... util import array2shortstr, arraylist2str, arraytuple2str, dflist2str, objectlist2str, resels2str, scalarlist2string, DisplayParams



class GeneralLinearModel(object):
	def __init__(self):
		self.QQ   = None   # (co-)variance model
		self.X    = None   # design matrix

	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'X' , array2shortstr )
		dp.add( 'QQ' , arraylist2str, 'covariance component models' )
		return dp.asstr()
	
	@property
	def J(self):
		return None if (self.X is None) else self.X.shape[0]

	def fit(self, y):
		y      = np.asarray(y, dtype=float)
		y      = y if (y.ndim==2) else np.array([y]).T
		Xi     = np.linalg.pinv( self.X )
		b      = Xi @ y
		e      = y - self.X @ b
		# self.__class__ = FittedGeneralLinearModel
		# self._set_fit(y, b, e)
		return GLMFit(self, y, b, e)

	def isequal(self, other, verbose=False):
		# if type(self) != type(other):
		# 	return False
			
		if (self.QQ is not None) and (other.QQ is not None):
			for Q0,Q1 in zip(self.QQ, other.QQ):
				if not np.all(Q0 == Q1):
					return False

		if not np.all(self.X == other.X):
			return False

		return True

	def set_design_matrix(self, X):
		self.X       = X
	def set_variance_model(self, QQ):
		self.QQ      = QQ



class TestStatisticF(object):
	def __init__(self, f, df, v, ss, ms, C, ind=0):
		self.STAT  = 'F'
		self.C     = C
		self.ind   = ind
		self.z     = f
		self.df    = df
		self.v     = v
		self.ss    = ss
		self.ms    = ms
		
	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'STAT' )
		dp.add( 'C', array2shortstr )
		dp.add( 'ind' )
		_astr      = array2shortstr if self.dvdim==1 else None
		dp.add( 'z', _astr )
		dp.add( 'df', dflist2str )
		dp.add( 'ms', _astr )
		dp.add( 'ss', _astr )
		return dp.asstr()
		
		
	@property
	def dvdim(self):
		return 0 if isinstance(self.z, float) else 1


	def isequal(self, other, verbose=False):
		import pytest
		# if type(self) != type(other):
		# 	return False
			
		if self.STAT != other.STAT:
			return False
		
		if not self.df == pytest.approx(other.df):
			return False

		for s in ['C', 'z']: 
			x0,x1  = getattr(self, s), getattr(other, s)
			if s == 'z':
				if not self.z == pytest.approx(other.z):
					return False
			else:
				if not np.all(x0 == x1):
					return False

		return True
		
		
class GLMFit(object):


	def __init__(self, model, y, b, e):
		# self._df   = None   # effective degrees of freedom (for one contrast)
		# self._f    = None   # F statistic (for one contrast)
		# self._v    = None   # variance scale (for one contrast); same as df when equal variance is assumed
		self.model  = model
		self.V      = None   # estimated (co-)variance
		self.b      = b      # betas (fitted parameters)
		self.dvdim  = 0 if ((y.ndim==1) or (1 in y.shape)) else 1 # dependent variable dimensionality
		self.e      = e      # residuals
		# self.fwhm   = None   # estimated residual smoothness
		# self.resels = None  # resel counts
		self.h      = None   # (co-)variance hyperparameters
		self.mse    = None   # mean squared error
		self.sse    = None   # sum of error squares
		self.y      = y      # (J,Q) dependent variable array where J=num.observations and Q=num.continuum nodes
		self._estimate_variance()
		self._calculate_sse()
		# if self.dvdim == 1:
		# 	from ... geom import estimate_fwhm, resel_counts
		# 	self.fwhm   = estimate_fwhm( e )
		# 	self.resels = resel_counts(e, self.fwhm, element_based=False, roi=None)

	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def isequal(self, other, verbose=False):
		import pytest
		# print(  f'isequal, verbose={verbose}' )
		# if type(self) != type(other):
		# 	return False
			
		if self.model != other.model:
			return False
		
		# if not self.df == other.df:
		# 	return False

		for s in ['V', 'b', 'e', 'sse', 'y']: 
			x0,x1  = getattr(self, s), getattr(other, s)
			res    = True
			if s=='sse':
				res = self.sse == pytest.approx(other.sse)
			else:
				if not np.all(x0 == x1):
					res = False
			if verbose:
				print( f'{s}:  {res}' )
			if not res:
				return False
			#
			# if not np.all(x0 == x1):
			# 	return False

		return True

		
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

	
	def _calculate_adjusted_df_greenhouse_geisser(self):
		pass
		#
		# # this works for 0D data:
		# if self.dvdim==1:
		# 	y      = self.y.ravel()
		# 	ytable = np.vstack(  [y[self.A==u]  for u in self.uA]  )
		# 	k,n    = ytable.shape
		# 	S      = np.cov(ytable, ddof=1)
		# else:
		# 	S       = np.array([h*q  for h,q in zip(self.h, self.QQ)]).sum(axis=0)  # Eqn.10.14  (Friston, 2007)
		# 	k       = self.uA.size
		# 	n       = self.J / k
		# # # my BAD 1D attempt:
		# # k      = self.uA.size
		# # n      = self.J / k
		# # S      = self.V
		#
		# # # new 1D attempt:
		# # S       = np.array([h*q  for h,q in zip(self.h, self.QQ)]).sum(axis=0)  # Eqn.10.14  (Friston, 2007)
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

	def _calculate_effective_df(self, C, X=None):
		X             = self.model.X if (X is None) else X
		trRV,trRVRV   = traceRV(self.V, X)
		trMV,trMVMV   = traceMV(self.V, self.model.X, C)
		df0           = max(trMV**2 / trMVMV, 1.0)
		df1           = trRV**2 / trRVRV
		df            = df0, df1
		v             = trMV, trRV
		return df,v
		# self._df       = df0, df1
		# self._v       = v0, v1

	def _calculate_sse(self):
		y,X      = self.y, self.model.X
		PX       = X @ np.linalg.pinv(X)      # X projector
		YIPY     = y.T @ ( np.eye( self.J ) - PX ) @ y   # eqn.9.13 denominator (Friston 2007, p.135)
		self.sse = float(YIPY) if (self.dvdim==0) else np.diag(YIPY)



	def _estimate_variance(self):
		# i             = np.any(self.C, axis=1)
		# _X            = self.X[:,i]  # design matrix excluding non-contrast columns
		# _C            = self.C[i]
		# X             = self.model.X
		n,s           = self.y.shape
		# trRV          = n - rank(_X)
		trRV          = n - rank(self.model.X)
		ss            = (self.e**2).sum(axis=0)
		q             = np.diag(  np.sqrt( trRV / ss )  ).T
		Ym            = self.y @ q
		# Ym            = self.e @ q
		YY            = Ym @ Ym.T / s
		V,h           = reml(YY, self.model.X, self.model.QQ)
		# V,h           = reml(YY, self.X, self.QQ)
		V            *= (n / np.trace(V))
		self.h        = h
		self.V        = V


	def calculate_f_stat(self, C, gg=False, _Xeff=None, ind=0):
		# build projectors:
		y,X      = self.y, self.model.X
		# PX      = X @ np.linalg.pinv(X)      # X projector
		H        = np.linalg.pinv( X.T ) @ C  # text between eqns. 9.17 & 9.18 (Friston 2007, p.136)
		PH       = H @ np.linalg.inv(H.T @ H) @ H.T     # H projector
		# estimate df:
		df,v     = self._calculate_effective_df( C, _Xeff )
		v0,v1    = v
		self.mse = self.sse / v1
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


