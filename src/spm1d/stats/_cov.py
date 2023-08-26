'''
Covariance compoonent modeling and estimation

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)


The module supports the modeling and estimation of
covariance components. These "components" represent
separate contributions to the overall inter-observation
variance-covariance.

These covariance models permit corrections mainly for
three key dataset characteristics:
- heteroscedasticity (unequal group variances),
- non-sphericity (within-subject difference variance
inequality) and
- autocorrelation (error correlation between
neighboring observations)

As a simple example:
Two simple covariance models for a two-sample test are:

- Model 1: Constant variance for all observations
- Model 2: Separate variance for groups A and B

Substantially more complex covariance models are
also possible including models of autoregression
(e.g. error correlation between closely neighboring
observations)

Modeled covariance components are estimated using
REML (restricted maximum likelihood). The REML code
is based on the MATLAB routines in "spm_reml.m" as
released with SPM8 at www.fil.ion.ucl.ac.uk/spm/

Specific version details:
    spm_reml.m
    $Id: spm_reml.m 1165 2008-02-22 12:45:16Z guillaume $
    authors: John Ashburner & Karl Friston

Users can access covariance component modeling through
the "equal_var" or "cov_model" keyword arguments that
are available in relevant spm1d.stats procedures. The
"equal_var" keyword argument is a legacy argument from
spm1d v.0.4;  support for it is retained because it may
be more attractive to some users than the new (v.0.5)
and more-complex "cov_model" keyword argument. Through
"cov_model", arbitrary covariance models are supported.
All models are routed through this module's REML estimates.

For more details refer to Chapter 10 "Covariance Components"
from Friston et al. (2007)

References:

Friston, K. J., Penny, W. D., Ashburner, J. T., Kiebel,
S. J., & Nichols, T. E. (Eds.). (2011). Statistical
parametric mapping: the analysis of functional brain
images. Elsevier.
'''

# Copyright (C) 2023  Todd Pataky




# import itertools
# from copy import deepcopy
from math import sqrt,exp,log
import numpy as np
# from . _la import rank
rank = np.linalg.matrix_rank
# eps = np.finfo(float).eps



class CovarianceModel(object):
	def __init__(self, X):
		self.Q         = []
		self.X         = np.asarray( X )
		self.Xi        = np.linalg.pinv( self.X )
		self.J         = self.X.shape[0]
		self.isgroup   = None
		self._init_groupcols()


	def _init_groupcols(self):
		def _isgroup(x):
			return (not np.all(x==1)) and np.all( np.isin(x, [0,1]) )
		self.isgroup  = np.array([_isgroup(x)  for x in self.X.T])

	@property
	def nrow(self):
		return self.X.shape[0]
	@property
	def ncol(self):
		return self.X.shape[1]
	@property
	def ngroups(self):
		return self.isgroup.sum()
	@property
	def ncovcomp(self):
		return len(self.Q)
	
	def add_autocorr(self):
		'''
		Friston et al. (2007) Eq.8.38, p.122  ("Q2" component)
		'''
		J = self.J
		Q = np.zeros( (J,J) )
		for i in range(J):
			for ii in range(J):
				if i!=ii:
					Q[i,ii] = exp( -abs(i-ii) )
		self.Q.append( Q )
		
	def add_constant_var(self):
		'''
		Friston et al. (2007) Eq.8.37, p.122 ("Q1" component)
		'''
		self.Q.append(  np.eye(self.J) )

	def add_group_vars(self):
		Q           = []
		J           = self.X.shape[0]
		Xg          = self.X[:, self.isgroup]
		for x in Xg.T:
			self.Q.append( np.diag(x) )

	def get_model(self):
		return self.Q




class CovarianceEstimator(object):
	def __init__(self, Y, X, e, Q=None):
		self.J  = Y.shape[0]
		self.Y  = Y     # data array
		self.X  = X     # design matrix
		self.e  = e     # residuals
		self.Q  = None  # covariance model
		
	def _reml(self):
		pass

	def estimate(self):
		J = self.J
		if self.Q is None:
			V = np.eye( J )
			df = J - rank(self.X)
		else:
			V,_         = self._reml()
			trRV,trRVRV = traceRV(V, X)
			df          = trRV**2 / trRVRV
			
		return V,df


def _spm_en(a):  # Euclidean normalization following spm_en.m in SPM8
	return a / np.linalg.norm(a, axis=0)

def _spm_svd(X, u=1e-6, t=0):  # SVD following spm_svd.m in SPM8
	import scipy.linalg
	v,s,_ = scipy.linalg.svd( X.T @ X , full_matrices=False, lapack_driver='gesvd')
	i     = np.logical_and(   ( s / s.mean() ) >= u  ,  s >= u   )
	v     = v[:,i]
	u     = _spm_en( X @ v )  
	return u


def reml(YY, X, Q, N=1, K=128):   # updated 2023-06-19
	from copy import deepcopy
	from math import sqrt,exp,log
	n     = X.shape[0]
	W     = deepcopy(Q)
	
	q     = np.asarray(np.all(YY<np.inf, axis=0)).flatten()
	Q     = [QQ[q,:][:,q]   for QQ in Q]

	m     = len(Q)
	# h     = np.matrix([float(np.any(np.diag(QQ)))  for QQ in Q]).T
	h     = np.array(   [float(np.any(np.diag(QQ)))  for QQ in Q]   )
	
	X0    = _spm_svd( X )
	
	# print( np.around(YY,4)[:,:5] )
	
	# # print( m, n, q )
	#
	# # X0     = np.linalg.qr(X, mode='reduced')[0]
	# # print(X0.shape)
	# X0,_,_ = scipy.linalg.svd(model.X, full_matrices=False, lapack_driver='gesvd')
	# # print( np.around(X0, 3) )
	#     # * 'reduced'  : returns q, r with dimensions
	#     #                (..., M, K), (..., K, N) (default)
	#     # * 'complete' : returns q, r with dimensions (..., M, M), (..., M, N)
	#     # * 'r'        : returns r only with dimensions (..., K, N)
	#     # * 'raw'      : returns h, tau with dimensions (..., N, M), (..., K,)
	# # X0    = np.linalg.svd(X)
	dFdhh = np.zeros( (m,m) )
	
	# print( np.around(YY[:,:5], 4) )
	# print(YY.shape)
	

	hE   = np.zeros( m )
	hP   = np.eye(m) / exp(32)

	dF  = np.inf
	for k in range(K):
		C    = np.zeros( (n,n) )
		for i in range(m):
			C   += Q[i] * float(h[i])
		iC   = np.linalg.inv(C) + np.eye(n)/exp(32)
		iCX  = iC @ X0
		Cq   = np.linalg.inv( X0.T @ iCX )
		
		

		# Gradient dF/dh (first derivatives)
		P    = iC - iCX@Cq@iCX.T
		U    = np.eye(n) - P@YY/N


		PQ   = [P@QQ for QQ in Q]
		dFdh = np.array([-np.trace(PQQ@U)*0.5*N   for PQQ in PQ]).T
		
		# print( np.around(dFdh, 4) )
		# # print( np.around(dFdh, 4)[:,:5] )
		# print()
		

		# Expected curvature E{dF/dhh} (second derivatives)
		for i in range(m):
			for j in range(m):
		            dFdhh[i,j] = -np.trace(PQ[i]@PQ[j])*0.5*N
		            dFdhh[j,i] =  dFdhh[i,j]

		# # print( np.around(dFdh, 4) )
		# print( np.around(dFdhh, 4)[:,:] )
		# print()
		# # break


		#add hyper-priors
		e     = h - hE
		# print( e**0.5 )
		# print( hP @ e )
		dFdh -= hP@e
		dFdhh -= hP

		# print( np.around(e, 4) )
		# print( np.around(dFdh, 4) )
		# print( np.around(dFdhh, 4) )
		# print()
		# # break


		# Fisher scoring
		def _spm_dx(dfdx, f, t):
			import scipy.linalg
			t   = np.diag(   np.exp(t - np.log(np.diagonal(-dfdx)) )   )
			a   = np.vstack( [t@f,  (t @ dfdx).T] ).T
			a   = np.vstack(  [np.zeros((1,a.shape[1])), a]  )
			dx  = scipy.linalg.expm( a )
			dx  = dx[1:, 0]
			return dx
			
		dh  = _spm_dx(dFdhh, dFdh, 4)
		h   = h + dh
		dF    = float( dFdh.T @ dh )
		# # print( np.around( h ,4) )
		
		# print( dF )
		# # print(dh)
		# print()
		# # return np.eye(X.shape[0]), np.zeros(X.shape[0])
		# # break
		
		
		#
		#final covariance estimate (with missing data points)
		if dF < 0.1:
			V     = 0
			for i in range(m):
				V += Q[i]*float(h[i])
			return V, h
		
		
		
		
		# import scipy.linalg
		# dfdx,f,t  = dFdhh, dFdh, 4
		# t         = np.diag(   np.exp(t - np.log(np.diagonal(-dfdx)) )   )
		# #
		# # print( np.around( t@f ,4) )
		# # print( np.around( t@dfdx ,4) )
		# a   = np.vstack( [t@f,  (t @ dfdx).T] ).T
		# a   = np.vstack(  [np.zeros((1,a.shape[1])), a]  )
		# dx  = scipy.linalg.expm( a )
		# dx  = dx[1:, 0]
		# # print( np.around( dx ,4) )
		# # print()
		
		
		# dh    = -np.linalg.inv(dFdhh)@dFdh / log(k+3)
		# h    += dh
		# dF    = float(dFdh.T@dh)
		#
		# # print(dh)
		#
		# #final covariance estimate (with missing data points)
		# if dF < 0.1:
		# 	V     = 0
		# 	for i in range(m):
		# 		V += Q[i]*float(h[i])
		# 	return V, h
		#


def _reml_old(YY, X, Q, N=1, K=128):   # superceded by new version on 2023-06-19
	'''
	superceded by new version on 2023-06-19

	Primary difference:
	- dh estimate useing _spm_dx  in the new version
	'''
	from copy import deepcopy
	n     = X.shape[0]
	W     = deepcopy(Q)

	q     = np.asarray(np.all(YY<np.inf, axis=0)).flatten()
	Q     = [QQ[q,:][:,q]   for QQ in Q]

	m     = len(Q)
	# h     = np.matrix([float(np.any(np.diag(QQ)))  for QQ in Q]).T
	h     = np.array(   [float(np.any(np.diag(QQ)))  for QQ in Q]   )

	# print( h )

	X0    = np.linalg.qr(X)[0]
	dFdhh = np.zeros( (m,m) )

	hE   = np.zeros( m )
	hP   = np.eye(m) / exp(32)

	dF  = np.inf
	for k in range(K):
		C    = np.zeros( (n,n) )
		for i in range(m):
			C   += Q[i] * float(h[i])
		iC   = np.linalg.inv(C) + np.eye(n)/exp(32)
		iCX  = iC @ X0
		Cq   = np.linalg.inv( X0.T @ iCX )

		# Gradient dF/dh (first derivatives)
		P    = iC - iCX@Cq@iCX.T
		U    = np.eye(n) - P@YY/N

		PQ   = [P@QQ for QQ in Q]
		dFdh = np.array([-np.trace(PQQ@U)*0.5*N   for PQQ in PQ]).T

		# Expected curvature E{dF/dhh} (second derivatives)
		for i in range(m):
			for j in range(m):
		            dFdhh[i,j] = -np.trace(PQ[i]@PQ[j])*0.5*N
		            dFdhh[j,i] =  dFdhh[i,j]

		#add hyper-priors
		e     = h - hE
		# print( e )
		# print( hP @ e )
		dFdh -= hP@e
		dFdhh -= hP

		# Fisher scoring
		dh    = -np.linalg.inv(dFdhh)@dFdh / log(k+3)
		h    += dh
		dF    = float(dFdh.T@dh)

		#final covariance estimate (with missing data points)
		if dF < 0.1:
			V     = 0
			for i in range(m):
				V += Q[i]*float(h[i])
			return V, h




# def reml(YY, X, Q, N=1, K=128):
# 	'''
# 	Previous implementation that uses np.matrix
#
# 	Kept as a reference
# 	'''
# 	from copy import deepcopy
# 	n     = X.shape[0]
# 	W     = deepcopy(Q)
#
# 	q     = np.asarray(np.all(YY<np.inf, axis=0)).flatten()
# 	Q     = [QQ[q,:][:,q]   for QQ in Q]
#
# 	m     = len(Q)
# 	h     = np.matrix([float(np.any(np.diag(QQ)))  for QQ in Q]).T
# 	X0    = np.linalg.qr(X)[0]
# 	dFdhh = np.zeros((m,m))
#
# 	hE   = np.matrix(np.zeros((m,1)))
# 	hP   = np.eye(m)/exp(32)
#
# 	dF  = np.inf
# 	for k in range(K):
# 		C    = np.matrix(np.zeros((n,n)))
# 		for i in range(m):
# 			C   += Q[i] * float(h[i])
# 		iC   = np.linalg.inv(C) + np.eye(n)/exp(32)
# 		iCX  = iC*X0
# 		Cq   = np.linalg.inv(X0.T*iCX)
#
# 		# Gradient dF/dh (first derivatives)
# 		P    = iC - iCX*Cq*iCX.T
# 		U    = np.eye(n) - P*YY/N
#
# 		PQ   = [P*QQ for QQ in Q]
# 		dFdh = np.matrix([-np.trace(PQQ*U)*0.5*N   for PQQ in PQ]).T
#
# 		# Expected curvature E{dF/dhh} (second derivatives)
# 		for i in range(m):
# 			for j in range(m):
# 		            dFdhh[i,j] = -np.trace(PQ[i]*PQ[j])*0.5*N
# 		            dFdhh[j,i] =  dFdhh[i,j]
#
# 		#add hyper-priors
# 		e     = h - hE
# 		dFdh -= hP*e
# 		dFdhh -= hP
#
# 		# Fisher scoring
# 		dh    = -np.linalg.inv(dFdhh)*dFdh / log(k+3)
# 		h    += dh
# 		dF    = float(dFdh.T*dh)
#
# 		#final covariance estimate (with missing data points)
# 		if dF < 0.1:
# 			V     = 0
# 			for i in range(m):
# 				V += Q[i]*float(h[i])
# 			return V, h
#



# def traceMV(V, X, c):
# 	c           = np.matrix(c)
# 	rankX       = rank(X)
# 	u,ds,v      = np.linalg.svd(X)
# 	u           = np.matrix(u[:,:rankX])
# 	ukX1o       = (np.matrix(np.diag(1/ds)) * np.matrix(v).T)*c
# 	ukX1o       = ukX1o[:rankX]
# 	X1o         = u * ukX1o
# 	###
# 	rnk1        = rank(X1o)
# 	u1,ds1,v1   = np.linalg.svd(X1o)
# 	u1          = np.matrix(u1[:,:rnk1])
# 	Vu          = V @ u1
# 	trMV        = (np.asarray(u1)*np.asarray(Vu)).sum()
# 	# trMVMV      = np.linalg.norm(u1.T*Vu,  ord='fro')**2
# 	trMVMV      = np.linalg.norm(u1.T@Vu,  ord='fro')**2
# 	return trMV, trMVMV


def traceMV(V, X, c):
	rankX       = rank(X)
	u,ds,v      = np.linalg.svd(X)
	u           = u[:,:rankX]
	ukX1o       = (np.diag(1/ds) @ v.T) @ c
	ukX1o       = ukX1o[:rankX]
	X1o         = u @ ukX1o
	rnk1        = rank(X1o)
	u1,ds1,v1   = np.linalg.svd(X1o)
	u1          = u1[:,:rnk1]
	Vu          = V @ u1
	trMV        = (u1 * Vu).sum()
	trMVMV      = np.linalg.norm(u1.T@Vu,  ord='fro')**2
	return trMV, trMVMV

def traceRV(V, X):
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
	
	


# # def _rank(A, tol=None):
# # 	'''
# # 	This is a slight modification of np.linalg.matrix_rank.
# # 	The tolerance performs poorly for some matrices
# # 	Here the tolerance is boosted by a factor of ten for improved performance.
# # 	'''
# # 	M = np.asarray(A)
# # 	S = np.linalg.svd(M, compute_uv=False)
# # 	if tol is None:
# # 		tol = 10 * S.max() * max(M.shape) * np.finfo(M.dtype).eps
# # 	rank = sum(S > tol)
# # 	return rank
#
#
#
# def estimate_df_T(Y, X, eij, Q):
# 	Y           = np.matrix(Y).T if (Y.ndim==1) else np.matrix(Y)
# 	X           = np.matrix(X)
# 	eij         = np.matrix(eij).T if (eij.ndim==1) else np.matrix(eij)
# 	n,s         = Y.shape
# 	### ReML estimates:
# 	trRV        = n - _rank(X)
# 	ResSS       = (np.asarray(eij)**2).sum(axis=0)
# 	q           = np.diag(np.sqrt( trRV / ResSS )).T
# 	Ym          = Y*q
# 	YY          = Ym*Ym.T / s
# 	V,h         = reml(YY, X, Q)
# 	V           = V * (n / np.trace(V))
# 	### effective degrees of freedom:
# 	trRV,trRVRV = traceRV(V, X)
# 	df          = trRV**2 / trRVRV
# 	return df
#
#
# # def estimate_df_T(Y, X, eij, Q):
# # 	n,s         = Y.shape if (Y.ndim==2) else (Y.size,1)
# # 	### ReML estimates:
# # 	trRV        = n - _rank(X)
# # 	ResSS       = (np.asarray(eij)**2).sum(axis=0)
# # 	q           = np.diag(np.sqrt( trRV / ResSS )).T
# # 	Ym          = Y*q
# # 	YY          = Ym*Ym.T / s
# # 	V,h         = reml(YY, X, Q)
# # 	V           = V * (n / np.trace(V))
# # 	### effective degrees of freedom:
# # 	trRV,trRVRV = traceRV(V, X)
# # 	df          = trRV**2 / trRVRV
# # 	return df
#
#
#
# # def estimate_df_anova1(Y, X, eij):
# # 	n,s           = Y.shape                                #numbers ofresponses and nodes
# # 	nnLevels      = np.asarray(X, dtype=int).sum(axis=0)   #number of responses in each level
# # 	rankX         = _rank(X)
# # 	### create contrast matrix:
# # 	c             = np.matrix(np.zeros((rankX, rankX*(rankX-1) )))
# # 	for col,(i0,i1) in enumerate(itertools.combinations(range(rankX),2)):
# # 		c[i0,col] = 1
# # 		c[i1,col] = -1
# # 	c[:,col+1:]   = -c[:,:col+1]
# # 	### create non-sphericity components matrix:
# # 	Q,i0          = [], 0
# # 	for nn in nnLevels:
# # 		QQ        = np.zeros((n,n))
# # 		QQ[i0:i0+nn,i0:i0+nn]  =  np.eye(nn)
# # 		i0       += nn
# # 		Q.append( np.matrix(QQ) )
# # 	### ReML estimates:
# # 	trRV          = n - rankX
# # 	ResSS         = (np.asarray(eij)**2).sum(axis=0)
# # 	q             = np.diag(np.sqrt( trRV / ResSS )).T
# # 	Ym            = Y*q
# # 	YY            = Ym*Ym.T / s
# # 	V,h           = reml(YY, X, Q)
# # 	V            *= (n / np.trace(V))
# # 	### effective degrees of freedom (denominator):
# # 	trRV,trRVRV   = traceRV(V, X)
# # 	df2           = trRV**2 / trRVRV
# # 	### effective degrees of freedom (numerator):
# # 	trMV,trMVMV   = traceMV(V, X, c)
# # 	df1           =  trMV**2 / trMVMV
# # 	df1           = max(df1,1.0)
# # 	return df1, df2
#
#
# # def estimate_df_anova2(Y, A, B, X, eij, C):
# # 	J,s       = Y.shape
# # 	rankX     = _rank(X)
# # 	### construct non-sphericity components:
# # 	uA,uB     = np.unique(A), np.unique(B)
# # 	nA,nB     = uA.size, uB.size
# # 	Q         = []
# # 	for u in uA:
# # 		Q.append( np.diag((A==u) +0) )
# # 	for u in uB:
# # 		Q.append( np.diag((B==u) +0) )
# # 	### ReML estimates:
# # 	trRV      = J - rankX
# # 	ResSS     = (np.asarray(eij)**2).sum(axis=0)
# # 	q         = np.diag(np.sqrt( trRV / ResSS )).T
# # 	Ym        = Y*q
# # 	YY        = Ym*Ym.T / s
# # 	V,h       = reml(YY, X, Q)
# # 	V        *= (J / np.trace(V))
# # 	### effective degrees of freedom (denominator):
# # 	trRV,trRVRV = traceRV(V, X)
# # 	df2         = trRV**2 / trRVRV
# # 	### effective degrees of freedom (numerator):
# # 	df1         = []
# # 	for CC in C:
# # 		trMV,trMVMV = traceMV(V, X, CC.T)
# # 		df1.append( trMV**2 / trMVMV )
# # 	df1       = [max(x,1.0)  for x in df1]
# # 	return df1, df2
#
#
#
# def estimate_df_anova1(Y, X, eij, Q, c):
# 	n,s           = Y.shape                                #numbers ofresponses and nodes
# 	rankX         = _rank(X)
# 	### ReML estimates:
# 	trRV          = n - rankX
# 	ResSS         = (np.asarray(eij)**2).sum(axis=0)
# 	q             = np.diag(np.sqrt( trRV / ResSS )).T
# 	Ym            = Y*q
# 	YY            = Ym*Ym.T / s
# 	V,h           = reml(YY, X, Q)
# 	V            *= (n / np.trace(V))
# 	### effective degrees of freedom (denominator):
# 	trRV,trRVRV   = traceRV(V, X)
# 	df2           = trRV**2 / trRVRV
# 	### effective degrees of freedom (numerator):
# 	trMV,trMVMV   = traceMV(V, X, c)
# 	df1           =  trMV**2 / trMVMV
# 	df1           = max(df1,1.0)
# 	return df1, df2
# 	# df1,df2 = 2,2
#
#
# def estimate_df_anova2(Y, X, eij, Q, C):
# 	J,s       = Y.shape
# 	rankX     = _rank(X)
# 	### ReML estimates:
# 	trRV      = J - rankX
# 	ResSS     = (np.asarray(eij)**2).sum(axis=0)
# 	q         = np.diag(np.sqrt( trRV / ResSS )).T
# 	Ym        = Y*q
# 	YY        = Ym*Ym.T / s
# 	V,h       = reml(YY, X, Q)
# 	V        *= (J / np.trace(V))
# 	### effective degrees of freedom (denominator):
# 	trRV,trRVRV = traceRV(V, X)
# 	df2         = trRV**2 / trRVRV
# 	### effective degrees of freedom (numerator):
# 	df1         = []
# 	for CC in C:
# 		trMV,trMVMV = traceMV(V, X, CC)
# 		df1.append( trMV**2 / trMVMV )
# 	df1       = [max(x,1.0)  for x in df1]
# 	return df1, df2
#
#
# def reml(YY, X, Q, N=1, K=128):
# 	n     = X.shape[0]
# 	W     = deepcopy(Q)
#
# 	q     = np.asarray(np.all(YY<np.inf, axis=0)).flatten()
# 	Q     = [QQ[q,:][:,q]   for QQ in Q]
#
# 	m     = len(Q)
# 	h     = np.matrix([float(np.any(np.diag(QQ)))  for QQ in Q]).T
# 	X0    = np.linalg.qr(X)[0]
# 	dFdhh = np.zeros((m,m))
#
# 	hE   = np.matrix(np.zeros((m,1)))
# 	hP   = np.eye(m)/exp(32)
#
# 	dF  = np.inf
# 	for k in range(K):
# 		C    = np.matrix(np.zeros((n,n)))
# 		for i in range(m):
# 			C   += Q[i] * float(h[i])
# 		iC   = np.linalg.inv(C) + np.eye(n)/exp(32)
# 		iCX  = iC*X0
# 		Cq   = np.linalg.inv(X0.T*iCX)
#
# 		# Gradient dF/dh (first derivatives)
# 		P    = iC - iCX*Cq*iCX.T
# 		U    = np.eye(n) - P*YY/N
#
# 		PQ   = [P*QQ for QQ in Q]
# 		dFdh = np.matrix([-np.trace(PQQ*U)*0.5*N   for PQQ in PQ]).T
#
# 		# Expected curvature E{dF/dhh} (second derivatives)
# 		for i in range(m):
# 			for j in range(m):
# 		            dFdhh[i,j] = -np.trace(PQ[i]*PQ[j])*0.5*N
# 		            dFdhh[j,i] =  dFdhh[i,j]
#
# 		#add hyper-priors
# 		e     = h - hE
# 		dFdh -= hP*e
# 		dFdhh -= hP
#
# 		# Fisher scoring
# 		dh    = -np.linalg.inv(dFdhh)*dFdh / log(k+3)
# 		h    += dh
# 		dF    = float(dFdh.T*dh)
#
# 		#final covariance estimate (with missing data points)
# 		if dF < 0.1:
# 			V     = 0
# 			for i in range(m):
# 				V += Q[i]*float(h[i])
# 			return V, h
#
#
#
#
#
#
#
#

#
