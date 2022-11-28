'''
ANOVA computational core using an R-like linear model interface.
'''

# Copyright (C) 2016  Todd Pataky



import numpy as np
from ... import rft1d


eps         = np.finfo(float).eps


class LinearModel(object):
	def __init__(self, Y, X, roi=None):
		Y               = np.asarray(Y, dtype=float)
		self.dim        = Y.ndim - 1            #dependent variable dimensionality (0 or 1)
		self.Y          = self._asmatrix(Y)     #stacked dependent variable (JxQ)
		self.X          = np.matrix(X)          #design matrix
		self.J          = self.X.shape[0]       #number of observations
		self.Q          = self.Y.shape[1]       #number of field nodes
		self.QT         = None                  #QR decomposition of design matrix
		self.eij        = None                  #residuals
		self.roi        = roi                   #regions of interest
		# self.contrasts  = contrasts             #list of contrast objects
		self._R         = None                  #residual forming matrix
		self._beta      = None                  #least-squares parameters
		self._rankR     = None                  #error degrees of freedom
		self._dfE       = None                  #error degrees of freedom (equivalent to _rankR)
		self._SSE       = None                  #sum-of-squares (error)
		self._MSE       = None                  #mean-squared error
		if self.dim==1:
			self.eij    = None
			self.fwhm   = None
			self.resels = None
		### labels:
		self.term_labels = None
		self.Fterms      = None

	def _asmatrix(self, Y):
		return np.matrix(Y).T if Y.ndim==1 else np.matrix(Y)

	def _rank(self, A, tol=None):
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

	def fit(self, approx_residuals=None):
		Y,X,J           = self.Y, self.X, self.J
		Xi              = np.linalg.pinv(X)         #design matrix pseudoinverse
		self._beta      = Xi*Y                      #estimated parameters
		self._R         = np.eye(J) - X*Xi          #residual forming matrix
		self._rankR     = self._rank(self._R)
		self._SSE       = np.diag( Y.T * self._R * Y )
		self._dfE       = self._rankR
		if self._dfE > eps:
			self._MSE = self._SSE / self._dfE
		if approx_residuals is None:
			self.eij    = np.asarray(self.Y - X*self._beta)  #residuals
		else:
			C           = approx_residuals
			A           = X * C.T
			Ai          = np.linalg.pinv(A)
			beta        = Ai*Y
			self.eij    = np.asarray(Y - A*beta)  #approximate residuals
		if self.dim==1:
			self.fwhm   = rft1d.geom.estimate_fwhm(self.eij)            #smoothness
			### compute resel counts:
			if self.roi is None:
				self.resels = rft1d.geom.resel_counts(self.eij, self.fwhm, element_based=False) #resel
			else:
				B      = np.any( np.isnan(self.eij), axis=0)  #node is true if NaN
				B      = np.logical_and(np.logical_not(B), self.roi)  #node is true if in ROI and also not NaN
				mask   = np.logical_not(B)  #true for masked-out regions
				self.resels = rft1d.geom.resel_counts(mask, self.fwhm, element_based=False) #resel
		self.QT         = np.linalg.qr(X)[0].T


