
# Copyright (C) 2016  Todd Pataky

from math import log
import numpy as np
from spm1d.stats.anova import designs,models
from spm1d.stats.anova.ui import aov



eps    = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors



#---------------------------------------------------------------------------------
#  ONE-SAMPLE TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

class _CalculatorOneSample(object):
	def __init__(self, nResponses, mu=None):
		self.J     = nResponses
		self.mu    = 0 if mu is None else mu
	def get_test_stat(self, y):
		return self.get_test_stat_mu_subtracted( y - self.mu )
	def get_test_stat_mu_subtracted(self, y):
		pass


class CalculatorTtest(_CalculatorOneSample):
	def __init__(self, nResponses, mu=None):
		super(CalculatorTtest, self).__init__(nResponses, mu)
		self.sqrtN       = int(self.J)**0.5
	def get_test_stat_mu_subtracted(self, y):
		return y.mean(axis=0) / (  y.std(axis=0, ddof=1) / self.sqrtN  )


class CalculatorHotellings0D(_CalculatorOneSample):
	def get_test_stat_mu_subtracted(self, y):
		m       = np.matrix( y.mean(axis=0) )       #estimated mean
		W       = np.matrix( np.cov(y.T, ddof=1) )  #estimated covariance
		T2      = self.J * m * np.linalg.inv(W) * m.T
		return float(T2)

class CalculatorHotellings1D(_CalculatorOneSample):
	def _T2_onesample_singlenode(self, y):
		if np.ma.is_masked(y):
			T2   = 0
		else:
			y    = np.matrix(y)
			n    = y.shape[0]      #nResponses
			m    = y.mean(axis=0)  #mean vector
			W    = np.cov(y.T) + eps  #covariance
			T2   = n * m * np.linalg.inv(W) * m.T
		return float(T2)
	
	def get_test_stat_mu_subtracted(self, y):
		T2      = [self._T2_onesample_singlenode( y[:,i,:] )   for i in range(y.shape[1])]
		return np.asarray(T2)





#---------------------------------------------------------------------------------
#  TWO-SAMPLE TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

class _CalculatorTwoSample(object):
	def __init__(self, nA, nB):
		self.nA1         = nA - 1
		self.nB1         = nB - 1
		self.df          = nA + nB - 2
	def get_test_stat(self, yA, yB):
		pass


class CalculatorTtest2( _CalculatorTwoSample ):
	def __init__(self, nA, nB):
		super(CalculatorTtest2, self).__init__(nA, nB)
		self.sqrtAB      = (1.0/nA + 1.0/nB)**0.5
	def get_test_stat(self, yA, yB):
		mA,mB  = yA.mean(axis=0), yB.mean(axis=0)
		sA,sB  = yA.std(axis=0, ddof=1), yB.std(axis=0, ddof=1)
		s      = (   (  self.nA1*sA*sA + self.nB1*sB*sB  )  /  self.df   )**0.5
		return (mA-mB) / s / self.sqrtAB


class CalculatorHotellings20D( _CalculatorTwoSample ):
	def __init__(self, nA, nB):
		super(CalculatorHotellings20D, self).__init__(nA, nB)
		self.nABAB       = (nA * nB) / float( nA + nB )
	def get_test_stat(self, yA, yB):
		yA,yB     = np.matrix(yA), np.matrix(yB)
		mA,mB     = yA.mean(axis=0), yB.mean(axis=0)
		WA,WB     = np.cov(yA.T), np.cov(yB.T)
		W         = (self.nA1*WA + self.nB1*WB) / self.df + eps
		T2        = self.nABAB  * (mB-mA) * np.linalg.inv(W) * (mB-mA).T
		return float(T2)

class CalculatorHotellings21D( _CalculatorTwoSample ):
	def __init__(self, nA, nB):
		super(CalculatorHotellings21D, self).__init__(nA, nB)
		self.nABAB       = (nA * nB) / float( nA + nB )

	def _T2_twosample_singlenode(self, yA, yB):  #at a single node:
		if np.ma.is_masked(yA):
			T2   = 0
		else:
			yA,yB    = np.matrix(yA), np.matrix(yB)
			mA,mB    = yA.mean(axis=0), yB.mean(axis=0)  #means
			WA,WB    = np.cov(yA.T), np.cov(yB.T)
			W        = (self.nA1*WA + self.nB1*WB) / self.df + eps
			T2       = self.nABAB  * (mB-mA) * np.linalg.inv(W) * (mB-mA).T
		return float(T2)

	def get_test_stat(self, yA, yB):
		T2      = [self._T2_twosample_singlenode( yA[:,i,:], yB[:,i,:] )   for i in range(yA.shape[1])]
		return np.asarray(T2)





class CalculatorMANOVA10D( object ):
	def __init__(self, A, I):
		### counts:
		J           = A.size           #number of responses
		u           = np.unique(A)
		nGroups     = u.size
		self.n1pk   = -((J-1) - 0.5*(I + nGroups))
		### design matrix:
		X           = np.zeros((J, nGroups))
		for i,uu in enumerate(u):
			X[A==uu, i] = 1
		self.X      = np.matrix(X)
		self.Xi     = np.linalg.pinv( self.X )
		### reduced design matrix:
		self.X0     = np.matrix(  np.ones(J)  ).T
		self.X0i    = np.linalg.pinv( self.X0 )

	def get_test_stat(self, Y):
		### SS for original design:
		Y     = np.matrix(Y)
		b     = self.Xi * Y
		R     = Y - self.X*b
		R     = R.T * R
		### SS for reduced design:
		b0    = self.X0i * Y
		R0    = Y - self.X0*b0
		R0    = R0.T * R0
		### Wilk's lambda:
		lam   = np.linalg.det(R) / (np.linalg.det(R0) + eps)
		x2    = self.n1pk * log(lam)
		return x2


class CalculatorMANOVA11D( CalculatorMANOVA10D ):
	def get_test_stat(self, Y):
		x2    = [CalculatorMANOVA10D.get_test_stat(self, Y[:,i,:])   for i in range(Y.shape[1])]
		return np.array(x2)







#---------------------------------------------------------------------------------
#  REGRESSION TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------



class CalculatorRegress0D(object):
	def __init__(self, x):
		self.x           = np.asarray(x, dtype=float)
		self.J           = self.x.size
		self.df          = self.J - 2     #degrees of freedom
		### design matrix:
		X                = np.ones( (self.J, 2) )
		X[:,0]           = self.x
		self.X           = np.matrix(X)
		self.Xi          = np.linalg.pinv(X)
		self.c           = np.matrix([1,0]).T
		self.cXXc        = float(  self.c.T * np.linalg.inv(self.X.T*self.X) * self.c  )
	
	def get_test_stat(self, y):
		Y      = np.matrix(y).T
		b      = self.Xi * Y            #parameters
		eij    = Y - self.X*b           #residuals
		R      = eij.T*eij              #residual sum of squares
		sigma2 = float(R) / self.df     #variance
		t      = float(self.c.T*b)  /   (sigma2*self.cXXc)**0.5
		return t


class CalculatorRegress1D(CalculatorRegress0D):
	def get_test_stat(self, y):
		Y      = np.matrix(y)
		b      = self.Xi * Y            #parameters
		eij    = Y - self.X*b           #residuals
		R      = eij.T*eij              #residual sum of squares
		sigma2 = np.diag(R) / self.df   #variance
		t      = np.array(self.c.T*b).flatten()  /   ((sigma2*self.cXXc)**0.5 + eps)
		return t


class CalculatorCCA0D(object):
	def __init__(self, x):
		self.x           = np.asarray(x, dtype=float)
		self.J           = x.size
		self.X           = np.matrix(x).T
		Z                = np.matrix( np.ones(self.J) ).T
		self.Rz          = np.eye(self.J) - Z * np.linalg.inv(Z.T*Z) * Z.T
		XStar            = self.Rz * self.X
		self.XXXiX       = XStar  *  np.linalg.inv( XStar.T * XStar  )  * XStar.T
		self.p           = 1.0   #nContrasts
		self.r           = 1.0   #nNuisanceFactors
		self.m           = self.J - self.p - self.r

	def get_test_stat(self, y):
		if np.ma.is_masked(y):
			x2     = 0
		else:
			### estimate maximum canonical correlation:
			Y          = np.matrix(y)
			YStar      = self.Rz * Y
			H          = YStar.T * self.XXXiX * YStar / self.p
			W          = YStar.T  * (np.eye(self.J)  -  self.XXXiX) * YStar  / self.m
			F          = np.linalg.inv(W) * H
			ff         = np.linalg.eigvals( F )
			fmax       = float( np.real(ff.max()) )
			r2max      = fmax * self.p  / (self.m + fmax*self.p)
			rmax       = r2max**0.5
			### compute test statistic:
			m          = y.shape[1]  # df = m  (nComponents)
			x2         = -(self.J - 1 - 0.5*(m+2) )  *  log( (1-rmax**2) )
		return x2


class CalculatorCCA1D(CalculatorCCA0D):

	def get_test_stat(self, y):
		x2         = [super(CalculatorCCA1D, self).get_test_stat(y[:,i,:])   for i in range(y.shape[1])]
		return np.array(x2)








#---------------------------------------------------------------------------------
#  ANOVA TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

class _CalculatorANOVAsingleF(object):
	def get_test_stat(self, y):
		model   = models.LinearModel(y, self.design.X)
		model.fit()
		F       = aov(model, self.design.contrasts, self.design.f_terms)[0]
		return F.z

class _CalculatorANOVAmultiF(object):
	def get_test_stat(self, y):
		model   = models.LinearModel(y, self.design.X)
		model.fit()
		FF      = aov(model, self.design.contrasts, self.design.f_terms)
		return [F.z for F in FF]



class CalculatorANOVA1(_CalculatorANOVAsingleF):
	def __init__(self, A):
		self.design      = designs.ANOVA1(A)
class CalculatorANOVA1rm(_CalculatorANOVAsingleF):
	def __init__(self, A, SUBJ):
		self.design      = designs.ANOVA1rm(A, SUBJ)



class CalculatorANOVA2(_CalculatorANOVAmultiF):
	def __init__(self, A, B):
		self.design      = designs.ANOVA2(A, B)
class CalculatorANOVA2nested(_CalculatorANOVAmultiF):
	def __init__(self, A, B):
		self.design      = designs.ANOVA2nested(A, B)
class CalculatorANOVA2onerm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, SUBJ):
		self.design      = designs.ANOVA2onerm(A, B, SUBJ)
class CalculatorANOVA2rm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, SUBJ):
		self.design      = designs.ANOVA2rm(A, B, SUBJ)



class CalculatorANOVA3(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C):
		self.design      = designs.ANOVA3(A, B, C)
class CalculatorANOVA3nested(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C):
		self.design      = designs.ANOVA3nested(A, B, C)
class CalculatorANOVA3onerm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C, SUBJ):
		self.design      = designs.ANOVA3onerm(A, B, C, SUBJ)
class CalculatorANOVA3tworm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C, SUBJ):
		self.design      = designs.ANOVA3tworm(A, B, C, SUBJ)
class CalculatorANOVA3rm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C, SUBJ):
		self.design      = designs.ANOVA3rm(A, B, C, SUBJ)




