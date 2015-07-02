
import numpy as np
import rft1d
from .. import _spm



eps         = np.finfo(float).eps




class _ANOVA(object):
	def __init__(self, Y, X, contrasts):
		Y               = np.asarray(Y, dtype=float)
		self.dim        = Y.ndim - 1            #dependent variable dimensionality (0 or 1)
		self.Y          = self._asmatrix(Y)     #stacked dependent variable (JxQ)
		self.X          = np.matrix(X)          #design matrix
		self.J          = self.X.shape[0]       #number of observations
		self.Q          = self.Y.shape[1]       #number of field nodes
		self.eij        = None
		self.contrasts  = contrasts             #list of contrast objects
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
		self._estimate_parameters()

	
	### PRIVATE METHODS ##################################
		
	def _asmatrix(self, Y):
		return np.matrix(Y).T if Y.ndim==1 else np.matrix(Y)
		
	def _estimate_parameters(self):
		Y,X,J           = self.Y, self.X, self.J
		Xi              = np.linalg.pinv(X)         #design matrix pseudoinverse
		self._beta      = Xi*Y                      #estimated parameters
		self._R         = np.eye(J) - X*Xi          #residual forming matrix
		self._rankR     = self._rank(self._R)
		self._SSE       = np.diag( Y.T * self._R * Y )
		self._dfE       = self._rankR
		self.eij        = np.asarray(self.Y - X*self._beta)  #residuals
		if self._dfE > eps:
			self._MSE = self._SSE / self._dfE
		if self.dim==1:
			self.fwhm   = rft1d.geom.estimate_fwhm(self.eij)            #smoothness
			self.resels = rft1d.geom.resel_counts(self.eij, self.fwhm, element_based=False) #resel 
			
	# def _rank(self, A, tol=None):
	# 	return float( np.linalg.matrix_rank(A, tol=tol) )

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



	### COMPUTATIONAL CORE (PRIVATE) ##################################
	###  all methods accept contrast matrices (as np.matrix)

	def _compute_ss(self, C):
		J,Y,X,b,R     = self.J, self.Y, self.X, self._beta, self._R
		X0            = self._get_design_matrix_reduced(C)    #reduced design matrix
		R0            = np.eye(J) - X0*np.linalg.pinv(X0)     #residual forming matrix (reduced design)
		M             = R0 - R                                #projection matrix
		SS            = np.diag( b.T * X.T * M * X * b )
		df            = self._rank(M)
		if self.dim == 0:
			return float(SS), df
		else:
			return SS, df

	def _compute_ss_rm(self, C):
		J,Y,X,b,R     = self.J, self.Y, self.X, self._beta, self._R
		X0            = self._get_design_matrix_reduced(C)    #reduced design matrix
		R0            = np.eye(J) - X0*np.linalg.pinv(X0)     #residual forming matrix (reduced design)
		M             = R0 - R                                #projection matrix
		Xb            = X*b
		SS            = np.diag( b.T * X.T * M * Xb )
		eij           = np.asarray(Y - X0*b)  #residuals
		df            = self._rank(M)
		if self.dim == 0:
			return float(SS), df, eij, X0
		else:
			return SS, df, eij, X0

	def _compute_test_statistic(self, C):
		SS,df         = self._compute_ss(C)
		MS            = SS / df
		f             = MS / self._MSE
		return f, (df,self._dfE), (SS,self._SSE), (MS,self._MSE)
	
	def _compute_test_statistic_rm(self, contrast):
		C,CE          = contrast.get_compound_matrices()
		SS0,df0,eij0,X00  = self._compute_ss_rm(C.T)
		SSE,dfE,eij,X0    = self._compute_ss_rm(CE.T)
		SS            = SS0 - SSE
		df            = df0 - dfE
		if df<0:  #df will be less than zero if a redundant term is added to the contrast when there are more than 4 factor levels;  see factors._00_parse. if n>4
			df        = contrast.n
		MS,MSE        = (SS/df), (SSE/dfE)
		f             = MS / MSE
		return f, (df,dfE), (SS,SSE), (MS,MSE), eij, X0

	def _get_design_matrix_reduced(self, C):
		# Xc   = self.X * C
		C0   = np.eye(C.shape[0]) - C*np.linalg.pinv(C)
		X0   = self.X * C0
		return X0


	### PUBLIC METHODS ##################################
	###  all methods accept contrast objects
	
	def compute_ss(self, contrast):
		return self._compute_ss(contrast.C.T)
	def compute_test_statistic(self, contrast):
		return self._compute_test_statistic(contrast.C.T)
	def compute_test_statistics(self):
		F = []
		for contrast in self.contrasts:
			if contrast.isrm:
				f,df,ss,ms,eij,X0  = self._compute_test_statistic_rm(contrast)
			else:
				f,df,ss,ms  = self._compute_test_statistic(contrast.C.T)
				eij         = self.eij
				X0          = None
			if self.dim == 0:
				F.append( _spm.SPM0D_F(f, df, ss, ms, eij, X0) )
			else:
				F.append( _spm.SPM_F(f, df, self.fwhm, self.resels, self.X, self._beta, eij, X0) )
		return F
	def get_design_matrix_reduced(self, contrast):
		return self._get_design_matrix_reduced(contrast.C.T)
	




class ANOVA1(_ANOVA):
	pass
class ANOVA1rm(_ANOVA):
	pass
class ANOVA2(_ANOVA):
	pass
class ANOVA2rm(_ANOVA):
	pass
class ANOVA2onerm(_ANOVA):
	pass
class ANOVA3(_ANOVA):
	pass
class ANOVA3onerm(_ANOVA):
	pass
class ANOVA3tworm(_ANOVA):
	pass




class ANOVA2nested(_ANOVA):
	def compute_test_statistics(self):
		CA,CB         = [c.C for c in self.contrasts]
		SSA,uA        = self._compute_ss(CA.T)
		SSB,uB        = self._compute_ss(CB.T)
		MSA,MSB       = (SSA/uA), (SSB/uB)
		fA            = MSA / MSB
		fB            = MSB / self._MSE
		### assemble:
		SS,MS,DF      = [(SSA,SSB), (SSB,self._SSE)], [(MSA,MSB), (MSB,self._MSE)], [(uA,uB), (uB,self._dfE)]
		F             = [float(fA), float(fB)] if self.dim==0 else [fA,fB]
		return [_spm.SPM0D_F(f, df, ss, ms)  for f,df,ss,ms in zip(F,DF,SS,MS)]






class ANOVA3nested(_ANOVA):
	def compute_test_statistics(self):
		CA,CB,CC      = [c.C for c in self.contrasts]
		SSA,uA        = self._compute_ss(CA.T)
		SSB,uB        = self._compute_ss(CB.T)
		SSC,uC        = self._compute_ss(CC.T)
		MSA,MSB,MSC   = (SSA/uA), (SSB/uB), (SSC/uC)
		fA,fB,fC      = MSA/MSB, MSB/MSC, MSC/self._MSE
		### assemble:
		F             = [fA, fB, fC]
		DF            = [(uA,uB), (uB,uC), (uC,self._dfE)]
		SS            = [(SSA,SSB), (SSB,SSC), (SSC,self._SSE)]
		MS            = [(MSA,MSB), (MSB,MSC), (MSC,self._MSE)]
		F             = map(float, F) if self.dim==0 else F
		return [_spm.SPM0D_F(f, df, ss, ms)  for f,df,ss,ms in zip(F,DF,SS,MS)]


