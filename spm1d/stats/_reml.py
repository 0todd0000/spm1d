'''
Restricted maximum likelihood estimates

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)


The module contains functions which correct for non-sphericity.

The code is based on the Matlab routines in "spm_reml.m" as
released with SPM8 at www.fil.ion.ucl.ac.uk/spm/.

Specific version details:
    spm_reml.m
    $Id: spm_reml.m 1165 2008-02-22 12:45:16Z guillaume $
    authors: John Ashburner & Karl Friston
'''

# Copyright (C) 2016  Todd Pataky




import itertools
from copy import deepcopy
from math import sqrt,exp,log
import numpy as np



eps         = np.finfo(float).eps


def _rank(A, tol=None):
	'''
	This is a slight modification of np.linalg.matrix_rank.
	The tolerance performs poorly for some matrices
	Here the tolerance is boosted by a factor of ten for improved performance.
	'''
	M = np.asarray(A)
	S = np.linalg.svd(M, compute_uv=False)
	if tol is None:
		tol = 10 * S.max() * max(M.shape) * np.finfo(M.dtype).eps
	rank = sum(S > tol)
	return rank



def estimate_df_T(Y, X, eij, Q):
	n,s         = Y.shape
	### ReML estimates:
	trRV        = n - _rank(X)
	ResSS       = (np.asarray(eij)**2).sum(axis=0)
	q           = np.diag(np.sqrt( trRV / ResSS )).T
	Ym          = Y*q
	YY          = Ym*Ym.T / s
	V,h         = reml(YY, X, Q)
	V           = V * (n / np.trace(V))
	### effective degrees of freedom:
	trRV,trRVRV = traceRV(V, X)
	df          = trRV**2 / trRVRV
	return df



# def estimate_df_anova1(Y, X, eij):
# 	n,s           = Y.shape                                #numbers ofresponses and nodes
# 	nnLevels      = np.asarray(X, dtype=int).sum(axis=0)   #number of responses in each level
# 	rankX         = _rank(X)
# 	### create contrast matrix:
# 	c             = np.matrix(np.zeros((rankX, rankX*(rankX-1) )))
# 	for col,(i0,i1) in enumerate(itertools.combinations(range(rankX),2)):
# 		c[i0,col] = 1
# 		c[i1,col] = -1
# 	c[:,col+1:]   = -c[:,:col+1]
# 	### create non-sphericity components matrix:
# 	Q,i0          = [], 0
# 	for nn in nnLevels:
# 		QQ        = np.zeros((n,n))
# 		QQ[i0:i0+nn,i0:i0+nn]  =  np.eye(nn)
# 		i0       += nn
# 		Q.append( np.matrix(QQ) )
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


# def estimate_df_anova2(Y, A, B, X, eij, C):
# 	J,s       = Y.shape
# 	rankX     = _rank(X)
# 	### construct non-sphericity components:
# 	uA,uB     = np.unique(A), np.unique(B)
# 	nA,nB     = uA.size, uB.size
# 	Q         = []
# 	for u in uA:
# 		Q.append( np.diag((A==u) +0) )
# 	for u in uB:
# 		Q.append( np.diag((B==u) +0) )
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
# 		trMV,trMVMV = traceMV(V, X, CC.T)
# 		df1.append( trMV**2 / trMVMV )
# 	df1       = [max(x,1.0)  for x in df1]
# 	return df1, df2



def estimate_df_anova1(Y, X, eij, Q, c):
	n,s           = Y.shape                                #numbers ofresponses and nodes
	rankX         = _rank(X)
	### ReML estimates:
	trRV          = n - rankX
	ResSS         = (np.asarray(eij)**2).sum(axis=0)
	q             = np.diag(np.sqrt( trRV / ResSS )).T
	Ym            = Y*q
	YY            = Ym*Ym.T / s
	V,h           = reml(YY, X, Q)
	V            *= (n / np.trace(V))
	### effective degrees of freedom (denominator):
	trRV,trRVRV   = traceRV(V, X)
	df2           = trRV**2 / trRVRV
	### effective degrees of freedom (numerator):
	trMV,trMVMV   = traceMV(V, X, c)
	df1           =  trMV**2 / trMVMV
	df1           = max(df1,1.0)
	return df1, df2
	# df1,df2 = 2,2


def estimate_df_anova2(Y, X, eij, Q, C):
	J,s       = Y.shape
	rankX     = _rank(X)
	### ReML estimates:
	trRV      = J - rankX
	ResSS     = (np.asarray(eij)**2).sum(axis=0)
	q         = np.diag(np.sqrt( trRV / ResSS )).T
	Ym        = Y*q
	YY        = Ym*Ym.T / s
	V,h       = reml(YY, X, Q)
	V        *= (J / np.trace(V))
	### effective degrees of freedom (denominator):
	trRV,trRVRV = traceRV(V, X)
	df2         = trRV**2 / trRVRV
	### effective degrees of freedom (numerator):
	df1         = []
	for CC in C:
		trMV,trMVMV = traceMV(V, X, CC)
		df1.append( trMV**2 / trMVMV )
	df1       = [max(x,1.0)  for x in df1]
	return df1, df2


def reml(YY, X, Q, N=1, K=128):
	n     = X.shape[0]
	W     = deepcopy(Q)
	
	q     = np.asarray(np.all(YY<np.inf, axis=0)).flatten()
	Q     = [QQ[q,:][:,q]   for QQ in Q]

	m     = len(Q)
	h     = np.matrix([float(np.any(np.diag(QQ)))  for QQ in Q]).T
	X0    = np.linalg.qr(X)[0]
	dFdhh = np.zeros((m,m))

	hE   = np.matrix(np.zeros((m,1)))
	hP   = np.eye(m)/exp(32)

	dF  = np.inf
	for k in range(K):
		C    = np.matrix(np.zeros((n,n)))
		for i in range(m):
			C   += Q[i] * float(h[i])
		iC   = np.linalg.inv(C) + np.eye(n)/exp(32)
		iCX  = iC*X0
		Cq   = np.linalg.inv(X0.T*iCX)
	
		# Gradient dF/dh (first derivatives)
		P    = iC - iCX*Cq*iCX.T
		U    = np.eye(n) - P*YY/N
	
		PQ   = [P*QQ for QQ in Q]
		dFdh = np.matrix([-np.trace(PQQ*U)*0.5*N   for PQQ in PQ]).T
		
		# Expected curvature E{dF/dhh} (second derivatives)
		for i in range(m):
			for j in range(m):
		            dFdhh[i,j] = -np.trace(PQ[i]*PQ[j])*0.5*N
		            dFdhh[j,i] =  dFdhh[i,j]

		#add hyper-priors
		e     = h - hE
		dFdh -= hP*e
		dFdhh -= hP
		
		# Fisher scoring
		dh    = -np.linalg.inv(dFdhh)*dFdh / log(k+3)
		h    += dh
		dF    = float(dFdh.T*dh)
		
		#final covariance estimate (with missing data points)
		if dF < 0.1:
			V     = 0
			for i in range(m):
				V += Q[i]*float(h[i])
			return V, h





	

	


def traceMV(V, X, c):
	rankX       = _rank(X)
	u,ds,v      = np.linalg.svd(X)
	u           = np.matrix(u[:,:rankX])
	ukX1o       = (np.matrix(np.diag(1/ds)) * np.matrix(v).T)*c
	ukX1o       = ukX1o[:rankX]
	X1o         = u * ukX1o
	###
	rnk1        = _rank(X1o)
	u1,ds1,v1   = np.linalg.svd(X1o)
	u1          = np.matrix(u1[:,:rnk1])
	Vu          = V*u1
	trMV        = (np.asarray(u1)*np.asarray(Vu)).sum()
	trMVMV      = np.linalg.norm(u1.T*Vu,  ord='fro')**2
	return trMV, trMVMV

def traceRV(V, X):
	# rk   = _rank(X);
	rk   = np.linalg.matrix_rank(X)
	sL   = X.shape[0]
	u    = np.linalg.qr(X)[0]

	Vu      = V*u
	trV     = np.trace(V)
	trRVRV  = np.linalg.norm(V,  ord='fro')**2
	trRVRV -= 2*np.linalg.norm(Vu, ord='fro')**2
	trRVRV += np.linalg.norm(u.T*Vu, ord='fro')**2
	trMV    = np.sum(np.array(u)*np.array(Vu))
	trRV    = trV - trMV
	return trRV, trRVRV