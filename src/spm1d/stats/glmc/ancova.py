

import numpy as np



def _spm_en(a):  # Euclidean normalization following spm_en.m in SPM8
	return a / np.linalg.norm(a, axis=0)

def _spm_svd(X, u=1e-6, t=0):  # SVD following spm_svd.m in SPM8;  slightly different results than scipy.linalg.svd
	import scipy.linalg
	v,s,_ = scipy.linalg.svd( X.T @ X , full_matrices=False, lapack_driver='gesvd')
	i     = np.logical_and(   ( s / s.mean() ) >= u  ,  s >= u   )
	v     = v[:,i]
	u     = _spm_en( X @ v )
	return v, np.diag(s**0.5), u




class MatrixWithProjections(object):  # following spm_sp:  Orthogonal (design) matrix space setting & manipulation
	def __init__(self, X):
		self.X   = X
		self.u   = None
		self.ds  = None
		self.v   = None
		self.tol = None
		self._svd()
		self.tol = max( X.shape ) * max(np.abs(self.ds)) * np.finfo(float).eps
		self.rk  = (self.ds > self.tol).sum()
		
	@property
	def m(self):
		return self.X.shape[0]
	@property
	def n(self):
		return self.X.shape[1]
		
	def _svd(self):
		from scipy.linalg import svd
		X  = self.X
		if X.shape[0] < X.shape[1]:
			v,s,u = svd(X.T, full_matrices=False, lapack_driver='gesvd')
		else:
			u,s,v = svd(X, full_matrices=False)
		self.u   = u
		self.ds  = s
		self.v   = v.T

class SpaceTested(object):
	def __init__(self, desmat, c):
		# self.ukX1o = None   # Coordinates of pinv(X') in the base of uk
		# see SPM8.spm_FcUtil('c) and SPM8..spm_SpUtil('+c->Tsp')
		r = desmat.rk
		if r > 0:
			x = np.diag(np.ones(r) / desmat.ds[:r]) @ desmat.v[:,:r].T
		else:
			n = desmat.X.shape[1]
			x = np.zeros( (n, n) )
		u = x @ c
		u[ np.abs(u) < desmat.tol ] = 0
		self.u = u
		# self.X = sf_uk(desmat) @ u
		
	@property
	def ukX1o(self):
		return self.u


class SpaceUntested(object):
	def __init__(self, desmat, c):
		cm      = MatrixWithProjections(c)
		self.u  = sf_cukx(desmat) @ sf_r( cm )
	@property
	def ukX0(self):
		return self.u


class FContrast(object):
	def __init__(self, desmat, c):
		self.c   = c
		self.X0  = SpaceUntested( desmat, c )
		self.X1o = SpaceTested( desmat, c )
		# self.h   = hsqr(self, desmat)
		# _X1o = sf_uk(desmat) @ self.X1o.ukX1o
		#
		# print(_X1o)
		




def hsqr(xCon, xX):   # Extra sum of squares matrix for beta's from contrast
	a    = MatrixWithProjections( xCon.X1o.ukX1o )
	return sf_uk(a).T @ sf_cukx(xX)
	
	

def sf_cukx(sX):  # coordinates of sX.X in the basis sX.u(:,1:rk)
	r = sX.rk
	if r > 0:
		x = np.diag( sX.ds[:r]  ) @ sX.v[:r].T
	else:
		x = np.zeros( (sX.n,sX.n) )
	return x
	


def sf_r(sX):
	I = np.eye( sX.m )
	return I - sf_op(sX)

def sf_op(sX):
	r = sX.rk
	if r > 0:
		u  = sX.u[:,:r]
		op = u @ u.T
	else:
		op = np.zeros( (sX.m,sX.m) )
	return op
	

def sf_uk(sX):
	return sX.u[:,:sX.rk]

def traceMV(V, X):  # a bit different from traceMV in _cov.py
	sX     = MatrixWithProjections( X )
	rk     = sX.rk
	u      = sX.u[:,:rk]
	Vu     = V @ u
	trMV   = (u.T * ( u.T @ V )).sum()
	trMVMV = np.linalg.norm( u.T @ Vu , ord='fro')**2
	return trMV, trMVMV

def traceRV(V, X):
	rank = np.linalg.matrix_rank
	rk      = rank(X)
	sL      = X.shape[0]
	u       = np.linalg.qr(X)[0]
	Vu      = V @ u
	trV     = np.trace(V)
	trRVRV  = np.linalg.norm(V,  ord='fro')**2
	trRVRV -= 2*np.linalg.norm(Vu, ord='fro')**2
	trRVRV += np.linalg.norm(u.T @ Vu, ord='fro')**2
	trMV    = np.sum(  u * Vu  )  # element-wise multiplication (see spm8/spm_SpUtil.m, Line 550)
	trRV    = trV - trMV
	return trRV, trRVRV

def glmc_ancova_V(y, X, c, V):  # follows SPM8.. spm_ancova.m
	J           = y.shape[0]
	pX          = np.linalg.pinv(X)
	beta        = pX @ y
	# res         = fit.e
	# ResSS       = fit.sse
	res         = y - X @ beta 
	ResSS       = (res**2).sum()
	xX          = MatrixWithProjections(X)
	xCon        = FContrast( xX, c )
	h           = hsqr(xCon, xX)  # now calcualted in FContrast object
	X1o         = sf_uk(xX) @ xCon.X1o.ukX1o
	Vn          = V * V.shape[0] / np.trace(V)
	trRV,trRVRV = traceRV(Vn, xX.X)
	trMV,trMVMV = traceMV(Vn, X1o)
	# trMV,trMVMV = here_traceMV(Vn, xCon.X1o.X)
	df          = trMV**2 / trMVMV, trRV**2 / trRVRV
	F           = ((h @ beta)**2).sum(axis=0) / (ResSS * trMV/trRV)
	return F,df,beta,xX,xCon



def glmc_ancova(y, X, c, QQ=None):
	if QQ is None:
		V      = np.eye( X.shape[0] )
	else:
		from . models import GeneralLinearModel
		from . designs import unadjusted_df
		df0    = unadjusted_df(X, c)
		model  = GeneralLinearModel(X, df0, QQ)
		fit    = model.fit(y)
		V,h    = fit._estimate_var(QQ)
	return glmc_ancova_V(y, X, c, V)


